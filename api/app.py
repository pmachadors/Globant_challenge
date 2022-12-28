from flask import Flask,jsonify,request,abort
from flask_restful import Api,fields
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import Schema, fields
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

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
    result = jobs_schema.dump(JobsModel.query.order_by(JobsModel.id).all())
    return result

@app.get('/departments') 
def get_departments():
    departments_schema = DepartmentsSchema(many=True)
    result = departments_schema.dump(DepartmentModel.query.order_by(DepartmentModel.id).all())
    return result

@app.get('/hired_employees') 
def get_hired_employees():
    hired_employees_schema = HiredEmployeeSchema(many=True)
    result = hired_employees_schema.dump(HiredEmployeesModel.query.order_by(HiredEmployeesModel.id).all())
    return result

@app.post('/insert') 
def post_jobs():
    data_insert = []
    data_request = request.get_json()

    jobs_schema = JobsSchema()                            
    departments_schema = DepartmentsSchema()
    hired_employees_schema = HiredEmployeeSchema()

    if len(data_request) > 1000:
        abort(500,f'Rows limit is 1000.')

    for tables in data_request: 
          
        for table,fields in tables.items():        
            if table == 'jobs':
                    for values in fields:
                        if 'job' in values:
                            try:
                                job = JobsModel(job=values['job'])
                                db.session.add(job)
                                db.session.commit()
                                data_insert.append(jobs_schema.dump(job))
                            except SQLAlchemyError:
                                abort(500,f'Erro while inserting {values}')
                        else:
                            print (f'Only field job is required. {values} not inserted')
            elif table == 'departments':
                for values in fields:
                        if 'department' in values:
                            try:
                                department = DepartmentModel(department=values['department'])
                                db.session.add(department)
                                db.session.commit()
                                data_insert.append(departments_schema.dump(department))
                            except SQLAlchemyError:
                                abort(f'Erro while inserting {values}',500)
                        else:
                            print (f'Only field department is required. {values} not inserted')
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
                    abort(500,f'Erro while inserting {values}')
            else:
                print(f'Table {table} does not exist. Not inserted:{table}{fields}')
                        
    if not data_insert:
        abort(500,f'None job inserted')
    return data_insert,200

@app.route('/backup', methods=['GET', 'POST'])
def backup():
    tables_request = request.get_json()
    list_backup = []
    
    for tables in tables_request.values():
        for table in tables:
            if not table in ('jobs','departments','hired_employees'):
                print ({"table not valid": table})
            else:
                avro_schema = avro.schema.parse(open(f'api/avro/{table}.avsc', 'r').read())
                writer = DataFileWriter(open(f'api/avro/{table}.avro', 'wb'), DatumWriter(), avro_schema)
                result = db.engine.execute(f'select * from {table}')
                for row in result:
                    writer.append(dict(row))
                writer.close()
                list_backup.append({table:"Backup executed!"})

    if list_backup:
        return list_backup
    else:
        abort(500,f'None table restored') 

def check_backup(table_name):
    path = os.getcwd()
    tables = (os.listdir(f'{path}/api/avro/'))
    table_name = table_name + '.avro'
    if table_name in tables:
        return True
    else:
        return False

@app.route('/restore', methods=['GET', 'POST'])
def restore():
    tables_request = request.get_json()
    list_restore = []

    for tables in tables_request.values():
        for table in tables:
            if not table in ('jobs','departments','hired_employees'):
                    print ({"Table not valid": table})
            else:
                if check_backup(table):
                    data_reader = DataFileReader(open(f'api/avro/{table}.avro', 'rb'), DatumReader())
                    db.engine.execute(f'delete from {table}')
                    db.session.commit()

                    if table == 'jobs':
                            for row in data_reader:
                                row = JobsModel(id=row['id'], job=row['job'])
                                db.session.add(row)
                                db.session.commit()            
                            list_restore.append({table:"Table restored!"})    
                            data_reader.close()
                        
                    elif table == 'departments':
                            for row in data_reader:
                                row = DepartmentModel(id=row['id'], department=row['department'])
                                db.session.add(row)
                                db.session.commit()
                            list_restore.append({table:"Table restored!"})    
                            data_reader.close()
                    elif table == 'hired_employees':
                            for row in data_reader:                        
                                row = HiredEmployeesModel(id=row['id'], name=row['name'], datetime=row['datetime'], department_id=row['department_id'], job_id=row['job_id'])
                                db.session.add(row)
                                db.session.commit()                                
                            list_restore.append({table:"Table restored!"})
                            data_reader.close()
                else:
                    print ({f'Table {table} without backup'})

    if list_restore:
        return list_restore
    else:
        abort(500,'None table restored')

@app.route('/hired_2021_quarter', methods=['GET', 'POST'])
def hired_2021_quarter():
    path = os.getcwd()
    with open(f'{path}/api/dml/hired_2021_quarter.sql') as file:
        sql_quarter = file.read()
        result = db.engine.execute(sql_quarter)
        return jsonify({'result': [dict(row) for row in result]})

@app.route('/hired_department', methods=['GET', 'POST'])
def hired_department():
    path = os.getcwd()
    with open(f'{path}/api/dml/hired_department.sql') as file:
        sql_hired_department = file.read()
        result = db.engine.execute(sql_hired_department)
        return jsonify({'result': [dict(row) for row in result]})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    
