from flask import Flask, render_template, redirect, flash
from helpers import currency
from forms import RegistrationForm, LoginForm, ArticleForm, CommentForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from werkzeug.utils import secure_filename
import os
import uuid as uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'
app.config['SECRET_KEY']='this_key_is_secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
UPLOAD_FOLDER = 'static/user_images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
from models import User, Article, Comment

c = currency()
usd, eur = c['USD'], c['EUR']

@app.context_processor
def context():
	return dict(usd=usd, eur=eur)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.route("/")
@app.route("/home")
def home():
	articles = Article.query.all()
	return render_template('home.html', articles=articles)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
	form = RegistrationForm()
	if form.validate_on_submit():
		try:
			user = User(username=form.username.data, email=form.email.data)
			user.set_password(form.password.data)
			db.session.add(user)
			db.session.commit()
			flash('You are registered!')
			return redirect('/home')
		except:
			flash('Please, enter valid and unique credentials!')
			return redirect('/register')

	return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password!')
			return redirect('login')
		login_user(user)
		flash('You are logged in!')
		return redirect('home')
		
	return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('Successfully logged out!')
	return redirect('home')

@app.route('/write_article', methods=['GET', 'POST'])
@login_required
def write_article():
	form = ArticleForm()
	if form.validate_on_submit():
		image_filename = str(uuid.uuid1())+'_'+secure_filename(form.image.data.filename)
		file_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
		article = Article(title=form.title.data, text=form.text.data, author=current_user.id, image=file_path, article_type=form.article_type.data)
		form.image.data.save(file_path)
		db.session.add(article)
		db.session.commit()
		flash('Your article was submited!')
		return redirect('/home')
	return render_template('write_article.html', form=form)

@app.route('/<article_title>', methods=['GET', 'POST'])
def read_article(article_title):
	article = Article.query.filter_by(title=article_title).first()
	comments = Comment.query.filter_by(article_id=article.id)
	form = CommentForm()
	if form.validate_on_submit():
		article = Article.query.filter_by(title=article_title).first()
		comment = Comment(text=form.text.data, author=current_user.id, article_id=article.id)
		db.session.add(comment)
		db.session.commit()
		return redirect(f'/{article_title}')
	return render_template('read_article.html', article=article, user=current_user, form=form, comments=comments) 

@app.route('/home/<category>', methods=['GET', 'POST'])
def categories(category):
	articles = Article.query.filter_by(article_type=category)
	
	return render_template('categories.html', articles=articles, category=category)
