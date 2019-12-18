from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    userid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    phoneNumber = db.Column(db.String(11), unique=True)
    email = db.Column(db.String(50), unique=True)
    studentID = db.Column(db.Integer, nullable=False, unique=True)
    password = db.Column(db.String(50))
    intro = db.Column(db.Text)
    circle1 = db.Column(db.Integer)
    circle2 = db.Column(db.Integer)
    circle3 = db.Column(db.Integer)
    circle4 = db.Column(db.Integer)
    circle5 = db.Column(db.Integer)


class Posts(db.Model):
    postid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('userid'))
    circleid = db.Column(db.Integer, db.ForeignKey('circleid'))
    postTime = db.Column(db.datetime.datetime)
    centent = db.Column(db.Text)
    img1 = db.Column(db.url)
    img2 = db.Column(db.url)
    img3 = db.Column(db.url)
    img4 = db.Column(db.url)
    img5 = db.Column(db.url)
    img6 = db.Column(db.url)
    img7 = db.Column(db.url)
    img8 = db.Column(db.url)
    img9 = db.Column(db.url)
    likes = db.Column(db.Integer)
    favorites = db.Column(db.Integer)


class Circle(db.Model):
    circleid = db.Column(db.Integer)
    circleName = db.String(20, unique=True)
    peopleNumber = db.Column(db.Integer)
    intro = db.Column(db.Text)


class Comments(db.Model):
    postid = db.Column(db.Integer, db.ForeignKey('postid'))
    userid = db.Column(db.Integer, db.ForeignKey('userid'))
    commentTime = db.Column(db.datetime.datetime)
    centent = db.Column(db.Text)
    likes = db.Column(db.Integer)


class Favorites(db.Model):
    postid = db.Column(db.Integer, db.ForeignKey('postid'))
    userid = db.Column(db.Integer, db.ForeignKey('userid'))
    favouriteTime = db.Column(db.datetime.datetime)


class Likes(db.Model):
    postid = db.Column(db.Integer, db.ForeignKey('postid'))
    userid = db.Column(db.Integer, db.ForeignKey('userid'))
    likeTime = db.Column(db.datetime.datetime)


class Block(db.Model):
    postid = db.Column(db.Integer, db.ForeignKey('postid'))
    userid = db.Column(db.Integer, db.ForeignKey('userid'))

class Report(db.Model):
    postid = db.Column(db.Integer, db.ForeignKey('postid'))
    userid = db.Column(db.Integer, db.ForeignKey('userid'))
    reason = db.Column(db.Text)


class createCircle(db.Model):
    circleName = db.String(20, unique=True)
    applyNumber = db.Column(db.Integer)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
