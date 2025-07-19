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
  attribution: `<a href="https://regobs.no/">NVE &amp; Varsom RegObs</a>`,
  isOverlayLegend: true,
  LegendContent: `<h3 id="sidebar-h3" style="display: flex; align-items: center; justify-content: space-between;">
  Run-out Area
  <a href="https://regobs.no/?hazard=10&daysBack=2&orderBy=changeTime&regions=3003" target="_blank" rel="noopener noreferrer" style="margin-left: 10px;">
    <img src="/partner_logos/Varsom_Logo_RGB.svg" alt="Logo" style="width: 55px; height: 55px;">
  </a>
</h3><div class="layer">
  <div class="legend-item">
    <img
      src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAL0lEQVQ4jWNhoDJgoZ2Bviv+U2TS5ghGVAOpBEYNHDVw1MBRA+ltILQ8o56BVAIAYfAEXe1mu6MAAAAASUVORK5CYII="
      alt="2"
    /><span>Short runouts (50% of the avalanches reach farther)</span>
  </div>
  <div class="legend-item">
    <img
      src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAMUlEQVQ4jWNhoDJgoZmBPrP//6fEoC2pjIwoBlILjBo4auCogaMG0tlAWHlGNQOpBQARfQVswO3xygAAAABJRU5ErkJggg=="
      alt="2"
    /><span>Medium runouts (25% of the avalanches reach farther)</span>
  </div>
  <div class="legend-item">
    <img
      src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAMUlEQVQ4jWNhoDJgoZmBszY++0+JQWn+UowoBlILjBo4auCogaMG0tlAWHlGNQOpBQD3PwUhIVtc9gAAAABJRU5ErkJggg=="
      alt="2"
    /><span
      >Long runouts (5% of the avalanches reach farther) - Some avalanches may
      have longer runouts than displayed as runout zones in the map.</span
    >
  </div>
</div>`,
});

var nve_steepness_slope = dynamicMapLayer({
  url: "https://gis3.nve.no/arcgis/rest/services/wmts/Bratthet_med_utlop_2024/MapServer",
  layers: [6],
  label: "Slope Steepness",
  attribution: `<a href="https://regobs.no/">NVE &amp; Varsom RegObs</a>`,
  isOverlayLegend: true,
  LegendContent: `<h3 id="sidebar-h3" style="display: flex; align-items: center; justify-content: space-between;">
  Avalanche Slope Steepness
  <a href="https://regobs.no/?hazard=10&daysBack=2&orderBy=changeTime&regions=3003" target="_blank" rel="noopener noreferrer" style="margin-left: 10px;">
    <img src="/partner_logos/Varsom_Logo_RGB.svg" alt="Logo" style="width: 55px; height: 55px;">
  </a>
</h3>
<div class="legend-item">
  <img
    src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAMUlEQVQ4jWNhoDJgoZmB//8z/KfEIEZGBkYUA6kFRg0cNXDUwFED6WwgrDyjmoHUAgAJMQNUcB1RQwAAAABJRU5ErkJggg=="
    alt="2"
  /><span>30°-35°</span>
</div>
<div class="legend-item">
  <img
    src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAMUlEQVQ4jWNhoDJgoZmB/1cx/KfEIMYwBkYUA6kFRg0cNXDUwFED6WwgrDyjmoHUAgAmaQOpc7oJQgAAAABJRU5ErkJggg=="
    alt="3"
  /><span>35°-40°</span>
</div>
<div class="legend-item">
  <img
    src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAMUlEQVQ4jWNhoDJgoZmB/0MZ/lNiEONqBkYUA6kFRg0cNXDUwFED6WwgrDyjmoHUAgBDoQP+WgjkigAAAABJRU5ErkJggg=="
    alt="4"
  /><span>40°-45°</span>
</div>
<div class="legend-item">
  <img
    src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAMUlEQVQ4jWNhoDJgoZmB/xkY/lNiECMDAyOKgdQCowaOGjhq4KiBdDYQVp5RzUBqAQBgfwJTXu298gAAAABJRU5ErkJggg=="
    alt="5"
  /><span>45°-50°</span>
</div>
<div class="legend-item">
  <img
    src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAMUlEQVQ4jWNhoDJgoZmBxQwM/ykxqJeBgRHFQGqBUQNHDRw1cNRAOhsIK8+oZiC1AACRKwLf7sQuVQAAAABJRU5ErkJggg=="
    alt="6"
  /><span>&lt;50°</span>
</div>`,
});

//Boat Regulation Layer
var miljo_landing_location = dynamicMapLayer({
  url: "https://kart2.miljodirektoratet.no/arcgis/rest/services/svalbard/ilandstigningslokaliteter_svalbard/MapServer",
  layers: [0, 1, 2, 3],
  attribution: "Miljødirektoratet",
  label: "Landing location in tourism activities",
  isOverlayLegend: true,
  LegendContent: "esri",
});

var miljo_speed_bird_cliffs = dynamicMapLayer({
  url: "https://kart2.miljodirektoratet.no/arcgis/rest/services/svalbard/motorferdsel_svalbard/MapServer",
  layers: [0],
  attribution: "Miljødirektoratet",
  label: "Speed restriction in from of birds cliffs",
  isOverlayLegend: true,
  LegendContent: "esri",
});

//Snowscooter traffic Regulation Layers
var miljo_snoscooter_resident = dynamicMapLayer({
  url: "https://kart2.miljodirektoratet.no/arcgis/rest/services/svalbard/motorferdsel_svalbard/MapServer",
  layers: [1, 3],
  attribution: "Miljødirektoratet",
  label: "Motor Traffic regulation for residents",
  isOverlayLegend: true,
  LegendContent: "esri",
});

var miljo_snoscooter_tourists = dynamicMapLayer({
  url: "https://kart2.miljodirektoratet.no/arcgis/rest/services/svalbard/motorferdsel_svalbard/MapServer",
  layers: [2, 4],
  attribution: "Miljødirektoratet",
  label: "Motor Traffic regulation for travelers / tourism",
  isOverlayLegend: true,
  LegendContent: "esri",
});

//Regulations
var np_natural_reserve = dynamicMapLayer({
  url: "https://geodata.npolar.no/arcgis/rest/services/Temadata/N_Nature_Reserves_Svalbard/MapServer",
  layers: [0, 1, 3],
  attribution: "Norsk Polarinstitutt",
  label: "Natural Reserves",
  isOverlayLegend: true,
  LegendContent: "esri",
});

var np_traffic_regulations = dynamicMapLayer({
  url: "https://geodata.npolar.no/arcgis/rest/services/Temadata/Transportation_Svalbard/MapServer",
  layers: [4],
  label: "Traffic regulations",
  isOverlayLegend: true,
  LegendContent: "esri",
});

var overlaysLayers = [
  {
    label: "Avalanche",
    collapsed: true,
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
    collapsed: true,
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
    collapsed: true,
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
    collapsed: true,
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
