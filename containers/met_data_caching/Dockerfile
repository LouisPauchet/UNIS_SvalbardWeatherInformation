FROM python:3.13-slim

WORKDIR /app

COPY ./containers/met_data_caching/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


COPY ./source /app/source
COPY ./containers/met_data_caching/met_data_caching.py /app/run.py





RUN mkdir /app/cache
RUN mkdir /app/static
COPY ./static/config /app/static/config

CMD ["python", "run.py"]