from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your username"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your password"},
    )
    remember_me = BooleanField("Remember me", default=False)
    
    submit = SubmitField("Login")
    
    