import boto3
import pandas as pd
import os 
import pymysql

tables = {'companydb.jobs': 'id int not null, job  varchar(100), PRIMARY KEY (ID)',
         'companydb.departments': 'id int not null, job  varchar(100), PRIMARY KEY (ID)',
         'companydb.hired_employees': 'id int not null, name varchar(200), datetime varchar(50), department_id int, job_id int, PRIMARY KEY (id), FOREIGN KEY (department_id) REFERENCES companydb.departments(id), FOREIGN KEY (job_id) REFERENCES companydb.jobs(id)'}
         
def read_s3(table_name):   
    s3_bucket_name=f's3://globant-data/{table_name}.csv'
    return pd.read_csv(s3_bucket_name, header=None)

def rename_columns(df,dict):
    return df.rename(columns=dict)

def mysql_connector():
    endpoint='companydb.c3hqda7obrsd.us-east-1.rds.amazonaws.com'
    user='admin'
    pwd = os.getenv('mysql_pwd')

    try:
        return pymysql.connect(host=endpoint, user=user, passwd=pwd)
    except Exception as e:
        print("Database connection failed due to {}".format(e))

def create_database(dbname):
    conn = mysql_connector()

    try:
        cursor = conn.cursor()                                    
        
        sql_query = 'show databases'
        cursor.execute(sql_query)
        databases = cursor.fetchall()
        
        for database in databases:
            if dbname == database[0]:
                print (f'Database {dbname} already exists!')
                return
            
        sql_statement = 'create database '+ dbname  
        cursor.execute(sql_statement)
        print (f'Database {dbname} created!')

    except Exception as e:
        print("Exeception occured:{}".format(e))
    finally:
        cursor.close()
    
def create_table(table_name, table_scheme):
    try:
        conn = mysql_connector()
        cursor = conn.cursor()
        cursor.execute(f'create table {table_name} ({table_scheme});')

        print (f'Table {table_name} created!')
    except Exception as e:
        print("Exeception occured:{}".format(e))
    finally:
        cursor.close()

if __name__ == "__main__":
    
    s3_client=boto3.client('s3')

    # Creating dataframe jobs and renaming columns
    df_jobs = read_s3('jobs')
    df_jobs = rename_columns(df_jobs,{0: 'id',1: 'job'})

    # Creating dataframe departments and renaming columns
    df_departments = read_s3('departments')
    df_departments = rename_columns(df_departments,{0: 'id',1: 'department'})

    # Creating dataframe hired_employees, renaming columns and droping null name, department_id and job_id
    df_hired= read_s3('hired_employees')
    df_hired = rename_columns(df_hired,{0: 'id',
                                              1: 'name', 
                                              2: 'datetime',
                                              3: 'department_id',
                                              4: 'job_id'
                                             })

    df_hired.dropna(inplace=True)

    create_database('companydb')

    for table_name, table_schema in tables.items():
        create_table (table_name,table_schema)


    
