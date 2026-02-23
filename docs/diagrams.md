# How does everything fit together?

The HOT Tech Team is working to improve the user experience across
multiple tools, and working towards an end to end data flow between
projects.

During disaster response, or a humanitarian mapping campaign, a project
manager or mapper may require:

- High quality base imagery.
- Remotely mapped features, derived from this imagery.
- Field-verified information about these features.
- Data exported in a useful format for further analysis.

The goal of our proposed
[E2E Flow](https://hotosm.github.io/e2e-mapping) is to fill in these
gaps to aid an effective response.

## E2E

### 1. Imagery

```mermaid
flowchart LR
  subgraph FlightApps["Flight Apps"]
    subgraph Proprietary["Proprietary"]
      direction TB
      DroneDeploy@{ img: "/images/logos/dronedeploy-logo.svg", label: "DroneDeploy", pos: "b", w: 120, h: 50 }
      Litchi@{ img: "/images/logos/litchi-logo.png", label: "Litchi", pos: "b", w: 92, h: 50 }
    end
    subgraph OpenGCS["Open-Source / MAVLink"]
      direction TB
      QGroundControl@{ img: "/images/logos/qgroundcontrol-logo.svg", label: "QGroundControl", pos: "b", w: 52, h: 52 }
    end
  end

  subgraph Capture["Capture"]
    direction TB
    Drones@{ img: "/images/logos/drone-icon.svg", label: "Drones", pos: "b", w: 56, h: 56 }
    DGPS@{ img: "/images/logos/transmitter.svg", label: "DGPS Receiver", pos: "b", w: 52, h: 52 }
  end

  subgraph HOT["Maintained by HOT"]
    direction TB
    DroneTM@{ img: "/images/logos/dronetm-logo.svg", label: "DroneTM", pos: "b", w: 50, h: 46 }
    ScaleODM@{ img: "/images/logos/hot-logo.svg", label: "ScaleODM", pos: "b", w: 96, h: 58 }
  end

  subgraph Processing["Processing"]
    direction TB
    ODM@{ img: "/images/logos/odm-logo.svg", label: "OpenDroneMap", pos: "b", w: 120, h: 40 }
  end

  OAM@{ img: "/images/logos/oam-logo.svg", label: "OpenAerialMap", pos: "b", w: 56, h: 56 }
  Satellite@{ img: "/images/logos/satellite-icon.svg", label: "Open Satellite Imagery", pos: "b", w: 54, h: 54 }

  DroneTM -- "Waypoint files" --> DroneDeploy
  DroneTM -- "Waypoint files" --> Litchi
  DroneTM -- "Waypoint files" --> QGroundControl
  DroneDeploy -- "Automated flight" --> Drones
  Litchi -- "Automated flight" --> Drones
  QGroundControl -- "Automated flight" --> Drones
  DGPS -- "Ground Control Points" --> DroneTM
  Drones -- "Raw imagery" --> DroneTM
  DroneTM -- "Photos + metadata" --> ScaleODM
  ScaleODM -- "Autoscaled tasks" --> ODM
  ODM -- "Processed imagery" --> OAM
  DroneTM -- "Imagery Metadata" --> OAM
  Satellite -- "Basemap imagery" --> OAM

  style HOT fill:#FDD0D6,stroke:#D73F3F,stroke-width:2px
  style FlightApps fill:#FFF59B,stroke:#FAA71E,stroke-width:2px
  style Proprietary fill:#FFF9C3,stroke:#FAA71E,stroke-width:1px
  style OpenGCS fill:#FFF9C3,stroke:#FAA71E,stroke-width:1px
  style Capture fill:#FFF59B,stroke:#FAA71E,stroke-width:2px
  style Processing fill:#FFF59B,stroke:#FAA71E,stroke-width:2px
```

### 2. Remote Mapping

```mermaid
flowchart LR
  subgraph HOT["Maintained by HOT"]
    direction TB
    OAM@{ img: "/images/logos/oam-logo.svg", label: "OpenAerialMap", pos: "b", w: 56, h: 56 }
    FAIR@{ img: "/images/logos/hot-logo.svg", label: "fAIr", pos: "b", w: 96, h: 58 }
    TM@{ img: "/images/logos/hot-logo.svg", label: "Tasking Manager", pos: "b", w: 96, h: 58 }
    Sandbox@{ img: "/images/logos/generic-data-icon.svg", label: "OSM Sandbox", pos: "b", w: 48, h: 48 }
    RawDataAPI@{ img: "/images/logos/hot-logo.svg", label: "Raw Data API", pos: "b", w: 96, h: 58 }
    ExportTool@{ img: "/images/logos/hot-logo.svg", label: "Export Tool", pos: "b", w: 96, h: 58 }
  end

  subgraph External["External Ecosystem"]
    direction TB
    MapSwipe@{ img: "/images/logos/mapswipe-logo.svg", label: "MapSwipe", pos: "b", w: 54, h: 54 }
    Rapid@{ img: "/images/logos/rapid-logo.png", label: "Rapid", pos: "b", w: 96, h: 40 }
    OtherSources@{ img: "/images/logos/generic-data-icon.svg", label: "Other Data Sources", pos: "b", w: 48, h: 48 }
    Overture@{ img: "/images/logos/overture-logo.svg", label: "Overture", pos: "b", w: 52, h: 50 }
  end

  OSM@{ img: "/images/logos/osm-logo.svg", label: "OpenStreetMap", pos: "b", w: 80, h: 80 }

  OAM -- "1. Imagery context" --> FAIR
  MapSwipe -- "2. Training / validation data" --> FAIR
  FAIR -- "3. Model predictions" --> TM
  FAIR -. "3. Direct features (no TM)" .-> Rapid
  OSM -- "4a. Existing map data" --> TM
  Overture -- "4b. Reference data" --> TM
  OtherSources -- "4c. Additional data" --> TM
  TM -. "5. Optional validation" .-> MapSwipe
  TM -- "6. Conflation UI" --> Rapid
  TM --> Sandbox
  Rapid -- "7. Mapped output" --> OSM
  OSM --> RawDataAPI --> ExportTool

  style HOT fill:#FDD0D6,stroke:#D73F3F,stroke-width:2px
  style External fill:#FFF59B,stroke:#FAA71E,stroke-width:2px
```

### 3. Field Mapping

```mermaid
flowchart LR
  OAM@{ img: "/images/logos/oam-logo.svg", label: "OpenAerialMap", pos: "b", w: 56, h: 56 }

  subgraph HOT["Maintained by HOT"]
    direction TB
    FMTM@{ img: "/images/logos/hot-logo.svg", label: "Field Mapping TM", pos: "b", w: 96, h: 58 }
  end

  subgraph Mobile["Mobile Data Collection"]
    direction TB
    ODK@{ img: "/images/logos/odk-logo.svg", label: "ODK", pos: "b", w: 100, h: 55 }
    KoBoToolbox@{ img: "/images/logos/kobotoolbox-logo.svg", label: "KoBoToolbox", pos: "b", w: 54, h: 54 }
    QField@{ img: "/images/logos/qgis-logo.svg", label: "QField", pos: "b", w: 54, h: 54 }
    ChatMap@{ img: "/images/logos/hot-logo.svg", label: "ChatMap", pos: "b", w: 96, h: 58 }
    ONA@{ img: "/images/logos/ona.io-logo.png", label: "ONA", pos: "b", w: 52, h: 52 }
  end

  Panoramax@{ img: "/images/logos/panoramax-logo.svg", label: "Panoramax", pos: "b", w: 52, h: 52 }
  OSM@{ img: "/images/logos/osm-logo.svg", label: "OpenStreetMap", pos: "b", w: 80, h: 80 }

  OAM -- "Imagery basemap" --> FMTM
  FMTM -- "Create Coordinate Mapping Project" --> ODK
  FMTM -- "Create Coordinate Mapping Project" --> KoBoToolbox
  FMTM -- "Create Coordinate Mapping Project" --> QField
  FMTM -- "Create Coordinate Mapping Project" --> ChatMap
  FMTM -- "Create Coordinate Mapping Project" --> ONA
  ODK -- "Submit data" --> FMTM
  KoBoToolbox -- "Submit data" --> FMTM
  QField -- "Submit data" --> FMTM
  ChatMap -- "Submit data" --> FMTM
  ONA -- "Submit data" --> FMTM
  ODK -. "Street imagery" .-> Panoramax
  KoBoToolbox -. "Street imagery" .-> Panoramax
  QField -. "Street imagery" .-> Panoramax
  Panoramax -- "ML-extracted tags" --> OSM
  FMTM -- "Geometries and Tags" --> OSM

  style HOT fill:#FDD0D6,stroke:#D73F3F,stroke-width:2px
  style Mobile fill:#FFF59B,stroke:#FAA71E,stroke-width:2px
```

### 4. Data Insights

```mermaid
flowchart LR
  OSM@{ img: "/images/logos/osm-logo.svg", label: "OpenStreetMap", pos: "b", w: 80, h: 80 }

  subgraph HOT["Maintained by HOT"]
    direction TB
    RawDataAPI@{ img: "/images/logos/hot-logo.svg", label: "Raw Data API", pos: "b", w: 96, h: 58 }
    ExportTool@{ img: "/images/logos/hot-logo.svg", label: "Export Tool", pos: "b", w: 96, h: 58 }
  end

  subgraph Analytics["Analytics"]
    ohsomeNow@{ img: "/images/logos/ohsomenow-logo.svg", label: "ohsomeNow Statistics", pos: "b", w: 120, h: 35 }
  end

  subgraph Outputs["Visualisation & Distribution"]
    direction TB
    HDX@{ img: "/images/logos/humdata-logo.svg", label: "Humanitarian Data Exchange", pos: "b", w: 70, h: 68 }
    QGIS@{ img: "/images/logos/qgis-logo.svg", label: "QGIS", pos: "b", w: 54, h: 54 }
    UMap@{ img: "/images/logos/umap-logo.svg", label: "uMap", pos: "b", w: 60, h: 60 }
  end

  OSM -- "Software queries" --> RawDataAPI
  OSM -- "Historical analysis" --> ohsomeNow
  RawDataAPI -- "Human exports" --> ExportTool
  ExportTool -- "Humanitarian datasets" --> HDX
  ExportTool -- "GIS data" --> QGIS
  ExportTool -- "Map layers" --> UMap
  ohsomeNow -- "Statistics & trends" --> QGIS

  style HOT fill:#FDD0D6,stroke:#D73F3F,stroke-width:2px
  style Analytics fill:#FFF59B,stroke:#FAA71E,stroke-width:2px
  style Outputs fill:#FFF59B,stroke:#FAA71E,stroke-width:2px
```
