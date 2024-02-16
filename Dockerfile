# Use an official Python runtime as a parent image
FROM python:3.9.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy specific files into the container
COPY gps_data.py db_inserting.py folder_manager.py gps_process.py hex_converter.py logger.py mdvr_config.ini requirements.txt /usr/src/app/

# Install required packages, including the SQL Server ODBC driver
RUN apt-get update && \
    apt-get install -y --no-install-recommends unixodbc unixodbc-dev curl gnupg && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql17 && \
    pip install --no-cache-dir -r requirements.txt

# Create a volume for persistent data
VOLUME /usr/src/app/logs


# Run alarm_processor.py when the container launches
CMD ["python", "./gps_data.py"]
