from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os

user='admin'
pwd = os.getenv('mysql_pwd')
port = 3306
db_name = 'companydb'
endpoint='companydb.c3hqda7obrsd.us-east-1.rds.amazonaws.com'

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{pwd}@{endpoint}:{port}/{db_name}'
db = SQLAlchemy(app)

class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'Job(id = {self.id}'

resource_fields = {
	'id': fields.Integer,
	'job': fields.String
}

class Jobs_request(Resource):

    @marshal_with(resource_fields)
    def get(self,job_id):   
        result = Jobs.query.filter_by(id=job_id).first()
        return result
        
api.add_resource(Jobs_request,'/jobs/<int:job_id>')

if __name__ == '__main__':
    app.run(debug=True)