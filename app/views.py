from flask import render_template
from app import app, models

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/route/<route>')
def route(route):
    all = models.TotalRouteTime.query.filter(models.TotalRouteTime.route==route).order_by(models.TotalRouteTime.timestamp)
    return render_template('route.html', data=all)
