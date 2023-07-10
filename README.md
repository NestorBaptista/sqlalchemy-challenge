# sqlalchemy-challenge

## Climate Analysis and Flask API:

This repository contains a climate analysis and a Flask API for exploring climate data in Honolulu, Hawaii.

To analyze and explore the climate data, run the climate_starter.ipynb Jupyter Notebook using the provided hawaii.sqlite database. The notebook uses Python, SQLAlchemy, Pandas, and Matplotlib.

### The Flask API provides the following routes:

/api/v1.0/precipitation: Retrieve precipitation data for the last 12 months.<br/>
/api/v1.0/stations: Get a list of stations.<br/>
/api/v1.0/tobs: Retrieve temperature observations for the most active station in the previous year.<br/>
/api/v1.0/<start>: Calculate min, avg, and max temperatures from a given start date to the end of the dataset.<br/>
/api/v1.0/<start>/<end>: Calculate min, avg, and max temperatures for a specified date range.<br/>
Refer to the API routes for more details on parameters and responses.
