import "../css/geocoding.css";
import L from "leaflet";

/**
 * Fetches place information from the Norwegian Polar Institute API based on the provided ID.
 * @param {string} id - The ID of the place to fetch information for.
 * @returns {Promise<Object>} - A promise that resolves to the place information data.
 */
async function fetchPlaceInformation(id) {
  const response = await fetch(
    `https://v2-api.npolar.no/placename/feature/${id}`
  );
  const data = await response.json();
  return data;
}

/**
 * Displays place information on the map and in the information div.
 * @param {string} name - The name of the place.
 * @param {string} id - The ID of the place.
 * @param {Object} map - The Leaflet map object.
 */
async function displayPlaceInformation(name, id, map) {
  const placeInformationDiv = document.getElementById(
    "geocoding-place-information"
  );
  const data = await fetchPlaceInformation(id);
  const [longitude, latitude] = data.geometry.coordinates;
  console.log([longitude, latitude]);
  console.log(map);

  // Add a marker to the map if coordinates are available
  if (latitude && longitude) {
    const marker = L.marker([latitude, longitude]).addTo(map);
    map.setView([latitude, longitude], map.getZoom()); // Center the map on the marker
    marker.bindPopup(`<b>${name}</b>`).openPopup();
  }

  let previousNamesHTML = "<p>No previous names found.</p>";
  if (data.replaces && data.replaces.length > 0) {
    const previousNamesData = await Promise.all(
      data.replaces.map((replace) => fetchPlaceInformation(replace["@id"]))
    );
    previousNamesHTML = `
      <table id="geocoding-informations-table">
        <thead>
          <tr>
            <th>Previous Name</th>
            <th>Used in</th>
          </tr>
        </thead>
        <tbody>
          ${data.replaces
            .map(
              (replace, index) => `
              <tr onclick="window.open('https://placenames.npolar.no/${replace["@id"]}', '_blank')" style="cursor:pointer;">
                <td>${replace.name}</td>
                <td>${previousNamesData[index].beginLifespanVersion}</td>
              </tr>
              `
            )
            .join("")}
        </tbody>
      </table>
    `;
  }

  placeInformationDiv.innerHTML = `
    <div id="geocoding-informations-header">
      <div id="geocoding-informations-text">
        <h2 id="sidebar-h2">${name}</h2>
        <p id="geocoding-informations-lifespan">Since ${data.beginLifespanVersion}</p>
      </div>
      <div id="geocoding-informations-logo">
        <a href="https://www.npolar.no" target="_blank">
          <img src="/partner_logos/npolar.svg" alt="Norwegian Polar Institute Logo" style="width: 90px; height: auto;">
        </a>
      </div>
    </div>
    <p id="geocoding-informations-definition">${data.definition.en}</p>
    <h3 id="sidebar-h3">Origin (en)</h3>
    <p id="geocoding-informations-origin">${data.origin.en}</p>
    <h3 id="sidebar-h3">Previous Names</h3>
    <div id="geocoding-informations-previous-names">${previousNamesHTML}</div>
  `;
}

// searchHandler.js

/**
 * Fetches place name suggestions from the Norwegian Polar Institute API based on the provided query.
 * @param {string} query - The search query for place names.
 * @returns {Promise<Array<Object>>} - A promise that resolves to an array of place name suggestions.
 */
export async function fetchSuggestions(query) {
  const response = await fetch(
    `https://api.npolar.no/placename/?q-name.@value=${query}&filter-area=Svalbard&filter-status=official&not-terrain.nn=utmål|verneområde&format=geojson&fields=id,type,geometry,name,area,terrain,terrain_type&limit=10`
  );
  const data = await response.json();
  return data.features.map((feature) => ({
    name: feature.name["@value"],
    id: feature.id,
  }));
}

/**
 * Displays suggestions in the suggestions container and handles user interactions.
 * @param {Array<Object>} suggestions - An array of suggestion objects.
 * @param {HTMLElement} suggestionsContainer - The container element to display suggestions in.
 * @param {HTMLElement} searchInput - The search input element.
 * @param {Object} map - The Leaflet map object.
 */
export function displaySuggestions(
  suggestions,
  suggestionsContainer,
  searchInput,
  map
) {
  suggestionsContainer.innerHTML = "";
  let selectedSuggestionIndex = -1; // No suggestion selected initially

  suggestions.forEach((suggestion, index) => {
    const div = document.createElement("div");
    div.textContent = suggestion.name;
    div.dataset.id = suggestion.id; // Store the ID in a data attribute
    div.addEventListener("click", () => {
      displayPlaceInformation(suggestion.name, suggestion.id, map);
      searchInput.value = "";
      suggestionsContainer.style.display = "none";
    });
    suggestionsContainer.appendChild(div);
  });

  // Handle keyboard navigation
  searchInput.addEventListener("keydown", (event) => {
    const suggestions = suggestionsContainer.querySelectorAll("div");
    if (suggestions.length === 0) {
      return;
    }
    switch (event.key) {
      case "ArrowDown":
        event.preventDefault();
        selectedSuggestionIndex =
          (selectedSuggestionIndex + 1) % suggestions.length;
        updateSuggestionsHighlight(suggestions, selectedSuggestionIndex);
        break;
      case "ArrowUp":
        event.preventDefault();
        selectedSuggestionIndex =
          (selectedSuggestionIndex - 1 + suggestions.length) %
          suggestions.length;
        updateSuggestionsHighlight(suggestions, selectedSuggestionIndex);
        break;
      case "Enter":
        if (selectedSuggestionIndex >= 0) {
          const selectedSuggestion = suggestions[selectedSuggestionIndex];
          displayPlaceInformation(
            selectedSuggestion.textContent,
            selectedSuggestion.dataset.id,
            map
          );
          searchInput.value = "";
          suggestionsContainer.style.display = "none";
        }
        break;
    }
  });

  suggestionsContainer.style.display = "block";

  /**
   * Updates the highlight of suggestions based on the selected index.
   * @param {NodeList} suggestions - The list of suggestion elements.
   * @param {number} selectedIndex - The index of the selected suggestion.
   */
  function updateSuggestionsHighlight(suggestions, selectedIndex) {
    suggestions.forEach((suggestion, index) => {
      if (index === selectedIndex) {
        suggestion.classList.add("selected");
      } else {
        suggestion.classList.remove("selected");
      }
    });
  }
}

/**
 * Initializes the geocoding search bar with event listeners for input and suggestion display.
 * @param {string} inputId - The ID of the search input element.
 * @param {string} suggestionsContainerId - The ID of the suggestions container element.
 * @param {Object} map - The Leaflet map object.
 */
export function initializeGeocodingSearchBar(
  inputId,
  suggestionsContainerId,
  map
) {
  const searchInput = document.getElementById(inputId);
  const suggestionsContainer = document.getElementById(suggestionsContainerId);

  searchInput.addEventListener("input", async () => {
    const query = searchInput.value.trim();
    if (query.length > 2) {
      const suggestions = await fetchSuggestions(query);
      displaySuggestions(suggestions, suggestionsContainer, searchInput, map);
    } else {
      suggestionsContainer.style.display = "none";
    }
  });
}
