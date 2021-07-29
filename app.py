# import dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd
import datetime as dt

from flask import Flask, jsonify

# database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# flask setup
app = Flask(__name__)

# flask route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    most_recent_date = dt.date(2017, 8 ,23)
    last_12_months = most_recent_date - dt.timedelta(days=365)
    session = Session(engine)
    date_prcp = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date.between(last_12_months, most_recent_date)).all()
    session.close()
    date_precipitation = {date: prcp for date, prcp in date_prcp}
    return jsonify(date_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    all_stations = session.query(Station.station).all()
    session.close()
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    most_recent_date = dt.date(2017, 8 ,23)
    last_12_months = most_recent_date - dt.timedelta(days=365)
    session = Session(engine)
    date_tobs = session.query(Measurement.tobs).\
    filter(Measurement.station == "USC00519281").\
    filter(Measurement.date.between(last_12_months, most_recent_date)).all()
    session.close()
    return jsonify(date_tobs)

@app.route("/api/v1.0/<start>")
def start(start = None):
    most_recent_date = dt.date(2017, 8 ,23)
    session = Session(engine)
    tobs_start_only = session.query(Measurement.tobs).filter(Measurement.date.between(start, most_recent_date)).all()
    session.close()
    tobs_start_only_df = pd.DataFrame(tobs_start_only)
    tmin = tobs_start_only_df["tobs"].min()
    tmax = tobs_start_only_df["tobs"].max()
    tavg = tobs_start_only_df["tobs"].mean()
    return jsonify(tmin, tmax, tavg)

@app.route("/api/v1.0/<start>/<end>")
def startend(start = None, end = None):
    session = Session(engine)
    tobs_start_only = session.query(Measurement.tobs).filter(Measurement.date.between(start, end)).all()
    session.close()
    tobs_start_only_df = pd.DataFrame(tobs_start_only)
    tmin = tobs_start_only_df["tobs"].min()
    tmax = tobs_start_only_df["tobs"].max()
    tavg = tobs_start_only_df["tobs"].mean()
    return jsonify(tmin, tmax, tavg)

if __name__ == "__main__":
    app.run(debug=True)