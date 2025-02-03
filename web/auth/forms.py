from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from web.models import User

level_choice = [('','Course Level'), ('novice','Novice'), ('beginner','Beginner'), ('expert','Expert'),  ('pro','Pro'), ('advanced','Advanced') ]
gender_choice = [('', 'sex'), ('f', 'Female'), ('m', 'Male'), ('O', 'Other')]
lang_choice = [('', 'language'), ('english', 'english'), ('french', 'french'), ('spanish', 'spanish'), ('latin', 'latin'), ('pidgin', 'pidgin'), ('other', 'other')]
city_choice = [('', 'current city'), ('Lagos','Lagos'), ('Portharcourt','Portharcourt'), ('New York','New York'), ('Canada','Canada'), ('Calabar','Calabar'), ('Uyo','Uyo')]

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=50)])
    tnc = BooleanField('Terms & Conditions', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class SigninForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    def validate_me(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Invalid Login Details. Try')


class UpdateMeForm(FlaskForm):
    #poster = FileField('Add Course Poster Image', validators=[ DataRequired(), FileAllowed(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp4'])])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'svg', 'webp', 'gif', 'jpeg', 'png'])])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone',  validators=[ DataRequired(), Length(min=2, max=20)])
    lang = SelectField('Language', choices=lang_choice)
    city = SelectField('City', choices=city_choice)
    about = TextAreaField('Profile Summary', validators=[DataRequired(), Length(min=10, max=300)])
    #socials = StringField('Socials',  validators=[Length(min=2, max=20)])
    gender = SelectField('Gender', validators=[DataRequired()], choices=gender_choice)
    time = IntegerField('Time Duration(Hrs)')
    submit = SubmitField('Update Now')

    def validate_username(self, username):
        #if ( (current_user.is_admin()) | (current_user.username == usr.username) ):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(f'That username `{username.data}` is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
            
    def validate_phone(self, phone):
        if phone.data != current_user.phone:
            user = User.query.filter_by(phone=phone.data).first()
            if user:
                raise ValidationError('That phone number belongs to a different account. Please choose a different one.')


class ForgotForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(f'Email({email.data}) Not Recognized')


class ResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')