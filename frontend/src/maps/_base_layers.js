import L from "leaflet";
import { tiledMapLayer } from "esri-leaflet";

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

var np_toposvalbard = tiledMapLayer({
  url: "https://geodata.npolar.no/arcgis/rest/services/Basisdata/NP_Basiskart_Svalbard_WMTS_3857/MapServer",
});

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
    label: "Topo",
    children: [{ label: "NP Topography", layer: np_toposvalbard }],
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
