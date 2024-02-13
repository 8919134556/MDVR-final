import os
import requests
from datetime import datetime
import configparser
import json
from hex_converter import HexConverter

class ImageUploader:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('mdvr_config.ini')
        self.VSS_ip = self.config.get('VSS_Server', 'VSS_IP')
        self.VSS_port = self.config.get('VSS_Server', 'VSS_PORT')
        self.hex_converter = HexConverter()

    def create_folder_structure(self, unit_no):
        today_date = datetime.now().strftime("%d-%m-%Y")
        log_directory = self.config.get('Logging', 'LogDirectory')
        folder_path = os.path.join(log_directory, f"Snap_shot/{today_date}/{unit_no}/")
        
        # Check if the folder for today already exists, create if not
        os.makedirs(folder_path, exist_ok=True)
        
        return folder_path

    def download_and_save_image(self, unit_no, path):
        URL = f"http://{self.VSS_ip}:{self.VSS_port}/vss/record/showImage.action?token=d3c390fc71494c40a00298a37e5c2c1f&scheme=http&fileName={path}&deviceID={unit_no}&fileSize=30000&fileType=3"
        time_stamp = datetime.now().strftime("%H-%M-%S")
        folder_path = self.create_folder_structure(unit_no)
        file_name = time_stamp+"_"+os.path.basename(path)
        file_path = os.path.join(folder_path, file_name)

        # Download and save the image
        response = requests.get(URL)
        with open(file_path, 'wb') as file:
            file.write(response.content)

    def process_substring(self, substring, unit_no):
        data = substring[4:8]
        msg_type = data[2:4] + data[0:2]
        if msg_type == "1020":
            ascii_result = self.hex_converter.convert_hex_to_ascii(substring[16:-4])
            if ascii_result is not None:
                # Convert hex to ASCII
                json_data = json.loads(ascii_result) 
                if "rl" in json_data and isinstance(json_data["rl"], list):
                    for item in json_data["rl"]:
                        if "fn" in item:
                            image_path = item["fn"]
                            self.download_and_save_image(unit_no, image_path)
        else:
            pass

    def extract_substrings(self, unit_no, hex_data):
        """
        Extract substrings from hex_data starting with pattern_start and ending with pattern_end.
        """
        start_pattern = "4801"
        end_pattern = "0a00"

        # Initialize start_index
        start_index = 0

        # Find occurrences of start_pattern after each end_pattern
        while True:
            start_index = hex_data.find(start_pattern, start_index)

            # Break if start_pattern is not found
            if start_index == -1:
                break

            # Extract the substring starting with start_pattern and ending with end_pattern
            substring = hex_data[start_index:start_index + hex_data[start_index:].find(end_pattern) + len(end_pattern)]
            # Process the substring as needed
            self.process_substring(substring, unit_no)

            # Move start_index forward to avoid an infinite loop
            start_index += 1

if __name__ == "__main__":
    # Create an instance of the ImageUploader class
    uploader = ImageUploader()

    # Pass values from another code
    hex_data = "48012010fc0000007b22657272223a2230222c22726c223a5b7b226368223a2231222c22666e223a222f6d6e742f7364312f706963747572652f50696332303233313131373230353434373135304e30302e6a7067227d2c7b226368223a2232222c22666e223a222f6d6e742f7364312f706963747572652f50696332303233313131373230353434373635384e30312e6a7067227d2c7b226368223a2233222c22666e223a222f6d6e742f7364312f706963747572652f50696332303233313131373230353434383136394e30322e6a7067227d5d2c227373223a2236423842343536372d32334336333237422d41393938334336342d3733343833333636227d0a0048019210540000007b226574223a2231323830222c22666e223a222f6d6e742f7364312f706963747572652f50696332303233313131373230353434353837394130302e6a7067222c226674223a2234222c227373223a22227d0a00"
    unit_no = "91006"

    # Call the function to extract substrings
    uploader.extract_substrings(unit_no, hex_data)

