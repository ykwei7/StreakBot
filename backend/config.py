#!/usr/bin/python
from configparser import ConfigParser
import os


def config():
    # create a parser
    # parser = ConfigParser()
    # # read config file
    # parser.read(filename)

    # # get section, default to postgresql
    # db = {}
    # if parser.has_section(section):
    #     params = parser.items(section)
    #     for param in params:
    #         db[param[0]] = param[1]
    # else:
    #     raise Exception(
    #         "Section {0} not found in the {1} file".format(section, filename)
    #     )
    DATABASE_URL = "postgres://ffcolanxbauwgg:1475cd723d146b6529f274676fdd6e323a7defdac7b36243031e0e056094357d@ec2-44-196-174-238.compute-1.amazonaws.com:5432/d7dtssdu0kitkl"
    # DATABASE_URL = os.environ.get("DATABASE_URL")
    return DATABASE_URL
