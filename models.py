from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100), index=True, unique=True)
	email = db.Column(db.String(128), index=True, unique=True)
	password_h = db.Column(db.String(128))
	articles = db.relationship('Article', backref='user', lazy='dynamic')
	comments = db.relationship('Comment', backref='user', lazy='dynamic')

	def set_password(self, password):
		self.password_h = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_h, password)


class Article(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(128), index=True, unique=True)
	text = db.Column(db.Text)
	date = db.Column(db.DateTime, default=datetime.utcnow)
	image = db.Column(db.String())
	article_type = db.Column(db.String(), index=True)
	author = db.Column(db.Integer, db.ForeignKey('user.id'))
	comments = db.relationship('Comment', backref='article')

class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(250))
	date = db.Column(db.DateTime, default=datetime.utcnow)
	author = db.Column(db.Integer, db.ForeignKey('user.id'))
	article_id = db.Column(db.Integer, db.ForeignKey('article.id'))