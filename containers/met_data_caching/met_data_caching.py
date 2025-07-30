from source.cacheHandler.cacheHandler import CacheHandler

station_handler = CacheHandler()

station_handler.cache_stations_status()
station_handler.cache_realtime_data()
station_handler.cache_past_hourly_data()