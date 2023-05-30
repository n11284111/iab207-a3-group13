from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment
from .forms import EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
#additional import:
from flask_login import login_required, current_user

destbp = Blueprint('event', __name__, url_prefix='/events')

@destbp.route('/<id>')
def show(id):
    destination = db.session.scalar(db.select(Event).where(Event.id==id))
    # create the comment form
    form = CommentForm()    
    return render_template('events/show.html', destination=destination, form=form)

@destbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = EventForm()
  if form.validate_on_submit():
    #call the function that checks and returns image
    db_file_path = check_upload_file(form)
    event = Event(
      name=form.name.data,
      artist=form.artist.data,
      description=form.description.data,       
      genre = form.genre.data,
      location = form.location.data,
      date = form.date.data,
      start_time = form.start_time.data,
      end_time = form.end_time.data,
      tickets = form.tickets.data,
      ticket_price = form.ticket_price.data,   
      image=db_file_path,
      status = form.status.data
      )
    # add the object to the db session
    db.session.add(event)
    # commit to the database
    db.session.commit()
    flash('Successfully created new travel destination', 'success')
    #Always end with redirect when form is valid
    return redirect(url_for('event.create'))
  return render_template('events/create.html', form=form)

# id = db.Column(db.Integer, primary_key=True)
# name = db.Column(db.String(80))
# artist = db.Column(db.String(30))
# description = db.Column(db.String(200))
# genre = db.Column(db.String(20))
# location = db.Column(db.String(100))
# date = db.Column(db.DateTime)
# start_time = db.Column(db.DateTime)
# end_time = db.Column(db.DateTime)
# tickets_available = db.Column(db.Integer)
# ticket_price = db.Column(db.Float)    
# image = db.Column(db.String(400))
# status = db.Column(db.String(20))

def check_upload_file(form):
  #get file data from form  
  fp = form.image.data
  filename = fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH, 'static/image', secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/image/' + secure_filename(filename)
  #save the file and return the db upload path
  fp.save(upload_path)
  return db_upload_path

@destbp.route('/<destination>/comment', methods=['GET', 'POST'])  
@login_required
def comment(destination):  
    form = CommentForm()  
    #get the destination object associated to the page and the comment
    destination = db.session.scalar(db.select(Event).where(Event.id==destination))
    if form.validate_on_submit():  
      #read the comment from the form
      comment = Comment(text=form.text.data, destination=destination,
                        user=current_user) 
      #here the back-referencing works - comment.destination is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 

      #flashing a message which needs to be handled by the html
      flash('Your comment has been added', 'success')  
      # print('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('event.show', id=destination.id))
    