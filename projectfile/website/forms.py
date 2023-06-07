from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateField, TimeField, IntegerField, FloatField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'png', 'jpg'}

#Create new event
class EventForm(FlaskForm):

  name = StringField('Event Name', validators=[InputRequired()])
  artist = StringField('Artist', validators=[InputRequired()])
  description = TextAreaField('Description', 
          validators=[InputRequired()])
  genre = StringField('Genre', validators=[InputRequired()])
  location = StringField('Location', validators=[InputRequired()])

  date = DateField('Date', validators=[InputRequired()])
  start_time = TimeField('Start Time', validators=[InputRequired()])
  end_time = TimeField('End Time', validators=[InputRequired()])
  tickets = IntegerField('Number of Tickets Available', validators=[InputRequired()])
  ticket_price = FloatField('Ticket Price', validators=[InputRequired()])
  image = FileField('Destination Image', validators=[
    FileRequired(message='Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])
  status = StringField('Event Status', validators=[InputRequired()])

  submit = SubmitField("Create")
    
#User login
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

#User register
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    
    #linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    #submit button
    submit = SubmitField("Register")

#User comment
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')
