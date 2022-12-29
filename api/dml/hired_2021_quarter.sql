-- Number of employees hired for each job and department in 2021 divided by quarter. The
-- table must be ordered alphabetically by department and job.1

with query1 as (
    select d.department, j.job, 
    if(QUARTER(datetime)=1,count(h.name),0) as q1,
    if(QUARTER(datetime)=2,count(h.name),0) as q2, 
    if(QUARTER(datetime)=3,count(h.name),0) as q3,
    if(QUARTER(datetime)=4,count(h.name),0) as q4
    from hired_employees h, departments d, jobs j
    where year(h.datetime) = 2021
    and h.job_id = j.id
    and h.department_id = d.id
    group by d.department, j.job,QUARTER(datetime)
    order by d.department, j.job
)
select query1.department, query1.job, 
    sum(q1) q1, sum(q2) q2,sum(q3)q3,sum(q4) q4
    from query1
    group by query1.department, query1.job;