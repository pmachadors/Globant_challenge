from flask import Flask,jsonify,request
from flask_restful import Api,marshal_with,fields,abort
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.exc import SQLAlchemyError

user='admin'
pwd = os.getenv('mysql_new_pwd')
port = 3306
db_name = 'companydb'
endpoint='company.c3hqda7obrsd.us-east-1.rds.amazonaws.com'

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{pwd}@{endpoint}:{port}/{db_name}'
db = SQLAlchemy(app)

class JobsModel(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(100), nullable=False)

    # hired_employees = db.relationship('HiredEmployeesModel', back_populates='jobs',lazy='dynamics')

    # def __repr__(self):
    #     return f'Job(id = {self.id}'

class DepartmentModel(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(100), nullable=False)

#     hired_employees = db.relationship('HiredEmployeesModel', back_populates='departments',lazy='dynamics')

#     def __repr__(self):
#         return f'Department(id = {self.id}'

class HiredEmployeesModel(db.Model):
    __tablename__ = 'hired_employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    datetime = db.Column(db.String(50), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    # department = db.relationship('DepartmentModel', back_populates='hired_employees')    
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    # job = db.relationship('JobsModel', back_populates='hired_employees')

jobs_fields = {
	'id': fields.Integer,
	'job': fields.String
}

departments_fields = {
	'id': fields.Integer,
	'department': fields.String
}

hired_employees_fields= {
    'id': fields.Integer,
	'name': fields.String,
    'datetime': fields.String,
    'department_id': fields.String,
    'job_id': fields.String
}

@app.get('/jobs') 
@marshal_with(jobs_fields)
def get_jobs():
    result = JobsModel.query.all()
    return result

@app.get('/departments') 
@marshal_with(departments_fields)
def get_departments():
    result = DepartmentModel.query.all()
    return result

@app.get('/hired_employees') 
@marshal_with(hired_employees_fields)
def get_hired_employees():
    # result = HiredEmployeesModel.query.all()
    result = HiredEmployeesModel.query.first()
    return result


def post_jobs():
    jobs_request = request.get_json()

    for data in jobs_request:
        if data == 'jobs':
            for key, value in data.items:
                if key == 'job':
                    print (print(value))

@app.post('/jobs') 
@marshal_with(jobs_fields)
def post_jobs():
    jobs_insert = []
    jobs_request = request.get_json()
    for data in jobs_request:
        if 'job' in data:
            job = JobsModel(job=data['job'])
            try:
                db.session.add(job)
                db.session.commit()
                jobs_insert.append(job)
            except SQLAlchemyError:
                abort(500,message=f'Erro while inserting {data}')
        elif 'department' in data:
            department = DepartmentModel(department=data['department'])
            try:
                db.session.add(department)
                db.session.commit()
                jobs_insert.append(department)
            except SQLAlchemyError:
                abort(500,message=f'Erro while inserting {data}')
        else:
            print (f'Field job or department is required. {data} not inserted')
    if not jobs_insert:
        abort(500,message=f'None job inserted')
    return jobs_insert,200

if __name__ == '__main__':
    app.run(debug=True)

