#!/usr/bin/python
from configparser import ConfigParser
import os
from dotenv import load_dotenv


def config():
    
    load_dotenv("../secret.env")
    DATABASE_URL = os.getenv("DATABASE_URL")
    # DATABASE_URL = os.environ.get("DATABASE_URL")
    return DATABASE_URL
