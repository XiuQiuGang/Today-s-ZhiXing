from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

ma = Marshmallow()
db = SQLAlchemy()


class User(db.Model):
    __table_name__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
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


class Circle(db.Model):
    __table_name__ = 'circle'
    circle_id = db.Column(db.Integer, primary_key=True)
    circleName = db.Column(db.String(20), unique=True)
    peopleNumber = db.Column(db.Integer)
    intro = db.Column(db.Text)


class Posts(db.Model):
    __table_name__ = 'posts'
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    circle_id = db.Column(db.Integer, db.ForeignKey('circle.circle_id'))
    postTime = db.Column(db.DateTime)
    contend = db.Column(db.Text)
    img = db.Column(db.String(100))
    likes = db.Column(db.Integer)
    favorites = db.Column(db.Integer)


class Comments(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    commentTime = db.Column(db.DateTime)
    contend = db.Column(db.Text)
    likes = db.Column(db.Integer)


class Favorites(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    favouriteTime = db.Column(db.DateTime)


class Likes(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    likeTime = db.Column(db.DateTime)


class Block(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)


class Report(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    reason = db.Column(db.Text)


class CreateCircle(db.Model):
    circle_id = db.Column(db.Integer, primary_key=True)
    circleName = db.Column(db.String(20))
    applyNumber = db.Column(db.Integer)

