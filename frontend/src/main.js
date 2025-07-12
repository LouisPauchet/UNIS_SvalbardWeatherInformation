import L from "leaflet";
import { baseMaps, base_layer_default } from "./maps/_base_layers";
import { overlaysLayers } from "./maps/_overlays_layers";
import "leaflet-minimap";
import "leaflet.control.layers.tree";
import "leaflet-sidebar-v2";

import "leaflet/dist/leaflet.css";
import "leaflet.control.layers.tree/L.Control.Layers.Tree.css";
import "leaflet-minimap/dist/Control.MiniMap.min.css";
import "leaflet-sidebar-v2/css/leaflet-sidebar.min.css";

document.addEventListener("DOMContentLoaded", () => {
  var map = L.map("map", {
    center: [78.2, 15.6],
    zoom: 10,
    layers: [base_layer_default],
  });

  L.control.scale().addTo(map);

  var layerControl = L.control.layers
    .tree(baseMaps, overlaysLayers, {
      namedToggle: true,
      collapseAll: "Collapse all",
      expandAll: "Expand all",
      collapsed: false,
    })
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

  // add panels dynamically to the sidebar
  sidebar
    .addPanel({
      id: "js-api",
      tab: '<i class="fa fa-gear"></i>',
      title: "JS API",
      pane: '<p>The Javascript API allows to dynamically create or modify the panel state.<p/><p><button onclick="sidebar.enablePanel(\'mail\')">enable mails panel</button><button onclick="sidebar.disablePanel(\'mail\')">disable mails panel</button></p><p><button onclick="addUser()">add user</button></b>',
    })
    // add a tab with a click callback, initially disabled
    .addPanel({
      id: "mail",
      tab: '<i class="fa fa-envelope"></i>',
      title: "Messages",
      button: function () {
        alert("opened via JS callback");
      },
      disabled: true,
    });

  // be notified when a panel is opened
  sidebar.on("content", function (ev) {
    switch (ev.id) {
      case "autopan":
        sidebar.options.autopan = true;
        break;
      default:
        sidebar.options.autopan = false;
    }
  });

  var userid = 0;
  function addUser() {
    sidebar.addPanel({
      id: "user" + userid++,
      tab: '<i class="fa fa-user"></i>',
      title: "User Profile " + userid,
      pane: "<p>user ipsum dolor sit amet</p>",
    });
  }
});
