#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3, json, logging
import sys, time, os

logger = logging.getLogger()

class mySQLDatabase:
    #DB_FILEPATH = "/home/alex/car.dashboard/database.sqlite"
    DB_TABLENAME = "datas"

    def __init__(self, sensor="None", commit_every = 1):
        self.sensor = sensor
        self.connect_db()

        self.COUNTER_MAX = commit_every
        self.__counter = 0

    def db_filepath(self):
        ROOT_DIR = "/media/usb"
        DB_DIR = "car.datas"
        DB_FILE = "car.db.sqlite"
        if not os.path.isdir(ROOT_DIR):
            logger.error("No USB key found: " + ROOT_DIR + " doesn't exist")
            return None
        if len(os.listdir(ROOT_DIR)) < 1:
            logger.error("No USB key found: " + ROOT_DIR + " is empty")
            return None

        d = os.path.join(ROOT_DIR, DB_DIR)
        if not os.path.isdir(d):
            os.makedirs(d)

        f = os.path.join(d, DB_FILE)
        return f


    def connect_db(self):
        if self.db_filepath() is None:
            self._db = None
            return

        self._db = sqlite3.connect(self.db_filepath())
        cur = self._db.cursor()

        try:
            cur.execute("CREATE TABLE " + self.DB_TABLENAME + " (dt DATETIME, sensor TEXT, json_data TEXT)")
            self._db.commit()
        except sqlite3.OperationalError as e:
            if e.message == 'table datas already exists':
                return
            else:
                logger.critical("Connecting to DB !!")
                sys.exit(1)

    def insert(self, data_dict):
        if self._db is None:
            self.connect_db()
        if self._db is None:
            logger.warning("Database not available, not logging !")
            return

        sql_cmd = ""
        if "datetime" not in data_dict.keys():
            logger.error("Inserting data in DB: no 'datetime' in provided data_dict")
            return

        data_dt = data_dict["datetime"]
        json_data = json.dumps(data_dict)

        sql_cmd = "INSERT INTO datas(dt,sensor,json_data) VALUES('" + data_dt + "','" + self.sensor + "','" + json_data + "')"
        logger.debug(sql_cmd)

        self._execute(sql_cmd)

    def _execute(self, sql_cmd):
        if self._db is None:
            return
        cur = self._db.cursor()

        while 1:
            c = 0
            try:
                cur.execute(sql_cmd)
                break
            except sqlite3.OperationalError as e:
                if e.message == "database is locked":
                    c += 1
                else:
                    raise e

                if c < 10:
                    logger.warning("Database locked, retrying in 1 sec...")
                    time.sleep(1)
                    continue
                else:
                    logger.critical("Database locked for more than 10 secs, aborting operations !")
                    sys.exit(1)


        if self.__counter < self.COUNTER_MAX:
            self.__counter += 1
        else:
            logger.info("Commiting %d changes in DB"%self.__counter)
            self._db.commit()
            self.__counter = 0
        cur.close()



