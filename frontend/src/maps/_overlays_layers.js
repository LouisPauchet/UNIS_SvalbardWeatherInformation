import L from "leaflet";
import { tiledMapLayer, dynamicMapLayer } from "esri-leaflet";

// Avalanche Layers
// var nve_runout_area = L.tileLayer(
//   "https://gis3.nve.no/arcgis/rest/services/wmts/Bratthet_med_utlop_2024/MapServer/WMTS?" +
//     "&REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0" +
//     "&STYLE=default" +
//     "&TILEMATRIXSET=GoogleMapsCompatible" +
//     "&FORMAT=image/png" +
//     "&LAYER=wmts_Bratthet_med_utlop_2024" +
//     "&TILEMATRIX={z}" +
//     "&TILEROW={y}" +
//     "&TILECOL={x}",
//   {
//     minZoom: 0,
//     maxZoom: 15,
//     attribution: "Norwegian Water Resources and Energy Directorate",
//     tileSize: 256,
//   }
// );

var nve_runout_area = dynamicMapLayer({
  url: "https://gis3.nve.no/arcgis/rest/services/wmts/Bratthet_med_utlop_2024/MapServer",
  layers: [7, 8, 9],
});

var nve_steepness_slope = dynamicMapLayer({
  url: "https://gis3.nve.no/arcgis/rest/services/wmts/Bratthet_med_utlop_2024/MapServer",
  layers: [6],
});

var overlaysLayers = [
  {
    label: "Avalanche",
    children: [
      {
        label: "Run Out Area",
        layer: nve_runout_area,
      },
      {
        label: "Slope Steepness",
        layer: nve_steepness_slope,
      },
    ],
  },
];

export { overlaysLayers };
