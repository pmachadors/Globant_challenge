<!-- <h1 align="center"> Globant Data Engineer challenge </h1> -->
# Data Engineer challenge

![AWS](https://img.shields.io/badge/account-AWS-green)
![Docker Version](https://img.shields.io/badge/docker-v20.10.21-blue)
![Docker Compose](https://img.shields.io/badge/docker--compose-v1.29.2-blue)
![Ubuntu](https://img.shields.io/badge/ubuntu-v22.04-blue)
![Python](https://img.shields.io/badge/python-v3.10-blue)
![Insomnia](https://img.shields.io/badge/insomnia-v2022.7.0-blue)

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

The csv files were stored in AWS S3 bucket and the database choosed was AWS RDS MySql. I used python and flask do build the REST API, and Insomnia software to test it.

# Requirements
docker docker-compose aws account python3

# Functionalities
1. Historical data import was made by python script import_historical_data.py. The script will create the database and tables and also insert data from csv jobs, departments and hired_employees stored in S3 AWS.

  Usage:
  Export your RDS MySql connection variables like that:

  export mysql_user=your_user
  export db_name=your_db
  export end_point=your_end_point
  export mysql_new_pwd=your_password

  python3 import_historical_data.py

  ![create companydb](https://user-images.githubusercontent.com/113646668/209831732-c345b5ac-2ef3-4beb-8fe4-deedd26133de.png)

  
2. REST API created in flask. Endpoints:
 
   Usage:  
    Clone this repository:
     ```
     git clone https://github.com/pmachadors/Globant_challenge.git
     ```

    Run docker-compose:

     ```
     docker-compose up --build
     ```

   2.3. Search all jobs[GET]
   ```
   http://127.0.0.1:5000/jobs
   ```

   ![jobs](https://user-images.githubusercontent.com/113646668/209836147-c85eb023-c6c4-4785-88de-20e935fdbfe7.png)
   

   2.4. Search all Departments[GET]
   ```
   http://127.0.0.1:5000/departments
   ```

   ![departments](https://user-images.githubusercontent.com/113646668/209836198-201782a4-e7ed-402b-b91a-1603e53973b6.png)


   2.5. Search all Hired_employees[GET]
   ```
   http://127.0.0.1:5000/hired_employees
   ```
   ![hired_employees](https://user-images.githubusercontent.com/113646668/209836256-f8767cdc-fc24-4ada-934e-d6f81f216543.png)



   2.6. Backup your tables as Avro format[GET or POST]
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


   2.7. Restore your tables from Avro format[GET or POST]
   ```
   http://127.0.0.1:5000/restore
   ``` 

   Usage:

   Especify your restore type, in this case, table.

   {"table"}
   list of tables you want to restore:
   ["departments"]

   ex:
   {"table": ["departments"]}

   ![restore](https://user-images.githubusercontent.com/113646668/209833454-6cf24180-5eb6-4721-9fb6-a90f8b49e016.png)



   2.8. Insert new rows, 1 up to 1000 at once. Put your data into json format[POST]

   ```
   http://127.0.0.1:5000/insert
   ```
   ![insert](https://user-images.githubusercontent.com/113646668/209837343-8e177ee9-f890-4f95-94f2-c567e7d186d6.png)



   Usage:
    [{"Table name": ["table_field": "value"}]]

   [
   {"jobs": [{"job": "job1"}]},
   {"jobs": [{"job": "job2"}]},
   {"departments": [{"department": "department1"}]},
   {"hired_employees": [{"name": "pablo"},{"datetime": "2021-11-07T02:48:42Z"},{"department_id": 1},{"job_id": 1}]}
   ]

   2.9. Number of employees hired for each job and department in 2021 divided by quarter. The table must be ordered alphabetically by department and job[GET or POST]
   ```
   http://127.0.0.1:5000/hired_2021_quarter
   ```
   ![hired_2021_quarter](https://user-images.githubusercontent.com/113646668/209837383-ce2e3917-a6c3-4d97-86f9-0f7b898f723b.png)



   2.10. List of ids, name and number of employees hired of each department that hired more employees than the mean of employees hired in 2021 for all the departments, ordered by the number of employees hired (descending)[GET or POST]
   ```
   http://127.0.0.1:5000/hired_department
   ```

   ![hired_department](https://user-images.githubusercontent.com/113646668/209837407-e05c1330-2137-43bf-84e3-c5c69aa9cca0.png)

 
  
  
