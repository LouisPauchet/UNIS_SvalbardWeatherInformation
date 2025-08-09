import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from source.logger.logger import Logger
from source.configHandler.confighandler import ConfigHandler
from source.datasource.FrostSource import FrostSource
from source.datasource.IWINFixedSource import IWINFixedSource
from source.datasource.FrostBoatSource import FrostBoatSource

# Mapping dictionary for supported data sources
DATASOURCE_MAPPING = {
    "FrostSource": FrostSource,
    "FrostBoatSource" : FrostBoatSource,
    "IWINFixedSource": IWINFixedSource
}


def get_datasource(station_id, config=None):
    """
    Factory function to return the appropriate DataSource instance based on station_id.

    Args:
        station_id (str): The ID of the station.

    Returns:
        DataSource: An instance of the correct subclass.
    """
    logger = Logger.setup_logger("get_datasource")
    config = ConfigHandler()

    logger.debug(f"Fetching metadata for station_id: {station_id}")
    station = config.get_metadata(station_id)
    #print(station)
    # Get the datasource name from metadata
    source_name = station.get('datasource', None)
    type = station.get('type', 'fixed')

    # Validate the datasource
    if source_name not in DATASOURCE_MAPPING:
        #print(type)
        if type == 'mobile':
            logger.info(f"Unknown datasource '{source_name}' for station_id {station_id}, defaulting to FrostBoatSource.")
            source_name = "FrostBoatSource"
        else:
            logger.info(f"Unknown datasource '{source_name}' for station_id {station_id}, defaulting to FrostSource.")
            source_name = "FrostSource"
        

    logger.debug(f"Datasource identified for {station_id}: {source_name}")

    # Get the actual class from the mapping dictionary
    source_class = DATASOURCE_MAPPING[source_name]

    logger.debug(f"Fetching API Key for: {source_name}")
    # Get API credentials for this datasource
    api_key = config.get_api_credential(source_name)

    # logger.debug(f"Key to be passed : {api_key}")


    return source_class(api_key=api_key)
