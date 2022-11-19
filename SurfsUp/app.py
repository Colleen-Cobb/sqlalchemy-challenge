
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# 1. Import Flask
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################


# Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
            f"Welcome to my 'Home' page! Here are the available routes:<br/>"
            f"/api/v1.0/precipitation"
            f"/api/v1.0/stations"
            f"/api/v1.0/tobs"
            f"/api/v1.0/<start>"
            f"/api/v1.0/<start>/<end>"


# Define what to do when a user hits the /api/v1.0/precipitation route
@app.route("/api/v1.0/precipitation")
def prcp():
    #Create our Session (link) from Python to the DB
    session=Session(engine)

    """Return a list of precipitation data inlcuding date and prcp value for the last 12 months"""

    # Query the prcp for the last 12 months
    recent_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    recent_day= (dt.datetime.strptime(recent_date, "%Y-%m-%d")).date()
    year_ago= recent_day - dt.timedelta(days=365)



    results= session.query(Measurement.date, Measurement.prcp).\
                filter((Measurement.date >= year_ago).all()
    
    session.close()

    # Create a dictionary from the row data
    prcp_values= []
    for date, prcp in results:
     


    print("Server received request for precipitation results...")
    return "Here are the precipitation results from the last 12 months!"
    return jsonify(prcp_values)

# Define what to do when a user hits the /api/v1.0/stations route
@app.route("/api/v1.0/stations")
def station():
    print("Server received request for station results...")
    return "Here are the stations located in Honolulu, Hawaii"

# Define what to do when a user hits the /api/v1.0/tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for temperature observations for the most active station...")




if __name__ == "__main__":
    app.run(debug=True)