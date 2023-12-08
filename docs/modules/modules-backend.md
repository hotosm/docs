# Backend Python Modules

## [OSM Login Python](https://hotosm.github.io/osm-login-python)

A way to consistently implement OSM login (via underlying OAuth2) in
our applications.

## [OSM Raw Data](https://hotosm.github.io/osm-rawdata)

OMS Raw Data supports the creation of data extracts into GeoJson or a
Postgres database. There is more detail on these modules on the [project
website](https://hotosm.github.io/osm-rawdata)).

### [PostgresClient()](https://hotosm.github.io/osm-rawdata/api/#postgrespy)
 
This program extracts data from a local postgres data, or the remote
Underpass one. A boundary polygon is used to define the area to be
covered in the extract. 

### [MapImporter()](https://hotosm.github.io/osm-rawdata/api/#importerpy)

Imports data into a postgres database that is using the Underpass
schema. This currently supports three input formats, Geojson, all OSM
formats, and Parquet files from Overture.

### [QueryConfig()](https://hotosm.github.io/osm-rawdata/api/#configpy)

This reads a config file in YAML format that describes the database
query. This is used to generate the queries for the different
database sources.

### [Overture()](https://hotosm.github.io/osm-rawdata/api/#overturepy)

Parses Overture Parquet files and creates a data structure of the
data so it can be imported into postgres, or generate an output
GeoJson file.

***
## [OSM Fieldwork](https://hotosm.github.io/osm-fieldwork)

Various utility programs useful for field data collection using ODK
Collect. These modules are used extensively in FMTM for all the
backend data processing.

There is more detail on these modules on the [project
website](https://hotosm.github.io/osm-fieldwork)).

### [BaseMapper()](https://hotosm.github.io/osm-fieldwork/api/basemapper/)

This makes basemaps of satellite imagery for ODK Collect and OsmAnd.

### [CSVDump()](https://hotosm.github.io/osm-fieldwork/api/CSVDump)

Converts the CSV files downloaded from ODK Central into OSM XML and
GeoJson so they can be edited in JOSM or QGIS.

### [JsonDump()](https://hotosm.github.io/osm-fieldwork/api/json2osm/)

Converts the JSON files downloaded from ODK Central into OSM XML and
GeoJson so they can be edited in JOSM or QGIS.

### [FilterData()](https://hotosm.github.io/osm-fieldwork/api/filter_data)

This scans an XLSForm, and removes all features from the data extract
that are not in the choices sheet. This is required to use the data
extract in ODK Collect.

### [MakeExtract()](https://hotosm.github.io/osm-fieldwork/api/make_data_extract/)

For ODK Collect, this makes the filtered data extract using
[osm-rawdata](https://hotosm.github.io/osm-rawdata/) and FilterData().

### [OdkCentral()](https://hotosm.github.io/osm-fieldwork/api/OdkCentral/)

This supports working with the REST API for ODK Central.

### [OsmFile()](https://hotosm.github.io/osm-fieldwork/api/osmfile/)

Produces OSM XML out files.

***
## [FMTMSplitter](https://hotosm.github.io/fmtm-splitter)

A splitting algorithm using PostGIS to divide an idea into task areas,
factoring in prominent map features (roads, rivers, etc).

The division is configurable via various parameters.

## [fAIr Utilities](https://hotosm.github.io/fAIr-utilities)

Various machine learning utils used within the fAIr backend.

***
## Conflator

This is a project for conflating external data sets with OpenStreetMap
data.

There is more detail on these modules on the [project
website](https://hotosm.github.io/conflator/)

### ConflateBuildings()

Conflate buildings from external datasets like the Microsoft or Google
building footprints.

### ConflatePOI()

Conflate POIs from external datasets like ODK Collect.
