from fastapi import FastAPI

api_v3 = FastAPI(
    title="Svalbard Weather Information API",
    description="API Documentation of the backend of the Svalbard Weather Information Application",
    version="3.0.0",
    # servers=[
    #     {"url": "https://swi.unis.no/api/v1", "description": "Production server"},
    #     {"url": "http://localhost:8000", "description": "Local development server"}
    # ]
)

from source.cacheHandler.cacheHandler import CacheHandler

cache_handler = CacheHandler(serve_only = True)

def api_v3_get_cache_handler():
    return cache_handler


from .routes import station, realtime_data, timeserie_data

api_v3.include_router(station.router, prefix="/stations", tags=["Weather Stations"])
api_v3.include_router(realtime_data.router, prefix="/data/realtime", tags=['Meteorological Data'])
api_v3.include_router(timeserie_data.router, prefix="/data/timeseries", tags=['Meteorological Data'])

@api_v3.get('/')
def root():
    return {'Hello':'World'}