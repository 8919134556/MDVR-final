import pyodbc
from configparser import ConfigParser
from threading import Lock
import datetime
from logger import Logger

class DatabaseManager:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DatabaseManager, cls).__new__(cls)
                cls._instance._connection = None
                cls._instance._cursor = None
                cls._instance.connect()
            return cls._instance

    def connect(self):
        if self._connection is None:
            config = ConfigParser()
            config.read('mdvr_config.ini')  # Adjust the file path as needed
            driver = config.get('Database', 'driver')
            server = config.get('Database', 'server')
            database = config.get('Database', 'database')
            username = config.get('Database', 'username')
            password = config.get('Database', 'password')

            connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
            self._connection = pyodbc.connect(connection_string, autocommit=True)
            self._cursor = self._connection.cursor()

    def insert_record(self, unit_no, vehicle_no, location_type, device_date_time, direction_in_degree, satellite, speed, lat, lon, x_acceleration,
        y_acceleration, z_acceleration, tilt, impact, fuel_consumption, balance_fuel, hd_status, hd_size, hd_balance, ibutton_to_send, messageType, ignition, gsm_signal,
        polling_mode, ha, hb, panic, fuel_bar, over_speed, analog, seat_belt, previous_value, ec, tp, SD_Type, SD_Status, version,
        device_Network_Type, alert_datetime, immobilizer,IN1,IN2):
        
        
        query = '''EXEC InsertIntoMdvrgpsandalarmdata @unit_no = ?, @vehicle_no = ?, @location_type = ?, @track_time = ?, @direction_in_degree = ?, @satellite = ?, @speed = ?, @lat = ?, @lon = ?, @x_acceleration = ?,
            @y_acceleration = ?, @z_acceleration = ?, @tilt = ?, @impact = ?, @fuel_consumption = ?, @balance_fuel = ?, @hd_status = ?, @hd_size = ?, @hd_balance = ?, @ibutton1 = ?, @message_type = ?, @ignition = ?, @gsm_signal = ?,
            @polling_mode = ?, @ha = ?, @hb = ?, @panic = ?, @fuel_bar = ?, @over_speed = ?, @analog = ?, @seat_belt = ?, @prev_value = ?,
            @ec = ?, @tp = ?, @SD_Type = ?, @SD_Status = ?, @version = ?, @Network_Type = ?, @alert_datetime = ?, @immobilizer = ?, @IN1 = ?, @IN2 = ?'''

        # Assuming you have the parameters defined earlier in your code
        params = (unit_no, vehicle_no, location_type, device_date_time, direction_in_degree, satellite, speed, lat, lon, x_acceleration,
                y_acceleration, z_acceleration, tilt, impact, fuel_consumption, balance_fuel, hd_status, hd_size, hd_balance, ibutton_to_send, messageType, ignition, gsm_signal,
                polling_mode, ha, hb, panic, fuel_bar, over_speed, analog, seat_belt, previous_value, ec, tp, SD_Type, SD_Status, version,
                device_Network_Type, alert_datetime, immobilizer, IN1, IN2)

        self._cursor.execute(query, params)

    def abnormal_data(self, unit_no, device_date_time, SD_Type, SD_Status,polling_mode,update_time, status):
        query = '''INSERT INTO [dbo].[storage_abnormal_data] (
            unit_no, track_time, SD_Type, SD_Status, polling_mode, update_time, status
        ) VALUES (?, ?, ?, ?, ?,  ?, ?)
        '''
        values = (
            unit_no, device_date_time, SD_Type, SD_Status, polling_mode, update_time, status
        )
        self._cursor.execute(query, values)

    
    def alarm_video_file_detailes(self,unit_no, alert_date, from_time, to_time, channel_no, 
                            alarm_type, Video_file_name,folder_name,folder_path, track_time, insert_date_time,
                            alert_date_time,alert_from_time, alert_to_time,dt):
        logger = Logger()
        query = """
            INSERT INTO dbo.alarm_file_details (
                UnitNo, alertDate, fromTime, toTime, channelNo,alarmType,VideofileName, folderName,folderPath,
                trackTime,insertDateTime,alertDateTime, alertFromTime, alertToTime,
                dt
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        values = (
            unit_no, alert_date, from_time, to_time, channel_no, 
            alarm_type, Video_file_name,folder_name,folder_path, track_time, insert_date_time,
            alert_date_time,alert_from_time, alert_to_time,dt
        )
        try:
            self._cursor.execute(query, values)
        except pyodbc.IntegrityError as e:
            pass
        except Exception as e:
            logger.log_data("video_error", f'Error While from video download')
        


# Example usage:
if __name__ == "__main__":
    db_manager = DatabaseManager()
    # unit_no = "91006"
    # alert_datetime = datetime.datetime.now()
    # polling_mode = "abnormal start"
    # SD_Type = "0"
    # SD_Status = "loss"
    # update_time = None
    # status = "not updated"

    # db_manager.abnormal_data(unit_no, alert_datetime,SD_Type,SD_Status,polling_mode, update_time, status)


    unit_no = "91006"
    alert_date = "2023-12-06"
    from_time = "13:00:15"
    to_time = "13:05:15"
    channel_no = 1
    alarm_type = 12
    Video_file_name = "D:"
    folder_name = "D folder"
    folder_path = "folder/testing" 
    track_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    insert_date_time = datetime.datetime.now()
    alert_date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    alert_from_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    alert_to_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dt = 12
    db_manager.alarm_video_file_detailes(unit_no, alert_date, from_time, to_time, channel_no, 
                        alarm_type, Video_file_name,folder_name,folder_path, track_time, insert_date_time,
                        alert_date_time,alert_from_time, alert_to_time,dt)

