# Use an official Debian base image with Python 3.8
FROM python:3.8

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt /usr/src/app/

# Upgrade pip and install Python dependencies
RUN python3 -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the remaining application files into the container
COPY ClientHandler.py hex_converter.py logger.py mdvr_config.ini raw_data_processor.py redis_uploader.py request_command.py Response_generator.py server_Socket.py snap_shot_image_uploader.py /usr/src/app/

# Create a volume for persistent data
VOLUME /usr/src/app/logs

# Expose port 8010
EXPOSE 8010

# Run server_Socket.py when the container launches
CMD ["python", "./server_Socket.py"]
