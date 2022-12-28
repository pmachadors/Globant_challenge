create table departments (
    id int not null AUTO_INCREMENT, 
    department varchar(100) not null UNIQUE, 
    PRIMARY KEY (id)
);

create table jobs (
    id int not null AUTO_INCREMENT, 
    job varchar(100) not null UNIQUE, 
    PRIMARY KEY (ID)
);

create table hired_employees (
    id int not null AUTO_INCREMENT, 
    name varchar(200) not null UNIQUE, 
    datetime varchar(50) not null UNIQUE, 
    department_id int not null,
    job_id int not null,
    PRIMARY KEY (id),
    FOREIGN KEY (department_id) 
        REFERENCES companydb.departments(id)
        ON DELETE CASCADE, 
    FOREIGN KEY (job_id) 
        REFERENCES companydb.jobs(id)
        ON DELETE CASCADE
);

