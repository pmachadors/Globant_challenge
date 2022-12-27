from flask import Flask,jsonify,request
from flask_restful import Api,marshal_with,fields,abort
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import Schema, fields


user= os.getenv('mysql_user')
pwd = os.getenv('mysql_new_pwd')
port = 3306
db_name = os.getenv('db_name')
endpoint= os.getenv('end_point')

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{pwd}@{endpoint}:{port}/{db_name}'
db = SQLAlchemy(app)

class JobsModel(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(100), nullable=False)

    # hired_employees = db.relationship('HiredEmployeesModel', back_populates='jobs',lazy='dynamics')

    def __repr__(self):
        return f'Job(id = {self.id}'

class JobsSchema(Schema):
    id = fields.Int()
    job = fields.Str()


class DepartmentModel(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(100), nullable=False)

#     hired_employees = db.relationship('HiredEmployeesModel', back_populates='departments',lazy='dynamics')

    def __repr__(self):
        return f'Department(id = {self.id}'

class DepartmentsSchema(Schema):
    id = fields.Int()
    department = fields.Str()

class HiredEmployeesModel(db.Model):
    __tablename__ = 'hired_employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    datetime = db.Column(db.String(50), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    # department = db.relationship('DepartmentModel', back_populates='hired_employees')    
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    # job = db.relationship('JobsModel', back_populates='hired_employees')

    def __repr__(self):
        return f'Hired_employee(id = {self.id}'

class HiredEmployeeSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    datetime = fields.Str()
    department_id = fields.Int()
    job_id = fields.Int()

@app.get('/jobs') 
def get_jobs():
    jobs_schema = JobsSchema(many=True)
    result = jobs_schema.dump(JobsModel.query.all())
    return result

@app.get('/departments') 
def get_departments():
    departments_schema = DepartmentsSchema(many=True)
    result = departments_schema.dump(DepartmentModel.query.all())
    return result

@app.get('/hired_employees') 
def get_hired_employees():
    hired_employees_schema = HiredEmployeeSchema(many=True)
    result = hired_employees_schema.dump(HiredEmployeesModel.query.all())
    return result


@app.post('/insert') 
def post_jobs():
    data_insert = []
    data_request = request.get_json()

    jobs_schema = JobsSchema()                            
    departments_schema = DepartmentsSchema()
    hired_employees_schema = HiredEmployeeSchema()

    for table,fields in data_request.items():        
        if table == 'jobs':
                for values in fields:
                    if 'job' in values:
                        try:
                            job = JobsModel(job=values['job'])
                            db.session.add(job)
                            db.session.commit()
                            data_insert.append(jobs_schema.dump(job))
                        except SQLAlchemyError:
                            abort(500,message=f'Erro while inserting {values}')
                    else:
                        print (f'Field job is required. {values} not inserted')
        elif table == 'departments':
             for values in fields:
                    if 'department' in values:
                        try:
                            department = DepartmentModel(department=values['department'])
                            db.session.add(department)
                            db.session.commit()
                            data_insert.append(departments_schema.dump(department))
                        except SQLAlchemyError:
                            abort(500,message=f'Erro while inserting {values}')
                    else:
                        print (f'Field department is required. {values} not inserted')
        elif table == 'hired_employees':
            for values in fields:
                if 'name' in values:
                    value_name = [values['name']]
                elif 'datetime' in values:
                    value_datetime = [values['datetime']]
                elif 'department_id' in values:
                    value_departments_id = [values['department_id']]
                elif 'job_id' in values:
                    value_job_id = [values['job_id']]
            try:
                hired_employee = HiredEmployeesModel(name=value_name,datetime=value_datetime, department_id=value_departments_id, job_id=value_job_id)
                db.session.add(hired_employee)
                db.session.commit()
                data_insert.append(hired_employees_schema.dump(hired_employee))
            except SQLAlchemyError:
                abort(500,message=f'Erro while inserting {values}')
        else:
            print(f'Table {table} does not exist. Not inserted:{table}{fields}')
                    
    if not data_insert:
        abort(500,message=f'None job inserted')
    return data_insert,200
    
if __name__ == '__main__':
    app.run(debug=True)

