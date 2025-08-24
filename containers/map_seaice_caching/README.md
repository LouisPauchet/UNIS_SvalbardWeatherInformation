# Sea Ice Map Caching Container

This container is designed to fetch the latest sea ice chart from the Norwegian Meteorological Institute (https://cryo.met.no/en/latest-ice-charts) and trigger a GeoWebCache cleanup using a truncate task.

### Environment Variables

To establish a connection with GeoServer, the following environment variables must be configured:

| Variable                     | Description                                      |
| ---------------------------- | ------------------------------------------------ |
| `SWI-GEOSERVER-URL`          | URL of the GeoServer instance                    |
| `SWI-GEOSERVER-USERNAME`     | Username for GeoServer authentication            |
| `SWI-GEOSERVER-PWD`          | Password for GeoServer authentication            |
| `SWI-SEAICE-LAYER-FILE-NAME` | Name of the output shapefile (default: `latest`) |

### Output

The generated shapefile will be saved in `/swi/export`. Ensure this directory is mapped to the corresponding storage location on GeoServer.
