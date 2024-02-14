import redis
import configparser

class RecordsCount:
    def __init__(self) -> None:
        # Read Redis configuration from a config file
        config = configparser.ConfigParser()
        config.read('mdvr_config.ini')  # Assuming the configuration is stored in a file named 'redis_config.ini'

        # Connect to the Redis server
        self.redis_host = config.get('Redis', 'host')
        self.redis_port = config.getint('Redis', 'port')
        self.redis_client = redis.StrictRedis(host=self.redis_host, port=self.redis_port, decode_responses=True)

    def get_or_create_count(self, unit_no):
        # Key and value
        key = unit_no

        # Retrieve the current count
        current_count = self.redis_client.hget(key, 'count')

        if current_count is not None:
            # Increment the existing count
            new_count = int(current_count) + 1
            self.redis_client.hset(key, 'count', new_count)
        else:
            # Set the initial count if the key doesn't exist
            new_count = self.redis_client.hset(key, 'count', 1)

        return current_count
    
    def add_to_key(self, key, field, value):
        try:
            # Set the value for the field in the hash
            self.redis_client.hset(key, field, value)
            return True
        except Exception as e:
            print(f"Error adding value to key {key}: {e}")
            return False
        
    def get_field(self, key, field):
        # Retrieve the current count
        value = self.redis_client.hget(key, field)
        return value


    def reset_count(self, unit_no):
        new_count = 1
        key = unit_no
        self.redis_client.hset(key, 'count', new_count)



if __name__ == "__main__":
    # Example usage
    count = RecordsCount()
    count.get_or_create_count("91006")
    count.reset_count("72088")
    count.add_to_key("72088", "perv_value", "68")

