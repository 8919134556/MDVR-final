import os
import shutil
from datetime import datetime, timedelta
import configparser
from logger import Logger

class FolderManager:
    def __init__(self, config_file="mdvr_config.ini"):
        self.config = configparser.ConfigParser()
        self.logging = Logger()
        self.config.read(config_file)
        self.base_directories = [path.strip() for path in self.config.get('Folders', 'base_directories').split(',')]
        self.days_to_keep = int(self.config.get('Folders', 'days_to_keep'))

    def delete_old_folders(self):
        try:
            # Get the current date and time
            current_time = datetime.now()

            for base_path in self.base_directories:
                # Check if the base directory exists
                if not os.path.exists(base_path):
                    self.logging.log_data("deletion_path_error", f"Base directory does not exist: {base_path}")
                    continue

                # Iterate through each folder in the base path
                for folder_name in os.listdir(base_path):
                    folder_path = os.path.join(base_path, folder_name)

                    # Check if the item in the path is a directory
                    if os.path.isdir(folder_path):
                        # Get the creation time of the folder
                        folder_creation_time = datetime.fromtimestamp(os.path.getctime(folder_path))

                        # Calculate the difference in days
                        days_difference = (current_time - folder_creation_time).days

                        # Check if the folder is older than the specified days_to_keep
                        if days_difference > self.days_to_keep:
                            # Delete the folder and its contents
                            shutil.rmtree(folder_path)
                            self.logging.log_data("Deleted_folder", f"Deleted folder: {folder_path}")
                        else:
                            pass
        except Exception as e:
            self.logging.log_data("Deleted_error", f"Deleted error: {e}")
                            

if __name__ == "__main__":
    folder_manager = FolderManager()

    # Call the method to delete old folders
    folder_manager.delete_old_folders()
