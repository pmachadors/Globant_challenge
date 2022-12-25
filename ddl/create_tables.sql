create table departments (
    id int not null AUTO_INCREMENT, 
    department varchar(100), 
    PRIMARY KEY (id)
);

create table jobs (
    id int not null AUTO_INCREMENT, 
    job  varchar(100), 
    PRIMARY KEY (ID)
);

create table hired_employees (
    id int not null AUTO_INCREMENT, 
    name varchar(200), 
    datetime varchar(50), 
    department_id int,
    job_id int,
    PRIMARY KEY (id),
    FOREIGN KEY (department_id) REFERENCES companydb.departments(id), 
    FOREIGN KEY (job_id) REFERENCES companydb.jobs(id)
);

