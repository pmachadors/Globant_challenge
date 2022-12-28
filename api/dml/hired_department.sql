-- List of ids, name and number of employees hired of each department that hired more
-- employees than the mean of employees hired in 2021 for all the departments, ordered
-- by the number of employees hired (descending).

select d.id, d.department, count(h.id) qtd_employees
from departments d, hired_employees h
where d.id = h.department_id
group by d.id
having count(h.id) > (select count(h.id)/(select count(distinct(d.id)) from departments d)
from hired_employees h
where year(h.datetime) = 2021)
order by 3 desc;