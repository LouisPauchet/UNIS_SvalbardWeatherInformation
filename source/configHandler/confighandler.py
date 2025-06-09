import json
from source.logger.logger import Logger
import difflib
import os


config_files = [
    'static/config/fixed_stations.json',
    'static/config/mobile_stations.json'
]

variable_config_file = 'static/config/variables.json'

class StationNotFoundError(Exception):
    """
    Exception raised when a station is not found in the configuration files.
    """
    def __init__(self, station_id, suggestions=None):
        message = f"Station ID '{station_id}' not found."
        if suggestions:
            message += f" Did you mean: {', '.join(suggestions)}?"
        super().__init__(message)
        self.station_id = station_id
        self.suggestions = suggestions


class ConfigHandler:
    """
    A handler for managing configuration files and providing station-specific data.

    Attributes:
        config_files (list): List of file paths to configuration JSON files.
        _cached_configs (list or None): Cached configuration data, loaded once and reused.
        logger (logging.Logger): Logger instance for logging actions and errors.
    """

    def __init__(self, variable_config_file=variable_config_file):
        """
        Initialize the ConfigHandler with default configuration files and logger.
        """
        self.config_files = config_files
        self.variables_config_file = variable_config_file
        self.variable_config = None
        self._cached_configs = None
        self._cached_credential = None
        self.logger = Logger.setup_logger(self.__class__.__name__)
        self._env_variable_mapping = self._load_env_variable_mapping()
        self._load_var_config()

    def get_variable(self, station_id):
        """
        Fetch a mapping of variable identifiers for a specific station.

        Args:
            station_id (str): The ID of the station.

        Returns:
            dict: Mapping of variable element IDs to names, or None if not found.

        Raises:
            ValueError: If `station_id` is not provided.
        """
        if not station_id:
            raise ValueError("station_id must be provided")

        configs = self._load_config()
        for config in configs:
            if config.get("id") == station_id:
                return config.get("variables", None)

        suggestions = difflib.get_close_matches(
            station_id,
            [config.get("id") for config in configs if "id" in config],
            n=3, cutoff=0.6)
        raise StationNotFoundError(station_id, suggestions)

    def get_metadata(self, station_id):
        """
        Fetch metadata for a specific station.

        Args:
            station_id (str): The ID of the station.

        Returns:
            dict: Metadata for the station, or None if not found.

        Raises:
            ValueError: If `station_id` is not provided.
        """
        if not station_id:
            raise ValueError("station_id must be provided")

        configs = self._load_config()
        for config in configs:
            if config.get("id") == station_id:
                if "datasource" not in config:
                    #config["datasource"] = "FrostDatasource"
                    pass
                return config
        return None

    def get_stations(self, type="all"):
        """
        Get a list of station IDs based on the specified type.

        Args:
            type (str): Type of stations to fetch. Options are:
                - "all": Return all station IDs.
                - "mobile": Return IDs of mobile stations.
                - "fixed": Return IDs of fixed stations.

        Returns:
            list: List of station IDs matching the specified type.

        Raises:
            AssertionError: If `type` is not one of ["all", "mobile", "fixed"].
        """
        assert type in ["all", "mobile", "fixed"], \
            "Type must be one of ['all', 'mobile', 'fixed']"

        configs = self._load_config()
        stations = []
        for config in configs:
            if type == "all" or config.get("type") == type:
                stations.append(config.get("id"))
        return stations

    def _load_var_config(self):
        """
        Loads and caches variable configuration from a JSON file.

        If the configuration is already cached, it returns the cached version.
        Otherwise, it reads and parses the JSON file, augmenting each entry with an 'id'
        field corresponding to its key. Handles file and JSON parsing errors.

        Returns:
            dict: The variable configuration data with each entry containing an 'id' field.
        """
        if self.variable_config is not None:
            return self.variable_config

        try:
            with open(self.variables_config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)['variables']
            
            for key in data.keys():
                data[key]['id'] = key

            self.variable_config = data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self._handle_error(e)



    def _load_config(self):
        """
        Load configurations from a list of JSON files.

        Each configuration dictionary is augmented with a 'station_type'
        field. If the configuration contains the key 'mobile', the station_type
        is set to 'mobile'; otherwise it defaults to 'fixed'.

        Returns:
            list: A combined list of configuration dictionaries from all files.

        Notes:
            - Caches the configuration data to avoid repeated file I/O.
            - Logs and handles errors such as missing files or invalid JSON.

        Raises:
            FileNotFoundError: If a configuration file is not found.
            json.JSONDecodeError: If a configuration file contains invalid JSON.
        """
        if self._cached_configs is not None:
            return self._cached_configs

        configs = []
        for file in self.config_files:
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    # Ensure we have a list of config dictionaries
                    config_list = data if isinstance(data, list) else [data]
                    for config in config_list:
                        # Add station type: if the config contains the key 'mobile',
                        # mark it as 'mobile', otherwise default to 'fixed'
                        if 'mobile' in file:
                            config['type'] = 'mobile'
                        else:
                            config['type'] = 'fixed'
                    configs.extend(config_list)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                self._handle_error(e)

        self._cached_configs = configs
        return configs
    

    def _load_env_variable_mapping(self):
        env_config_file = 'private/example_api.json'
        try:
            with open(env_config_file, 'r') as f:
                data = json.load(f)
                return {item["datasource"]: item["api_key"] for item in data}
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger = Logger.setup_logger("ConfigHandler")
            logger.error(f"Error loading environment variable mapping: {e}")
            return {}

    def get_api_credential(self, datasource: str) -> str | None:
        """
        Retrieve API credentials for a given datasource.

        Args:
            datasource (str): The name of the datasource to retrieve credentials for.

        Returns:
            str or None: The API key if found, otherwise None.
        """
        logger = Logger.setup_logger("ConfigHandler")
        config_file = 'private/api.json'

        # Check environment variables first
        if datasource in self._env_variable_mapping:
            env_var_name = self._env_variable_mapping[datasource]
            api_key = os.getenv(env_var_name)
            if api_key:
                logger.info(f"API key retrieved from environment variable for datasource: {datasource}")
                return api_key
            else:
                logger.info(f"No API key found in environment variable for datasource: {datasource}")

        # Return cached credentials if available
        if self._cached_credential is not None:
            api_key = self._cached_credential.get(datasource)
            if api_key:
                logger.info(f"Using cached API key for datasource: {datasource}")
            else:
                logger.info(f"No API key required for datasource: {datasource} (cached).")
            return api_key

        # Load and parse the configuration file
        try:
            with open(config_file, 'r') as f:
                data = json.load(f)
                configs = data if isinstance(data, list) else [data]
        except FileNotFoundError:
            logger.error(f"API credential file '{config_file}' not found.")
            return None
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON in '{config_file}'.")
            return None
        except IOError as e:
            logger.error(f"Error reading file '{config_file}': {e}")
            return None

        # Store loaded configs in cache
        self._cached_configs = configs

        # Extract credentials and cache them
        self._cached_credential = {
            item["datasource"]: item.get("api_key")
            for item in configs if "datasource" in item
        }

        api_key = self._cached_credential.get(datasource)
        if api_key:
            logger.info(f"API key retrieved successfully for datasource: {datasource}")
        else:
            logger.info(f"No API key required for datasource: {datasource}.")

        return api_key
    def _handle_error(self, error):
        """
        Log and handle errors that occur during configuration loading or data fetching.

        Args:
            error (Exception): The exception that occurred.
        """
        self.logger.error(f"Error occurred: {error}")
