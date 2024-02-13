from abnormal_storage_count import RecordsCount
import requests
from configparser import ConfigParser
import json

class VSSApiHandler:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read('mdvr_config.ini')
        self.VSS_ip = self.config.get('VSS_Server', 'VSS_IP')
        self.VSS_port = self.config.get('VSS_Server', 'VSS_PORT')
        self.VSS_username = self.config.get('VSS_Server', 'VSS_USERNAME')
        self.VSS_password = self.config.get('VSS_Server', 'VSS_PASSWORD')
        self.inserting_redis = RecordsCount() 

    def login(self):
        token = None
        login_url = f"http://{self.VSS_ip}:{self.VSS_port}/vss/user/apiLogin.action"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        login_data = {
            "username": f"{self.VSS_username}",
            "password": f"{self.VSS_password}"
        }
        # Convert the data to JSON format
        json_data = json.dumps(login_data)
        print(json_data)

        try:
            response = requests.post(login_url, data=json_data, headers=headers)
            if response.status_code == 200:
                json_response = response.json()
                print(json_response)
                if json_response["status"] == 10000:
                    token = json_response['data']['token']
                    self.inserting_redis.add_to_key("vss_token", "Token", token)
                    print("Login successful.")
                else:
                    print("Unexpected status in the API response.")
            else:
                print(f"Failed to login. Status code: {response.status_code}")
        except Exception as e:
            print(f"Login failed. Exception: {e}")
        
        return token


if __name__=="__main__":
    vss_api_handler = VSSApiHandler()
    vss_api_handler.login()


