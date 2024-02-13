import redis
import configparser

class RedisUploader:
    def __init__(self, config_file="mdvr_config.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.redis_host = self.config.get('Redis', 'host')
        self.redis_port = self.config.getint('Redis', 'port')
        self.redis_client = redis.StrictRedis(host=self.redis_host, port=self.redis_port, db=0, decode_responses=True)

    def upload_record(self,redis_key, record):
        if not self.redis_client:
            raise RuntimeError("Redis client not connected. Call connect_to_redis() first.")
        try:
            self.redis_client.rpush(redis_key, record)
        except Exception as e:
            print(f"Error uploading record to Redis: {e}")

if __name__ == "__main__":
    # Define your test records (replace this with your dynamic data source)
    test_records = "91007|V1|4G|48014110AE0000002436423842343536372D32334336333237422D41393938334336342D373334383333363600170B01000636EFE70101170B01000636280500003F00130083E3840500219F1902000707000000C400B201C500010000001F00000101010F0000000000001F080000000000000000000000000100010F01EAED0000000000000F0000000C000000000000003F000000000000000000000001007A7B00001806000002020010090000022C0001000000"
    redis_key = "gps_1041"
    # Create an instance of RedisUploader, reading redis_key from the config
    redis_uploader = RedisUploader()

    for _ in range(10):
        redis_uploader.upload_record(redis_key, test_records)
    
