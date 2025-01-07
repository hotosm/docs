# Backend Python Modules

## [OSM Login Python](https://hotosm.github.io/osm-login-python)

A way to consistently implement OSM login (via underlying OAuth2) in
our applications.

## [OSM Raw Data](https://hotosm.github.io/osm-rawdata)

OMS Raw Data supports the creation of data extracts into GeoJson or a
Postgres database. There is more detail on these modules on the [project
website](https://hotosm.github.io/osm-rawdata)).

## [OSM Fieldwork](https://hotosm.github.io/osm-fieldwork)

Various utility programs useful for field data collection using ODK
Collect. These modules are used extensively in FMTM for all the
backend data processing.

There is more detail on these modules on the [project
website](https://hotosm.github.io/osm-fieldwork).

## [FMTMSplitter](https://hotosm.github.io/fmtm-splitter)

A splitting algorithm using PostGIS to divide an idea into task areas,
factoring in prominent map features (roads, rivers, etc).

The division is configurable via various parameters.

## [fAIr Utilities](https://hotosm.github.io/fAIr-utilities)

Various machine learning utils used within the fAIr backend.

## [GeoJSON AOI Parser](https://hotosm.github.io/geojson-aoi-parser)

Consistent parsing of user GeoJSON upload, for processing by tools
such as raw-data-api, FMTM, Drone-TM, etc.
