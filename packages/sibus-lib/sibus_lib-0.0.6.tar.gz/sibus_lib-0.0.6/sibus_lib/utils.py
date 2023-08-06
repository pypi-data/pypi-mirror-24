#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime as dt
import random

def nice_float(value):
    return float("%.6f" % float(value))

def parse_num(s):
    try:
        return int(s)
    except ValueError:
        try:
            return nice_float(s)
        except ValueError:
            return s

def datetime_now():
    return dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")

def random_value(value, percent_range=30):
    t = (random.random() - 0.5)*(percent_range/100.0)
    return value * (1+t)

def datetime_to_float(d):
    epoch = dt.datetime.utcfromtimestamp(0)
    total_seconds =  (d - epoch).total_seconds()
    # total_seconds will be in decimals (millisecond precision)
    return total_seconds

def float_to_datetime(fl):
    return dt.datetime.fromtimestamp(fl)

def datetime_now_float():
    return datetime_to_float(dt.datetime.utcnow())

def sibus_install():
    import os, shutil
    from pkg_resources import Requirement, resource_filename, resource_exists
    from sibus_lib.SmartConfig import SmartConfigFile

    print "installing SiBus Library..."

    sibus_config = resource_filename(Requirement.parse("sibus_lib"), "resources/sibus.yml")
    config_exists = resource_exists(Requirement.parse("sibus_lib"), "resources/sibus.yml")

    config_dst = os.path.join("/etc/default", "sibus.yml")

    if not config_exists:
        raise "Config file not found ! " + sibus_config

    print "Copying config file in "+config_dst
    shutil.copy(sibus_config, config_dst)

    cfg_data = SmartConfigFile(config_dst)

    db_host = cfg_data.get(["sql_database", "host", ], "127.0.0.1")
    db_port = cfg_data.get(["sql_database", "port", ], 3306)
    db_login = cfg_data.get(["sql_database", "login", ], "root")
    db_password = cfg_data.get(["sql_database", "password", ], "SECRET_KEY")
    db_database = cfg_data.get(["sql_database", "database", ], "sibus_database")

    from sqlalchemy import create_engine
    from sqlalchemy_utils import database_exists, create_database

    _sql_url = "mysql+mysqldb://%s:%s@%s:%d/%s" % (db_login, db_password, db_host, db_port, db_database)
    print "Creating SQL database with " + _sql_url
    engine = create_engine(_sql_url)
    if not database_exists(engine.url):
        create_database(engine.url)

    print "Installation complete !"






