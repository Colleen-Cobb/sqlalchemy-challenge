
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
    return (
        f"Welcome to the climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )   

# Define what to do when a user hits the /api/v1.0/precipitation route

@app.route("/api/v1.0/precipitation")
def prcp():
    #Create our Session (link) from Python to the DB
    session=Session(engine)

    """Return a list of precipitation data inlcuding date and prcp value for the last 12 months"""

    prcp_data = session.query(Measurement.date, Measurement.prcp).\
                    filter(Measurement.date >= '2016-08-23').\
                    filter(Measurement.date <= '2017-08-23').\
                    order_by(Measurement.date).all()

    
    session.close()

    prcp_values= list(np.ravel(prcp_data))

    return jsonify(prcp_values)

# Define what to do when a user hits the /api/v1.0/stations route
@app.route("/api/v1.0/stations")
def station():
   #Create our Session (link) from Python to the DB
    session=Session(engine)

    """Return a list of stations from the dataset"""

    stations= session.query(Station.name).all()

    session.close()

    station_list=list(np.ravel(stations))

    return jsonify(station_list)

# # Define what to do when a user hits the /api/v1.0/tobs route
@app.route("/api/v1.0/tobs")
def tobs():
       #Create our Session (link) from Python to the DB
    session=Session(engine)

    """Return a list of temperature observations for the most active station"""

    sel=[Station.station, func.count(Measurement.station)]

    active_station=session.query(*sel).\
        filter(Station.station==Measurement.station).\
        group_by(Station.station).\
        order_by(func.count(Measurement.station).desc()).all()

    most_active=session.query(*sel).\
        filter(Station.station==Measurement.station).\
        group_by(Station.station).\
        order_by(func.count(Measurement.station).desc()).first()

    most_active_station=most_active[0]


    sel_temp = [(Measurement.date),
        (Measurement.tobs)]

    tobs= session.query(*sel_temp).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.date <= '2017-08-23').all()





    session.close()

    tobs_list=list(np.ravel(tobs))

    return jsonify(tobs_list)



if __name__ == "__main__" : 
    app.run(debug=True)