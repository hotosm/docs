# End-to-End Overview

This is an overview of the proposed end-to-end workflow that ties together all of
HOT's tools.

Outcome: to enable communities to generate their own maps for their area of interest
(neighbourhood, city, region), rich in data derived from local knowledge.

## Requirements

- A project owner / coordinator who can pull all of the pieces together.
- Users in the area of interest with drones, and willing to produce imagery.
  - This has typically been a barrier, but with decent cheap consumer drones
    being available now, the opportunity to produce high-resolution base imagery
    has opened up.
- A small team of digitisers, who use TM to generate a traning dataset for AI
  models.
  - This could feasibly be remote, but ideally local for better knowledge of
    what the reality is on the ground.
- A group of local people who can verify features on the ground, adding tags to them
  with their local knowledge, via an easy to fill out mobile survey.

## Methodology (Diagram)

## Methodology (Description)

> 🚧 denotes 'blockers' or unknowns in the current workflow.

### 1. Collect Drone Imagery

- Fly drones in grids to collect imagery for the entire area.
- This will use Drone Aerial Tasking Manager (DATM), if it comes to fruition.

🚧 If DATM succeeds.

### 2. Process a Base Map & Upload to OAM

- Get the imagery from the drones, and preprocess on a drive using EXIF info.
- Use Node Open Drone Map (NodeODM) to merge into an mosaic.
- Upload the mosaic to OAM.
- A TMS URL is generated for you.

### 3. Digitise Features in Tasking Manager

- Load the OAM imagery as a TMS into Tasking Manager.
- Use a sandboxed version of TM for producing training data.
- Only map a small sample area that is representative of the entire area.

🚧 We need an instance of TM isolated from OSM, so we don't mess with existing data.
Alternatively we need a way to bulk delete geoms via iD Editor.

### 4. Generate a Model Using fAIr

- Load the mapped features into fAIr and generate a model.
- Use the model to predict the remaining features in the area.

### 5. Validate Predicted Features in TM

- Load the predicted features back into a TM project.
  - fAIr allows for feedback to be given to the model, but this cannot be done
    **collaboratively**.
- Collaboratively split the geoms as needed, and provide feedback on the generated
  geoms.

🚧 We should assess if we need this step, or the input from a single experienced
validator directly in fAIr would be good enough.

🚧 Can iD Editor be used to split buildings nicely? Is this a good workflow?

### 6. Process Final Features in fAIr

- Load the corrected features in fAIr.
- The data could be used to re-train the model.
  - This process of fAIr-->TM-->fAIr could be done multiple times.
- Output the final validated features as a GeoJSON.

### 7. Input Into FMTM

- Now we have validated, AI-generated features for an area, they can be field
  validated and tagged.

  > Note the features are not yet in OSM, as they will be field validated first.

- As part of a field (mobile) survey, the features will be validated and tagged with
  useful information.
- The final validated and tagged geometries will be bulk uploaded to OSM.

### 8. Extract from OpenSreetMap

- Now final validation from FMTM is uploaded to OpenStreetMap , Now we need to download them in useful fileformats that we want 
- This will be achieved with HOT Export Tool which allows us to export the data we created in different file formats including ( Shpaefile , Geojson , KML , CSV , Flatgeobuff and manymore ) 

🚧 A way to feed validation failures back to TM for re-digitisation would be great.
