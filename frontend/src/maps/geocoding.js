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
  let selectedSuggestionIndex = -1; // No suggestion selected initially

  searchInput.addEventListener("input", async () => {
    const query = searchInput.value.trim();
    if (query.length > 2) {
      const suggestions = await fetchSuggestions(query);
      displaySuggestions(suggestions, suggestionsContainer, searchInput);
      selectedSuggestionIndex = -1; // Reset selection on new input
    } else {
      suggestionsContainer.style.display = "none";
    }
  });

  searchInput.addEventListener("keydown", (event) => {
    const suggestions = suggestionsContainer.querySelectorAll("div");
    if (suggestions.length === 0) {
      return;
    }

    switch (event.key) {
      case "ArrowDown":
        event.preventDefault(); // Prevent cursor move in the input
        selectedSuggestionIndex =
          (selectedSuggestionIndex + 1) % suggestions.length;
        updateSuggestionsHighlight(suggestions, selectedSuggestionIndex);
        break;
      case "ArrowUp":
        event.preventDefault(); // Prevent cursor move in the input
        selectedSuggestionIndex =
          (selectedSuggestionIndex - 1 + suggestions.length) %
          suggestions.length;
        updateSuggestionsHighlight(suggestions, selectedSuggestionIndex);
        break;
      case "Enter":
        if (selectedSuggestionIndex >= 0) {
          searchInput.value = suggestions[selectedSuggestionIndex].textContent;
          suggestionsContainer.style.display = "none";
        }
        break;
    }
  });

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
