from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class NewRecipe(FlaskForm):
    title = StringField('Recipe Title', validators = [DataRequired()])
    description = TextAreaField('Description', validators = [DataRequired()])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    tags         = SelectMultipleField(
                      'Tags',
                      coerce=int,
                      validators=[Optional()]
                   )
    submit = SubmitField('Save')

class SearchForm(FlaskForm):
    query = StringField("Search", validators=[DataRequired()])
    submit = SubmitField("Go")

class RatingForm(FlaskForm):
    score = SelectField("Rate this recipe", choices=[(str(i), i) for i in range(1,6)], coerce=int)
    submit = SubmitField("Submit Rating")

class CommentForm(FlaskForm):
    body = TextAreaField("Your comment", validators=[DataRequired(), Length(max=500)])
    submit = SubmitField("Post Comment")

class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')

class EditProfileForm(FlaskForm):
    username        = StringField('Display Name', validators=[DataRequired(), Length(1,20)])
    email           = StringField('Email',        validators=[DataRequired(), Email()])
    password        = PasswordField('New Password', validators=[Optional(), Length(min=6)])
    confirm_password= PasswordField('Confirm New Password',
                                    validators=[EqualTo('password', message='Passwords must match')])
    submit          = SubmitField('Update Profile')
