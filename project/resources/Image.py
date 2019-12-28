from flask import request, send_file
from flask_restful import Resource
from ..my_model import db, User, UserSchema
import werkzeug
import os
from configparser import ConfigParser

users_schema = UserSchema(many=True)
user_schema = UserSchema()


class Image(Resource):
    @staticmethod
    def post():
        image_file = request.files['image']
        s = image_file.filename
        the_format = s.split('.')[1]
        parser = ConfigParser()
        basedir = os.path.abspath(os.path.dirname(__file__))
        print(basedir)
        parser.read(basedir+'/config.ini')
        image_nums = parser.get('data', 'image_nums')
        file_name = image_nums + '.' + the_format
        image_file.save(os.path.join(basedir[:-10], 'static', file_name))

        parser.set('data', 'image_nums', str(int(image_nums) + 1))
        print(parser.get('data', 'image_nums'))

        with open(basedir+"/config.ini", 'w') as f:
            parser.write(f)
        return 'http://120.27.247.14/static/'+file_name


class Video(Resource):
    @staticmethod
    def post():
        video_file = request.files['video']
        s = video_file.filename
        the_format = s.split('.')[1]
        parser = ConfigParser()
        basedir = os.path.abspath(os.path.dirname(__file__))
        print(basedir)
        parser.read(basedir+'/config.ini')
        image_nums = parser.get('data', 'video_nums')
        file_name = image_nums + '.' + the_format
        video_file.save(os.path.join(basedir[:-10], 'static', file_name))

        parser.set('data', 'video_nums', str(int(image_nums) + 1))
        print(parser.get('data', 'video_nums'))

        with open(basedir+"/config.ini", 'w') as f:
            parser.write(f)
        return 'http://120.27.247.14/static/'+file_name

