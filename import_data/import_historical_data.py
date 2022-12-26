import boto3
import pandas as pd
import os 
import mysql_utl

tables = {'companydb.jobs': 'id int not null AUTO_INCREMENT, job varchar(100) not null, PRIMARY KEY (ID)',
         'companydb.departments': 'id int not null AUTO_INCREMENT, department varchar(100) not null, PRIMARY KEY (ID)',
         'companydb.hired_employees': 'id int not null AUTO_INCREMENT, name varchar(200) not null, datetime varchar(50) not null, department_id int, job_id int, PRIMARY KEY (id), FOREIGN KEY (department_id) REFERENCES companydb.departments(id), FOREIGN KEY (job_id) REFERENCES companydb.jobs(id)'}
         
def read_s3(table_name):   
    s3_bucket_name=f's3://globant-data/{table_name}.csv'
    return pd.read_csv(s3_bucket_name, header=None)

def rename_columns(df,dict):
    return df.rename(columns=dict)

def df_insert(mysql_connection, df, table_name):
    for i,row in df.iterrows():
        if table_name == 'companydb.jobs':
            values = f"{row['id']},'{row['job']}'"
        elif table_name == 'companydb.departments':
            values = f"{row['id']},'{row['department']}'"            
        elif table_name == 'companydb.hired_employees':
            # values = f"{row['id']},'{row['name']}','{row['datetime']}',{row['department_id']},{row['job_id']}"
            values = f'{row["id"]},"{row["name"]}","{row["datetime"]}",{row["department_id"]},{row["job_id"]}'
        
        mysql_connection.insert(f"insert into {table_name} values ({values});")
        if i % 100 == 0:
                mysql_connection.commit()
    mysql_connection.commit()
    
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
    # df_hired['name'] = df_hired['name'].apply(lambda x: x.replace("'", " "))
    
    mysql_connection = mysql_utl.Mysql(endpoint='company.c3hqda7obrsd.us-east-1.rds.amazonaws.com', 
                                     user='admin', 
                                     pwd = os.getenv('mysql_new_pwd')
                                    )

    mysql_connection.create_database('companydb')

    for table_name, table_schema in tables.items():
        mysql_connection.create_table(table_name,table_schema)
    
    df_insert(mysql_connection,df_jobs,'companydb.jobs')
    df_insert(mysql_connection,df_departments,'companydb.departments')
    df_insert(mysql_connection,df_hired,'companydb.hired_employees')
    
    
