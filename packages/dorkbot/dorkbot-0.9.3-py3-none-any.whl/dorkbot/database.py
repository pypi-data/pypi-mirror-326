#!/usr/bin/env python3
if __package__:
    from dorkbot.target import Target
    from dorkbot.util import generate_fingerprint, get_database_attributes
else:
    from target import Target
    from util import generate_fingerprint, get_database_attributes
import logging
import os
import sys
from contextlib import closing


class TargetDatabase:
    def __init__(self, address, drop_tables=False, create_tables=False):
        protocols = ["postgresql://", "sqlite3://"]
        if not any(address.startswith(protocol) for protocol in protocols):
            address = f"sqlite3://{address}"
        for key, value in get_database_attributes(address).items():
            setattr(self, key, value)

        if address.startswith("sqlite3://"):
            try:
                os.makedirs(os.path.dirname(os.path.abspath(self.database)), exist_ok=True)
            except OSError as e:
                logging.error(f"Failed to create parent directory for database file - {str(e)}")
                sys.exit(1)

        self.connect()

        if drop_tables:
            logging.debug("Dropping tables")
            self.execute("DROP TABLE IF EXISTS targets")
            self.execute("DROP TABLE IF EXISTS sources")
            self.execute("DROP TABLE IF EXISTS fingerprints")
            self.execute("DROP TABLE IF EXISTS blocklist")

        if create_tables:
            self.execute("CREATE TABLE IF NOT EXISTS targets"
                         f" (id {self.id_type},"
                         " url VARCHAR UNIQUE,"
                         " source_id INTEGER,"
                         " fingerprint_id INTEGER,"
                         " scanned INTEGER DEFAULT 0)")
            self.execute("CREATE TABLE IF NOT EXISTS sources"
                         f" (id {self.id_type},"
                         " source VARCHAR UNIQUE)")
            self.execute("CREATE TABLE IF NOT EXISTS fingerprints"
                         f" (id {self.id_type},"
                         " fingerprint VARCHAR UNIQUE,"
                         " scanned INTEGER DEFAULT 0)")
            self.execute("CREATE TABLE IF NOT EXISTS blocklist"
                         f" (id {self.id_type},"
                         " item VARCHAR UNIQUE)")

    def connect(self, retries=3):
        for i in range(retries):
            try:
                self.db = self.module.connect(self.database, **self.connect_kwargs)
                break
            except self.module.Error as e:
                retry_conditions = ["Connection timed out"]
                if i < retries and any(error in str(e) for error in retry_conditions):
                    logging.warning(f"Database connection failed (retry {i} of {retries}) - {str(e)}")
                    continue
                else:
                    logging.error(f"Database connection failed (will not retry) - {str(e)}")
                    sys.exit(1)

    def close(self):
        self.db.close()

    def execute(self, *sql, many=False, fetchone=False, fetchall=False, retries=3):
        statement, parameters = (sql[0], sql[1] if len(sql) == 2 else ())

        for i in range(retries):
            try:
                with closing(self.db.cursor()) as c:
                    result = None
                    if many:
                        c.executemany(statement, parameters)
                    else:
                        c.execute(statement, parameters)
                    if fetchone:
                        result = c.fetchone()
                    elif fetchall:
                        result = c.fetchall()
                self.db.commit()
                return result
            except self.module.Error as e:
                retry_conditions = ["connection", "SSL"]
                if i < retries and any(error in str(e) for error in retry_conditions):
                    logging.warning(f"Database execution failed (retry {i} of {retries}) - {str(e)}")
                    self.connect()
                    continue
                else:
                    logging.error(f"Database execution failed (will not retry) - {str(e)}")
                    sys.exit(1)

    def get_urls(self, unscanned_only=False, source=False, random=False, count=False):
        if source and source is not True:
            sql = "SELECT t.url FROM targets t" \
                  + " INNER JOIN sources s on s.id = t.source_id"
        elif source is True:
            sql = "SELECT t.url, s.source FROM targets t" \
                  + " LEFT JOIN sources s on s.id = t.source_id"
        else:
            sql = "SELECT t.url FROM targets t"

        if unscanned_only:
            sql += " LEFT JOIN fingerprints f on f.id = t.fingerprint_id" \
                + " WHERE t.scanned = '0' AND (t.fingerprint_id IS NULL OR f.scanned = '0')"

        if source and source is not True:
            if unscanned_only:
                sql += " AND s.source = %s" % self.param
            else:
                sql += " WHERE s.source = %s" % self.param
            parameters = (source,)
        else:
            parameters = ()

        if random:
            sql += " ORDER BY RANDOM()"

        if count > 0:
            sql += f" LIMIT {count}"

        rows = self.execute(sql, parameters, fetchall=True)
        urls = [" | ".join([str(column or "") for column in row]) for row in rows]
        return urls

    def get_next_target(self, source=False, random=False):
        sql = "SELECT t.url, t.id, f.id FROM targets t"
        if source and source is not True:
            sql += " INNER JOIN sources s on s.id = t.source_id"
        sql += " LEFT JOIN fingerprints f on f.id = t.fingerprint_id" \
            + " WHERE (t.fingerprint_id IS NULL AND t.scanned = '0') OR f.scanned = '0'"
        if source and source is not True:
            sql += " AND s.source = %s" % self.param
            parameters = (source,)
        else:
            parameters = ()
        if random:
            sql += " ORDER BY RANDOM()"

        target = None
        while True:
            row = self.execute(sql, parameters, fetchone=True)
            if not row:
                break

            url = row[0]
            target_id = row[1]
            fingerprint_id = row[2]

            if not fingerprint_id:
                fingerprint = generate_fingerprint(url)
                fingerprint_id = self.get_fingerprint_id(fingerprint)
                if fingerprint_id:
                    self.update_target_fingerprint(target_id, fingerprint_id)
                    logging.debug(f"Skipping (matches scanned fingerprint): {url}")
                    continue
                else:
                    self.mark_target_scanned(target_id)
                    self.add_fingerprint(fingerprint, scanned=True)
            else:
                self.mark_fingerprint_scanned(fingerprint_id)

            target = url
            break
        return target

    def add_target(self, url, source=None):
        logging.debug(f"Adding target {url}")
        if source:
            source_id = self.get_source_id(source)
            if not source_id:
                source_id = self.add_source(source)
        else:
            source_id = None

        self.execute("%s INTO targets (url, source_id) VALUES (%s, %s) %s"
                     % (self.insert, self.param, self.param, self.conflict),
                     (url, source_id))

    def add_targets(self, urls, source=None, chunk_size=1000):
        logging.debug(f"Adding {len(urls)} targets")
        if source:
            source_id = self.get_source_id(source)
            if not source_id:
                source_id = self.add_source(source)
        else:
            source_id = None

        for x in range(0, len(urls), chunk_size):
            urls_chunk = urls[x:x + chunk_size]
            self.execute("%s INTO targets (url, source_id) VALUES (%s, %s) %s"
                         % (self.insert, self.param, self.param, self.conflict),
                         [(url, source_id) for url in urls_chunk], many=True)

    def mark_target_scanned(self, target_id):
        self.execute("UPDATE targets SET scanned = 1 WHERE id = %s" % self.param, (target_id,))

    def delete_target(self, url):
        logging.debug(f"Deleting target {url}")
        self.execute("DELETE FROM targets WHERE url = %s" % self.param, (url,))

    def flush_targets(self):
        logging.info("Flushing targets")
        self.execute("DELETE FROM targets")
        self.execute("DELETE FROM sources")

    def add_source(self, source):
        logging.debug(f"Adding source {source}")
        row = self.execute("%s INTO sources (source) VALUES (%s) %s RETURNING id"
                           % (self.insert, self.param, self.conflict),
                           (source,), fetchone=True)
        return row if not row else row[0]

    def get_source_id(self, source):
        row = self.execute("SELECT id FROM sources WHERE source = %s"
                           % self.param, (source,), fetchone=True)
        return row if not row else row[0]

    def get_sources(self):
        rows = self.execute("SELECT source FROM sources", fetchall=True)
        return [row[0] for row in rows if rows]

    def add_fingerprint(self, fingerprint, scanned=False):
        logging.debug(f"Adding fingerprint {fingerprint}")
        row = self.execute("%s INTO fingerprints (fingerprint, scanned) VALUES (%s, %s) %s RETURNING id"
                           % (self.insert, self.param, self.param, self.conflict),
                           (fingerprint, 1 if scanned else 0), fetchone=True)
        return row if not row else row[0]

    def update_target_fingerprint(self, target_id, fingerprint_id):
        self.execute("UPDATE targets SET fingerprint_id = %s WHERE id = %s"
                     % (self.param, self.param), (fingerprint_id, target_id))

    def flush_fingerprints(self):
        logging.info("Flushing fingerprints")
        self.execute("UPDATE targets SET fingerprint_id = NULL")
        self.execute("DELETE FROM fingerprints")

    def reset_scanned(self):
        logging.info("Resetting scanned")
        self.execute("UPDATE targets SET scanned = 0")
        self.execute("UPDATE fingerprints SET scanned = 0")

    def get_fingerprint_id(self, fingerprint):
        row = self.execute("SELECT id FROM fingerprints WHERE fingerprint = %s"
                           % self.param, (fingerprint,), fetchone=True)
        return row if not row else row[0]

    def mark_fingerprint_scanned(self, fingerprint_id):
        self.execute("UPDATE fingerprints SET scanned = 1 WHERE id = %s" % self.param, (fingerprint_id,))

    def prune(self, blocklists, source, random):
        sql = "SELECT t.url, t.id, f.id, f.fingerprint FROM targets t"
        if source and source is not True:
            sql += " INNER JOIN sources s on s.id = t.source_id"
        sql += " LEFT JOIN fingerprints f on f.id = t.fingerprint_id" \
            + " WHERE t.scanned = '0' AND (t.fingerprint_id IS NULL OR f.scanned = '0')"
        if source and source is not True:
            sql += " AND s.source = %s" % self.param
            parameters = (source,)
        else:
            parameters = ()
        if random:
            sql += " ORDER BY RANDOM()"

        fingerprints = {}
        targets = self.execute(sql, parameters, fetchall=True)
        if not targets:
            return
        targets.reverse()
        while targets:
            url, target_id, fingerprint_id, fingerprint = targets.pop()

            if True in [blocklist.match(Target(url)) for blocklist in blocklists]:
                logging.debug(f"Deleting (matches blocklist pattern): {url}")
                self.delete_target(url)

            elif fingerprint_id:
                if fingerprint in fingerprints:
                    self.mark_target_scanned(target_id)
                    logging.debug(f"Skipping (matches existing fingerprint): {url}")
                else:
                    fingerprints[fingerprint] = fingerprint_id
                    targets = self.get_new_targets(targets, fingerprints)

            else:
                fingerprint = generate_fingerprint(url)

                if fingerprint in fingerprints:
                    fingerprint_id = fingerprints[fingerprint]
                    self.update_target_fingerprint(target_id, fingerprint_id)
                    self.mark_target_scanned(target_id)
                    logging.debug(f"Skipping (matches existing fingerprint): {url}")
                else:
                    fingerprint_id = self.get_fingerprint_id(fingerprint)

                    if fingerprint_id:
                        fingerprints[fingerprint] = fingerprint_id
                        self.update_target_fingerprint(target_id, fingerprint_id)
                        self.mark_target_scanned(target_id)
                        targets = self.get_new_targets(targets, fingerprints)
                        logging.debug(f"Skipping (matches existing fingerprint): {url}")
                    else:
                        fingerprint_id = self.add_fingerprint(fingerprint, scanned=False)
                        fingerprints[fingerprint] = fingerprint_id
                        self.update_target_fingerprint(target_id, fingerprint_id)
                        targets = self.get_new_targets(targets, fingerprints)

    def get_new_targets(self, targets, fingerprints):
        return [target for target in targets if target[3] not in fingerprints]

    def generate_fingerprints(self, source):
        logging.info("Generating fingerprints")
        sql = "SELECT t.url, t.id FROM targets t"
        if source and source is not True:
            sql += " INNER JOIN sources s on s.id = t.source_id"
        sql += " WHERE t.fingerprint_id IS NULL"
        if source and source is not True:
            sql += " AND s.source = %s" % self.param
            parameters = (source,)
        else:
            parameters = ()

        targets = self.execute(sql, parameters, fetchall=True)
        targets.reverse()
        fingerprints = {}
        while targets:
            url, target_id = targets.pop()
            fingerprint = generate_fingerprint(url)
            if fingerprint in fingerprints:
                fingerprint_id = fingerprints[fingerprint]
                self.update_target_fingerprint(target_id, fingerprint_id)
            else:
                fingerprint_id = self.get_fingerprint_id(fingerprint)
                if fingerprint_id:
                    fingerprints[fingerprint] = fingerprint_id
                    self.update_target_fingerprint(target_id, fingerprint_id)
                else:
                    fingerprint_id = self.add_fingerprint(fingerprint, scanned=False)
                    fingerprints[fingerprint] = fingerprint_id
                    self.update_target_fingerprint(target_id, fingerprint_id)
