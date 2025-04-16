# Frontend Modularization

## Shared UI Components

Consistent styling and component functionality across all of our projects.

Currently in design and prototype stage,
but will be rolled out for all projects eventually.

[link](https://github.com/hotosm/ui)

## Shared Map Components

We are contributing to and building out the
[svelte-maplibre](https://github.com/dimfeld/svelte-maplibre)
package.

This is built around MapLibre, with a goal to export the components
to standard web components (custom elements) that could be embedded
into any frontend framework.

This would allow for a consistent declarative API for a web map
library to be integrated into our tools.

The plan would be to support various cloud optimised geo data formats:

- COG
- flatgeobuf
- GeoParquet
- PMTiles

## QR Codes

[Reads and decodes](https://github.com/hotosm/qrcodes) base64 and zlib
encoded JSON data within a QRCode in Javascript
