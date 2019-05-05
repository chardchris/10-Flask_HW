import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/temp/start <br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results_p = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > '2016-08-22').all()
    
    precip = dict(results_p)

    return jsonify(precip)    

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations."""
    results = session.query(Station.station).all()

    stations = list(np.ravel(results))
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    temp_results = session.query(Measurement.date, Measurement.tobs).\
       filter(Measurement.station == 'USC00519281').\
       filter(Measurement.date > '2016-08-22').all()
    
    #returning a list of temperatures here seems stupid, so I used a dictionary to include the date
    temps = dict(temp_results)
    
    return jsonify(temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def calc(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""

    sel = [func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]

    if not end:
        results_3 = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps_1 = list(np.ravel(results_3))
        return jsonify(temps_1)

    results_4 = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps_2 = list(np.ravel(results_4))
    
    return jsonify(temps_2)


if __name__ == '__main__':
    app.run(debug=True)




