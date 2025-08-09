FROM openelevation/open-elevation:latest

# Set the working directory
WORKDIR /code

# Copy the run script to the container
COPY run.sh /code/prep-and-run-server.sh

# Make the script executable
RUN chmod +x /code/prep-and-run-server.sh

# Expose the necessary ports
EXPOSE 8080
EXPOSE 8443

# Command to run the script when the container starts
CMD ["/code/prep-and-run-server.sh"]
