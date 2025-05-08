# Future Plans / Ideas

This page describes various things we **want** at HOT, and are either
in the process of achieving, or have marked as potential future
projects.

If you are software developer and wish to contribute to something new,
fun, and exciting, feel free to reach out about one of these ideas.

## End-To-End

- We are hard at work building a full end-to-end mapping workflow, from
  our suite of available tools.
- A conceptual diagram of this can be seen on the
  [home page](https://docs.hotosm.org/#the-hot-ecosystem-of-tools)
  of this site.
- The whole idea is to allow a community to either:
  - Create a map, starting from absolutely nothing using the entire
    suite of tools. Imagery --> digitize --> field map --> export.
  - Choose a subset of our tools to fill the data gaps missing for
    their map. For example, maybe they have great digitized features
    already, but need to field-verify them and add extra tag info.

### E2E Site

- We need a centralized entrypoint for E2E mapping.
- Work a website to achieve this was started in
  [this project](https://hotosm.github.io/e2e-mapping), however,
  capacity has been limited to continue it!
- Eventually, it is envisioned that we will have a place that users
  can access, to:
  - Explain what E2E is, and what is possible.
  - Showcase the tools used in E2E and their capabilities.
  - Some hand-holding tutorials to easily link together all the tools
    required to successfully carry out an E2E mapping project.
- The key part here is an **interactive** tutorial, where the user can
  start by drawing an AOI for where they need to map, then each step
  will be explained, with helper buttons and visualisations to assist
  in the E2E mapping journey.

### Shared Login

- All of our tools need a shared login mechanism.
- Currently every tool has separate login, so a user visiting one tool
  needs to log in again when accessing another in the E2E suite.
- A very **nice to have** feature would be seamless login between our
  entire suite of tools:
  - **Simple**: the same auth cookie work across all apps, but user
    information is managed per-app still. Users are seamlessly logged
    in when moving between apps. This would be possible as every app
    shares the domain hotosm.org.
  - **Hard**: the authentication is managed somewhere centrally. The
    user logs in and user details are stored in a centralised 'HOT' database.
    The auth details are then passed to each application, but the app
    doesn't store user data. This one is technically difficult and I
    wouldn't advocate for it (we are essentially creating our own
    OAuth provider). In this case I think it's better to centralise
    around OSM auth.
- This links in to [shared ui components](#shared-ui-components) below,
  as the login will likely be faciliated within a 'header' component,
  containing OAuth flows for various providers (OSM, Google, etc).

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
  no centralized design from the start (a need to move quickly...).
- The proposed solution is to converge around a single **web component**
  library, such as [Web Awesome](https://backers.webawesome.com).
- Web Awesome is free to use / open-source, has strong backers, and
  would allow for a consistent style across all tools, regardless of
  framework used (framework-agnostic, web standards).
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
- We have many implementations of MapLibre in our different tools. Ideally
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

- Parsing of user uploaded GeoJSON AOIs (not as simple as it
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
- It will load various data sources: OSM, custom data, Overture, etc.
- Various imagery sources can be loaded in. Ideally high-resolution drone
  or recent open satellite imagery.
- The UI allows the user to select the best geometry / tags for a given
  feature, based on the available imagery.
- The feature is validated by others (optional), then uploaded to OSM
  as the new source of truth.
- If features came from FieldTM are **field verified** they should
  take precedence, and will be tagged as such in OSM.

### Tasking Manager Conflation

- Use Tasking Manager as a collaborative conflation tool.
- Create a new 'conflation' project type.
- Users load the imagery, and datasets required.
- Tasking allows the conflation process to be subdivided amongst
  the community, and validated.
- Final data is uploaded to OSM.

## Other Ideas

- Now we have [raw-data-api-py](https://github.com/hotosm/raw-data-api-py),
  it would be quite simple to make a QGIS plugin for this. Users of QGIS
  could download the latest OSM data directly into their project.
- We could also have a QGIS plugin to easily access data via the
  [Humanitarian Data Exchange](https://data.humdata.org)
