from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, ValidationError
from models import User

class SignupForm(FlaskForm):
    """User registration form"""
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Invalid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='Password must be at least 6 characters')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.')


class LoginForm(FlaskForm):
    """User login form"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class RoadmapForm(FlaskForm):
    """Form for creating/editing roadmaps manually"""
    title = StringField('Roadmap Title', validators=[DataRequired(), Length(min=5, max=200)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=20)])
    category = SelectField('Category', choices=[('skill', 'Skill'), ('course', 'Course'), ('job', 'Job Role')], validators=[DataRequired()])
    difficulty = SelectField('Difficulty', choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], validators=[DataRequired()])


class StepForm(FlaskForm):
    """Form for adding steps manually"""
    title = StringField('Step Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    level = SelectField('Level', choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], default='Beginner') # New Field
    resources = TextAreaField('Resources')


class RequestResetForm(FlaskForm):
    """Form to request password reset"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    """Form to reset password"""
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])


class FeedbackForm(FlaskForm):
    """Form for user feedback"""
    category = SelectField('Category', choices=[
        ('General', 'General Inquiry'),
        ('Feature', 'Feature Request'),
        ('Bug', 'Report a Bug'),
        ('Content', 'Content Suggestion')
    ], validators=[DataRequired()])
    
    rating = SelectField('Rate your Experience', choices=[
        ('5', '⭐⭐⭐⭐⭐ (Excellent)'),
        ('4', '⭐⭐⭐⭐ (Good)'),
        ('3', '⭐⭐⭐ (Average)'),
        ('2', '⭐⭐ (Poor)'),
        ('1', '⭐ (Bad)')
    ], validators=[DataRequired()])
    
    message = TextAreaField('Message', validators=[
        DataRequired(),
        Length(min=10, max=1000, message="Please provide at least 10 characters.")
    ])
