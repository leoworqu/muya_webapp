from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from muya.models import User


class registrationForm(FlaskForm):
    # Form for user registration
    username = StringField('Username', validators=[DataRequired(),
                                                  Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),
                                                                     EqualTo('password')])
    submit = SubmitField('Sign up')


class loginForm(FlaskForm):
    # Form for user login
    email = StringField('Email', validators=[DataRequired(),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')

class accountUpdateForm(FlaskForm):
    # Form for updating user account information
    username = StringField('Username', validators=[DataRequired(),
                                                  Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(),
                                             Email()])
    profile_picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

    submit = SubmitField('Update')


class postForm(FlaskForm):
    # Form for creating a new post/job
    title = StringField('Title of Job', validators=[DataRequired()])
    description = TextAreaField('Detailed description of Job' , validators=[DataRequired()])
    service_picture = FileField('Upload Job Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Create Job')


class reviewForm(FlaskForm):
    # Form for submitting a review/comment on a service
    comment = TextAreaField('Add a Comment' , validators=[DataRequired()])
    like_or_dislike = BooleanField('DisLike This Service')
    submit = SubmitField('submit')