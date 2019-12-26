from flask import Blueprint
from flask_restful import Api
from resources.Hello import Hello
from resources.Category import CategoryResource
from resources.Comment import CommentResource
from resources.User import Register, Login, GetUser, UpdateUserInformation
from resources.Image import Image

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes

api.add_resource(Hello, '/Hello')
api.add_resource(CategoryResource, '/Category')
api.add_resource(CommentResource, '/Comment')

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(GetUser, '/getUsers')
api.add_resource(UpdateUserInformation, '/edit_user_info')

api.add_resource(Image, '/image')
