from flask import Blueprint
from flask_restful import Api
from .resources.Hello import Hello
from .resources.Comment import CommentResource
from .resources.User import Register, Login, GetUsers, UpdateUserInformation, ViewUserInfo
from .resources.Image import Image
from .resources.Post import GetPosts, PostAction, GetPost, SearchUser, GetByCircle, HistoryPost
from .resources.Circle import GetCircles, GetCircle, CreateCircle, SearchCircle, QuitCircle
from .resources.Interact import LikePostResource, LikeCommentResource, Favourite
from .resources.View import ViewComment, ViewLike, ViewFavourite
from .resources.Block import BlockPost

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes

# Try
api.add_resource(Hello, '/Hello')

# User
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(GetUsers, '/getUsers')
api.add_resource(UpdateUserInformation, '/edit_user_info')
api.add_resource(ViewUserInfo, '/view_user_info')

# Image
api.add_resource(Image, '/image')

# Post
api.add_resource(GetPosts, '/get_posts')
api.add_resource(PostAction, '/post')
api.add_resource(GetPost, '/get_post_info')
api.add_resource(SearchUser, '/search_post')
api.add_resource(GetByCircle, '/get_by_circle')
api.add_resource(HistoryPost, '/history_post')

# Circle
api.add_resource(GetCircles, '/view_circles')
api.add_resource(GetCircle, '/get_circle')
api.add_resource(CreateCircle, '/join_circle')
api.add_resource(SearchCircle, '/search_circle')
api.add_resource(QuitCircle, '/quit_circle')

# Comment
api.add_resource(CommentResource, '/comment')

# Interact
api.add_resource(LikePostResource, '/like_post')
api.add_resource(LikeCommentResource, '/like_comment')
api.add_resource(Favourite, '/favorite')

# View
api.add_resource(ViewComment, '/view_my_comment')
api.add_resource(ViewLike, '/view_my_like')
api.add_resource(ViewFavourite, '/view_my_favourite')

# Block
api.add_resource(BlockPost, '/block_post')

