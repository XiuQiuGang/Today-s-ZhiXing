from flask import make_response, Blueprint
from flask import current_app as app
from . import db
from project.model import User


main = Blueprint('main', __name__)
@main.route('/')
def create():
    """Endpoint to create a user."""
    new_user = User(user_id='1', name='abc', phoneNumber='18812345678', email='huzujun1024@gmail.com',
                    studentID='17301095', password='123456', intro='Haha')
    db.session.add(new_user)
    db.session.commit()
    print(1)
    return make_response("User created!")
