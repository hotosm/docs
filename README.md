# Welcome to HOTOSM's Docs

📖 Welcome to the HOT Technical [documentation](https://docs.hotosm.org)
for all of our open-source tools.

This website is primary an index linking to the documentation for each
specific tool, including including setup and usage instructions, API
documentation, and product roadmaps.

This documentation is available under the `Projects` section in the sidebar.

The following additional documentation is provided:

- A high level overview of how our tools inter-relate and can be used to
  form an End-To-End mapping workflow.
- Information on our development practices at HOT.
- Our community code of conduct for contribution.
- Our privacy policy for most of our tools.
- Developer guidelines and information to assist the development workflow.

HOT is working towards the modularization of our code to improve
maintainability and implement an end-to-end user flow between multiple
tools. There is more info about [modularization](modules.md) of our code.

## The HOT Ecosystem of Tools

```mermaid
flowchart LR
  subgraph Imagery["1) Imagery"]
    direction TB
    OAM@{ img: "/images/logos/oam-logo.svg", label: "OpenAerialMap", pos: "b", w: 56, h: 56 }
    DroneTM@{ img: "/images/logos/dronetm-logo.svg", label: "DroneTM", pos: "b", w: 50, h: 46 }
    Satellite@{ img: "/images/logos/satellite-icon.svg", label: "Open Satellite Imagery", pos: "b", w: 54, h: 54 }
  end

  subgraph HOTDigitization["2) HOT Digitization Tools"]
    direction TB
    TM@{ img: "/images/logos/hot-logo.svg", label: "Tasking Manager", pos: "b", w: 96, h: 58 }
    FAIR@{ img: "/images/logos/hot-logo.svg", label: "fAIr", pos: "b", w: 96, h: 58 }
  end

  subgraph FieldMapping["3) Field Mapping"]
    direction TB
    FMTM@{ img: "/images/logos/hot-logo.svg", label: "Field Mapping TM", pos: "b", w: 96, h: 58 }
    ChatMap@{ img: "/images/logos/hot-logo.svg", label: "ChatMap", pos: "b", w: 96, h: 58 }
    Panoramax@{ img: "/images/logos/panoramax-logo.svg", label: "Panoramax", pos: "b", w: 52, h: 52 }
  end

  subgraph DataAccess["4) Data Access & Outputs"]
    direction TB
    RawDataAPI@{ img: "/images/logos/hot-logo.svg", label: "Raw Data API", pos: "b", w: 96, h: 58 }
    ExportTool@{ img: "/images/logos/hot-logo.svg", label: "Export Tool", pos: "b", w: 96, h: 58 }
    HDX@{ img: "/images/logos/humdata-logo.svg", label: "Humanitarian Data Exchange", pos: "b", w: 70, h: 68 }
  end

  subgraph External["External Ecosystem"]
    direction TB
    OSM@{ img: "/images/logos/osm-logo.svg", label: "OpenStreetMap", pos: "b", w: 96, h: 58 }
    MapSwipe@{ img: "/images/logos/mapswipe-logo.svg", label: "MapSwipe", pos: "b", w: 54, h: 54 }
    OhsomeNow@{ img: "/images/logos/ohsomenow-logo.svg", label: "ohsomeNow Statistics", pos: "b", w: 96, h: 58 }
    UMap@{ img: "/images/logos/umap-logo.svg", label: "uMap", pos: "b", w: 96, h: 58 }
    Overture@{ img: "/images/logos/overture-logo.svg", label: "Other Data Sources", pos: "b", w: 96, h: 58 }
  end

  Satellite --> OAM
  DroneTM --> OAM
  OAM --> TM
  OAM --> FAIR
  TM --> FAIR
  FAIR --> TM
  OSM --> TM
  MapSwipe --> FAIR
  TM --> OSM
  OSM --> FMTM
  FMTM --> OSM
  FMTM --> Panoramax
  Panoramax --> OSM
  OSM --> ChatMap
  OSM --> RawDataAPI
  RawDataAPI --> ExportTool
  RawDataAPI --> HDX
  UMap --> FMTM
  OhsomeNow --> TM
  Overture --> TM

  style Imagery fill:#FDD0D6,stroke:#D73F3F,stroke-width:2px
  style HOTDigitization fill:#FDD0D6,stroke:#D73F3F,stroke-width:2px
  style FieldMapping fill:#FDD0D6,stroke:#D73F3F,stroke-width:2px
  style DataAccess fill:#FDD0D6,stroke:#D73F3F,stroke-width:2px
  style External fill:#FFF59B,stroke:#FAA71E,stroke-width:2px
```
