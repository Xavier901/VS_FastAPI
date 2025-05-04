from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session


#database connection
SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:root@localhost/API5'
    #database type,database username,password,host name,database name

engine=create_engine(SQLALCHEMY_DATABASE_URL)
sessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()
        