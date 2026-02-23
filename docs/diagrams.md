# How does everything fit together?

The HOT Tech Team is working to improve the user experience across
multiple tools, and working towards an end to end data flow between
projects.

During disaster response, or a humanitarian mapping campaign, a project
manager or mapper may require:

- High quality base imagery.
- Digitized map features, derived from this imagery.
- Field-verified information about these features.
- Data exported in a useful format for further analysis.

The goal of our proposed
[E2E Flow](https://hotosm.github.io/e2e-mapping) is to fill in these
gaps to aid an effective response.

## E2E

### 1. Imagery Collection

```mermaid
flowchart TD
  subgraph Capture
    Drones["Drones"]
    DroneTM["DroneTM"]
    DroneDeploy["DroneDeploy"]
    Litchi["Litchi"]
    WaypointFiles["Waypoint Files"]
    DGPS["DGPS Receiver"]
  end

  subgraph Processing
    ODM["OpenDroneMap"]
    K8s["Kubernetes"]
    S3["S3 Object Storage"]
  end

  subgraph Access
    OAM["OpenAerialMap"]
  end

  DroneTM -- "Photos, Metadata, CRS" --> ODM
  ODM -- "Merged Imagery" --> DroneTM
  DroneTM -- "Orthophoto Tile Map Service" --> OAM
  DroneTM --> DroneDeploy
  DroneTM --> Litchi
  DroneTM --> WaypointFiles
  DroneDeploy --> Drones
  Litchi --> Drones
  WaypointFiles --> Drones
  Drones -- "Raw Imagery" --> DroneTM
  DroneTM -- "Photos, Metadata, CRS" --> DGPS
  DGPS -- "Ground Control Points" --> DroneTM
  DroneTM -- "COG (2D), COPC (3D)" --> S3
  ODM --> K8s
  K8s -- "Job Autoscaling" --> ODM
```

### 2. Digitization

```mermaid
flowchart TD
  subgraph HOTTools
    TM["Tasking Manager"]
    OSM["OpenStreetMap"]
    Sandbox["OSM Sandbox"]
    FAIR["fAIr"]
    MapSwipe["MapSwipe"]
    Rapid["Rapid"]
    UMap["uMap"]
  end

  subgraph External
    OtherSources["Other Data Sources"]
    Overture["Overture"]
  end

  TM -- "Training Data" --> FAIR
  UMap -- "Training Data Outside HOT Ecosystem" --> FAIR
  FAIR -- "Validation of Model Output" --> MapSwipe
  MapSwipe -- "Re-training of AI Model" --> FAIR
  TM --> Sandbox
  OtherSources --> TM
  Overture --> TM
  FAIR -- "Final Model Predictions" --> TM
  TM -- "Final Output Validation (Optional)" --> MapSwipe
  TM -- "Conflation UI" --> Rapid
  TM -- "No Imagery, fAIr Feature / Generation Not Possible" --> TM
  OSM --> TM
```

## Block Model Diagram

![block-model](./images/hot-tools-block-model.png)

## Overall Architecture

![detailed-e2e](./images/hot-components-model.png)

## Old HOT Ecosystem Digram (2023)

![Basic E2E Diagram](./techdoc/overview/HOTInformationFlow.png)
