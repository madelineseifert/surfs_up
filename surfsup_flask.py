# Dependencies
from flask import Flask, jsonify
from datetime import datetime
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurements = Base.classes.measurement
Stations = Base.classes.station

session = Session(engine)



#flask setup

app = Flask(__name__)



#homepage
@app.route("/")
def home():
    return ("Hawaii Weather Data Home page!<br/>"
    "/api/v1.0/precipitation<br/>"
    "/api/v1.0/stations<br/>"
    "/api/v1.0/tobs<br/>"
    "Enter start date in format YYYY-MM-DD<br/>"
    "/api/v1.0/<start><br/>"
    "Enter start and end dates in format YYYY-MM-DD<br/>"
    "/api/v1.0/<start>/<end>")

#precipitation route
 
@app.route("/api/v1.0/precipitation")
def precipitation():   
     
    recent = session.query(Measurements.date).order_by(Measurements.date.desc()).first()
    last = most_recent[0]
    year_before = last.replace(year = (last.year - 1))
    year_before = year_before.strftime("%Y-%m-%d")

    precip_list = []
    precip = session.query(Stations.name, Measurements.date, Measurements.prcp).filter(Measurements.station==Stations.station).filter(Measurements.date>=year_before).order_by(Measurements.date).all()
    for p in precip:
        # print({"date":p[0],"tobs":p[1]})
        precip_list.append({"station":p[0],"date":p[1],"prcp":p[2]})

    return jsonify(precip_list)

#station route
@app.route("/api/v1.0/stations")
def stations():    
    stations = session.query(Stations.station, Stations.name, Measurements.station, func.count(Measurements.tobs)).filter(Stations.station == Measurements.station).group_by(Measurements.station).order_by(func.count(Measurements.tobs).desc()).all()
    station_List = []
    for s in stations:
        station_List.append({"station":s[0],"name":s[1]})

    return jsonify(station_List)

#tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    recent = session.query(Measurements.date).order_by(Measurements.date.desc()).first()
    last = recent[0]
    year_before = last.replace(year = (last_date.year - 1))
    year_before = year_before.strftime("%Y-%m-%d")

    tobs = session.query(Stations.name,Measurements.date, Measurements.tobs).filter(Measurements.station==Stations.station).filter(Measurements.date>=year_before).order_by(Measurements.date).all()
    tobs_List = []
    for t in tobs:
       tobs_List.append({"station":t[0],"date":t[1],"temperature observation":t[2]})
    
    return jsonify(tobs_List)

#return list of temperature data
@app.route("/api/v1.0/<start>")
def startdate(start):

    start_date = datetime.strptime(start, '%Y-%m-%d')
   
    maximum = session.query(func.max(Measurements.tobs)).filter(Measurements.date >= start_date).scalar()
    minimum = session.query(func.min(Measurements.tobs)).filter(Measurements.date >= start_date).scalar()
    average = session.query(func.round(func.avg(Measurements.tobs))).filter(Measurements.date >= start_date).scalar()
  
    
    
    result = [{"Minimum temperature":minimum},{"Maximum temperature":maximum},{"Average temperature":average}]
    
    return jsonify(result)


@app.route("/api/v1.0/<start>/<end>")
def startenddate(start,end):

     start_date = datetime.strptime(start, '%Y-%m-%d')
     end_date = datetime.strptime(end, '%Y-%m-%d')

     maximum = session.query(func.max(Measurements.tobs)).filter(Measurements.date.between(start_date, end_date)).scalar()
     minimum = session.query(func.min(Measurements.tobs)).filter(Measurements.date.between(start_date, end_date)).scalar()
     average = session.query(func.round(func.avg(Measurements.tobs))).filter(Measurements.date.between(start_date, end_date)).scalar()
     
     
        
     result = [{"Minimum temperature":minimum},{"Maximum temperature":maximum},{"Average temperature":average}]
    
     return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)