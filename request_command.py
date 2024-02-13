
from logger import Logger
from hex_converter import HexConverter

class DeviceCommunicationHandler:

    def __init__(self):
        # If you have any other initialization logic, you can include it here
        self.logger = Logger()
        pass

    def send_gps_request(self, unit_no, session_id):
        strSLRR = ""
        try:
            if session_id:
                payload = f"{{\"ct\":\"65535\",\"ss\":\"{session_id}\"}}"
                response_hex = HexConverter.convert_ascii_to_hex(payload).lower()
                response_len = format((len(response_hex) + 4) // 2, '08x')
                response_len = HexConverter.string_reverse(response_len).lower()
                strSLRR = "48014040" + response_len + response_hex + "0a00"
            else:
                self.logger.log_data("GPSERROR_log", f"ERROR: Invalid session_id for GPS request - Unitno: {unit_no}")
        except Exception as ex:
            self.logger.log_data("GPSERROR_log", f"ERROR while sending GPS request: {unit_no} : {str(ex)}")
        return strSLRR

    def send_alarm_request(self, unit_no, session_id):
        strSLRR = ""
        try:
            if session_id:
                payload = f"{{\"ct\":\"65535\",\"ack\":\"1\",\"ss\":\"{session_id}\"}}"
                response_hex = HexConverter.convert_ascii_to_hex(payload).lower()
                response_len = format((len(response_hex) + 4) // 2, '08x')
                response_len = HexConverter.string_reverse(response_len).lower()
                strSLRR = "48015040" + response_len + response_hex + "0a00"
            else:
                self.logger.log_data("AlarmERROR_log", f"ERROR: Invalid session_id for alarm request - Unitno: {unit_no}")
        except Exception as ex:
            self.logger.log_data("AlarmERROR_log", f"ERROR while sending alarm request: {unit_no} : {str(ex)}")
        return strSLRR
    
    def send_snap_short_request(self, unit_no, session_id):
        strSLRR = ""
        try:
            if session_id:
                payload = f"{{\"cl\":\"1;2;3\",\"ss\":\"{session_id}\"}}"
                response_hex = HexConverter.convert_ascii_to_hex(payload).lower()
                response_len = format((len(response_hex) + 4) // 2, '08x')
                response_len = HexConverter.string_reverse(response_len).lower()
                strSLRR = "48012040" + response_len + response_hex + "0a00"
            else:
                self.logger.log_data("SnapShortERROR_log", f"ERROR: Invalid session_id for snap short request - Unitno: {unit_no}")
        except Exception as ex:
            self.logger.log_data("SnapShortERROR_log", f"ERROR while sending snap short request: {unit_no} : {str(ex)}")
        return strSLRR

# Entry point
if __name__ == "__main__":
    handler = DeviceCommunicationHandler()
    
    unit_no = "91006"
    session_id = "6B8B4567-23C6327B-A9983C64-73483366"

    Gps = handler.send_gps_request(unit_no, session_id)
    print(Gps)
    Alarm = handler.send_alarm_request(unit_no, session_id)
    print(Alarm)
    SnapShort = handler.send_snap_short_request(unit_no, session_id)
    print(SnapShort)

