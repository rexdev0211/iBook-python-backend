"""Connections to database, and function to create database tables if they don't exist."""
import ipaddress
import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session, select
from app.models import models


def get_engine():
    load_dotenv()
    # PostgreSQL
    # DB_con = os.environ["DB_con"]
    
    # MySQL
    DB_con = os.environ["DB_MySQL_con"]

    DATABASE_URL = DB_con
    return create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(get_engine())

def get_session():
    load_dotenv()
    # PostgreSQL
    # DB_con = os.environ["DB_con"]
    
    # MySQL
    DB_con = os.environ["DB_MySQL_con"]

    DATABASE_URL = DB_con
    engine = create_engine(DATABASE_URL, echo=True)
    with Session(engine) as session:
        yield session

def create_access_company_table():
    load_dotenv()
    DB_con = os.environ["DB_MySQL_con"]
    DATABASE_URL = DB_con
    engine = create_engine(DATABASE_URL, echo=True)
    with Session(engine) as session:
        access_company = models.AccessCompany(id=1, admin='', company='Test1', alias=1,name='Admin', login='adminOnly', excpaymentmode='', password='e10adc3949ba59abbe56e057f20f883e', limiter=0, passwordchange='2015-04-17', loan=1, profile=1, journal=1, account=1, report=1, readonly=0, timelimit=0, createdate='2020-06-25 20:16:53', ipaddress='',createdby='mastermini', allowrepayedit=1, domain='', employee_id='', counter=0, statusblock='', comm='', level='', team='', user1=1, user2=0, blockuser= 0, phoneno='', branching=0, openday='MTWHFSU', openhour='00:00:00', closehour='23:59:59', exctranstype='1,1,1,1,1,1,1', tnc_read=1, roles='', signature='')
        session.add(access_company)
        session.commit()