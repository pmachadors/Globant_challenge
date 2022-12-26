from flask import Flask,jsonify,request
from flask_restful import Api,marshal_with,fields,abort
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.exc import SQLAlchemyError

user='admin'
pwd = os.getenv('mysql_pwd')
port = 3306
db_name = 'companydb'
endpoint='companydb.c3hqda7obrsd.us-east-1.rds.amazonaws.com'

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{pwd}@{endpoint}:{port}/{db_name}'
db = SQLAlchemy(app)

class JobsModel(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(100), nullable=False)

jobs_fields = {
	'id': fields.Integer,
	'job': fields.String
}

@app.get('/jobs') 
@marshal_with(jobs_fields)
def get_jobs():
    result = JobsModel.query.all()
    return result


if __name__ == '__main__':
    app.run(debug=True)