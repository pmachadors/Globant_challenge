from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLAlCHEMY_DATRABASE_URI'] = 'sqlite:///database.db'
# engine = create_engine("mysql+pymysql://scott:tiger@localhost/foo")
db = SQLAlchemy(app)
# db.create_all()

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Video(name={self.name},views={self.views},likes={self.likes})'

#db.create_all()

video_put_arguments = reqparse.RequestParser()
video_put_arguments.add_argument('name',type=str,help='name of the video is required',required=True)
video_put_arguments.add_argument('views',type=int,help='views of the video is required',required=True)
video_put_arguments.add_argument('likes',type=int,help='likes of the video is required',required=True)
videos = {}

def video_doesnot_exist(video_id):
        if video_id not in videos:
            abort(404,message=f'Video {video_id} id is not valid')

def video_exists(video_id):
        if video_id in videos:
            abort(409,message=f'Video {video_id} already exists')

class Video(Resource):
    def get(self,video_id):
        video_doesnot_exist(video_id)
        return videos[video_id]

    def put(self,video_id):
        video_exists(video_id)
        args = video_put_arguments.parse_args()
        videos[video_id] = args
        return videos[video_id], 201
    
    def delete(self,video_id):
        video_doesnot_exist(video_id)
        del videos[video_id]
        return '', 204
    
api.add_resource(Video,'/video/<int:video_id>')

if __name__ == '__main__':
    app.run(debug=True)