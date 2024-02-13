class RawDataProcessor:
    @staticmethod
    def get_device_network_type(device_network_id):
        network_types = {
            "0": "unknown",
            "1": "wired",
            "2": "WIFI",
            "3": "2G",
            "4": "3G",
            "5": "4G",
            "6": "5G",
            "7": "WIFI+3/4/5G",
            "8": "CABLE+3/4/5G"
        }
        return network_types.get(device_network_id.lower(), "unknown")
    
    

# Example usage
if __name__ == "__main__":
    device_network_id = "2"
    network_type = RawDataProcessor.get_device_network_type(device_network_id)
    print(f"Device Network Type: {network_type}")

