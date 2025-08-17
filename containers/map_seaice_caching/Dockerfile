FROM python:slim

RUN mkdir /swi

WORKDIR /swi

COPY icechart_caching.py ./run.py

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "/swi/run.py"]
