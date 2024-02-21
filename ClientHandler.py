import json
import socket
import threading
import binascii
from logger import Logger
from hex_converter import HexConverter
from raw_data_processor import RawDataProcessor
from Response_generator import ResponseGenerator
from request_command import DeviceCommunicationHandler
from snap_shot_image_uploader import ImageUploader
from redis_uploader import RedisUploader
import time 


class MDVRClientHandler(threading.Thread):
    def __init__(self, client_socket, client_address, mdvr_server):
        super().__init__()
        self.logging = Logger()
        self.hex_converter =  HexConverter()
        self.raw_data_processor = RawDataProcessor()
        self.response_generator = ResponseGenerator()
        self.request_command = DeviceCommunicationHandler()
        self.snap_shot_image_uploader = ImageUploader()
        self.redis = RedisUploader()
        self.client_socket = client_socket
        self.client_address = client_address
        self.mdvr_server = mdvr_server
        self.SignalLinkResponseSent = False
        self.sendgpsstatusrequest = True
        self.sendalarmrequest = True
        self.sendrequestCnt = 0
        self.sendsnapshotrequest =False
        self.sendsnaprequestCnt = 0
        self.HeartBeat = False
        self.gps_latest_record = None


       
    def run(self):
        unit_no = None
        hex_data = None
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    pass
                if data:
                    hex_data = binascii.hexlify(data).decode('utf-8')

                if hex_data.startswith("4801"):
                    message_type = hex_data[4:8]
                    message_type = message_type[2:4] + message_type[0:2]
                    #************************************************Signal Link Request and Response *********************************
                    if message_type == "1001":
                        ascii_data = hex_data[16:-4]
                        # Extract values from the JSON object
                        ascii_result = self.hex_converter.convert_hex_to_ascii(ascii_data)
                        if ascii_result is not None:
                            # Convert hex to ASCII
                            json_data = json.loads(ascii_result) 
                            unit_no = json_data.get('dn', '')
                            session_id = json_data.get('ss', '')
                            version = json_data.get('ver', '')
                            device_network_id = json_data.get('at', '')
                            device_network_type = self.raw_data_processor.get_device_network_type(device_network_id)
                            self.logging.log_data("M_1001_SetUp", f"Incoming_signal_data: {unit_no} : {hex_data}")
                            generate_signal_response = self.response_generator.generate_signal_link_response_hex(session_id)
                            try:
                                self.client_socket.sendall(binascii.unhexlify(generate_signal_response))
                                self.logging.log_data("M_1001_Response", f"Response_signal_data: {unit_no} : {generate_signal_response}")
                                self.SignalLinkResponseSent = True
                            except Exception as e:
                                self.logging.log_data("M_1001_SetUp_failed", f"Failed_signal_data: {unit_no} : {hex_data}")                   
                        else:
                            self.logging.log_data("M_1001_SetUp_faild", f"Unable to convert hex to ASCII.")
                        time.sleep(2)
                    #*********************************************************Heart Beat *********************************************
                    elif message_type == "0001":
                        self.HeartBeat = True
                        self.logging.log_data("M_0001_HeartBeatRequest", f"Heart_Beat_Request_Data: {unit_no} : {hex_data}") 
                        try:
                            # Construct the final response in hexadecimal
                            hart_beat_response = self.response_generator.generate_heart_beat_response_hex()
                            self.client_socket.sendall(binascii.unhexlify(hart_beat_response))
                            self.logging.log_data("M_0001_Response", f"Response_Heart_beat_data: {unit_no} : {hart_beat_response}")
                        except Exception as e:
                            self.logging.log_data("M_0001_Heart_failed", f"Failed_Heart_beat_data: {unit_no} : {hex_data}")
                    #*******************************************************GPS Subscription Respond **********************************
                    elif message_type == "1040":
                        self.logging.log_data("M_1040_GPS_Subscription_Respond", f"GPS_Subscription_Respond: {unit_no} : {hex_data}")
                        # Extract values from the JSON object
                        ascii_result = self.hex_converter.convert_hex_to_ascii(ascii_data)
                        if ascii_result is not None:
                            # Convert hex to ASCII
                            json_data = json.loads(ascii_result) 
                            err_code = json_data.get('err', '')
                            if err_code == "0":
                                self.sendgpsstatusrequest = False
                    #*******************************************************GPS Service Data and Response *****************************
                    elif message_type == "1041":
                        self.logging.log_data("M_1041_GPS_Service_Data", f"GPS_Service_Data: {unit_no} : {hex_data}")
                        self.gps_latest_record = hex_data
                        # inserting into kafka producer
                        Key_name = "gps_1041"
                        records = f"{unit_no}|{version}|{device_network_type}|{hex_data}"
                        self.redis.upload_record(Key_name, records)
                        gps_service_response = self.response_generator.generate_gps_service_response_hex()
                        self.client_socket.sendall(binascii.unhexlify(gps_service_response))
                        self.logging.log_data("M_4041_GPS_Service_response", f"GPS_Service_response: {unit_no} : {gps_service_response}")
                    
                    #********************************************************Snap Short ************************************************
                    elif message_type == "1020":
                        self.logging.log_data("M_1020_Snap_Short", f"Snap_Short: {unit_no} : {hex_data}")
                        self.snap_shot_image_uploader.extract_substrings(unit_no, hex_data)
                        self.sendsnapshotrequest = False

                    #********************************************************Alarm Subscription Respond ********************************
                    elif message_type == "1050":
                        self.logging.log_data("M_1050_Alarm_Sub_Respond", f"Alarm_Subscription_Respond: {unit_no} : {hex_data}")
                        # Extract values from the JSON object
                        ascii_result = self.hex_converter.convert_hex_to_ascii(ascii_data)
                        if ascii_result is not None:
                            # Convert hex to ASCII
                            json_data = json.loads(ascii_result) 
                            err_code = json_data.get('err', '')
                            if err_code == "0":
                                self.sendalarmrequest = False
                        
                    #********************************************************Alarm Service Data and Response ***************************   
                    elif message_type == "1051":
                        self.logging.log_data("M_1051_Alarm_service_Data", f"Alarm_service_data: {unit_no} : {hex_data}")
                        self.sendsnapshotrequest = True
                        # inserting into kafka producer
                        key_name = "alarm_1051"
                        records = f"{unit_no}|{version}|{device_network_type}|{hex_data}"
                        self.redis.upload_record(key_name, records)
                        alarm_service_response = self.response_generator.generate_alarm_service_response_hex()
                        self.client_socket.sendall(binascii.unhexlify(alarm_service_response))
                        self.logging.log_data("M_4051_Alarm_service_Response", f"Alarm_service_Respond: {unit_no} : {alarm_service_response}")

                    else:
                        pass
                else:
                    pass

                #**********************************************Send GPS Request to device ************************************
                try:
                    if unit_no and self.SignalLinkResponseSent:
                        self.sendrequestCnt += 1
                        if self.sendrequestCnt == 1:
                            if self.sendgpsstatusrequest:
                                # GPS request to device
                                try:
                                    sendgpsrequest = self.request_command.send_gps_request(unit_no, session_id)
                                    if sendgpsrequest:
                                        self.client_socket.sendall(binascii.unhexlify(sendgpsrequest))
                                        self.logging.log_data("M_4040_GPSRequest", f"GPS ==> Unitno: {unit_no}: {sendgpsrequest}")
                                    else:
                                        self.logging.log_data("GPSERROR_log", f"ERROR: Invalid session_id for GPS request - Unitno: {unit_no}")
                                except Exception as e:
                                    self.logging.log_data("M_4040_GPSRequest_failed", f"Failed_gps_request_data: {unit_no} : {sendgpsrequest}")
                            else:
                                pass
                            if self.sendalarmrequest:
                                # Alarm request to device
                                try:
                                    send_alarm_request = self.request_command.send_alarm_request(unit_no, session_id)
                                    if send_alarm_request:
                                        self.client_socket.sendall(binascii.unhexlify(send_alarm_request))
                                        self.logging.log_data("M_5040_ALARMRequest", f"ALARM ==> Unitno: {unit_no}: {send_alarm_request}")
                                    else:
                                        self.logging.log_data("ALARMERROR_log", f"ERROR: Invalid session_id for alarm request - Unitno: {unit_no}")
                                except Exception as e:
                                    self.logging.log_data("M_5040_ALARMRequest_failed", f"Failed_Alarm_request_data: {unit_no} : {send_alarm_request}")
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                except Exception as ex:
                    self.logging.log_data("RequestERROR_log", f"ERROR while send GPS Alarm request: {unit_no} : {str(ex)}")

                #**********************************************Send Snap Shot Request to device *************************************
                try:
                    if unit_no and self.sendsnapshotrequest:
                        self.sendsnaprequestCnt += 1
                        if self.sendsnaprequestCnt == 1:
                            # Snap Short request to device
                            try:
                                send_snap_short_request = self.request_command.send_snap_short_request(unit_no, session_id)
                                if send_snap_short_request:
                                    self.client_socket.sendall(binascii.unhexlify(send_snap_short_request))
                                    self.logging.log_data("M_4020_SNAPRequest", f"SNAP ==> Unitno: {unit_no}: {send_snap_short_request}")
                                else:
                                    self.logging.log_data("SNAPERROR_log", f"ERROR: Invalid session_id for snap short request - Unitno: {unit_no}")
                            except Exception as e:
                                self.logging.log_data("M_4020_SNAPRequest_failed", f"Failed_Snap_request_data: {unit_no} : {send_snap_short_request}")
                        else:
                            pass
                    else:
                        pass
                except Exception as ex:
                    self.logging.log_data("RequestERROR_log", f"ERROR while send Snap request: {unit_no} : {str(ex)}")
            except socket.timeout:
                pass  # Ignore timeout, continue listening
            except Exception as e:
                self.logging.log_data("error", f"Exception occurred: {e}")
                break

if __name__ == "__main__":
    # Add any specific MDVR client testing logic here if needed
    pass

