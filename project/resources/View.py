from flask import jsonify, request
from flask_restful import Resource
from ..my_model import db, Post, Comment, Like, Favorite
from ..my_model import CommentSchema, LikeSchema, FavoriteSchema

comments_schema = CommentSchema(many=True)
likes_schema = LikeSchema(many=True)
favorites_schema = FavoriteSchema(many=True)


class ViewComment(Resource):
    @staticmethod
    def get():
        user_id = request.args['user_id']
        comments = Comment.query.filter_by(user_id=user_id)
        comment = comments_schema.dump(comments).data
        return comment, 200


class ViewLike(Resource):
    @staticmethod
    def get():
        user_id = request.args['user_id']
        likes = Like.query.filter_by(user_id=user_id)
        likes = likes_schema.dump(likes).data
        return likes, 200


class ViewFavourite(Resource):
    @staticmethod
    def get():
        user_id = request.args['user_id']
        favorite = Favorite.query.filter_by(user_id=user_id)
        favorite = favorites_schema.dump(favorite).data
        return favorite, 200
