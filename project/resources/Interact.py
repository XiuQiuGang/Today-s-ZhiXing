from flask import jsonify, request
from flask_restful import Resource
from ..my_model import db, Post, Comment, Like, Favorite, PostSchema, CommentSchema

comment_schema = CommentSchema()
post_schema = PostSchema()


class LikePostResource(Resource):
    @staticmethod
    def post():
        post_id = request.args['post_id']
        user_id = request.args['user_id']
        
        like = Like.query.filter_by(post_id=post_id, user_id=user_id).first()
        if like:
            return {"message": "has liked"}, 200

        post = Post.query.filter_by(post_id=post_id).first()
        post.like()
        result = post_schema.dump(post).data

        like = Like(post_id, user_id, result['user_id'])
        db.session.add(like)
        db.session.commit()

        return result, 200


class LikeCommentResource(Resource):
    @staticmethod
    def post():
        comment_id = request.args['comment_id']

        comment = Comment.query.filter_by(Comment_id=comment_id).first()
        comment.like()
        db.session.commit()
        result = comment_schema.dump(comment).data
        return result, 200


class Favourite(Resource):
    @staticmethod
    def post():
        post_id = request.args['post_id']
        user_id = request.args['user_id']

        favorite = Favorite.query.filter_by(post_id=post_id, user_id=user_id).first()
        if favorite:
            return {"message": "has favorite"}, 200

        favorite = Favorite(post_id, user_id)
        db.session.add(favorite)

        post = Post.query.filter_by(post_id=post_id).first()
        post.favorite()
        db.session.commit()
        result = post_schema.dump(post).data
        return result, 200
