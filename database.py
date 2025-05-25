from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:test123@127.0.0.1:3306/todoapplicationdatabase'


# engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread': False}) # sqlite3 required
engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessiontrack = sessionmaker(autocommit= False,autoflush=False,bind=engine)

Base = declarative_base()