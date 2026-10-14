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

### Overview

| Tool         | Description                                               |
| ------------ | --------------------------------------------------------- |
| Drone TM     | Get base imagery.                                         |
| OAM          | Stored and accessible base imagery.                       |
| Raw Data API | Extract data from OSM easily _for software_.              |
| TM           | Digitize map features remotely.                           |
| fAIr         | Speed up the remote digitization process                  |
| FieldTM      | Add extra information to digitised features in the field. |
| Export Tool  | Extract data from OSM easily _for humans_.                |
| ChatMap      | Collect field data using messaging apps.                  |
| uMap         | Share simple interactive maps of the results.             |

### When should I use each tool?

Many projects chain several tools together (imagery → digitisation →
field data → data access), i.e. what we call and End-To-End project.

But you may only need to use a single tool.

#### Drone TM

- **What it does:** splits an area into tasks and generates flight plans, so
  a team of pilots with low-cost drones (e.g. DJI Mini 4 Pro) can capture
  imagery together. Processes it into orthophotos, elevation models and 3D,
  then publishes to OAM.
- **Use it when:** satellite imagery is too old, too coarse or too cloudy, and
  you need fresh, very high resolution (~5cm) imagery of a neighbourhood or
  town, ideally flown by the local community.
- **Probably not when:** you need hundreds of km² quickly, for example in expansive
  rural areas (a micro-drone covers
  roughly 1-4 km² per day; use satellite or a fixed-wing drone instead), flying isn't
  permitted, or existing imagery is good enough.

#### OpenAerialMap (OAM)

- **What it does:** an open catalogue of satellite, aerial and drone imagery,
  served as map tiles to other tools and available to download.
- **Use it when:** you need openly licensed imagery as a basemap for TM, fAIr
  or FieldTM, or want to share imagery you collected so others can map from it.
- **Probably not when:** the imagery can't be shared openly (OAM is CC BY 4.0),
  or you need to analyse imagery: OAM stores and serves it, nothing more.

#### Tasking Manager (TM)

- **What it does:** splits an area into small tasks, so many remote volunteers
  can trace features (buildings, roads) from imagery into OSM, followed by
  a validation step.
- **Use it when:** you need complete and accurate OSM data for an area and can
  mobilise mappers and validators, e.g. the pre-disaster building baseline
  after an earthquake. Accuracy over speed.
- **Probably not when:** you need results within hours over a very large area
  (use fAIr to prioritise first), the data shouldn't go into OSM, or the
  information can only be gathered on the ground (FieldTM / ChatMap). Dense or
  complex areas need experienced mappers.

#### fAIr

- **What it does:** runs AI models on imagery to predict features (e.g.
  buildings, damage). The predictions are suggestions for people to check,
  and are never added to OSM automatically.
- **Use it when:**
  1. Speed matters more than precision: mapping is much faster, at the cost
     of accuracy and more validation work.
  2. You need to know where to focus: e.g. density or damage models to find
     the worst-hit areas after an earthquake, then detailed mapping of
     pre- and post-disaster imagery in TM.
- **Probably not when:** nobody can validate the output (predictions are
  preliminary until checked in MapSwipe, TM or the field), there is no high
  resolution imagery, or no model works well for your area and feature type.

> MapSwipe (not a HOT tool) is often the quickest way to validate fAIr output:
> volunteers swipe through imagery on a phone to answer yes / no questions at
> scale. It doesn't draw or edit features.

#### FieldTM

- **What it does:** coordinates field mapping teams. Splits the area into
  tasks, assigns them to mappers, and sets up the survey in ODK or QField.
  Data can go into OSM, or stay outside it.
- **Use it when:** a team needs to visit features across an area to collect
  details you can't see from above (building use, floors, materials), and you
  need to track progress of who is mapping where (coordination).
- **Probably not when:** one or two people are collecting ad-hoc data (use ODK,
  QField, StreetComplete or EveryDoor directly), untrained members of the
  public are reporting what they see (ChatMap), or the features haven't been
  digitised yet (TM / fAIr first).

#### ChatMap

- **What it does:** turns locations, photos, videos and messages shared in a
  group chat (e.g. WhatsApp) into a map. A chatbot can guide people through a
  simple survey.
- **Use it when:** you need fast ground reports from people who already use
  messaging apps and won't install anything new, e.g. damage, shelters or
  blocked roads after a disaster.
- **Probably not when:** you need structured, consistent data for every feature
  (FieldTM), or nobody can review incoming reports: public chat groups
  produce inconsistent data that needs moderating.

#### Export Tool

- **What it does:** a web interface to download OSM data for an area, filtered
  by feature type, in common GIS formats.
- **Use it when:** a person needs OSM data in QGIS, a spreadsheet or a report.
- **Probably not when:** software needs the data automatically (Raw Data API),
  or a country dataset already exists on the Humanitarian Data Exchange (HDX).

#### Raw Data API

- **What it does:** an API for fast, filtered OSM extracts. It sits behind the
  Export Tool, HDX exports, fAIr and FieldTM.
- **Use it when:** you're building software that needs fresh OSM data on demand.
- **Probably not when:** you just want a file (use the Export Tool). Due to be
  replaced by a cloud-native export pipeline in 2027.

#### uMap

- **What it does:** create and share simple interactive web maps, no GIS
  skills needed.
- **Use it when:** you want to share results (e.g. validated damage, project
  progress) with partners or the public quickly.
- **Probably not when:** you need analysis or very large datasets (use QGIS).

### How they fit together

- **Disaster response** (e.g. the 2026 Venezuela earthquake): fAIr density and
  damage models to prioritise areas → MapSwipe to validate the predictions →
  TM to map the building baseline in detail → ChatMap for ground reports →
  data shared on HDX and in uMap.
- **Community mapping:** Drone TM → OAM → TM (with fAIr to speed it up) →
  FieldTM → Export Tool / uMap.
