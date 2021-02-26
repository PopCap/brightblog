from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User
from flask_login import current_user

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # the following functions are custom validators for the WTForms
    # making sure there are no duplicates
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class PostForm(FlaskForm):
    title = StringField('Post Title', validators=[DataRequired(), Length(min=1, max=150)])
    post = TextAreaField('Post Content', validators=[DataRequired(), Length(min=1, max=3500)])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment = TextAreaField('', render_kw={'placeholder': 'Your thoughts?'}, validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField('Submit Comment')

    def validate_logged_in():
        # prevent users who are not logged in from commenting
        if current_user.is_anonymous:
            raise ValidationError('Please Login in to post a comment.')
