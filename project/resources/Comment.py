from flask import jsonify, request
from flask_restful import Resource
from ..my_model import db, Comment, CommentSchema

comments_schema = CommentSchema(many=True)
comment_schema = CommentSchema()


class CommentResource(Resource):
    @staticmethod
    def get():
        post_id = request.args['post_id']
        user = Comment.query.filter_by(post_id=post_id)
        result = comments_schema.dump(user).data
        return result, 200

    @staticmethod
    def post():
        post_id = request.args['post_id']
        user_id = request.args['user_id']
        contend = request.args['contend']
        comment = Comment(post_id, user_id, contend, 0)
        db.session.add(comment)
        db.session.commit()

        result = comment_schema.dump(comment).data
        return result, 200
