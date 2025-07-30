FROM python:3.13-slim

WORKDIR /app

COPY ../../source /app/source
COPY ./met_data_caching.py /app/run.py

RUN pip install --no-cache-dir -r ./containers/met_data_caching/requirements.txt

CMD ["python", "app/run.py"]