# HOTOSM Tools

## Data Types

There are two main types of geospatial data we must consider for maps.

### Raster

This is imagery data - a picture (jpeg, png, tiff, etc).

On the lowest level the data is represented by pixels.

The pixels are assigned a value within a **band**:

- Single band: the image could be greyscale, where the pixel value
  contains a level of gray on a spectrum from white-black.
- Multi band: most images encountered in the OSM world will contain three
  bands (RGB), which can be imagined to be stacked on top of one another.
  Red, green, and blue are primary colours than when combined can form
  any other colour.

We are mostly interested in multi-band **optical** imagery, i.e. what you
may see on Google / Bing Satellite.

**This underpins the usage of other data, by visually locating it in
space - it tells you where your data is!**

### Vector

This is point, polygon, and line data - what you find on OSM!

The shapes are represented by some complex maths underneath and
rendered on your screen.

**This is the data that is typically layered on top of basemaps (either
raster or vector-based basemaps) for usage.**

## How is this data used?

### Input Data

- Raster Basemaps:
  - Google, Bing, ESRI, Mapbox all provide web basemaps we can use.
  - Open Aerial Map (OAM) provides more bespoke basemaps of particular areas
    of interest (AOIs), over a certain time period. Often higher resolution.
- Vector Data:
  - OpenStreeMap (OSM) is the biggest reference of open map data.
    - HOT's Export Tool & Raw Data API provide easy access to this.
  - Any other vector data in various formats:
    - GIS layers provided by governments: region boundaries, roads, etc.
    - Data collected by NGOs and other organizations, open or not.

**All of this data can be used for various purposes, involving processing
and data analysis**.

### Processed Data

Generally always **vector** data in our context.

It's OSM vector data that has been processed and packaged in a certain
way so it can be used by other tools / users.

Using the input data described above, we want to produce data with
additional value:

- To generate new data to feed back into OSM (a complete loop).
- For other purposes such as humanitarian response, data analysis
  and reporting.

## HOT's Tools

With the above as context, HOT's tools roughly can be categorised as such:

### Tool Division

#### Input

| Tool         | Description                                  |
| ------------ | -------------------------------------------- |
| Drone TM     | Get base imagery.                            |
| OAM          | Stored and accessible base imagery.          |
| Raw Data API | Extract data from OSM easily _for software_. |

> Note: input may be into our own tools, or workflows of others.

#### Output

| Tool        | Description                                               |
| ----------- | --------------------------------------------------------- |
| TM          | Digitize map features remotely.                           |
| fAIr        | Speed up the remote digitization process                  |
| FMTM        | Add extra information to digitised features in the field. |
| Export Tool | Extract data from OSM easily _for humans_.                |

### Project Summaries

#### Drone TM

Drone TM is the newest tool being developed by HOT.

It's purpose is to fill the gap of reliable, high-quality, base imagery
that can be used during the digitization process.

Given an AOI, an area can be subdivided into task areas and flight
plans generated for each users specific drone.

In a **collaborative** manner a large amount of high quality base
imagery can be generated very quickly and with minimal cost.

#### OpenAerialMap (OAM)

OAM should underpin all of our tools.

It is essentially a repository of base imagery, which is ideally
high-resolution for a specifically targetted mapping area.

Imagery can be uploaded from Drone TM, or any other openly available
data source, by the community.

The imagery is made available to other tools via the Tile Map Service
protocol (TMS).

#### Raw Data API

Uses an innovative database structure to make OSM data much more easily
searchable with excellent performance.

This database is made accessible behind an API, where users (or software)
can request OSM data within specific filter criteria.

Data can be exported in various formats, from GeoJSON to GeoPackage and Flatgeobuf.

#### Export Tool

The purpose of Export Tool is to:

- Take the users input for what data they need, over what area.
- Calls Raw Data API to extract and filter the data.
- Receives back the data in the user requested format.

> This is essentially the more user-centric frontend for raw-data-api.

#### Tasking Manager

Creating additional vector data to go into OSM, using raster imagery as a
source.

Pretty much creating polygons and lines from things you and see on a map
and uploading them to OSM.

The mapping is crowdsourced, or organised by NGOs.

Resulting data needs to be validated.

> Another tool, MapSwipe, also fills this niche but takes a much more minimalistic
> approach.
>
> It allows users without any prior OSM or mapping experience to contribute more
> effectively, from a mobile device or web browser.

#### fAIr

TM is labour intensive. fAIr uses localised training data to generate
a model that can be used to predict vector features from a raster image.

Integration into TM means mapping of features can be a lot faster.

#### FMTM

Adding useful tags, in the field, from the vector data created in TM.

The tags provide extra information about what features actually are in OSM.

Again, the mapping can be crowdsourced, but more likely organised by NGOs / govs.

The FMTM mapping could also provide a feedback loop to TM, helping to
validate that features were mapped correctly.

> As with TM, another tool, StreeComplete, can help with this & may be
> part of the solution.
>
> However, FMTM allows mapping to be done **collaboratively**.
