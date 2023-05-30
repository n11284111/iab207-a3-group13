from flask import Blueprint, render_template, request, redirect, url_for
from .models import Destination
from . import db

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    destinations = db.session.scalars(db.select(Destination)).all()    
    return render_template('index.html', destinations=destinations)

@mainbp.route('/search', methods =["GET", "POST"])
def search():
    print(request)
    if request.method == "POST":
        searchval = request.form.get("search")
        if searchval and searchval != "":
            print(searchval)
            query = "%" + searchval + "%"
            destinations = db.session.query(Destination).filter(Destination.description.contains(query))
            return render_template('index.html', destinations=destinations)
        else:
            return redirect(url_for('main.index'))