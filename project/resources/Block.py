from flask import request
from flask_restful import Resource
from my_model import db, Post, PostSchema, Block, BlockSchema

posts_schema = PostSchema(many=True)
post_schema = PostSchema()
blocks_schema = BlockSchema(many=True)
block_schema = BlockSchema()


class BlockPost(Resource):
    @staticmethod
    def post():
        post_id = request.args['post_id']
        user_id = request.args['user_id']
        block = Block(post_id, user_id)
        db.session.add(block)
        db.session.commit()
        return 'success', 200
