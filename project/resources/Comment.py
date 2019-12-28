from flask import jsonify, request
from flask_restful import Resource
from ..my_model import db, Comment, CommentSchema, Post, PostSchema

comments_schema = CommentSchema(many=True)
comment_schema = CommentSchema()
posts_schema = PostSchema(many = True)
post_schema = PostSchema()


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
        post = Post.query.filter_by(post_id=post_id).first()
        post = post_schema.dump(post).data

        comment = Comment(post_id, user_id, contend, 0, post['user_id'])
        db.session.add(comment)
        db.session.commit()

        result = comment_schema.dump(comment).data

        return result, 200
