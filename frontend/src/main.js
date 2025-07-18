import "leaflet/dist/leaflet.css";
import "leaflet.control.layers.tree/L.Control.Layers.Tree.css";
import "leaflet-minimap/dist/Control.MiniMap.min.css";
import "leaflet-sidebar-v2/css/leaflet-sidebar.min.css";
import "./css/layer_side_bar.css";
import "./css/sidebar.css";

import L from "leaflet";
import { baseMaps, base_layer_default } from "./maps/_base_layers";
import { overlaysLayers } from "./maps/_overlays_layers";
import "leaflet-minimap";
import "leaflet.control.layers.tree";
import "leaflet-sidebar-v2";
import { setupOppacityLayerControl } from "./maps/opacity_control";
import { initializeGeocodingSearchBar } from "./maps/geocoding";

let map;

document.addEventListener("DOMContentLoaded", () => {
  map = L.map("map", {
    center: [78.2, 15.6],
    zoom: 10,
    layers: [base_layer_default],
  });

  map.zoomControl.setPosition("topright");
  L.control.scale({ position: "bottomright" }).addTo(map);

  var layerControl = L.control.layers
    .tree(baseMaps, overlaysLayers, {
      namedToggle: true,
      collapsed: false,
      selectorBack: true,
      openedSymbol: '<i class="fas fa-caret-down"></i>',
      closedSymbol: '<i class="fas fa-caret-left"></i>',
      spaceSymbol: "",
    })
    .collapseTree()
    .addTo(map);

  // var miniMap = new L.Control.MiniMap(minimap_layer, {
  //   toggleDisplay: true,
  //   minimized: false,
  //   position: "bottomleft",
  // }).addTo(map);

  // create the sidebar instance and add it to the map
  var sidebar = L.control
    .sidebar({ container: "sidebar" })
    .addTo(map)
    .open("home");

  setupOppacityLayerControl(map, overlaysLayers);

  initializeGeocodingSearchBar(
    "geocoding-search-input",
    "geocoding-search-bar-suggestions",
    map
  );

  document
    .querySelector("div.leaflet-control-layers-base")
    ?.insertAdjacentHTML(
      "beforebegin",
      '<div><h3 id="sidebar-h3">Base Layers</h3></div>'
    );

  document
    .querySelector("div.leaflet-control-layers-overlays")
    ?.insertAdjacentHTML(
      "beforebegin",
      '<div><h3 id="sidebar-h3">Overlay Layers</h3></div>'
    );

  document
    .getElementById("leaflet_layer_control")
    .appendChild(layerControl.getContainer());
});
