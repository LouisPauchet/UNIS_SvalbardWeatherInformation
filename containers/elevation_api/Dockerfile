FROM openelevation/open-elevation:latest

# Set the working directory
WORKDIR /code

# Create the data directory
RUN mkdir -p /code/data

# Install Packqge
RUN apt-get update && \
    apt-get install -y --no-install-recommends wget gdal-bin

# Get data, reproject and clean temporary files
RUN wget https://next.api.npolar.no/dataset/dce53a47-c726-4845-85c3-a65b46fe2fea/attachment/e3c4ca92-fde2-4abc-87e8-6a2d4a14863a/_blob -O /code/data/NP_DTM20.zip && \
    unzip /code/data/NP_DTM20.zip -d /code/data && \
    gdalwarp -overwrite -t_srs EPSG:4326 -r bilinear -of GTiff -co COMPRESS=NONE -co BIGTIFF=IF_NEEDED /code/data/NP_S0_DTM20/S0_DTM20.tif /code/data/NP_DTM20.tif && \
    rm -rf /code/data/NP_S0_DTM20 /code/data/NP_DTM20.zip

# Create tiles and clean temporary files
RUN /code/create-tiles.sh /code/data/NP_DTM20.tif 20 20 && \
    rm /code/data/NP_DTM20.tif

# Cleanup
RUN apt-get remove -y wget gdal-bin && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*