import pyodbc
from configparser import ConfigParser
from threading import Lock
import datetime

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
        try:
            if self._connection is None:
                config = ConfigParser()
                config.read('mdvr_config.ini')  # Adjust the file path as needed
                driver = config.get('Database', 'driver')
                server = config.get('Database', 'server')
                database = config.get('Database', 'database')
                username = config.get('Database', 'username')
                password = config.get('Database', 'password')

                connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
                # Using connection pooling by adding 'Pooling=True' to the connection string
                self._connection = pyodbc.connect(connection_string + ';Pooling=True', autocommit=True)
                self._cursor = self._connection.cursor()
        except pyodbc.Error as e:
            print(f"Error connecting to the database: {e}")

    def insert_records(self, records):
        """
        Bulk insert records into the database.
        
        Args:
            records (list): List of tuples, where each tuple represents a set of parameters for a record.
        """
        query = '''EXEC InsertIntoMdvrgpsandalarmdata @unit_no = ?, @vehicle_no = ?, @location_type = ?, 
                   @track_time = ?, @direction_in_degree = ?, @satellite = ?, @speed = ?, @lat = ?, @lon = ?,
                   @x_acceleration = ?, @y_acceleration = ?, @z_acceleration = ?, @tilt = ?, @impact = ?,
                   @fuel_consumption = ?, @balance_fuel = ?, @hd_status = ?, @hd_size = ?, @hd_balance = ?,
                   @ibutton1 = ?, @message_type = ?, @ignition = ?, @gsm_signal = ?, @polling_mode = ?,
                   @ha = ?, @hb = ?, @panic = ?, @fuel_bar = ?, @over_speed = ?, @analog = ?, @seat_belt = ?,
                   @prev_value = ?, @ec = ?, @tp = ?, @SD_Type = ?, @SD_Status = ?, @version = ?, 
                   @Network_Type = ?, @alert_datetime = ?, @immobilizer = ?, @IN1 = ?, @IN2 = ?'''

        try:
            # Using executemany for bulk insertion
            self._cursor.executemany(query, records)
        except pyodbc.Error as e:
            print(f"Error executing SQL query: {e}")

# Example usage:
if __name__ == "__main__":
    db_manager = DatabaseManager()

    # Example data for bulk insertion
    records = [
        ("91006", "91006", 0, datetime.datetime.now(), 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, "testing", 65200, 0, 0, "0000", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "testing", "1G", datetime.datetime.now(), 0, 0, 0),
        # Add more records as needed
    ]

    db_manager.insert_records(records)
