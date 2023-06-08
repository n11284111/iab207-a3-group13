from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from datetime import datetime
from . import db

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():  
    events = db.session.scalars(db.select(Event)).all()
    for event in events:
        if datetime.combine(event.date, event.start_time) < datetime.now():
            event.status = "Invalid"
            db.session.commit()

    return render_template('index.html', events=events, all_events=events)

@mainbp.route('/search', methods =["GET", "POST"])
def search():
    all_events = db.session.scalars(db.select(Event)).all()
    print(request)
    if request.method == "POST":
        searchval = request.form.get("search")
        if searchval and searchval != "":

            print(searchval)
            query = "%" + searchval + "%"
            events = db.session.query(Event).filter(Event.name.contains(query))
            return render_template('index.html', events=events, all_events=all_events)
        else:
            return redirect(url_for('main.index'))
        
@mainbp.route('/sort', methods =["GET", "POST"])
def sort():
    all_events = db.session.scalars(db.select(Event)).all()
    if request.method == "POST":
        genre = request.form.get("genre")
        if genre == "All":
            return redirect(url_for('main.index'))
        else:
            events = db.session.query(Event).filter(Event.genre == genre)
            return render_template('index.html', events=events, all_events=all_events)