# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy specific files into the container
COPY abnormal_storage_count.py alarm_processor.py alarm_video_downloader.py db_inserting.py event_type.py \
     folder_manager.py hex_converter.py logger.py mdvr_config.ini process_data.py requirements.txt \
     vss_server_login.py /usr/src/app/

# Install required packages, including the SQL Server ODBC driver
RUN apt-get update && \
    apt-get install -y --no-install-recommends unixodbc unixodbc-dev curl gnupg && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql17 && \
    pip install --no-cache-dir -r requirements.txt

# Expose port 80
EXPOSE 80

# Run alarm_processor.py when the container launches
CMD ["python", "./alarm_processor.py"]
