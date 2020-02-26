from flask import Flask, jsonify, render_template
from dbfunction import prcp_dict, stations_dict, temps_dict, start_temps, range_temps


app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results to a Dictionary 
    using date as the key and prcp as the value.
    Return the JSON representation of your dictionary."""
    return (jsonify(prcp_dict))

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    return (jsonify(stations_dict))

@app.route("/api/v1.0/temperature")
def temperature():
    """query for the dates and temperature observations 
    from a year from the last data point.  Return a JSON 
    list of Temperature Observations (tobs) for the 
    previous year."""
    return (jsonify(temps_dict))

@app.route("/api/v1.0/<start>")
def start(start):
    """Return a JSON list of the minimum temperature, 
    the average temperature, and the max temperature 
    for a given start range.  calculate TMIN, TAVG, 
    and TMAX for all dates greater than and equal to 
    the start date."""

    return (jsonify(start_temps(start)))

@app.route("/api/v1.0/<start>/<end>")
def range(start, end):
    """Return a JSON list of the minimum temperature, 
    the average temperature, and the max temperature 
    for a given start range.  When given the start and 
    the end date, calculate the TMIN, TAVG, and TMAX 
    for dates between the start and end date inclusive."""
    
    return (jsonify(range_temps(start, end)))
    #return (f"end Page: {start} - {end}")

if __name__ == '__main__':
    app.run(debug=True)