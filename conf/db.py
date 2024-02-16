import configparser
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URI: postgresql://username:password@domain.port/database

# Creating relative path to our database
file_config = pathlib.Path(__file__).parent.parent.joinpath('config.ini')
# first parent = dir conf, second parent = dir Project_1

config = configparser.ConfigParser()
config.read(file_config)

# Getting data from "config.ini"
user = config.get('DEV_DB', 'USER')
password = config.get('DEV_DB', 'PASSWORD')
domain = config.get('DEV_DB', 'DOMAIN')
port = config.get('DEV_DB', 'PORT')
db = config.get('DEV_DB', 'DB_NAME')

URI = f"postgresql://{user}:{password}@{domain}:{port}/{db}"

engine = create_engine(URI, echo=False, pool_size=5, max_overflow=0)
# pool_size - quantity of connections to db, has to be specified
# max_overflow - we don't allow to exceed the number of connections

DBSession = sessionmaker(bind=engine)
session = DBSession()

