# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        "Welcome!<br/><br/>"
        "Available Routes:<br/>"
        "<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        "<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        "<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        "<a href='/api/v1.0/<start>'>/api/v1.0/&lt;start&gt;</a><br/>"
        "<a href='/api/v1.0/<start>/<end>'>/api/v1.0/&lt;start&gt;/&lt;end&gt;</a><br/><br/>"
        "Note: Replace &lt;start&gt; with a valid start date (YYYY-MM-DD)<br/>"
        "Example: /api/v1.0/2015-01-01<br/><br/>"
        "Replace &lt;start&gt; and &lt;end&gt; with valid start and end dates (YYYY-MM-DD)<br/>"
        "Example: /api/v1.0/2015-01-01/2016-01-15")

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    end_date = dt.datetime.strptime(last_date, '%Y-%m-%d')
    start_date = end_date - dt.timedelta(days=365)

    results_precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= start_date).\
            order_by(Measurement.date).all()
    
    session.close()

    precipitation_data = {date: prcp for date, prcp in results_precipitation}

    return jsonify(precipitation_data)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()

    session.close()

    station_data = {station: count for station, count in active_stations}

    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    end_date = dt.datetime.strptime(last_date, '%Y-%m-%d')
    start_date = end_date - dt.timedelta(days=365)

    most_active_station = 'USC00519281'
    results_tobs = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= start_date).all()

    session.close()

    tobs_data = [{'date': result[0], 'temperature': result[1]} for result in results_tobs]

    return jsonify(tobs_data)


@app.route("/api/v1.0/<start>")
def temperature_stats_start(start):
    session = Session(engine)

    start_results = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    temperature_stats = {
        'start_date': start,
        'TMIN': start_results[0][0],
        'TAVG': start_results[0][1],
        'TMAX': start_results[0][2]
    }

    return jsonify(temperature_stats)


@app.route("/api/v1.0/<start>/<end>")
def temperature_stats_range(start, end):
    session = Session(engine)

    results = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    temperature_stats_two = {
        'start_date': start,
        'end_date': end,
        'TMIN': results[0][0],
        'TAVG': results[0][1],
        'TMAX': results[0][2]
    }

    return jsonify(temperature_stats_two)



if __name__ == "__main__":
    app.run(debug=True)