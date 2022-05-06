from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, IntegerField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from orionnen.models import User
from datetime import date

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is taken. Please choose another username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('User with this email already exists. Please choose another email.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no user with provided email.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class EditOrderForm(FlaskForm):
    buyer = StringField("Buyer's name")
    sku = StringField('SKU')
    prod_costs = FloatField('Production costs', validators=[Optional()])
    ship_costs = FloatField('Shipping costs', validators=[Optional()])
    undef_costs = FloatField('Undefined costs', validators=[Optional()])
    note = StringField('Note')
    submit = SubmitField('Submit')

class NewOrderForm(FlaskForm):
    order_id = IntegerField("Order ID", validators=[DataRequired()])
    date = DateField("Date", default=date.today())
    buyer = StringField("Buyer's name")
    sku = StringField('SKU')
    revenue = FloatField('Revenue', validators=[Optional()])
    note = StringField('Note')
    submit = SubmitField('Submit')

class InputCostsForm(FlaskForm):
    order_id = IntegerField("Order ID", validators=[Optional()])
    date = DateField("Date", default=date.today())
    value = FloatField("Value", validators=[DataRequired()])
    costs_name = StringField("Costs name")
    note = StringField('Note')
    type = SelectField('Type', choices=['Production costs', 'Shipping costs', 'Other costs'], validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditCostsForm(FlaskForm):
    date = DateField("Date", default=date.today())
    value = FloatField("Value", validators=[DataRequired()])
    costs_name = StringField("Costs name")
    note = StringField('Note')
    type = SelectField('Type', choices=['Production costs', 'Shipping costs', 'Other costs'], validators=[DataRequired()])
    submit = SubmitField('Submit')
