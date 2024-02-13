
from hex_converter import HexConverter

class ResponseGenerator:

    def __init__(self):
        # Include any initialization logic here
        pass

    def generate_signal_link_response_hex(self, session_id):
        ascii_response = '{"err":"0","ss":"' + session_id + '"}'
        hex_response = HexConverter.convert_ascii_to_hex(ascii_response).lower()
        response_len = format((len(hex_response) + 4) // 2, '08x')
        response_len = HexConverter.string_reverse(response_len)
        # Construct the final response in hexadecimal
        strSLRR = "48010140" + response_len + hex_response + "0a00"
        return strSLRR

    def generate_heart_beat_response_hex(self):
        # Construct the final response in hexadecimal
        heart_beat_response = "4801010000000000"
        strSLRR = heart_beat_response
        return strSLRR
    
    def generate_gps_service_response_hex(self):
        # Construct the final response in hexadecimal
        gps_service_response = "4801414000000000"
        strSLRR = gps_service_response
        return strSLRR
    
    def generate_alarm_service_response_hex(self):
        # Construct the final response in hexadecimal
        alarm_service_response = "4801514000000000"
        strSLRR = alarm_service_response
        return strSLRR
    

# Example usage
if __name__ == "__main__":
    generator = ResponseGenerator()

    # Example Signal Link Response
    session_id = "12FB-01DE-0001-0203"
    signal_link_response_hex = generator.generate_signal_link_response_hex(session_id)
    print("Signal Link Response Hex:", signal_link_response_hex)

    # Example Heartbeat Response
    heartbeat_response_hex = generator.generate_heart_beat_response_hex()
    print("Heartbeat Response Hex:", heartbeat_response_hex)

    # Example GPS Response
    gps_response_hex = generator.generate_gps_service_response_hex()
    print("GPS Response Hex:", gps_response_hex)

    # Example GPS Response
    alarm_response_hex = generator.generate_alarm_service_response_hex()
    print("Alarm Response Hex:", alarm_response_hex)

