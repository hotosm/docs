# Backend Python Modules

## [OSM Login Python](https://hotosm.github.io/osm-login-python)

A way to consistently implement OSM login (via underlying OAuth2) in
our applications.

## [Drone Flightplan](https://github.com/hotosm/drone-flightplan)

A module within DroneTM that can generate flightplans for various
drone models standalone. Useful to integrating into workflows
outside of DroneTM, such as within QGIS plugins.

## [PG Nearest City](https://hotosm.github.io/pg-nearest-city)

A very simple tool for reverse-geocoding points to the nearest
city over 1000 population. Requires no network requests and
runs entirely in an attached PostGIS instance.

## [GeoJSON AOI Parser](https://hotosm.github.io/geojson-aoi-parser)

Consistent parsing of user GeoJSON upload, for processing by tools
such as raw-data-api, FieldTM, Drone-TM, etc, using an underlying
PostGIS database.

## [Raw Data API Py](https://hotosm.github.io/raw-data-api-py)

A Python wrapper for HOT's raw-data-api. This allows for downloading
of frequently updated OSM data very conveniently.

## [OSM Fieldwork](https://hotosm.github.io/osm-fieldwork)

Various utility programs useful for field data collection using ODK
Central. These modules are used extensively in Field for all the
backend data processing.

## [FieldTM Splitter](https://hotosm.github.io/fmtm-splitter)

A splitting algorithm using PostGIS to divide an idea into task areas,
factoring in prominent map features (roads, rivers, etc).

The division is configurable via various parameters.

## [fAIr Utilities](https://github.com/hotosm/fAIr-utilities)

Various machine learning utils used within the fAIr backend.
