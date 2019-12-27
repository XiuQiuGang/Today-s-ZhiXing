from flask import request, send_file
from flask_restful import Resource
from my_model import db, User, UserSchema
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
        parser.read('config.ini')
        image_nums = parser.get('data', 'image_nums')
        file_name = image_nums + '.' + the_format
        image_file.save(os.path.join('static', file_name))

        parser.set('data', 'image_nums', str(int(image_nums) + 1))
        print(parser.get('data', 'image_nums'))

        with open("config.ini", 'w') as f:
            parser.write(f)
        return file_name

    @staticmethod
    def get():
        file_name = request.form['file_name']
        print(file_name, type(file_name))
        return send_file(os.path.join('static', file_name), as_attachment=True)
