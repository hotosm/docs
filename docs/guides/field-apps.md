# Other Field Mapping Apps

HOT's tools work alongside these open source field apps. This overview
covers their strengths; follow the official docs for details.

| App             | Platforms                 | Best for                                          | Data goes to                      |
| --------------- | ------------------------- | ------------------------------------------------- | --------------------------------- |
| ODK Collect     | Android                   | Structured surveys with forms                     | ODK Central (or OSM via Field-TM) |
| KoboToolbox     | Android, web              | Surveys, with free hosting for humanitarian orgs  | KoboToolbox server                |
| QField          | Android, iOS, desktop     | Full GIS editing in the field, based on QGIS      | QGIS project / QFieldCloud        |
| Every Door      | Android, iOS              | Quickly adding and updating shops and amenities   | OpenStreetMap                     |
| StreetComplete  | Android                   | Answering simple questions to complete OSM data   | OpenStreetMap                     |
| CoMaps          | Android, iOS              | Offline navigation, with simple OSM edits         | OpenStreetMap                     |
| Sketch Map Tool | Web + paper               | Participatory mapping with no phones in the field | GeoJSON / GeoTIFF download        |
| Panoramax       | Android, web, 360 cameras | Street-level photos to map from later             | A Panoramax instance (open)       |
| DHIS2 Capture   | Android                   | Health programme data for a national DHIS2 system | DHIS2 server (Ministry of Health) |

## ODK

- **What it does:** a suite for collecting structured data with forms.
  Forms are written as spreadsheets (XLSForm), filled in on phones with the
  ODK Collect app, and submissions are managed on an ODK Central server.
- **Good at:** surveys with many questions, validation rules and skip
  logic; working offline and syncing later; capturing points, lines,
  polygons, photos and audio.
- **With HOT tools:** Field-TM can set up ODK forms and assign mapping
  tasks, and can send the collected data to OSM or keep it outside OSM.
- **Docs:**
  [docs.getodk.org](https://docs.getodk.org) and the form reference at
  [xlsform.org](https://xlsform.org).

## KoboToolbox

- **What it does:** a survey platform built on the same form standard as
  ODK (XLSForm). Collect data with the KoboCollect app or in the browser.
- **Good at:** organisations that want a hosted server without running
  their own; the forms are largely interchangeable with ODK.
- **With HOT tools:** see the
  [Field-TM FAQ](https://docs.field.hotosm.org/about/faq/) on how Field-TM
  and Kobo relate.
- **Docs:**
  [support.kobotoolbox.org](https://support.kobotoolbox.org).

## QField

- **What it does:** a mobile GIS app built on QGIS. Prepare projects on
  desktop, then edit them in the field.
- **Good at:** editing many layers with full attribute forms, drawing
  detailed geometries, offline work, and using external GNSS receivers for
  higher accuracy. QFieldCloud can sync projects between QGIS and phones.
- **With HOT tools:** Field-TM supports QField as an alternative to ODK for
  teams that need more GIS features.
- **Docs:**
  [docs.qfield.org](https://docs.qfield.org).

## Every Door

- **What it does:** adds and updates OpenStreetMap points of interest,
  such as shops, amenities and building entrances, as you walk.
- **Good at:** fast, detailed OSM surveys of businesses and amenities
  by individuals or small groups.
- **Not for:** coordinated team projects or data that must stay out of OSM
  (use Field-TM or ChatMap).
- **Docs:** [every-door.app](https://every-door.app).

## StreetComplete

- **What it does:** an Android app with "quests": simple questions about
  nearby features (e.g. "Is this road lit?"). Answers update OpenStreetMap.
- **Good at:** beginners improving OSM data with no mapping knowledge.
- **Not for:** adding many new features or collecting data outside OSM.
- **Docs:** [streetcomplete.app](https://streetcomplete.app).

## CoMaps

- **What it does:** an offline maps and navigation app using OpenStreetMap
  data. Download a country, then search and get walking, cycling or driving
  directions offline. You can also add or correct places in
  OSM from the app.
- **Good at:** getting field teams to survey locations offline, and
  quick fixes to OSM (a missing shop, wrong opening hours).
- **Why CoMaps?** Organic Maps forked from Maps.me; CoMaps forked from
  Organic Maps in 2025. We recommend CoMaps because it is run as an open,
  community-governed project (Apache 2.0 licence, developed on Codeberg).
  The fork came after contributors raised concerns about Organic Maps'
  governance and transparency. Maps.me is now a commercial app with ads
  and tracking.
- **Not for:** structured surveys or team projects (use Field-TM).
- **Docs:** [comaps.app](https://www.comaps.app).

## Sketch Map Tool

- **What it does:** turns hand-drawn paper maps into digital data.
  Print a map of your area from the website (OSM or satellite imagery,
  including OpenAerialMap). People draw on it with coloured pens, then you
  photograph or scan it and upload it. The tool georeferences the image and
  detects the drawings automatically.
- **Good at:** community and participatory mapping where people don't
  have smartphones, or where talking around a paper map works better (risk
  mapping, evacuation routes, local knowledge). Only printing and uploading
  need internet.
- **Output:** GeoJSON (the drawn areas) and GeoTIFF (the georeferenced
  map), ready for QGIS or [uMap](share-results-umap.md).
- **Docs:**
  [sketch-map-tool.heigit.org](https://sketch-map-tool.heigit.org), made
  by HeiGIT (Heidelberg University).

## Panoramax

- **What it does:** an open alternative to Google Street View and
  Mapillary for street-level photos. Capture photo sequences with a phone
  or a 360° camera while walking or driving, then upload them. Faces and
  number plates are blurred automatically.
- **Good at:** collecting imagery once in the field so remote mappers can
  later add details that satellite or drone imagery can't show: shop
  names, building use, road surface, signs. The iD and JOSM editors can
  show Panoramax photos while mapping.
- **Open by design:** it is federated, so anyone (for example a national
  OSM community) can host an instance. Photos on the OpenStreetMap France
  instance are CC BY-SA 4.0, with permission to derive OSM data from them.
- **Docs:** [panoramax.fr](https://panoramax.fr), started by
  the French mapping agency (IGN) and OpenStreetMap France.

## DHIS2

- **What it does:** a health management information system run by
  Ministries of Health in over 70 countries, especially across Africa and
  Asia. Health workers report through the DHIS2 Capture Android app (works
  offline) or the web, and the national server provides dashboards and
  maps. Built by the HISP Centre at the University of Oslo, BSD licence.
- **Not a general mapping app:** it is built around health programmes and
  facility reporting, not open-ended field surveys or OSM.
- **For health ministry work:** facility and population data
  probably already live in DHIS2. Match your field data (e.g. facilities
  mapped with Field-TM) to its facility list instead of creating a new one.
- **With HOT tools:** we are exploring integrations, see
  [Field-TM issue #3134](https://github.com/hotosm/field-tm/issues/3134).
- **Docs:** [dhis2.org](https://dhis2.org) and
  [docs.dhis2.org](https://docs.dhis2.org).
