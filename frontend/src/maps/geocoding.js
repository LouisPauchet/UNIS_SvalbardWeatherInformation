import "../css/geocoding.css";
// searchHandler.js

export async function fetchSuggestions(query) {
  const response = await fetch(
    `https://api.npolar.no/placename/?q-name.@value=${query}&filter-area=Svalbard&filter-status=official&not-terrain.nn=utmål|verneområde&format=geojson&fields=id,type,geometry,name,area,terrain,terrain_type&limit=10`
  );
  const data = await response.json();
  return data.features.map((feature) => feature.name["@value"]);
}

export function displaySuggestions(
  suggestions,
  suggestionsContainer,
  searchInput
) {
  suggestionsContainer.innerHTML = "";
  suggestions.forEach((suggestion) => {
    const div = document.createElement("div");
    div.textContent = suggestion;
    div.addEventListener("click", () => {
      searchInput.value = suggestion;
      suggestionsContainer.style.display = "none";
    });
    suggestionsContainer.appendChild(div);
  });
  suggestionsContainer.style.display = "block";
}

export function initializeGeocodingSearchBar(inputId, suggestionsContainerId) {
  const searchInput = document.getElementById(inputId);
  const suggestionsContainer = document.getElementById(suggestionsContainerId);

  console.log(searchInput); // Should log the input element
  console.log(suggestionsContainer); // Should log the suggestions div

  searchInput.addEventListener("input", async () => {
    const query = searchInput.value.trim();
    if (query.length > 2) {
      const suggestions = await fetchSuggestions(query);
      console.log(suggestions); // Should log the array of suggestions
      displaySuggestions(suggestions, suggestionsContainer, searchInput);
    } else {
      suggestionsContainer.style.display = "none";
    }
  });
}
