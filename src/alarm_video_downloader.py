import requests
import json
import os
import configparser
from datetime import datetime, timedelta
import pytz
from logger import Logger
from vss_server_login import VSSApiHandler
from abnormal_storage_count import RecordsCount
import time
from db_inserting import DatabaseManager

class VideoDownloader:
    def __init__(self): 
        self.vss_api_handler = VSSApiHandler()
        self.config = configparser.ConfigParser()
        self.config.read('mdvr_config.ini')
        self.logging = Logger()
        self.VSS_ip = self.config.get('VSS_Server', 'VSS_IP')
        self.VSS_port = self.config.get('VSS_Server', 'VSS_PORT')
        self.VSS_username = self.config.get('VSS_Server', 'VSS_USERNAME')
        self.VSS_password = self.config.get('VSS_Server', 'VSS_PASSWORD')
        self.japan_timezone = pytz.timezone('Asia/Tokyo')
        self.get_token = RecordsCount()
        self.db_inserting = DatabaseManager()

    def create_folder_structure(self, unit_no):
        try:
            today_date = datetime.now(self.japan_timezone).strftime("%d-%m-%Y")
            log_directory = self.config.get('Logging', 'LogDirectory')
            folder_path = os.path.join(log_directory, f"Alarm_video/{today_date}/{unit_no}/")
            os.makedirs(folder_path, exist_ok=True)
        except Exception as e:
            self.logging.log_data("video_folder_error", f"While creation video folder: {folder_path}")
        return folder_path

    def download_video(self, video_url, save_path):
        try:
            response = requests.get(video_url, stream=True)
            response.raise_for_status()
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            self.logging.log_data("video_downloaded", f"Download successful. Video saved at: {save_path}")
        except requests.exceptions.RequestException as e:
            self.logging.log_data("video_download_error", f"Download failed. Error: {e}")

    def perform_download(self, unit_no, dt, start_time, end_time, event_type):
        token = None
        if token is None:
            token = self.get_token.get_field("vss_token", "Token")
            if token is None:
                token = self.vss_api_handler.login()
            else:
                pass
        else:
            pass
        api_url = f"http://{self.VSS_ip}:{self.VSS_port}/vss/record/videoFileSearch.action"
        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        adjusted_start_time = (start_time - timedelta(minutes=3)).strftime("%Y-%m-%d %H:%M:%S")
        adjusted_end_time = (end_time + timedelta(minutes=3)).strftime("%Y-%m-%d %H:%M:%S")
        api_data = {
            "token": token,
            "deviceID": unit_no,
            "startTime": adjusted_start_time, #"2023-11-20 15:39:59",
            "endTime":  adjusted_end_time, # "2023-11-20 18:40:09",
            "channelList": "1;2;3",
            "fileType": "2",
            "location": "4"
        }
        json_data = json.dumps(api_data)
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        print("waiting 1 min")
        time.sleep(50)
        response = requests.post(api_url, data=json_data, headers=headers)
        if response.status_code == 200:
            json_response = response.json()
            if json_response["status"] == 10000:
                try:
                    down_url_list = [file_info['downUrl'] for file_info in json_response['data']['files']]
                    if down_url_list:
                        save_path = self.create_folder_structure(unit_no)
                        for i, file_info in enumerate(json_response['data']['files'], start=1):
                            down_url = file_info['downUrl']
                            path_components = file_info['path'].split('/')
                            file_name = path_components[-1]
                            channel_no = file_info['channel']
                            video_save_path = os.path.join(save_path, file_name.replace(".hw", ".mp4"))
                            self.download_video(down_url, video_save_path)
                            alert_date_time = start_time
                            alert_date= alert_date_time.strftime("%Y-%m-%d")
                            alert_from_time = start_time
                            from_time = alert_from_time.strftime("%H:%M:%S")
                            alert_to_time  = end_time
                            to_time = alert_to_time.strftime("%H:%M:%S")
                            alarm_type = event_type
                            Video_file_name = file_name
                            folder_path = file_info['path']
                            folder_name = path_components[-4]
                            if folder_name == "alarmRecord":
                                folder_name = "alarmRecord"
                            else:
                                folder_name = "hftp"
                            track_time = alert_date_time
                            insert_date_time = datetime.now()

                            #************************inserting into db *******************************
                            self.db_inserting.alarm_video_file_detailes(unit_no, alert_date, from_time, to_time, channel_no, 
                            alarm_type, Video_file_name,folder_name,folder_path, track_time, insert_date_time,
                            alert_date_time,alert_from_time, alert_to_time,dt)
                    else:
                        self.logging.log_data("empty_video_URL", "No video URLs found.")
                except Exception as e:
                    self.logging.log_data("video_error", f"{e}")

            elif json_response["status"] == 10023:
                token = self.vss_api_handler.login()
                if token:
                    api_data["token"] = token
                    json_data = json.dumps(api_data)
                    print("waiting 1 min")
                    time.sleep(50)
                    response = requests.post(api_url, data=json_data, headers=headers)
                    if response.status_code == 200:
                        json_response = response.json()
                        if json_response["status"] == 10000:
                            try:
                                down_url_list = [file_info['downUrl'] for file_info in json_response['data']['files']]
                                if down_url_list:
                                    save_path = self.create_folder_structure(unit_no)
                                    for i, file_info in enumerate(json_response['data']['files'], start=1):
                                        down_url = file_info['downUrl']
                                        path_components = file_info['path'].split('/')
                                        file_name = path_components[-1]
                                        channel_no = file_info['channel']
                                        video_save_path = os.path.join(save_path, file_name.replace(".hw", ".mp4"))
                                        self.download_video(down_url, video_save_path)
                                        alert_date_time = start_time
                                        alert_date= alert_date_time.strftime("%Y-%m-%d")
                                        alert_from_time = start_time
                                        from_time = alert_from_time.strftime("%H:%M:%S")
                                        alert_to_time  = end_time
                                        to_time = alert_to_time.strftime("%H:%M:%S")
                                        alarm_type = event_type
                                        Video_file_name = file_name
                                        folder_path = file_info['path']
                                        folder_name = path_components[-4]
                                        if folder_name == "alarmRecord":
                                            folder_name = "alarmRecord"
                                        else:
                                            folder_name = "hftp"
                                        track_time = alert_date_time
                                        insert_date_time = datetime.now()

                                        #************************inserting into db *******************************
                                        self.db_inserting.alarm_video_file_detailes(unit_no, alert_date, from_time, to_time, channel_no, 
                                        alarm_type, Video_file_name,folder_name,folder_path, track_time, insert_date_time,
                                        alert_date_time,alert_from_time, alert_to_time,dt)
                                else:
                                    self.logging.log_data("empty_video_URL", "No video URLs found.")
                            except Exception as e:
                                self.logging.log_data("video_error", f"{e}")
                        else:
                            print("Error while login to VSS server.")
                    else:
                        pass
                else:
                    print("unauthorized or none token ")
                token = None
            else:
                print("Unexpected status in the API response.")
        else:
            self.logging.log_data("video_request_error", f"Request failed with status code {response.status_code} : {response.text}")

if __name__ == "__main__":
    unit_no = "91006"
    dt = 0
    start_time = "2023-12-05 19:59:11"
    end_time = "2023-12-05 19:59:40"
    event_type = 12
    video_downloader = VideoDownloader()
    video_downloader.perform_download(unit_no, dt, start_time, end_time, event_type)
