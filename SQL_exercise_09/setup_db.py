import sys, getpass
import pandas as pd
from sqlalchemy import create_engine

def create_db_engine():## Create an engine
    uname = 'postgres'
    upass = getpass.getpass()
    dbname = 'sqlpractice09'
    dbhost = 'localhost'
    port = '5432'
    engine = create_engine('postgresql://%s:%s@%s:%s/%s'%(uname,upass,dbhost,port,dbname))
    return engine

def main():
    engine = create_db_engine()
    df = pd.read_csv('cran_logs_2015-01-01.csv')
    df.to_sql('cran_logs', engine)

if __name__ == '__main__':
    main()
