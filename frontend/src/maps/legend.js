export function initializeLegend(map, sidebar) {
  // Create a panel for the legend in the sidebar
  const legendPanelContent = {
    id: "map-legend-panel",
    tab: '<i class="fa fa-list"></i>',
    pane: '<div id="map-legend-content"></div>',
    title: "Legend",
    position: "top",
  };

  // Add the panel to the sidebar
  sidebar.addPanel(legendPanelContent);

  // Function to update the legend based on active overlays
  async function updateLegend() {
    const legendContent = document.getElementById("map-legend-content");
    if (!legendContent) {
      console.error("Legend content not found");
      return;
    }

    legendContent.innerHTML = ""; // Clear current legends

    // Array to hold promises for each layer's legend
    let legendPromises = [];

    // Loop through each layer in the map
    map.eachLayer(function (layer) {
      // Check if the layer is an overlay and is currently added to the map
      if (map.hasLayer(layer) && layer.options.isOverlayLegend) {
        // Push the promise returned by getLayerLegend into the array
        legendPromises.push(getLayerLegend(layer));
      }
    });

    // Wait for all promises to resolve
    const legends = await Promise.all(legendPromises);

    // Append each resolved legend HTML to the content
    legends.forEach((legendHtml) => {
      if (legendHtml) {
        legendContent.innerHTML += legendHtml;
      }
    });

    // Show or hide the panel based on whether there is legend content
    if (legends.some((legendHtml) => legendHtml)) {
      sidebar.enablePanel("map-legend-panel");
    } else {
      sidebar.disablePanel("map-legend-panel");
    }
  }

  // Listen for when a layer is added or removed
  map.on("overlayadd overlayremove", function (event) {
    updateLegend();
  });

  // Initial legend update
  updateLegend();
}

// Function to get the legend HTML for a specific layer
async function getLayerLegend(layer) {
  // For debugging purposes, log the entire layer object
  console.log(layer);

  // Attempt to get the layer's name from the label property or use a default name
  var layerName = layer.options.label ? layer.options.label : "Unnamed Layer";

  // Return the legend HTML with the layer's name
  // Ensure ESRIformatLegend is an async function or returns a Promise
  var html = await ESRIformatLegend(
    layer.options.url,
    layerName,
    layer.options.layers
  );
  console.log(html);
  return html;
}

async function ESRIformatLegend(serverUrl, layerName, layers) {
  try {
    // Fetch the legend data from the ArcGIS REST server
    const response = await fetch(`${serverUrl}/legend?f=pjson`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    // Filter layers based on the provided layers array
    const filteredLayers = data.layers.filter((layer) =>
      layers.includes(layer.layerId)
    );

    // Generate HTML for each layer's legend
    let html = `<div class="legend"><h3 id="sidebar-h3">${layerName}</h3><div id="legend-layer-container">`;

    filteredLayers.forEach((layer) => {
      html += `<div class="layer"><h4 id="sidebar-h4">${layer.layerName}</h4>`;
      layer.legend.forEach((item) => {
        const label = item.label || layer.layerName;
        const imageData = `data:${item.contentType};base64,${item.imageData}`;
        html += `<div class="legend-item"><img src="${imageData}" alt="${label}"/><span>${label}</span></div>`;
      });
      html += "</div>"; // Close the layer div
    });

    html += "</div></div>"; // Close the legend-layer-container and legend divs
    return html;
  } catch (error) {
    console.error("Error fetching or processing the legend:", error);
    return '<div class="error">Error loading legend</div>';
  }
}
