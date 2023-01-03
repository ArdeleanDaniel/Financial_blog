from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
	username = StringField('Username', render_kw={'placeholder':'Username'}, validators=[DataRequired()])
	email = StringField('Email', render_kw={'placeholder':'Email'}, validators=[DataRequired(), Email()])
	password = PasswordField('Password', render_kw={'placeholder':'Password'}, validators=[DataRequired()])
	password2 = PasswordField('Confirm Password', render_kw={'placeholder':'Repeat Password'}, validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

class LoginForm(FlaskForm):
	username = StringField('Username', render_kw={'placeholder':'Username'}, validators=[DataRequired()])
	password = PasswordField('Password', render_kw={'placeholder':'Password'}, validators=[DataRequired()])
	submit = SubmitField('Log In')

class ArticleForm(FlaskForm):
	title = StringField('Title', render_kw={'placeholder':'Title'}, validators=[DataRequired()])
	text = TextAreaField('Text', render_kw={'placeholder':'Article text'},  validators=[DataRequired()])
	image = FileField('Article Image', validators=[DataRequired()])
	artycle_type = SelectField('Choose article type:', choices=[('Economy'), ('Finance'), ('Politics') , ('Other')], validators=[DataRequired()])
	submit = SubmitField('Submit Article')

class CommentForm(FlaskForm):
	text = TextAreaField('Comment', validators=[DataRequired(), Length(max=350, message='Your comment has more than 100 caracters!')]) 
	submit = SubmitField('Submit Comment')