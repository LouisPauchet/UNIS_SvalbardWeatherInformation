import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from source.configHandler.confighandler import ConfigHandler
from source.datasource.datasourceFactory import get_datasource

from source.logger.logger import Logger

import json
from datetime import datetime, timedelta
import shutil

class CacheHandler:
    def __init__(self, directory='./cache/', path_config = None, cleaning_list = None, serve_only = False):
        """
            Initialize a CacheHandler instance to manage caching of station data.

            Args:
                directory (str): The base directory where cache files are stored.
                    Default is './cache/'.
                path_config (dict, optional): A dictionary mapping cache entry names to file paths.
                    If None, defaults to:
                        {
                            'station_status': 'cache_stations_status.json',
                            'station_metadata_single': './000_stations_metadata/',
                            'realtime_data': './111_data_realtime/',
                            'hourly_data' : './111_hourly_data/',
                            'online': './000_status_online_stations/',
                            'offline': './000_status_offline_stations/',
                        }
                cleaning_list (list, optional): A list of cache entry keys to be cleared during cache operations.
                    Default is ['online', 'offline'].

            Returns:
                None
        """
        self.directory = directory
        self.logger = Logger.setup_logger("CacheHandler")
        self.config = ConfigHandler()
        self.online_stations = []
        os.makedirs(self.directory, exist_ok=True)

        if path_config is None:
            self.path_config = {
                'station_status' : 'cache_stations_status.json',
                'station_metadata_single' : './000_stations_metadata/',
                'realtime_data' : './111_data_realtime/',
                'hourly_data': './111_hourly_data/',
                'online' : './000_status_online_stations/',
                'offline': './000_status_offline_stations/',
            }
        else:
            self.path_config = path_config

        if os.environ.get('SWI_INSTANCE_SERVE_ONLY') == 'true' or serve_only:
            self.serve_only = True
            self.logger.info("This instance is in SERVE ONLY mode.")
        else:
            self.serve_only = False
        
        

        if cleaning_list is None:
            self.cleaning_list = ['online', 'offline']
        else:
            self.cleaning_list = cleaning_list

    def cache_stations_status(self):
        """
        Retrieve and cache the status and metadata for all stations.

        This method iterates over all available stations, checks if they are online, retrieves their metadata and available
        variables, and compiles a status report with a timestamp for each station. The resulting list of station states is
        written to a JSON cache file. Additionally, it clears specific cache entries as defined by the cleaning list.

        Args:
            None

        Returns:
            list: A list of dictionaries, each containing station information such as id, name, type, location, variables,
                  status (online/offline), last_updated timestamp, project, and icon.
        """
        self.logger.info("Starting to cache station statuses...")
        if self.serve_only:
            self.logger.info("This instance is in SERVE ONLY mode. Skipping Caching")
            return -1

        stations = self.config.get_stations(type="all")
        self.logger.info(f"Retrieved {len(stations)} stations for processing.")

        state = []

        for station_id in stations:
            try:
                self.logger.debug(f"Processing station status for: {station_id}")
                datasource = get_datasource(station_id,  config=self.config)
                is_online = datasource.is_station_online(station_id)
                self.logger.debug(f"Station {station_id} online status: {'online' if is_online else 'offline'}")

                if is_online:
                    self.online_stations.append(station_id)

                metadata = self.config.get_metadata(station_id) or {}
                variables = self.config.get_variable(station_id)
                timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

                infos = {
                    "id": station_id,
                    "name": metadata.get("name", "Unknown"),
                    "type": metadata.get("type", "Unknown"),
                    "location": {
                        "lat": metadata.get("lat", None),
                        "lon": metadata.get("lon", None),
                    },
                    "variables": list(variables.keys()) if variables else [],
                    "status": "online" if is_online else "offline",
                    "last_updated": timestamp or "Unknown",
                    "project" : metadata.get("project", "Unknown"),
                    "icon" : metadata.get("icon", "/static/images/red_dot.png"),
                }

                state.append(infos)
                self.logger.info(f"Successfully processed station {station_id}")

            except Exception as e:
                self.logger.error(f"Error processing station {station_id}: {e}", exc_info=True)

        self.logger.info(f"Finished caching station statuses. Total stations processed: {len(state)}")

        self._write_cache(state, self.path_config.get('station_status', 'cache_stations_status.json'))

        self._clear_cache(self.cleaning_list)

        return state

    def cache_realtime_data(self):
        """
        Retrieve and cache real-time data for online stations.

        This method fetches real-time data from each online station using the appropriate data source. If the list of online
        stations is not already populated, it calls cache_stations_status to update it. For each online station, the real-time
        data is written to a JSON file located in the path specified by the 'realtime_data' key in path_config.

        Args:
            None

        Returns:
            None
        """

        self.logger.info("Starting to cache realtime data...")

        if self.serve_only:
            self.logger.info("This instance is in SERVE ONLY mode. Skipping Caching")
            return -1

        realtime_data_path = self.path_config.get('realtime_data', '/realtime_data/')

        if self.online_stations is None or len(self.online_stations) == 0:
            self.logger.info("Unknown station status. Starting collection and caching of the station status...")
            self.cache_stations_status()


        if self.online_stations is None or len(self.online_stations) == 0:
            self.logger.warning("No online stations found. Skipping data caching.")
            return


        for station in self.online_stations:
            try:
                self.logger.debug(f"Fetching real-time data for station: {station}")
                datasource = get_datasource(station,  config=self.config)

                data = datasource.fetch_realtime_data(station)

                if not data:
                    self.logger.warning(f"No data fetched for {station}, skipping cache write.")
                    continue

                filename = os.path.join(realtime_data_path, f"{station}.json")

                self._write_cache(data, filename)

                self.logger.info(f"Saved real-time data for {station} at {filename}.")

            except Exception as e:
                self.logger.error(f"Error processing real-time data for {station}: {e}", exc_info=True)

        self.logger.info("Finished caching real-time data.")

    def cache_past_hourly_data(self, hours_ago=25):
        """
        Retrieve and cache hourly data for online stations.

        This method fetches hourly data from each online station using the appropriate data source. If the list of online
        stations is not already populated, it calls cache_stations_status to update it. For each online station, the hourly
        data is written to a JSON file located in a subdirectory specified by the 'hourly_data' key in path_config.

        Args:
            hours_ago (int): Number of hours ago to fetch data for. Default is 1.

        Returns:
            None
        """
        self.logger.info("Starting to cache hourly data...")

        if self.serve_only:
            self.logger.info("This instance is in SERVE ONLY mode. Skipping Caching")
            return -1

        hourly_data_path = self.path_config.get('hourly_data', '/hourly_data/')

        if self.online_stations is None or len(self.online_stations) == 0:
            self.logger.info("Unknown station status. Starting collection and caching of the station status...")
            self.cache_stations_status()

        if self.online_stations is None or len(self.online_stations) == 0:
            self.logger.warning("No online stations found. Skipping data caching.")
            return

        # Calculate the start and end times for the hourly data
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours_ago)

        for station in self.online_stations:
            try:
                self.logger.debug(f"Fetching hourly data for station: {station}")
                datasource = get_datasource(station, config=self.config)

                data = datasource.fetch_timeseries_data(
                    station,
                    start_time.isoformat(),
                    end_time.isoformat()
                )

                if not data or 'timeseries' not in data:
                    self.logger.warning(f"No data fetched for {station}, skipping cache write.")
                    continue

                # Create a subdirectory for each hourly shift
                for shift in range(1, hours_ago + 1):
                    shift_time = end_time - timedelta(hours=shift)
                    shift_path = os.path.join(hourly_data_path, f"-{shift}")
                    #os.makedirs(shift_path, exist_ok=True)

                    # Find the corresponding data entry for the shift
                    entry = next((e for e in data['timeseries'] if e['timestamp'].startswith(shift_time.isoformat()[:13])), None)
                    if entry:
                        # Prepare the data structure with a single record in timeseries
                        data_to_cache = {
                            "id": station,
                            "timeseries": [entry]
                        }
                        filename = os.path.join(shift_path, f"{station}.json")
                        self._write_cache(data_to_cache, filename)
                        self.logger.info(f"Saved hourly data for {station} at {filename}.")
                    else:
                        self.logger.warning(f"No data entry found for {station} at shift {shift}.")

            except Exception as e:
                self.logger.error(f"Error processing hourly data for {station}: {e}", exc_info=True)

        self.logger.info("Finished caching hourly data.")

    def get_cached_online_stations(self, type="all", status='online'):
        """
        Retrieve cached station information filtered by type and status.

        This method attempts to read a cache file containing stations filtered by the given status (online/offline). If the
        filtered cache file does not exist, it reads the complete station status cache, filters the data based on the provided
        station type and status, writes the filtered result to a new cache file, and returns the filtered data.

        Args:
            type (str): The station type to filter by. Use "all" to include stations of any type.
            status (str): The station status to filter by ('online' or 'offline').

        Returns:
            dict: A dictionary with a key (e.g., 'online_stations') mapping to a list of station dictionaries. Each station
                  dictionary includes keys: id, name, type, location, project, status, icon, and variables.
        """
        filename = os.path.join(self.path_config.get(status, '/status_online/'), f"{type}.json")

        cached_data = self._read_cache(filename)
        if cached_data is not None:
            return cached_data

        cached_stations = self._read_cache(self.path_config.get('station_status', 'cache_stations_status.json'))

        result_list = []
        for station in cached_stations:
            if station.get('status', 'offline') == status:
                if type == "all" or station.get('type') == type:
                    result_list.append(
                        {key: station[key] for key in ["id", "name", "type", "location", "project", "status", "icon", "variables"] if key in station}
                    )

        # result = {
        #     f"{status}_stations": result_list,
        # }

        result = result_list

        self._write_cache(result, filename)

        return result

    def get_cached_realtime_data(self, station_id):
        """
        Retrieve cached real-time data for a specific station.

        This method reads and returns the cached real-time data for the station with the provided station_id from the file
        specified by the 'realtime_data' path in path_config. If the file is missing or contains invalid data, appropriate
        warnings or error messages are logged.

        Args:
            station_id (str): The unique identifier of the station whose real-time data is to be retrieved.

        Returns:
            dict: A dictionary containing the station's real-time data if available.
            None: If no data is found or an error occurs.
        """
        self.logger.info(f"Fetching real-time data for station ID: {station_id}")
        try:
            realtime_data_path = self.path_config.get('realtime_data', '/realtime_data/')
            filename = os.path.join(realtime_data_path, f"{station_id}.json")

            cached_data = self._read_cache(filename)
            if cached_data is None:
                self.logger.warning(f"Cache file contains no valid data for station ID {station_id}")
            else:
                self.logger.info(f"Successfully retrieved cached data for station ID {station_id}")

            return cached_data

        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON format in cache file for station ID {station_id}: {e}", exc_info=True)
        except Exception as e:
            self.logger.critical(f"Unexpected error while fetching real-time data for station ID {station_id}: {e}",
                                 exc_info=True)

        return None

    def get_cached_hourly_data(self, station_id, shift):
        """
        Retrieve cached hourly data for a specific station and shift.

        This method reads and returns the cached hourly data for the station with the provided station_id and shift from
        the file specified by the 'hourly_data' path in path_config. If the shift is 0, it calls get_cached_realtime_data.
        If the file is missing or contains invalid data, appropriate warnings or error messages are logged.

        Args:
            station_id (str): The unique identifier of the station whose hourly data is to be retrieved.
            shift (int or str): The shift value indicating how many hours ago the data was cached.

        Returns:
            dict: A dictionary containing the station's hourly data if available.
            None: If no data is found or an error occurs.
        """
        self.logger.info(f"Fetching hourly data for station ID: {station_id} with shift: {shift}")

        try:
            # Convert shift to an integer if it's a string
            shift = int(shift)

            if shift == 0:
                return self.get_cached_realtime_data(station_id)

            hourly_data_path = self.path_config.get('hourly_data', '/hourly_data/')
            shift_path = os.path.join(hourly_data_path, f"{shift}")
            filename = os.path.join(shift_path, f"{station_id}.json")

            cached_data = self._read_cache(filename)
            if cached_data is None:
                self.logger.warning(f"Cache file contains no valid data for station ID {station_id} with shift {shift}")
            else:
                self.logger.info(f"Successfully retrieved cached data for station ID {station_id} with shift {shift}")

            return cached_data

        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON format in cache file for station ID {station_id} with shift {shift}: {e}", exc_info=True)
        except Exception as e:
            self.logger.critical(f"Unexpected error while fetching hourly data for station ID {station_id} with shift {shift}: {e}", exc_info=True)

        return None

    def get_cached_station_metadata(self, station_id):
        """
        Retrieve and cache metadata for a specific station.

        This method attempts to read a dedicated metadata file for the specified station from the path defined in
        'station_metadata_single'. If the file is not found, it retrieves the station's metadata from the overall station
        status cache, writes the metadata to the dedicated file, and returns the metadata.

        Args:
            station_id (str): The unique identifier of the station whose metadata is to be retrieved.

        Returns:
            dict: A dictionary containing the station's metadata, including keys such as name, type, location, project, and icon.
            None: If the metadata is not found or an error occurs.
        """
        self.logger.info(f"Fetching metadata for station ID: {station_id}")
        try:
            filename = os.path.join(self.path_config.get('station_metadata_single', 'stations_metadata'),
                                    f"{station_id}.json")
            cached_data = self._read_cache(filename)
            if cached_data is not None:
                return cached_data

            stations_metadata = self._read_cache(self.path_config.get('station_status', 'cache_stations_status.json'))
            if not stations_metadata:
                self.logger.warning("No station metadata found in cache.")
                return None

            for station in stations_metadata:
                if station.get('id') == station_id:
                    self._write_cache(station, filename)
                    return station

            self.logger.warning(f"Station ID {station_id} not found in metadata cache.")
            return None

        except Exception as e:
            self.logger.error(f"Unexpected error retrieving metadata for station {station_id}: {e}")
            return None


    def _clear_cache(self, entries):
        """
        Clear specified cache entries by deleting their corresponding files or directories.

        This private method iterates over the list of cache entry keys provided, retrieves each corresponding path from
        path_config, constructs the full path by joining with the base cache directory, and deletes the file or directory using
        the _delete_path method.

        Args:
            entries (list): A list of keys corresponding to cache entries to be cleared (e.g., ['online', 'offline']).

        Returns:
            None
        """

        self.logger.info(f"Starting cache clearing for {len(entries)} entries.")

        if self.serve_only:
            self.logger.info("This instance is in SERVE ONLY mode. Skipping Caching")
            return -1

        for entry in entries:
            file_path = self.path_config.get(entry)
            if file_path is None:
                self.logger.warning(f"No path configured for cache entry: {entry}")
                continue
            file_path = os.path.join(self.directory, file_path)

            if file_path:  # Ensure the path is valid
                self.logger.debug(f"Attempting to delete cache entry: {file_path}")
                self._delete_path(file_path)
            else:
                self.logger.warning(f"Invalid cache path for entry: {entry}")

        self.logger.info("Cache clearing completed.")


    def _write_cache(self, json_data, filename):
        """
        Write JSON-serializable data to a cache file.

        This private method constructs the full file path by combining the base cache directory with the provided filename,
        ensures that any necessary subdirectories exist, and writes the data as JSON to the file.

        Args:
            json_data (dict or list): The data to be written to the cache file in JSON format.
            filename (str): The relative path (including filename) where the data should be written.

        Returns:
            None
        """

        if self.serve_only:
            self.logger.info("This instance is in SERVE ONLY mode. Skipping Writing Data")
            return -1

        # Construct the full file path
        file_path = os.path.join(self.directory, filename)

        # Extract the directory path from the filename and ensure it exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(json_data, file, indent=4)
            self.logger.info(f"Cache written successfully to {file_path}")
        except Exception as e:
            self.logger.error(f"Error writing cache to {file_path}: {e}", exc_info=True)

    def _read_cache(self, struct):
        """
        Read and return JSON data from a cache file.

        This private method constructs the full file path by joining the base cache directory with the provided structure,
        attempts to read and parse the JSON data from the file, and returns it. If the file is not found or an error occurs,
        an appropriate message is logged and None is returned.

        Args:
            struct (str): The relative file path or structure identifier for the cache file to be read.

        Returns:
            dict or list: The JSON data from the cache file if successfully read.
            None: If the file is not found or an error occurs during reading.
        """
        file_path = os.path.join(self.directory, struct)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.logger.info(f"Cache read successfully from {file_path}")
                return data
        except FileNotFoundError:
            self.logger.warning(f"Cache file {file_path} not found.")
            return None
        except json.JSONDecodeError:
            self.logger.error(f"Error decoding JSON from {file_path}.")
            return None
        except Exception as e:
            self.logger.error(f"Error reading cache from {file_path}: {e}")
            return

    def _delete_path(self, path):
        """
        Delete the specified file or directory.

        This private method checks whether the provided path corresponds to a file or a directory. If it is a file, it
        is deleted using os.remove; if it is a directory, it is deleted recursively using shutil.rmtree. Appropriate log messages
        are recorded based on the outcome.

        Args:
            path (str): The path to the file or directory to be deleted.

        Returns:
            None
        """

        if self.serve_only:
            self.logger.info("This instance is in SERVE ONLY mode. Skipping Delete Path")
            return -1

        try:
            if os.path.isfile(path):  # Check if it's a file
                os.remove(path)
                self.logger.info(f"File deleted: {path}")
            elif os.path.isdir(path):  # Check if it's a directory
                shutil.rmtree(path)
                self.logger.info(f"Directory deleted: {path}")
            else:
                self.logger.warning(f"Path not found: {path}")
        except Exception as e:
            self.logger.error(f"Error deleting {path}: {e}", exc_info=True)
