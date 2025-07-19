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

//Avalanche Layers
var nve_runout_area = dynamicMapLayer({
  url: "https://gis3.nve.no/arcgis/rest/services/wmts/Bratthet_med_utlop_2024/MapServer",
  layers: [7, 8, 9],
  label: "Run-out Area",
});

var nve_steepness_slope = dynamicMapLayer({
  url: "https://gis3.nve.no/arcgis/rest/services/wmts/Bratthet_med_utlop_2024/MapServer",
  layers: [6],
  label: "Slope Steepness",
});

//Boat Regulation Layer
var miljo_landing_location = dynamicMapLayer({
  url: "https://kart2.miljodirektoratet.no/arcgis/rest/services/svalbard/ilandstigningslokaliteter_svalbard/MapServer",
  layers: [0, 1, 2, 3],
  label: "Landing location in tourism activities",
});

var miljo_speed_bird_cliffs = dynamicMapLayer({
  url: "https://kart2.miljodirektoratet.no/arcgis/rest/services/svalbard/motorferdsel_svalbard/MapServer",
  layers: [0],
  label: "Speed restriction in from of birds cliffs",
});

//Snowscooter traffic Regulation Layers
var miljo_snoscooter_resident = dynamicMapLayer({
  url: "https://kart2.miljodirektoratet.no/arcgis/rest/services/svalbard/motorferdsel_svalbard/MapServer",
  layers: [1, 3],
  label: "Motor Traffic regulation for residents",
});

var miljo_snoscooter_tourists = dynamicMapLayer({
  url: "https://kart2.miljodirektoratet.no/arcgis/rest/services/svalbard/motorferdsel_svalbard/MapServer",
  layers: [2, 4],
  label: "Motor Traffic regulation for travelers / tourism",
});

//Regulations
var np_natural_reserve = dynamicMapLayer({
  url: "https://geodata.npolar.no/arcgis/rest/services/Temadata/N_Nature_Reserves_Svalbard/MapServer",
  layers: [0, 1, 3],
  label: "Natural Reserves",
});

var np_traffic_regulations = dynamicMapLayer({
  url: "https://geodata.npolar.no/arcgis/rest/services/Temadata/Transportation_Svalbard/MapServer",
  layers: [4],
  label: "Traffic regulations",
});

var overlaysLayers = [
  {
    label: "Avalanche",
    children: [
      // nve_runout_area,
      // nve_steepness_slope,
      {
        label: "Run-out Area",
        layer: nve_runout_area,
      },
      {
        label: "Slope Steepness",
        layer: nve_steepness_slope,
      },
    ],
  },
  {
    label: "Boat Regulation",
    children: [
      {
        label: "Landing location in tourism activities",
        layer: miljo_landing_location,
      },
      {
        label: "Speed restriction in from of birds cliffs",
        layer: miljo_speed_bird_cliffs,
      },
    ],
  },
  {
    label: "Snow Scooter Regulation",
    children: [
      {
        label: "Motor Traffic regulation for residents",
        layer: miljo_snoscooter_resident,
      },
      {
        label: "Motor Traffic regulation for travelers / tourism",
        layer: miljo_snoscooter_tourists,
      },
    ],
  },
  {
    label: "Regulation",
    children: [
      {
        label: "Natural Reserves",
        layer: np_natural_reserve,
      },
      {
        label: "Traffic regulations",
        layer: np_traffic_regulations,
      },
    ],
  },
];

// Initialize an empty dictionary
var layerDictionary = {};

// Iterate over each item in overlaysLayers
overlaysLayers.forEach(function (item) {
  // Check if the item has children
  if (item.children) {
    // Iterate over each child
    item.children.forEach(function (child) {
      // Check if the child has a layer and a label
      if (child.layer && child.label) {
        // Add an entry to the dictionary
        layerDictionary[child.label] = child.layer.name;
      }
    });
  }
});

export { overlaysLayers, layerDictionary };
