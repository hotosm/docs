# Future Plans / Ideas

This page describes various things we **want** at HOT, and are either
in the process of achieving, or have marked as potential future
projects.

If you are software developer and wish to contribute to something new,
fun, and exciting, feel free to reach out about one of these ideas.

## Kubernetes

- Every HOT tool should be hosted in a Kubernetes cluster.
- This means every tool needs to be containerized and follow
  a [12factor](https://12factor.net) app development approach.
- Tools should be deployed using a GitOps approach, via ArgoCD.
  This means the container repositories for each tool are scanned,
  and when a new version is uploaded, it is automatically deployed.
- Load is shared amongst tools on cluster nodes, reducing overall
  costs of running multiple separate servers.
- Autoscaling capabilities when high load is detected for a tool,
  automatically spawning new containers as needed.

## Shared UI Components

See [this page](../modules/frontend.md) for more details.

- We don't have the resources to implement a very in-depth design
  system across all of our tools.
- We also have existing tech debt due to development velocity and
  no centralised design from the start (a need to move quickly...).
- The proposed solution is to converse around a single **web component**
  library, such as [Web Awesome](https://backers.webawesome.com).
- Web Awesome is free to use / open-source, has strong backers, and
  would allow for a consistent style across all tools, regardless of
  framework used (framework agnostic, web standards).
- It should also improve maintainability, as part of the promise of web
  components, is minimal requirement to upgrade into the future, as the
  World Wide Web Consortium (W3C) does not break existing web functionality.
- We would also avoid the framework churn, by having our **underlying
  building blocks** as web components, while building our wrapper apps in
  whichever technology we choose.
- A few additional **helper** components will be designed and made available
  as part of the [HOTOSM UI](https://github.com/hotosm/ui) library. For
  example, a consistent header, footer, and sidebar for every tool.

## Shared Map Components

See [this page](../modules/frontend.md) for more details.

- Historically we may have used OpenLayers and Leaflet in some places.
  This should be consolidated around MapLibre.
- We have many implementation of MapLibre in our different tools. Ideally
  we can use the same wrapper implementation, improving developer experience
  and speed of development.
- **Option 1**: contribute to an existing established tool, that can compile
  to plain JavaScript. This JS could be wrapped in a web-component for use in
  any web app, any framework.
  A top candidate would be
  [svelte-maplibre](https://github.com/dimfeld/svelte-maplibre).
- **Option 2**: build a web component wrapper for MapLibre from scratch. It
  is anticipated that community support would be high for this, being entirely
  framework agnostic and embeddable anywhere.

## Python Modules (Backend)

See [this page](../modules/backend.md) for more details.

We have a lot of duplicated logic that could be centralised:

- Parsing of user uploaded GeoJSON AOIs (no as simple as it
  sounds to do right).
  [geojson-aoi-parser](https://github.com/hotosm/geojson-aoi-parser)
- Download of OSM data via raw-data-api. Every tool doing this should
  use the [raw-data-api-py](https://github.com/hotosm/raw-data-api-py)
  wrapper.
- A bunch of OpenStreetMap-specific XLSForm surveys have been started
  in [osm-fieldwork](https://hotosm.github.io/osm-fieldwork), but this
  work needs some good community testing and peer review. The idea is to
  plug the XLSForms into FieldTM, for easy OSM-centric mapping of an area
  (to improve the map tags available, then push to OSM).

## AI / LLMs

- OSM tag extraction from images or free text. Some work has started
  on this in [osm-tagger](https://github.com/hotosm/osm-tagger).
- A geospatial query chatbot, based on LLMs. Users want data for an
  area. The LLM can provide commands / ways to get this data, either
  via raw-data-api, overpass, or other available tools.

## Easy OSM Conflation

- Various tools in our stack need to contribute data back to OSM, merging
  it with the existing data present there (conflation).
- There are two possible approaches we could take, listed below.

### Conflation Web Component

- A standalone 'conflation' web component that could be embedded in any
  tool.
- It will load various dataset sources: OSM, custom data, Overture, etc.
- Various imagery sources can be loaded in. Ideally high-resolution drone
  or recent open satellite imagery.
- The UI allows the user to select the best geometry / tags for a given
  feature, based on the available imagery.
- The feature is validated by others (optional), then uploaded to OSM
  as the new source of truth.
- If features came from FieldTM are are **field verified** they should
  take precedence, and will be tagged as such in OSM.

### Tasking Manager Conflation

- Use Tasking Manager as a collaborative conflation tool.
- Create a new 'conflation' project type.
- Users load the imagery, and datasets required.
- Tasking allow the conflation process to be subdivided amongst
  the community, and validated.
- Final data is uploaded to OSM.

## Other Ideas

- Now we have [raw-data-api-py](https://github.com/hotosm/raw-data-api-py),
  it would be quite simple to make a QGIS plugin for this. Users of QGIS
  could download the latest OSM data directly into their project.
- We could also have a QGIS plugin to easily access data via the
  [Humanitarian Data Exchange](https://data.humdata.org)
