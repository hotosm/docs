# Backend Modularization

## OSM Login Python

A way to consistently implement OSM login (via underlying OAuth2) in
our applications. [github link](https://hotosm.github.io/osm-login-python)

## OSM Raw Data

Creation of raw OpenStreetMap data extracts into GeoJson or a Postgres
database. There is more detail on these modules on the [project
website]([link](https://hotosm.github.io/osm-rawdata)).

### PostgresClient()
 
This program extracts data from a local postgres data, or the remote
Underpass one. A boundary polygon is used to define the area to be
covered in the extract. 

### MapImporter()

Imports data into a postgres database that is using the Uunderpass
schema. This currently supports three input formats, Geojson, all OSM
formats, and Parquet files from Overture.

### QueryConfig()

This reads a config file in YAML format that describes the database
query.

### overture.py

Parses Overture Parquet files and creates a data structure of the
data. Optionally

## OSM Fieldwork

Various utility programs useful for field data collection.

- Processing data collection using OpenDataKit into OpenStreetMap format.
- Basemap generation for offline fieldwork.
- Used extensively in FMTM for a variety of tasks.

[github link](https://hotosm.github.io/osm-fieldwork)

## FMTM Splitter

A splitting algorithm using PostGIS to divide an idea into task areas,
factoring in prominent map features (roads, rivers, etc).

The division is configurable via various parameters.

[github link](https://hotosm.github.io/fmtm-splitter)

## fAIr Utilities

Various machine learning utils used within the fAIr backend.

[githuib link](https://hotosm.github.io/fAIr-utilities)
