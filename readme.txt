1) Criei um servidor EC2 Ubuntu 20.04 (REST-API)
2) Crei um banco de dados RDS MySql 8.0 (Company)
3) Instalei o Client no EC2 
	- sudo apt install mysql-client
	- company.c3hqda7obrsd.us-east-1.rds.amazonaws.com
	- mysql -h company.c3hqda7obrsd.us-east-1.rds.amazonaws.com -u admin -p
	- create database company;
4) Importando dados antigos
python3 -m venv venv


