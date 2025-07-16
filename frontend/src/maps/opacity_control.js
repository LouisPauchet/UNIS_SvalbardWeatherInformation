import "../css/opacity_controls.css";

/**
 * @fileoverview This module provides functionality to create and manage opacity sliders for map layers.
 * It allows users to adjust the opacity of individual layers dynamically.
 */

/**
 * @external Layer
 * @see See {@link https://leafletjs.com/reference-1.7.1.html#layer|Leaflet Layer documentation}
 */

/**
 * Creates a slider for adjusting the opacity of a map layer.
 * @param {external:Layer} layer - The map layer to which the slider will be attached.
 * @param {string} name - The name or label of the layer to be displayed alongside the slider.
 */
export function createSlider(layer, name) {
  const sliderContainer = document.createElement("div");
  sliderContainer.className = "opacity-slider";

  // Get the current opacity of the layer
  const currentOpacity = layer.getOpacity();

  // Set the HTML content of the slider container
  sliderContainer.innerHTML = `
    <label>${name}</label>
    <input type="range" min="0" max="1" step="0.1" value="${currentOpacity}" class="custom-slider">
  `;

  // Append the slider to the designated container in the DOM
  document
    .getElementById("leaflet_opacity_control")
    .appendChild(sliderContainer);

  const slider = sliderContainer.querySelector("input");

  // Focus the slider for immediate user interaction
  slider.focus();

  // Add an event listener to update the layer's opacity as the slider value changes
  slider.addEventListener("input", function () {
    const opacity = parseFloat(this.value);
    layer.setOpacity(opacity);
  });
}

/**
 * Sets up the opacity control for map layers, including event listeners for adding and removing layers.
 * @param {object} map - The map object to which the opacity controls will be applied.
 * @param {object} overlayLayers - The overlay layers that will have opacity controls.
 */
export function setupOppacityLayerControl(map, overlayLayers) {
  // Listen for overlayadd events to create a slider when a layer is added
  map.on("overlayadd", function (eventLayer) {
    createSlider(eventLayer.layer, eventLayer.layer.options.label);
    console.log(eventLayer.layer.options.label);
  });

  // Listen for overlayremove events to remove the corresponding slider when a layer is removed
  map.on("overlayremove", function (eventLayer) {
    const sliders = document.querySelectorAll(".opacity-slider");
    sliders.forEach(function (slider) {
      if (
        slider
          .querySelector("label")
          .textContent.startsWith(eventLayer.layer.options.label)
      ) {
        slider.remove();
      }
    });
  });
}
