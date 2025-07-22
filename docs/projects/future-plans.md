# Future Plans / Ideas

This page describes various things we **want** at HOT, and are either
in the process of achieving, or have marked as potential future
projects.

If you are software developer and wish to contribute to something new,
fun, and exciting, feel free to reach out about one of these ideas.

## End-To-End Concept

- We are hard at work building a full end-to-end mapping workflow, leveraging
  our suite of available tools.
- A conceptual diagram of this can be seen on the
  [home page](https://docs.hotosm.org/#the-hot-ecosystem-of-tools)
  of this site.
- The goal is to allow the mapping commmunity to go trhough the entire
  mapping proces through community ownership and tools.
  Tools in the end-to-end mapping worklfow include a spectrum of solutions one
  can use depending on the need, not necessearily full set of tools.
  This can include:
  - Creating a map, starting from absolutely nothing using the entire
    suite of tools. Imagery --> digitize (extract data) --> field map --> export.
  - Choose a subset of our tools to fill the data gaps missing for
    their map. For example, maybe they have great digitized features
    already, but need to field-verify them and add extra tag info.

### A centralized E2E Site

- We need a centralized entrypoint for E2E mapping to make the workflow more accessilbe.
- Work a website to achieve this was started in
  [this project](https://hotosm.github.io/e2e-mapping), however,
  capacity has been limited to continue it so far.
- We envision to have a central place that users
  can access, to:
  - Understand what E2E is, and what it enables.
  - Showcase the tools used in E2E and their capabilities.
  - Some hand-holding tutorials to easily link together all the tools
    required to successfully carry out an E2E mapping project.
    For the latter, we target an **interactive** tutorial, where the user
    can start by drawing an AOI for where they need to map,

    then each step will be explained, with helper buttons and visualisations to assist
    in the E2E mapping journey.

### Shared Login accross tools

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

### Building Tools With Community In Mind

The full [end-to-end](#end-to-end-concept) mapping flow is built with community
mappers in mind. Empowering groups of people who wish to map the area
they live in, and produce open data for the benefit of others.

- **DroneTM**: collective base imagery collection using affordable
  drones distributed amongst a community of operators.
- **OpenAerialMap**: a centralized repository for aerial imagery, collected
  from DroneTM or other sources within the aerial imagery community.
- **fAIr**: a local geo-AI marketplace for the community to contribute
  feature prediction models, collectively test and rank model effectiveness,
  and assist the digitization effort with AI.
- **Tasking Manager**: collaborative mapping amongst remotely distributed
  communities.
- **FieldTM**: collaborative field mapping amongst local
  mapping groups (e.g. regional OSM chapters, or local NGOs).
- **Export Tool**: simple data export from OpenStreetMap, as a free service
  to the OSM community and mappers globally.

  Each of these tools needs continuous improvement. User roadmaps are available
  on the respective github pages

## Growing Our Software Dev Community

- We want to continue to foster the growth of a software development
  community around our tools.
- We should be open, inclusive, and welcome contribution in
  [many places](../become-a-contributor.md).
- HOT has excellent connections to NGOs and organizations, plus a
  very large community of active and engaged **mappers**, however,
  we have limited software development capabilities due to the size
  of our team!
- With some of our tools being recognized as
  [Digital Public Goods](https://www.un.org/digital-emerging-technologies/content/digital-public-goods),
  support the development of them has huge potential for impact on the
  end users in our priority regions.
- To facilitate this, we need to ensure that potential for contribution
  is well publicized and common knowledge. The onboarding process should
  be easy for new developers, plus we should be responsive and give back
  to users who continually demonstate their willingness to contribute.

  ## Cost-efficient and optimized architecture

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

## Reduced Code Duplication

### Shared UI Components

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

### Shared Map Components

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

### Python Modules (Backend)

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

## Other Ideas

### AI / LLMs

- OSM tag extraction from images or free text. Some work has started
  on this in [osm-tagger](https://github.com/hotosm/osm-tagger).
- A geospatial query chatbot, based on LLMs. Users want data for an
  area. The LLM can provide commands / ways to get this data, either
  via raw-data-api, overpass, or other available tools.

### Easy OSM Conflation

- Various tools in our stack need to contribute data back to OSM, merging
  it with the existing data present there (conflation).
- There are two possible approaches we could take, listed below.

#### Conflation Web Component

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

#### Tasking Manager Conflation

- Use Tasking Manager as a collaborative conflation tool.
- Create a new 'conflation' project type.
- Users load the imagery, and datasets required.
- Tasking allows the conflation process to be subdivided amongst
  the community, and validated.
- Final data is uploaded to OSM.

### Embeddable Web Components

Three projects spring to mind, where it would be really neat to have a small
lightweight web component, that could be embedded into any web tool / web page:

- [GCP Editor](https://github.com/hotosm/gcp-editor): developed for DroneTM,
  as a way to mark Ground Control Points on to captured images for more
  accurate georeferencing of the final imagery mosaic.
- [FieldTM Splitter](https://github.com/hotosm/fmtm-splitter/issues/66): this
  has yet to be developed, but the idea would be to have a self-contained
  splitting component, where an AOI can be divided based on certain criteria
  into task area. All of our tasking-manager type tools could benefit from this,
  in addition to organization wishing to subdivide areas for field activities.
- [OSM-Tagger](https://github.com/hotosm/osm-tagger): development of a web
  component is underway that would receive images or text from a user, and extract
  out potential OSM tags that could be applicable to the final dataset.

In general, it's great to have a completely standalone web component, with no
requirement to call an API.

This could be achievable by using JavaScript libs, WebAssembly, and awesome
projects such as [PGLite](https://pglite.dev/), an embedded Postgres database
in the browser.

For example, OSM-Tagger will probably always rely on an external API due to
it's reliance on Python Machine Learning libraries (this may change in future
as JavaScript / Web Machine Learning libraries improve).

But FieldTM Splitter could utilise PGLite to do the SQL splitting algorithms
entirely in the web browser.

### QGIS Plugins: Easy Data Access

- Now we have [raw-data-api-py](https://github.com/hotosm/raw-data-api-py),
  it would be quite simple to make a QGIS plugin for this. Users of QGIS
  could download the latest OSM data directly into their project.
- We could also have a QGIS plugin to easily access data via the
  [Humanitarian Data Exchange](https://data.humdata.org)

!!! note

    Before embarking on these plugin ideas, we should first assess if there
    is an actual need amongst communities first. Nothing worse than developing
    something that isn't actually needed / wanted.

### XLSForm Builder & Repository

Two problems:

1. XLSForms can be a bit tricky to build directly. Via a drag-and-drop
   web-ui would be easier.
2. Lots of duplication of XLSForms across projects. People would benefit
   from a centralised place to access some existing XLSForms.

Idea:

- We create a basic website that has an embedded form builder.
- The website also acts as an XLSForm resository, where any user
  can upload and contribute the XLSForm they designed, along with
  a description for what they were mapping.
- The form builder part should be a web component, so it can also
  be embedded into other sites too.
