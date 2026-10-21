# Share Results On A Map (uMap)

Most HOT tools let you download data. Share it with communities or partners
on a [uMap](https://umap.hotosm.org): a shareable web map. No GIS skills needed.

A typical map has three parts:

| Layer         | Where it comes from                           | Format         |
| ------------- | --------------------------------------------- | -------------- |
| Your data     | ChatMap, Field-TM, or any other GeoJSON / CSV | GeoJSON        |
| Context (OSM) | Export Tool: roads, buildings, health sites…  | GeoJSON        |
| Background    | OpenAerialMap imagery, or a standard OSM map  | Tile URL (XYZ) |

## 1. Get your data out

- **ChatMap:** open the exported chat in
  [ChatMap](https://chatmap.hotosm.org), remove any points you don't want
  to share, then click **Download** to get a GeoJSON file.
- **Field-TM:** download the project submissions from the project page.
- **OSM data for context:** in the
  [Export Tool](https://export.hotosm.org), draw your area, pick only the
  feature types you need (e.g. health facilities, main roads) and choose
  GeoJSON. Keep layers small: uMap gets slow with tens of thousands of
  features.

## 2. Create the map and import the data

1. Log in to [umap.hotosm.org](https://umap.hotosm.org) and create a map.
2. Click **Import data** and import each GeoJSON file into its own layer
   so viewers can switch layers on and off.
3. Set each layer's name, colour and icon in its properties.
4. Set what appears in the popup when someone clicks a point (e.g. the
   ChatMap message and photo).

## 3. Add imagery as the background (optional)

Recent drone or satellite imagery from OpenAerialMap makes a map much
easier for a community to recognise.

1. Find the image in the
   [OAM catalogue](https://api.imagery.hotosm.org/browser/) and copy its
   item ID.
2. Build the tile URL (see
   [Using imagery](https://docs.imagery.hotosm.org/usage/using-imagery/)):

   ```text
   https://api.imagery.hotosm.org/raster/collections/openaerialmap/items/{item_id}/tiles/WebMercatorQuad/{z}/{x}/{y}?assets=visual
   ```

3. In uMap's map settings, open **Custom background**, paste the URL into
   the URL template and add the image credit in the attribution field.

## 4. Share it

Save the map, check its permissions (who can view and edit), then share
the link or embed it in a website.

## Need more info?

- uMap: [uMap documentation](https://docs.umap-project.org)
- ChatMap: [ChatMap docs](https://github.com/hotosm/chatmap/tree/master/docs)
- Imagery URLs: [OAM: using imagery](https://docs.imagery.hotosm.org/usage/using-imagery/)
