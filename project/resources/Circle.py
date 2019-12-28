from flask import request
from flask_restful import Resource
from ..my_model import db, Circle, CircleSchema, User

circles_schema = CircleSchema(many=True)
circle_schema = CircleSchema()


class GetCircles(Resource):
    @staticmethod
    def get():
        circles = Circle.query.all()
        circles = circles_schema.dump(circles).data
        return circles, 200


class GetCircle(Resource):
    @staticmethod
    def get():
        circle_id = request.args['circle_id']
        circle = Circle.query.filter_by(circle_id=circle_id).first()
        result = circle_schema.dump(circle).data
        return result, 200


class CreateCircle(Resource):
    @staticmethod
    def post():
        circle_name = request.args['circle_name']
        user_id = request.args['user_id']
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return {"message": "The user does not exit"}, 200

        circle = Circle.query.filter_by(circle_name=circle_name).first()
        if not circle:
            circle = Circle(circle_name, 1)
            db.session.add(circle)
            db.session.commit()
            
            result = circle_schema.dump(circle).data
            return {'status': 0, 'result': result}, 200

        circle.add()
        circle = circle_schema.dump(circle).data
        print(circle)
        if not user.check(circle['circle_id']):
            return {'status': 1, 'message': 'The user has joined this circle!'}
        if not user.join(circle['circle_id']):
            return {'status': 2, 'message': 'The user has joined 5 circle!'}
        db.session.commit()
        result = circle_schema.dump(circle).data
        return {'status': 0, 'result': result}, 200


class QuitCircle(Resource):
    @staticmethod
    def post():
        circle_name = request.args['circle_name']
        user_id = request.args['user_id']
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return {"message": "The user does not exit"}, 200

        circle = Circle.query.filter_by(circle_name=circle_name).first()
        if not circle:
            return {"message": "The user does not exit"}, 200
        circle.quit()
        circle = circle_schema.dump(circle).data
        if not user.quit(circle['circle_id']):
            return {'status': 1, 'message': 'The user has not joined this circle!'}
        else:
            db.session.commit()
            result = circle_schema.dump(circle).data
            return {'status': 0, 'result': result}, 200


class SearchCircle(Resource):
    @staticmethod
    def get():
        key = request.args['key']
        circle = Circle.query.filter(Circle.circle_name.ilike('%' + key + '%'))
        result = circles_schema.dump(circle).data
        return result, 200
