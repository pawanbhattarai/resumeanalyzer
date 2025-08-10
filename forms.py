
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(), 
        Length(min=2, max=50, message='First name must be between 2 and 50 characters')
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(), 
        Length(min=2, max=50, message='Last name must be between 2 and 50 characters')
    ])
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=4, max=20, message='Username must be between 4 and 20 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(), 
        Email(message='Please enter a valid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password', message='Passwords must match')
    ])
    terms = BooleanField('I agree to the Terms of Service and Privacy Policy', validators=[DataRequired()])
    submit = SubmitField('Create Account')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email or login instead.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), 
        Email(message='Please enter a valid email address')
    ])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class AnalysisForm(FlaskForm):
    job_title = StringField('Job Title', validators=[
        Length(max=200, message='Job title must be less than 200 characters')
    ])
    company_name = StringField('Company Name', validators=[
        Length(max=200, message='Company name must be less than 200 characters')
    ])
    resume_text = TextAreaField('Resume Content', validators=[
        DataRequired(message='Please paste your resume content'),
        Length(min=50, message='Resume must be at least 50 characters long')
    ])
    job_description = TextAreaField('Job Description', validators=[
        DataRequired(message='Please paste the job description'),
        Length(min=50, message='Job description must be at least 50 characters long')
    ])
    save_analysis = BooleanField('Save this analysis to my history')
    submit = SubmitField('Analyze Compatibility')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), 
        Email(message='Please enter a valid email address')
    ])
    submit = SubmitField('Send Reset Link')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(), 
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Reset Password')

class AnalysisForm(FlaskForm):
    job_title = StringField('Job Title (Optional)', validators=[Length(max=200)])
    company_name = StringField('Company Name (Optional)', validators=[Length(max=200)])
    resume_text = TextAreaField('Resume Text', validators=[
        DataRequired(message='Please enter your resume text'),
        Length(min=50, message='Resume text must be at least 50 characters')
    ])
    job_description = TextAreaField('Job Description', validators=[
        DataRequired(message='Please enter the job description'),
        Length(min=50, message='Job description must be at least 50 characters')
    ])
    save_analysis = BooleanField('Save this analysis to my history')
    submit = SubmitField('Analyze Compatibility')

class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(), 
        Length(min=2, max=50, message='First name must be between 2 and 50 characters')
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(), 
        Length(min=2, max=50, message='Last name must be between 2 and 50 characters')
    ])
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=4, max=20, message='Username must be between 4 and 20 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(), 
        Email(message='Please enter a valid email address')
    ])
    submit = SubmitField('Update Profile')
    
    def __init__(self, original_username=None, original_email=None, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
    
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already registered. Please use a different email.')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(), 
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(), 
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Change Password')

class SavedResumeForm(FlaskForm):
    title = StringField('Resume Title', validators=[
        DataRequired(message='Please enter a title for your resume'),
        Length(min=3, max=200, message='Title must be between 3 and 200 characters')
    ])
    content = TextAreaField('Resume Content', validators=[
        DataRequired(message='Please enter your resume content'),
        Length(min=50, message='Resume content must be at least 50 characters')
    ])
    is_default = BooleanField('Set as default resume')
    submit = SubmitField('Save Resume')
