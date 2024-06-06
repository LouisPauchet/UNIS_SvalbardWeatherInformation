let trackLayers = {};
let boatMarkers = {};
let windMarkers = {};
let mobileStations = {};

function loadStations(mobileStationConfigUrl, windImagesUrl) {
    fetch(mobileStationConfigUrl)
        .then(response => response.json())
        .then(stations => {
            mobileStations = stations;
            const projectControls = document.getElementById('project-controls');
            const projects = {};

            stations.forEach(station => {
                const project = station.project || 'Uncategorized';
                if (!projects[project]) {
                    projects[project] = [];
                }
                projects[project].push(station);
            });

            for (const project in projects) {
                const projectDiv = document.createElement('div');
                const projectLabel = document.createElement('label');
                projectLabel.textContent = project;
                projectDiv.appendChild(projectLabel);

                projects[project].forEach(station => {
                    const stationDiv = document.createElement('div');
                    const stationCheckbox = document.createElement('input');
                    stationCheckbox.type = 'checkbox';
                    stationCheckbox.id = `station-${station.id}`;
                    stationCheckbox.checked = true;
                    stationCheckbox.addEventListener('change', () => {
                        toggleStation(station.id, stationCheckbox.checked, windImagesUrl);
                    });

                    const stationLabel = document.createElement('label');
                    stationLabel.setAttribute('for', `station-${station.id}`);
                    stationLabel.textContent = station.name;

                    stationDiv.appendChild(stationCheckbox);
                    stationDiv.appendChild(stationLabel);
                    projectDiv.appendChild(stationDiv);
                });

                projectControls.appendChild(projectDiv);
            }

            const durationSelect = document.getElementById('track-duration-select');
            const variableSelect = document.getElementById('variable-select-dropdown');
            
            durationSelect.addEventListener('change', () => {
                const duration = parseInt(durationSelect.value, 10);
                const variable = variableSelect.value;
                mobileStations.forEach(station => {
                    updateMobileStationData(station, duration, windImagesUrl, variable);
                });
            });

            variableSelect.addEventListener('change', () => {
                const duration = parseInt(durationSelect.value, 10);
                const variable = variableSelect.value;
                mobileStations.forEach(station => {
                    updateMobileStationData(station, duration, windImagesUrl, variable);
                });
            });

            // Initial load with default duration (1 hour) and variable (none)
            const initialDuration = parseInt(durationSelect.value, 10);
            const initialVariable = variableSelect.value;
            mobileStations.forEach(station => {
                updateMobileStationData(station, initialDuration, windImagesUrl, initialVariable);
            });
        });
}

function fetchMobileStationData(station, duration, variable) {
    return fetch(`/api/mobile-station-data/${station.id}?duration=${duration}&variable=${variable}`)
        .then(response => response.json());
}

function toggleStation(stationId, isVisible, windImagesUrl) {
    if (!isVisible) {
        if (trackLayers[stationId]) {
            trackLayers[stationId].forEach(layer => map.removeLayer(layer));
            delete trackLayers[stationId];
        }
        if (boatMarkers[stationId]) {
            map.removeLayer(boatMarkers[stationId]);
            delete boatMarkers[stationId];
        }
        if (windMarkers[stationId]) {
            map.removeLayer(windMarkers[stationId]);
            delete windMarkers[stationId];
        }
    } else {
        const durationSelect = document.getElementById('track-duration-select');
        const variableSelect = document.getElementById('variable-select-dropdown');
        const duration = parseInt(durationSelect.value, 10);
        const variable = variableSelect.value;

        const station = mobileStations.find(s => s.id === stationId);
        updateMobileStationData(station, duration, windImagesUrl, variable);
    }
}

function updateMobileStationData(station, duration, windImagesUrl, variable) {
    if (trackLayers[station.id]) {
        trackLayers[station.id].forEach(layer => map.removeLayer(layer));
        delete trackLayers[station.id];
    }

    if (duration === 0) {
        // No track to display, but show the boat icon
        fetchMobileStationData(station, duration, variable)
            .then(data => {
                updateBoatMarker(station.id, data, variable);
                updateWindMarker(station.id, data, windImagesUrl);
            });
        return;
    }

    fetchMobileStationData(station, duration, variable)
        .then(data => {
            updateBoatMarker(station.id, data, variable);
            updateWindMarker(station.id, data, windImagesUrl);

            const latlngs = data.track.map(dp => [dp.lat, dp.lon]);
            const values = data.track.map(dp => dp.variable);
            const minValue = Math.min(...values);
            const maxValue = Math.max(...values);
            const extendedMinValue = minValue - (0.1 * minValue);
            const extendedMaxValue = maxValue + (0.1 * maxValue);

            const colorScale = getColorScale(variable, extendedMinValue, extendedMaxValue);

            let segments = [];
            for (let i = 0; i < latlngs.length - 1; i++) {
                const segment = L.polyline([latlngs[i], latlngs[i + 1]], {
                    color: colorScale(values[i]),
                    weight: 5,
                    opacity: 0.7
                }).addTo(map);
                segments.push(segment);

                // Add popups to each point
                L.circleMarker(latlngs[i], {
                    radius: 5,
                    color: colorScale(values[i]),
                    fillColor: colorScale(values[i]),
                    fillOpacity: 0.9
                })
                .bindPopup(createPopupContent(station.name, data.track[i]))
                .addTo(map);
            }

            // Add popup to the last point
            L.circleMarker(latlngs[latlngs.length - 1], {
                radius: 5,
                color: colorScale(values[latlngs.length - 1]),
                fillColor: colorScale(values[latlngs.length - 1]),
                fillOpacity: 0.9
            })
            .bindPopup(createPopupContent(station.name, data.track[latlngs.length - 1]))
            .addTo(map);

            trackLayers[station.id] = segments;
            updateColorBar(variable, extendedMinValue, extendedMaxValue);
        });
}

function createPopupContent(stationName, dataPoint) {
    const date = new Date(dataPoint.time * 1000);
    const dateString = `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;
    const windDirectionLetter = getWindDirectionLetter(dataPoint.windDirection);

    return `
        <strong>Boat: ${stationName}</strong><br>
        Time: ${dateString}<br>
        Air Temperature: ${dataPoint.airTemperature ? dataPoint.airTemperature.toFixed(2) : 'N/A'} °C<br>
        Sea Surface Temperature: ${dataPoint.seaSurfaceTemperature ? dataPoint.seaSurfaceTemperature.toFixed(2) : 'N/A'} °C<br>
        Wind Speed: ${dataPoint.windSpeed ? dataPoint.windSpeed.toFixed(2) : 'N/A'} m/s<br>
        Wind Direction: ${dataPoint.windDirection ? `${dataPoint.windDirection.toFixed(2)}° (${windDirectionLetter})` : 'N/A'}<br>
        Relative Humidity: ${dataPoint.relativeHumidity ? dataPoint.relativeHumidity.toFixed(2) : 'N/A'} %
    `;
}

function getWindDirectionLetter(degrees) {
    const directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
    const index = Math.round(degrees / 45) % 8;
    return directions[index];
}

function updateBoatMarker(stationId, data, variable) {
    const boatIconUrl = '/static/images/boat_icon.png';
    const boatIcon = L.icon({
        iconUrl: boatIconUrl,
        iconSize: [32, 32],
        iconAnchor: [16, 16]
    });

    if (boatMarkers[stationId]) {
        map.removeLayer(boatMarkers[stationId]);
    }

    const variableInfo = variable !== 'none' && data.variable !== null ? `<br>${variable}: ${data.variable}` : '';
    const boatMarker = L.marker([data.lat, data.lon], { icon: boatIcon }).addTo(map);
    boatMarker.bindPopup(`Boat: ${stationId}<br>Wind Speed: ${data.windSpeed} kts<br>Wind Direction: ${data.windDirection}°${variableInfo}`);
    boatMarkers[stationId] = boatMarker;
}

function updateWindMarker(stationId, data, windImagesUrl) {
    const iconUrl = getWindSpeedIcon(windImagesUrl, data.windSpeed);
    const windIcon = L.icon({
        iconUrl: iconUrl,
        iconSize: [32, 32],
        iconAnchor: [16, 16]
    });

    if (windMarkers[stationId]) {
        map.removeLayer(windMarkers[stationId]);
    }

    const windMarker = L.marker([data.lat, data.lon], { icon: windIcon }).addTo(map);
    windMarker.bindPopup(`Wind Speed: ${data.windSpeed} kts<br>Wind Direction: ${data.windDirection}°`);
    windMarkers[stationId] = windMarker;
}

function getWindSpeedIcon(basePath, windSpeed) {
    const windSpeeds = [0, 5, 10, 15, 20, 25, 30, 35, 50, 55, 60, 65, 100, 105];
    let closest = windSpeeds.reduce((prev, curr) => Math.abs(curr - windSpeed) < Math.abs(prev - windSpeed) ? curr : prev);
    return `${basePath}/${closest.toString().padStart(2, '0')}kts.gif`;
}

function getColorScale(variable, minValue, maxValue) {
    const colorScale = {
        "airTemperature": d3.scaleSequential(d3.interpolateCool).domain([minValue, maxValue]),
        "seaSurfaceTemperature": d3.scaleSequential(d3.interpolateCool).domain([minValue, maxValue]),
        "windSpeed": d3.scaleSequential(d3.interpolateBlues).domain([minValue, maxValue]),
        "windDirection": d3.scaleSequential(d3.interpolateRainbow).domain([minValue, maxValue]),
        "relativeHumidity": d3.scaleSequential(d3.interpolateViridis).domain([minValue, maxValue])
    };

    return colorScale[variable];
}