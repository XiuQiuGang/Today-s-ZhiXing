from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

ma = Marshmallow()
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(50))
    email = db.Column(db.String(50))
    nick_name = db.Column(db.String(50))
    profile = db.Column(db.String(100))
    intro = db.Column(db.Text)
    circle1 = db.Column(db.Integer)
    circle2 = db.Column(db.Integer)
    circle3 = db.Column(db.Integer)
    circle4 = db.Column(db.Integer)
    circle5 = db.Column(db.Integer)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def update(self, nick_name, intro, profile):
        self.nick_name = nick_name
        self.intro = intro
        self.profile = profile
        self.circle1 = -1
        self.circle2 = -1
        self.circle3 = -1
        self.circle4 = -1
        self.circle5 = -1

    def join(self, circle_id):
        if self.circle1 == -1:
            self.circle1 = circle_id
        elif self.circle2 == -1:
            self.circle2 = circle_id
        elif self.circle3 == -1:
            self.circle3 = circle_id
        elif self.circle4 == -1:
            self.circle4 = circle_id
        elif self.circle5 == -1:
            self.circle5 = circle_id
        else:
            return False
        return True

    def check(self, circle_id):
        if self.circle1 == circle_id:
            return False
        if self.circle2 == circle_id:
            return False
        if self.circle3 == circle_id:
            return False
        if self.circle4 == circle_id:
            return False
        if self.circle5 == circle_id:
            return False
        return True

    def quit(self, circle_id):
        if self.circle1 == circle_id:
            self.circle1 = -1
        elif self.circle2 == circle_id:
            self.circle2 = -1
        elif self.circle3 == circle_id:
            self.circle3 = -1
        elif self.circle4 == circle_id:
            self.circle4 = -1
        elif self.circle5 == circle_id:
            self.circle5 = -1
        else:
            return False
        return True


class UserSchema(ma.Schema):
    user_id = fields.Integer()
    username = fields.String()
    password = fields.String()
    email = fields.Email()
    studentID = fields.Integer()
    intro = fields.String()
    nick_name = fields.String()
    profile = fields.String()
    circle1 = fields.Integer()
    circle2 = fields.Integer()
    circle3 = fields.Integer()
    circle4 = fields.Integer()
    circle5 = fields.Integer()


class Circle(db.Model):
    __tablename__ = 'circle'
    circle_id = db.Column(db.Integer, primary_key=True)
    circle_name = db.Column(db.String(20), unique=True)
    people_number = db.Column(db.Integer)

    def __init__(self, circle_name, people_number):
        self.circle_name = circle_name
        self.people_number = people_number

    def add(self):
        self.people_number += 1

    def quit(self):
        self.people_number -= 1


class CircleSchema(ma.Schema):
    circle_id = fields.Integer()
    circle_name = fields.String()
    people_number = fields.Integer()


class Post(db.Model):
    __tablename__ = 'post'
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    circle_id = db.Column(db.Integer, db.ForeignKey('circle.circle_id'))
    postTime = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    content = db.Column(db.String(10000))
    img = db.Column(db.String(100))
    likes = db.Column(db.Integer)
    favorites = db.Column(db.Integer)

    def __init__(self, user_id, circle_id, content, img):
        self.user_id = user_id
        self.circle_id = circle_id
        self.content = content
        self.img = img
        self.likes = 0
        self.favorites = 0

    def like(self):
        self.likes += 1

    def favorite(self):
        self.favorites += 1


class PostSchema(ma.Schema):
    post_id = fields.Integer()
    user_id = fields.Integer()
    circle_id = fields.Integer()
    content = fields.String()
    img = fields.String()
    likes = fields.Integer()
    favorites = fields.Integer()
    postTime = fields.DateTime()


class Comment(db.Model):
    __tablename__ = 'comment'
    Comment_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    comment_to = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    commentTime = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    content = db.Column(db.String(10000))
    likes = db.Column(db.Integer)

    def __init__(self, post_id, user_id, content, likes, comment_to):
        self.post_id = post_id
        self.user_id = user_id
        self.content = content
        self.likes = likes
        self.comment_to = comment_to

    def like(self):
        self.likes += 1


class CommentSchema(ma.Schema):
    post_id = fields.Integer()
    user_id = fields.Integer()
    content = fields.String()
    commentTime = fields.DateTime()
    likes = fields.Integer()


class Favorite(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    favoriteTime = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, post_id, user_id):
        self.post_id = post_id
        self.user_id = user_id


class FavoriteSchema(ma.Schema):
    post_id = fields.Integer()
    user_id = fields.Integer()
    favoriteTime = fields.DateTime()


class Like(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    like_to = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    likeTime = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, post_id, user_id, like_to):
        self.post_id = post_id
        self.user_id = user_id
        self.like_to = like_to


class LikeSchema(ma.Schema):
    post_id = fields.Integer()
    user_id = fields.Integer()
    likeTime = fields.DateTime()


class Block(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)

    def __init__(self, post_id, user_id):
        self.post_id = post_id
        self.user_id = user_id


class BlockSchema(ma.Schema):
    post_id = fields.Integer()
    user_id = fields.Integer()
