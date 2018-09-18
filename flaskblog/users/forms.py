from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flask_login import current_user



class RegistrationForm(FlaskForm):
    
    # Username Field
    username = StringField(
        'Username', 
        validators=[
            DataRequired(),
            Length(min=2, max=20)
        ]
    )
    
    # Email Field
    email = StringField(
        'Email', 
        validators=[
            DataRequired(),
            Email()
        ]
    )
    
    # Password Field
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired()
        ]
    )
    
    # Confirm Password Field
    confirm_password = PasswordField(
        'Confirm Password', 
        validators=[
            DataRequired(),
            EqualTo('password')
        ]
    )
    
    # Submit Field
    submit = SubmitField(
        'Sign Up'
    )

    # Username Unique Validation
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('This username has used already. Please choose another.')

    # Email Unique Validation
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('This email has used already. Please choose another.')



class LoginForm(FlaskForm):
    
    # Email Field
    email = StringField(
        'Email', 
        validators=[
            DataRequired(),
            Email()
        ]
    )
    
    # Password Field
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired()
        ]
    )
    
    # Confirm Password Field
    remember = BooleanField(
        'Remember Me'
    )
    
    # Submit Field
    submit = SubmitField(
        'Sign In'
    )



class UpdateUserForm(FlaskForm):
    
    # Username Field
    username = StringField(
        'Username', 
        validators=[
            DataRequired(),
            Length(min=2, max=20)
        ]
    )
    
    # Email Field
    email = StringField(
        'Email', 
        validators=[
            DataRequired(),
            Email()
        ]
    )
    
    # Email Field
    picture = FileField(
        'Change Profile Image', 
        validators=[
            FileAllowed(['jpg','png'])
        ]
    )
    
    # Submit Field
    submit = SubmitField(
        'Update'
    )

    # Username Unique Validation
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()

            if user:
                raise ValidationError('This username has used already. Please choose another.')

    # Email Unique Validation
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()

            if user:
                raise ValidationError('This email has used already. Please choose another.')



class RequestResetForm(FlaskForm):
    
    # Email Field
    email = StringField(
        'Email', 
        validators=[
            DataRequired(),
            Email()
        ]
    )
    
    # Submit Field
    submit = SubmitField(
        'Request Reset Password'
    )

    # Email Unique Validation
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')



class ResetPasswordForm(FlaskForm):
    
    # Password Field
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired()
        ]
    )
    
    # Confirm Password Field
    confirm_password = PasswordField(
        'Confirm Password', 
        validators=[
            DataRequired(),
            EqualTo('password')
        ]
    )
    
    # Submit Field
    submit = SubmitField(
        'Reset Password'
    )