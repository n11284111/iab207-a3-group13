from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment, Booking
from .forms import EventForm, CommentForm, BookingForm
from . import db
import os
from werkzeug.utils import secure_filename
#additional import:
from flask_login import login_required, current_user

eventbp = Blueprint('event', __name__, url_prefix='/events')

@eventbp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    # create the comment form
    form = CommentForm()    
    return render_template('events/show.html', event=event, form=form)

@eventbp.route('/create', methods=['GET', 'POST'])
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
    flash('Successfully created new music event', 'success')
    #Always end with redirect when form is valid
    return redirect(url_for('event.show', id=event.id))
  return render_template('events/create.html', form=form)

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

@eventbp.route('/<event>/comment', methods=['GET', 'POST'])  
@login_required
def comment(event):  
    form = CommentForm()  
    #get the event object associated to the page and the comment
    event = db.session.scalar(db.select(Event).where(Event.id==event))
    if form.validate_on_submit():  
      #read the comment from the form
      comment = Comment(text=form.text.data, event=event,
                        user=current_user) 
      #here the back-referencing works - comment.event is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 

      #flashing a message which needs to be handled by the html
      flash('Your comment has been added', 'success')  
      # print('Your comment has been added', 'success') 
    # using redirect sends a GET request to event.show
    return redirect(url_for('event.show', id=event.id))

@eventbp.route('/myevents', methods=['GET', 'POST']) 
@login_required
def myEvents():
    print(request)
    events = db.session.query(Event).filter(Event.user_id == current_user.id)
    return render_template('events/owned.html', events=events)

@eventbp.route('/<event>/book', methods=['GET', 'POST'])  
@login_required
def book(event):  
    print(request)
    if request.method == "POST":
        searchval = request.form.get("search")
        if searchval and searchval != "":
            print(searchval)
            query = "%" + searchval + "%"
            events = db.session.query(Event).filter(Event.name.contains(query))
            return render_template('index.html', events=events)
        else:
            return redirect(url_for('main.index'))

    