from fastapi import FastAPI

from .routes import station, realtime_data



api_v3 = FastAPI()

api_v3.include_router(station.router, prefix="/stations", tags=["stations"])
api_v3.include_router(realtime_data.router, prefix="/data/realtime", tags=['data', 'realtime'])

@api_v3.get('/')
def root():
    return {'Hello':'World'}