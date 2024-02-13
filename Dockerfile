# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy specific files into the container
COPY ClientHandler.py hex_converter.py logger.py mdvr_config.ini raw_data_processor.py redis_uploader.py request_command.py Response_generator.py server_Socket.py snap_shot_image_uploader.py requirements.txt /usr/src/app/

# Install required packages, including the SQL Server ODBC driver
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 80
EXPOSE 8010

# Run alarm_processor.py when the container launches
CMD ["python", "./server_Socket.py"]
