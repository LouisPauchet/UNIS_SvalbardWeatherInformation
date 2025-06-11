from fastapi import FastAPI

# Initialize the FastAPI application for version 3 of the API
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

# Initialize the cache handler in serve-only mode
cache_handler = CacheHandler(serve_only=True)

def api_v3_get_cache_handler():
    """
    Retrieve the cache handler instance for the API.

    Returns:
        CacheHandler: An instance of the CacheHandler configured for the API.
    """
    return cache_handler

# Import route modules
from .routes import station, realtime_data, timeserie_data, variables

# Include routers for different parts of the API
api_v3.include_router(station.router, prefix="/stations", tags=["Weather Stations"])
api_v3.include_router(realtime_data.router, prefix="/data/realtime", tags=['Meteorological Data'])
api_v3.include_router(timeserie_data.router, prefix="/data/timeseries", tags=['Meteorological Data'])
api_v3.include_router(variables.router, prefix="/variables", tags=['Meteorological Variables'])

@api_v3.get('/')
def root():
    """
    Root endpoint of the API.

    Returns:
        dict: A simple greeting message.
    """
    return {'Hello': 'World'}
