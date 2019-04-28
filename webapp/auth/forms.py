from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, PasswordField, validators
from webapp.auth.models import User

class LoginForm(FlaskForm):
    username = StringField("Username", [validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])
    remember_me = BooleanField('Remember Me')

class RegisterForm(FlaskForm):
    username = StringField("Username", [validators.DataRequired()])
    email = StringField("E-Mail", [validators.Email()])
    password = PasswordField("Password", [validators.DataRequired()])
    password_confirm = PasswordField("Repeat Password", [validators.EqualTo("password", message="Password does not match.")])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter(User.username.ilike(username.data)).first()
        if user is not None:
            raise validators.ValidationError("Username is already in use.")

    def validate_email(self, email):
        email = User.query.filter(User.email.ilike(email.data)).first()
        if email is not None:
            raise validators.ValidationError("Email is already in use.")