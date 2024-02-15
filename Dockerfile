# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt /usr/src/app/

# Install required packages, including the SQL Server ODBC driver
RUN apt-get update && \
    pip install --no-cache-dir --use-feature=fast-deps -U pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the remaining application files into the container
COPY ClientHandler.py hex_converter.py logger.py mdvr_config.ini raw_data_processor.py redis_uploader.py request_command.py Response_generator.py server_Socket.py snap_shot_image_uploader.py /usr/src/app/

# Create a volume for persistent data
VOLUME /usr/src/app/logs

# Expose port 8010
EXPOSE 8010

# Run server_Socket.py when the container launches
CMD ["python", "./server_Socket.py"]
