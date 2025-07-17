import "../css/geocoding.css";

async function fetchPlaceInformation(id) {
  const response = await fetch(
    `https://v2-api.npolar.no/placename/feature/${id}`
  );
  const data = await response.json();
  return data;
}

async function displayPlaceInformation(name, id) {
  const placeInformationDiv = document.getElementById(
    "geocoding-place-information"
  );
  const data = await fetchPlaceInformation(id);

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
    <h2 id="sidebar-h2">${name}</h2>
    <p id="geocoding-informations-lifespan">Since ${data.beginLifespanVersion}</p>
    <p id="geocoding-informations-definition">${data.definition.en}</p>
    <h3 id="sidebar-h3">Origin (en)</h3>
    <p id="geocoding-informations-origin">${data.origin.en}</p>
    <h3 id="sidebar-h3">Previous Names</h3>
    <div id="geocoding-informations-previous-names">${previousNamesHTML}</div>
  `;
}

// searchHandler.js
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

export function displaySuggestions(
  suggestions,
  suggestionsContainer,
  searchInput
) {
  suggestionsContainer.innerHTML = "";
  let selectedSuggestionIndex = -1; // No suggestion selected initially

  suggestions.forEach((suggestion, index) => {
    const div = document.createElement("div");
    div.textContent = suggestion.name;
    div.dataset.id = suggestion.id; // Store the ID in a data attribute

    div.addEventListener("click", () => {
      displayPlaceInformation(suggestion.name, suggestion.id);
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
            selectedSuggestion.dataset.id
          );
          searchInput.value = "";
          suggestionsContainer.style.display = "none";
        }
        break;
    }
  });

  suggestionsContainer.style.display = "block";

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

export function initializeGeocodingSearchBar(inputId, suggestionsContainerId) {
  const searchInput = document.getElementById(inputId);
  const suggestionsContainer = document.getElementById(suggestionsContainerId);

  searchInput.addEventListener("input", async () => {
    const query = searchInput.value.trim();
    if (query.length > 2) {
      const suggestions = await fetchSuggestions(query);
      displaySuggestions(suggestions, suggestionsContainer, searchInput);
    } else {
      suggestionsContainer.style.display = "none";
    }
  });
}
