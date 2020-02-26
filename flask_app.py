
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
engines = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engines, reflect=True)

# Save refs to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Creating our sessions (link) from Python to the DB
sessions = Session(engines)

# Calculating the date 1 year ago from the last data point in the database
lastdate = dt.datetime.strptime(sessions.query(func.max(Measurement.date)).all()[0][0], '%Y-%m-%d').date()
yearstart_date = lastdate - dt.timedelta(days=365)
firstdate = dt.datetime.strptime(sessions.query(func.min(Measurement.date)).all()[0][0], '%Y-%m-%d').date()

def precipitation():
    prcp_results = sessions.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= yearstart_date).filter(Measurement.date <= lastdate).order_by(Measurement.date.asc()).limit(5).all()

    # Save query results as Pandas DataFrame and set index to the date column
    prcp_df = pd.DataFrame(sessions.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= yearstart_date).filter(Measurement.date <= lastdate).all())

    prcp_df.sort_values('date', inplace=True)
    prcp_df.rename(columns={'date': 'Date', 'prcp' : 'Precipitation'}, inplace=True)


    # there is no way to convert the entire result to a dictionary because each day has multiple values
    # so I am assuming the homework wants max since that best looks like the plot
    return(prcp_df.groupby('Date')['Precipitation'].max().to_dict())

def stations():
    return({'stations' : [station[0] for station in sessions.query(Measurement.station).group_by(Measurement.station).all()]})

def get_temps(start_date, end_date):
    """Returns a dictionaary min, avg, and max temps for each date in range"""
    temps_raw = sessions.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).group_by(Measurement.date).all()
    
    temps = {}
    
    for temp in temps_raw:
        temps[temp[0]] = {'min' : temp[1], 'avg' : temp[2], 'max' : temp[3]}
        
    return(temps)

def start_temps(start_date):

    req_start = dt.datetime.strptime(start_date,'%Y-%m-%d').date()

    while req_start < first_date:
        req_start = req_start + dt.timedelta(days=1)
        
    while req_start > lastdate:
        req_start = req_start - dt.timedelta(days=1)
    
    start_dict = {}

    while req_start <= lastdate:
        start_dict[req_start.strftime('%Y-%m-%d')] = all_temps_dict[req_start.strftime('%Y-%m-%d')]
        req_start = req_start + dt.timedelta(days=1)
    
    return(start_dict)

def range_temps(start_date, end_date):
    """Function to find a year the covers the days requested
    and retunr min, avg, and max temps for a similiar time period"""
    req_start = dt.datetime.strptime(start_date,'%Y-%m-%d').date()
    req_end = dt.datetime.strptime(end_date,'%Y-%m-%d').date()
    
    range_days = req_end - req_start
    
    while req_start < firstdate:
        req_start = dt.date(day=req_start.day, month=req_start.month, year=req_start.year + 1)
    
    req_end = req_start + range_days
        
    while req_end > lastdate:
        req_end = dt.date(day=req_end.day, month=req_end.month, year=req_end.year - 1)
    
    req_start = req_end - range_days

    temp_dict = {}

    while req_start <= req_end:
        temp_dict[req_start.strftime('%Y-%m-%d')] = all_temps_dict[req_start.strftime('%Y-%m-%d')]
        req_start = req_start + dt.timedelta(days=1)
    
    return(temp_dict)

prcp_dict = precipitation()
stations_dict = stations()
temps_dict = get_temps(yearstart_date, lastdate)

all_temps_dict = get_temps(firstdate, lastdate)