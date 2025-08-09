#!/bin/bash

# Check if /code/data directory exists
if [ ! -d "/code/data" ] || [ -z "$(ls -A /code/data)" ]; then
    echo "Directory /code/data does not exist. Installing package and downloading data..."

    # Create the directory
    mkdir -p /code/data

    # Update package list and install necessary packages
    apt-get update && \
        # apt-get install -y --no-install-recommends wget gdal-bin unzip
        apt-get install -y --no-install-recommends wget unzip

    # Download, extract, reproject, and clean temporary files
    if wget -O /code/data/NP_DTM20.zip https://next.api.npolar.no/dataset/dce53a47-c726-4845-85c3-a65b46fe2fea/attachment/e3c4ca92-fde2-4abc-87e8-6a2d4a14863a/_blob; then
        unzip /code/data/NP_DTM20.zip -d /code/data && \
        gdalwarp -overwrite -t_srs EPSG:4326 -r bilinear -of GTiff -co COMPRESS=NONE -co BIGTIFF=IF_NEEDED /code/data/NP_S0_DTM20/S0_DTM20.tif /code/data/NP_DTM20.tif && \
        rm -rf /code/data/NP_S0_DTM20 /code/data/NP_DTM20.zip

        # Create tiles and clean temporary files
        if [ -f "/code/create-tiles.sh" ]; then
            /code/create-tiles.sh /code/data/NP_DTM20.tif 20 20 && \
            rm /code/data/NP_DTM20.tif
        else
            echo "Error: /code/create-tiles.sh not found."
            exit 1
        fi
    else
        echo "Error: Failed to download the data."
        exit 1
    fi

    # Cleanup
    # apt-get remove -y wget gdal-bin unzip && \
    apt-get remove -y wget unzip && \
        apt-get autoremove -y && \
        rm -rf /var/lib/apt/lists/*

    echo "Data ready."
else
    echo "Directory /code/data already exists. Skipping installation and data download."
fi

# Run the server
python3 server.py
