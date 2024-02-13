import os
from datetime import datetime
import configparser

class Logger:

    def __init__(self, config_file_path='mdvr_config.ini'):
        self.config = self.load_config(config_file_path)
        self.log_dir_path = self.config.get('Logging', 'LogDirectory')

    def load_config(self, config_file_path):
        config = configparser.ConfigParser()
        config.read(config_file_path)
        return config

    def log_data(self, file_name, data):
        now = datetime.now()
        formatted_datetime = now.strftime('%Y-%m-%d %H:%M:%S')

        # Create the date-wise folder if it doesn't exist
        date_folder_path = os.path.join(self.log_dir_path, now.strftime('%Y-%m-%d'))
        os.makedirs(date_folder_path, exist_ok=True)

        # Create the log file path with the specified file_name
        log_file_path = os.path.join(date_folder_path, f"{file_name}.log")

        # Write the log data to the file
        with open(log_file_path, 'a') as log_file:
            log_file.write(f"{formatted_datetime} - {data}\n")

# Example usage
if __name__ == "__main__":
    # Example usage with default config_file_path
    logger = Logger()

    unit_no = "91006"
    session_id = "6B8B4567-23C6327B-A9983C64-73483366"

    # Example GPS request logging
    logger.log_data("GPSRequest", f"GPS ==> Unitno: {unit_no}")
    # Other GPS request logic...

    # Example alarm request logging
    logger.log_data("AlarmRequest", f"Alarm ==> Unitno: {unit_no}")
    # Other alarm request logic...

