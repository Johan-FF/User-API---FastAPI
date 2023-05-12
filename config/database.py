from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

sqlite_file_name = "../dababase.sqlite"
base_dir = os.path.dirname(os.path.realpath(__file__)) 

database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"

engine = create_engine(database_url)

Session = sessionmaker(bind=engine)

Base = declarative_base()