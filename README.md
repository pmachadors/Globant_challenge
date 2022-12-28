<!-- <h1 align="center"> Globant Data Engineer challenge </h1> -->
# Data Engineer challenge

![AWS](https://img.shields.io/badge/account-AWS-green)
![Docker Version](https://img.shields.io/badge/docker-v20.10.21-blue)
![Docker Compose](https://img.shields.io/badge/docker--compose-v1.29.2-blue)
![Ubuntu](https://img.shields.io/badge/ubuntu-v22.04-blue)

# Description
Data Engineer challenge, consisting in steps:

1. Move historic data from files in CSV format to the new database.
2. Create a Rest API service to receive new data. This service must have:
2.1. Each new transaction must fit the data dictionary rules.
2.2. Be able to insert batch transactions (1 up to 1000 rows) with one request.
2.3. Receive the data for each table in the same service.
2.4. Keep in mind the data rules for each table.
3. Create a feature to backup for each table and save it in the file system in AVRO format.
4. Create a feature to restore a certain table with its backup.

The csv files are stored in AWS S3 bucket and the database choosed was AWS RDS MySql. I used Insomnia software to test my REST API.

# Requirements
docker docker-compose aws account

# Functionalities
1. Historical data import was made by python script import_historical_data.py. The script will create the database and tables and also insert data from csv jobs, departments and hired_employees stored in S3 AWS.

 ![create companydb](https://user-images.githubusercontent.com/113646668/209831732-c345b5ac-2ef3-4beb-8fe4-deedd26133de.png)

  
2. REST API created in flask. Endpoints:
  
  2.1. Search all jobs
  ```
  http://127.0.0.1:5000/jobs
  ```

  2.2. Search all Departments
  ```
  http://127.0.0.1:5000/departments
  ```
  
  2.3. Search all Hired_employees
  ```
  http://127.0.0.1:5000/hired_employees
  ```
  
  2.4. Backup your tables as Avro format
  ```
  http://127.0.0.1:5000/backup
  ``` 
  
  Usage:
  Especify your backup type, in this case, table.
  {"table"}
  list of tables you want to backup:
  ["jobs","departments", "hired_employees"]
  
  ex:
  {"table": ["jobs","departments", "hired_employees"]}
  
  Return message from tables backup:
  
  ![backup](https://user-images.githubusercontent.com/113646668/209832802-227db482-b9c4-4fba-9c79-5eb8765ec407.png)
  
  
  2.6. Post method: Insert new rows, 1 up to 1000 at once. Put your data into json format, example: 

  ```
  http://127.0.0.1:5000/insert
  ```
  
  Usage:
   [{"Table name": ["table_field": "value"}]]
  
  [
  {"jobs": [{"job": "job1"}]},
  {"jobs": [{"job": "job2"}]},
  {"departments": [{"department": "department1"}]},
  {"hired_employees": [{"name": "pablo"},{"datetime": "2021-11-07T02:48:42Z"},{"department_id": 1},{"job_id": 1}]}
  ]
  
  2.7. Get or Post method: Number of employees hired for each job and department in 2021 divided by quarter. The table must be ordered alphabetically by department and job.
  ```
  http://127.0.0.1:5000/hired_2021_quarter
  ```
  
  2.6. Get or Post method: List of ids, name and number of employees hired of each department that hired more employees than the mean of employees hired in 2021 for all the departments, ordered by the number of employees hired (descending).
  ```
  http://127.0.0.1:5000/hired_department
  ```
 
  
  
