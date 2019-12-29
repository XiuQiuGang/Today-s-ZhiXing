from flask import request
from flask_restful import Resource
from ..my_model import db, User, UserSchema
import requests
users_schema = UserSchema(many=True)
user_schema = UserSchema()


class GetUsers(Resource):
    @staticmethod
    def get():
        users = User.query.all()
        users = users_schema.dump(users).data
        return {'status': 'success', 'data': users}, 200


class ViewUserInfo(Resource):
    @staticmethod
    def get():
        user_id = request.args['user_id']
        user = User.query.filter_by(user_id=user_id).first()
        result = user_schema.dump(user).data
        return result, 200

class Register(Resource):
    @staticmethod
    def post():
        json_data = request.get_json(force=True)
        
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 422
        user = User.query.filter_by(username=data['username']).first()
        if user:
            return {'status_code': 1}, 200

        user = User.query.filter_by(email=data['email']).first()
        if user:
            return {'status_code': 2}, 200

        # print(data['email'].split('@')[1])
        if data['email'].split('@')[1] != 'bjtu.edu.cn':
            return {'status_code': 3}, 200

        user = User(
            username=data['username'],
            password=data['password'],
            email=data['email']
        )
        db.session.add(user)
        db.session.commit()

        return {'status_code': 0}, 200


class Login(Resource):
    @staticmethod
    def post():
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 422
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            return {'status_code': 2}, 200

        result = user_schema.dump(user).data
        print(result)
        if result['password'] != data['password']:
            return {'status_code': 3}, 200

        if result['intro'] is None:
            return {'status_code': 1, 'user_id': result['user_id']}, 200

        return {'status_code': 0, 'user_id': result['user_id']}, 200


class UpdateUserInformation(Resource):
    @staticmethod
    def put():
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 422
        user = User.query.filter_by(user_id=data['user_id']).first()
        if not user:
            return {'message': 'user does not exist'}, 400

        result = user_schema.dump(user).data
        print(result)
        user.update(data['nick_name'], data['intro'], data['profile'])
        db.session.commit()
        result = user_schema.dump(user).data
        return result, 200
