import L from "leaflet";
import { tiledMapLayer, dynamicMapLayer } from "esri-leaflet";

var minimap_layer = tiledMapLayer({
  url: "https://geodata.npolar.no/arcgis/rest/services/Basisdata/NP_Basiskart_Svalbard_WMTS_3857/MapServer",
});

// var np_toposvalbard = L.tileLayer(
//   "https://geodata.npolar.no/arcgis/rest/services/Basisdata/NP_Basiskart_Svalbard_WMTS_3857/MapServer/WMTS?" +
//     "&REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0" +
//     "&STYLE=default" +
//     "&TILEMATRIXSET=GoogleMapsCompatible" +
//     "&FORMAT=image/jpeg" +
//     "&LAYER=Basisdata_NP_Basiskart_Svalbard_WMTS_3857" +
//     "&TILEMATRIX={z}" +
//     "&TILEROW={y}" +
//     "&TILECOL={x}",
//   {
//     minZoom: 0,
//     maxZoom: 15,
//     attribution: "Norwegian Polar Institute",
//     tileSize: 256,
//   }
// );

var np_toposvalbard = L.layerGroup([
  tiledMapLayer({
    url: "https://geodata.npolar.no/arcgis/rest/services/Basisdata/NP_Basiskart_Svalbard_WMTS_3857/MapServer",
  }),
  tiledMapLayer({
    url: "https://geodata.npolar.no/arcgis/rest/services/Basisdata/FKB_Svalbard_WMTS_3857/MapServer",
    minZoom: 14,
  }),
]);

// var np_orthophoto = L.tileLayer(
//   "https://geodata.npolar.no/arcgis/rest/services/Basisdata/NP_Ortofoto_Svalbard_WMTS_3857/MapServer/WMTS?" +
//     "&REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0" +
//     "&STYLE=default" +
//     "&TILEMATRIXSET=GoogleMapsCompatible" +
//     "&FORMAT=image/jpeg" +
//     "&LAYER=Basisdata_NP_Ortofoto_Svalbard_WMTS_3857" +
//     "&TILEMATRIX={z}" +
//     "&TILEROW={y}" +
//     "&TILECOL={x}",
//   {
//     minZoom: 0,
//     maxZoom: 17,
//     attribution: "Norwegian Polar Institute",
//     tileSize: 256,
//   }
// );

var np_orthophoto = tiledMapLayer({
  url: "https://geodata.npolar.no/arcgis/rest/services/Basisdata/NP_Ortofoto_Svalbard_WMTS_3857/MapServer",
});

// var kartverket_sea_chart = L.tileLayer(
//   "https://cache.kartverket.no/v1/wmts?" +
//     "SERVICE=WMTS" +
//     "&VERSION=1.0.0" +
//     "&REQUEST=GetTile" +
//     "&LAYER=sjokartraster" +
//     "&STYLE=default" +
//     "&FORMAT=image/png" +
//     "&TILEMATRIXSET=utm33n" +
//     "&TILEMATRIX={z}" +
//     "&TILEROW={y}" +
//     "&TILECOL={x}",
//   {
//     minZoom: 0,
//     maxZoom: 17,
//     attribution: "Kartverket - Not For Navigation",
//     tileSize: 256,
//   }
// );

var kartverket_sea_chart = L.tileLayer.wms(
  "https://wms.geonorge.no/skwms1/wms.sjokartraster2",
  {
    layers: "all",
    format: "image/png",
    transparent: true,
    version: "1.3.0",
    crs: L.CRS.EPSG3857,
    attribution:
      'Sjøkartraster by Kartverket <br> <span style="color: red;">Not For Navigation</span>',
  }
);
// var esri_worldimagery = L.tileLayer(
//   "https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/WMTS?" +
//     "&REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0" +
//     "&STYLE=default" +
//     "&TILEMATRIXSET=GoogleMapsCompatible" +
//     "&FORMAT=image/jpeg" +
//     "&LAYER=World_Imagery" +
//     "&TILEMATRIX={z}" +
//     "&TILEROW={y}" +
//     "&TILECOL={x}",
//   {
//     minZoom: 0,
//     maxZoom: 17,
//     attribution:
//       "Esri, Maxar, Earthstar Geographics, and the GIS User Community",
//     tileSize: 256,
//   }
// );

var esri_worldimagery = tiledMapLayer({
  url: "https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer",
});

var baseMaps = [
  {
    label: "Topographie",
    children: [
      { label: "Topo Svalbard", layer: np_toposvalbard },
      { label: "Nautical Chart", layer: kartverket_sea_chart },
    ],
  },
  {
    label: "Imagery",
    children: [
      { label: "NP OrthoPhoto", layer: np_orthophoto },
      { label: "ESRI WorldImagery", layer: esri_worldimagery },
    ],
  },
];

let base_layer_default = np_toposvalbard;

export { baseMaps, base_layer_default, minimap_layer };
