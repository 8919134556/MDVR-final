import asyncio
import aioredis
import configparser
from logger import Logger
from datetime import datetime
from hex_converter import HexConverter
from folder_manager import FolderManager
from gps_process import GpsDataProcessor


class GPSData:
    def __init__(self, config_file="mdvr_config.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.logging = Logger()
        self.converion = HexConverter()
        self.redis_client = None
        self.redis_key = self.config.get('Redis', 'key')
        self.folder_manager = FolderManager()
        self.gpsdataprocess =  GpsDataProcessor() 
        self.previous_date_time = ''

    async def redis_setup(self):
        redis_host = self.config.get('Redis', 'host')
        redis_port = self.config.getint('Redis', 'port')
        self.redis_client = await aioredis.create_redis_pool(f'redis://{redis_host}:{redis_port}')
        
    async def fetch_and_process_data_from_redis(self, sleep_duration=1, max_iterations=None):
        iterations = 0
        while max_iterations is None or iterations < max_iterations:
            try:
                value = await self.redis_client.blpop(self.redis_key, timeout=sleep_duration)
                if value:
                    decoded_value = value[1].decode('utf-8')
                    await self.gps_process_data(decoded_value)
                else:
                    await asyncio.sleep(sleep_duration)
            except aioredis.RedisError as redis_error:
                # Handle specific Redis errors here
                self.logging.log_data("RedisError", f"Redis error: {redis_error}")
                await asyncio.sleep(sleep_duration)  # Add some delay before retrying
            iterations += 1

    async def gps_process_data(self,data):
        data_parts = data.split('|')
        if len(data_parts) == 4:
            unit_no, version, device_Network_Type, hex_data = data_parts
            messageType = hex_data[6:8]+hex_data[4:6] 
            if hex_data:
                if messageType == '1041':
                    resprocess_Gps_Service_Data = self.gpsdataprocess.process_gps_service_data(
                        unit_no, messageType, "Normal",0,0,0,0,0,0,0,0,hex_data,version,0,0,None,None,device_Network_Type,None,0,0,0,0,0,0,0,0,0,self.previous_date_time)
                    self.previous_date_time = resprocess_Gps_Service_Data
                    message = f"{datetime.now()} - hex_data: {hex_data}, Unit: {unit_no}"
                    self.logging.log_data("1041", message)
                else:
                    message = f"Invalid message type data : {hex_data} "
                    self.logging.log_data("Invalid_msg_type", message)
            else:
                pass
        else:
            self.logging.log_data("Invalid_data", f"Error: Invalid data format retrieved from Redis : ",{data_parts}) 


    async def delete_old_folders(self):
        while True:
            try:
                await asyncio.sleep(24 * 60 * 60)  # Sleep for 24 hours
                delete_folder = self.folder_manager.delete_old_folders()
            except Exception as e:
                self.logging.log_data("deletion", "While getting error in deletion program")  
                    
    
if __name__ == '__main__':
    gpsprocessor = GPSData()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(gpsprocessor.redis_setup())
    tasks = [
        gpsprocessor.fetch_and_process_data_from_redis(),
        gpsprocessor.delete_old_folders()
    ]

    loop.run_until_complete(asyncio.gather(*tasks))