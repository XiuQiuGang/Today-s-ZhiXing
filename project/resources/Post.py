from flask import request
from flask_restful import Resource
from ..my_model import db, Post, PostSchema, User, Block, BlockSchema

posts_schema = PostSchema(many=True)
post_schema = PostSchema()
blocks_schema = BlockSchema(many=True)
block_schema = BlockSchema()


class GetPosts(Resource):
    @staticmethod
    def get():
        posts = Post.query.all()
        posts = posts_schema.dump(posts).data
        return {'status': 'success', 'data': posts}, 200


class GetPost(Resource):
    @staticmethod
    def get():
        post_id = request.args['post_id']
        post = Post.query.filter_by(post_id=post_id).first()
        result = post_schema.dump(post).data
        return result, 200


class GetByCircle(Resource):
    @staticmethod
    def get():
        circle_id = request.args['circle_id']
        user_id = request.args['user_id']
        blocks = Block.query.filter_by(user_id=user_id)
        blocks = posts_schema.dump(blocks).data
        blocks = [block['post_id'] for block in blocks]
        post = Post.query.filter_by(circle_id=circle_id)
        start = request.args['start']
        end = request.args['end']
        result = posts_schema.dump(post).data

        new_result = []
        for r in result:
            if r['post_id'] not in blocks:
                new_result.append(r)
        new_result.sort(key=lambda the_post: the_post['postTime'])
        return new_result[int(start) - 1: min(int(end), len(result))]


class SearchUser(Resource):
    @staticmethod
    def get():
        key = request.args['key']
        post = Post.query.filter(Post.content.ilike('%' + key + '%'))
        result = posts_schema.dump(post).data
        return result, 200


class PostAction(Resource):
    @staticmethod
    def post():
        user_id = request.form['user_id']
        user = User.query.filter_by(user_id=user_id).first()

        if not user:
            return {'message': 'The User does not exist'}, 200

        post = Post(request.form['user_id'], request.form['circle_id'], request.form['content'],
                    request.form['img'])
        db.session.add(post)
        db.session.commit()

        result = post_schema.dump(post).data
        return result, 200


class HistoryPost(Resource):
    @staticmethod
    def get():
        user_id = request.args['user_id']
        posts = Post.query.filter_by(user_id=user_id)
        posts = posts_schema.dump(posts).data
        return posts, 200
