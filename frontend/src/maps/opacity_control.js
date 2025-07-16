import "../css/opacity_controls.css";

export function createSlider(layer, name) {
  const sliderContainer = document.createElement("div");
  sliderContainer.className = "opacity-slider";

  // Get the current opacity of the layer
  const currentOpacity = layer.getOpacity();

  sliderContainer.innerHTML = `
    <label>${name}</label>
    <input type="range" min="0" max="1" step="0.1" value="${currentOpacity}" class="custom-slider">
  `;

  // Append the slider to the leaflet_opacity_control div
  document
    .getElementById("leaflet_opacity_control")
    .appendChild(sliderContainer);

  const slider = sliderContainer.querySelector("input");

  // Focus the slider
  slider.focus();

  slider.addEventListener("input", function () {
    const opacity = parseFloat(this.value);
    layer.setOpacity(opacity);
  });
}

// Function to setup layer control and event listeners
export function setupOppacityLayerControl(map, overlayLayers) {
  // Listen for overlayadd and overlayremove events
  map.on("overlayadd", function (eventLayer) {
    createSlider(eventLayer.layer, eventLayer.layer.options.label);
    console.log(eventLayer.layer.options.label);
  });

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
