from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from . import db

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():  
    events = db.session.scalars(db.select(Event)).all()  
    return render_template('index.html', events=events)

@mainbp.route('/search', methods =["GET", "POST"])
def search():
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