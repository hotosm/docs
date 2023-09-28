# Frontend Modularization

## Shared UI Components

Consistent styling and component functionality across all of our projects.

Currently in design and prototype stage,
but will be rolled out for all projects eventually.

[link](https://hotosm.github.io/shared-ui-components)

## Shared Map Components

Map components using OpenLayers underneath.

Currently in design and prototype stage,
but will be rolled out for all projects eventually.

Will likely use PlanetLab's [Maps](https://github.com/planetlabs/maps)
at it's core, with fleshed out higher level components:

- Layer switcher
- Attribute table
- Various layer types

The plan would be to support various cloud optimised geo data formats:

- COG
- flatgeobuf
- GeoParquet
- PMTiles

There is also the possibility of designing this with [Svelte](https://svelte.dev/),
then embedding the compiled plain JS into our React apps (in discussion).

[link](https://hotosm.github.io/shared-map-components)
