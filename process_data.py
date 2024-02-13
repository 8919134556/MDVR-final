from hex_converter import HexConverter
from db_inserting import DatabaseManager



class AlarmDataProcessor:
    def __init__(self):
        self.hex_converter = HexConverter()
        self.database_manager = DatabaseManager()
        

    def process_alarm_service_data(self, unit_no, messageType, polling_mode, ha, hb, panic, fuel_bar,over_speed,analog,
                                    seat_belt, previous_value, bit_data,version, ec, tp, SD_Type, SD_Status, device_Network_Type, 
                                    alert_datetime,dt, Up0, Dw0, Up1, Dw1, tm, Va, Cur, Pat):
        direction_in_degree = 0
        satellite = 0
        speed = 0
        lat = 0
        lon = 0
        x_acceleration = 0
        y_acceleration = 0
        z_acceleration = 0
        tilt = 0
        impact = 0
        fuel_consumption = 0
        balance_fuel = 0
        ignition = 0
        gsm_signal = 0
        location_type = None
        altitude = 0
        ibutton_to_send = None
        hdVal = 0
        Total_Mileage = 0
        Current_day_mileage = 0
        hd_status = None
        hd_size = None
        hd_balance = None
        immobilizer = None
        IN1 = 0
        IN2 = 0

        try:
            if messageType == "1041":
                load_data = bit_data[16:]
                load_data = load_data.lower()
                ssid_len = int(load_data[0:2], 16)
                bit_data = load_data[(ssid_len * 2) + 2:]
            elif messageType == "1051":
                bit_data = bit_data

            devicetimetemp = bit_data[:12]
            i_year = int(devicetimetemp[:2], 16)
            i_month = int(devicetimetemp[2:4], 16)
            i_day = int(devicetimetemp[4:6], 16)
            i_hour = int(devicetimetemp[6:8], 16)
            i_minute = int(devicetimetemp[8:10], 16)
            i_second = int(devicetimetemp[10:12], 16)
            device_date_time = f"{i_year + 2000}-{i_month:02d}-{i_day:02d} {i_hour:02d}:{i_minute:02d}:{i_second:02d}"

            content = bit_data[12:16]
            if content != "0000":
                content_reverse = self.hex_converter.string_reverse(content)
                binary_content = self.hex_converter.hex_to_binary(content_reverse, 16)
                binary_content = self.hex_converter.string_reverse_binary(binary_content)
                content_data_pos = 16

                if binary_content[0:1] == "1": # location info
                    location_info = bit_data[content_data_pos:content_data_pos+2]
                    location_info_bin = self.hex_converter.hex_to_binary(location_info, 16)
                    if location_info_bin[0:1] == "0":
                        direction = 0
                    elif location_info_bin[0:1] == "1":
                        direction = 1

                    if location_info_bin[1:2] == "0":
                        longitude_Mark = "East"
                        longitude_Sign = ""
                    elif location_info_bin[1:2] == "1":
                        longitude_Mark = "West"
                        longitude_Sign = "-"

                    if location_info_bin[2:3] == "0":
                        Altitude = "Above sea level"
                    elif location_info_bin[2:3] == "1":
                        Altitude = "lower than sea level"
                    
                    if location_info_bin[3:4] == "0":
                        mileage_data_exist = "0"
                    elif location_info_bin[3:4] == "1":
                        mileage_data_exist = "1"
                    
                    if location_info_bin[4:5] == "0":
                        latitude_mark = "North"
                        latitude_Sign = ""
                    elif location_info_bin[4:5] == "1":
                        latitude_mark = "South"
                        latitude_Sign = "-"
                    location_type = bit_data[content_data_pos+2:content_data_pos+4] # location type
                    track_time_Temp = bit_data [content_data_pos+4:32]
                    iYear1 = int(track_time_Temp[0:2], 16)
                    iMonth1 = int(track_time_Temp[2:4], 16)
                    iDay1 = int(track_time_Temp[4:6], 16)
                    iHour1 = int(track_time_Temp[6:8], 16)
                    iMinute1 = int(track_time_Temp[8:10], 16)
                    iSecond1 = int(track_time_Temp[10:12], 16)
                    acquisition_time = f"{iYear1 + 2000}-{iMonth1:02d}-{iDay1:02d} {iHour1:02d}:{iMinute1:02d}:{iSecond1:02d}"
                    direction_in_degree = int(bit_data[content_data_pos+16:content_data_pos+18], 16)
                    satellite = int(bit_data[content_data_pos+18:content_data_pos+20], 16)
                    if direction == 1:
                        direction_in_degree = direction_in_degree + 180
                    speed_temp = self.hex_converter.string_reverse(bit_data[content_data_pos+20:content_data_pos+24])
                    speed = int(speed_temp, 16)/100
                    altitude = int(self.hex_converter.string_reverse(bit_data[content_data_pos+24:content_data_pos+28]), 16)/100
                    positioning_accuracy = bit_data[content_data_pos+28:content_data_pos+32]
                    Degree_of_longitude = int(bit_data[content_data_pos+32:content_data_pos+34], 16)
                    Minute_of_longitude_temp = self.hex_converter.string_reverse(bit_data[content_data_pos+34:content_data_pos+42])
                    Minute_of_longitude = float(int(Minute_of_longitude_temp, 16)) / 10000 / 60
                    lon = float(Degree_of_longitude+Minute_of_longitude)
                    lonStr = longitude_Sign + str(lon)
                    lon = float(lonStr)

                    Degree_of_latitude = int(bit_data[content_data_pos+42:content_data_pos+44], 16)
                    Minute_of_latitude_temp = self.hex_converter.string_reverse(bit_data[content_data_pos+44:content_data_pos+52])
                    Minute_of_latitude = float(int(Minute_of_latitude_temp, 16)) / 10000 / 60
                    lat = float(Degree_of_latitude+Minute_of_latitude)
                    latStr = latitude_Sign + str(lat)
                    lat = float(latStr)
                    content_data_pos = content_data_pos + 52

                if binary_content[1:2] == "1": # G-sensor
                    Identifier_bit_binary = self.hex_converter.hex_to_binary(bit_data[content_data_pos:content_data_pos+2], 16)
                    Identifier_bit_binary = self.hex_converter.string_reverse_binary(Identifier_bit_binary)
                    xyz_data_exist = Identifier_bit_binary[0:1]
                    tilt_data_exist = Identifier_bit_binary[1:2]
                    impact_data_exist = Identifier_bit_binary[2:3]
                    content_data_pos = content_data_pos+2 # 70

                    if xyz_data_exist == "1":
                        x_acceleration = int(self.hex_converter.string_reverse(bit_data[content_data_pos:content_data_pos+4]), 16)
                        
                        if x_acceleration > 32767:
                            x_acceleration -= 65536
                            x_acceleration /= 100.0
                        else:
                            x_acceleration /= 100.0

                        y_acceleration = int(self.hex_converter.string_reverse(bit_data[content_data_pos+4:content_data_pos+8]), 16)
                        
                        if y_acceleration > 32767:
                            y_acceleration -= 65536
                            y_acceleration /= 100.0
                        else:
                            y_acceleration /= 100.0

                        z_acceleration = int(self.hex_converter.string_reverse(bit_data[content_data_pos+8:content_data_pos+12]), 16)
                        
                        if z_acceleration > 32767:
                            z_acceleration -= 65536
                            z_acceleration /= 100.0
                        else:
                            z_acceleration /= 100.0
                        content_data_pos = content_data_pos+12 # 82

                    if tilt_data_exist == "1":
                        tilt = int(self.hex_converter.string_reverse(bit_data[content_data_pos:content_data_pos+4]), 16) / 100.0
                        content_data_pos = content_data_pos+4 # 86
            
                    if impact_data_exist == "1":
                        impact = int(self.hex_converter.string_reverse(bit_data[content_data_pos:content_data_pos+4]), 16) / 100.0
                        content_data_pos = content_data_pos + 4 # 90

                if binary_content[2:3] == "1": # basic status
                    # here two possible one 68 or 90 position if G-sensor enable we get 90 position or it disable we get 68 position  
                    Identifier_bit_binary_1 = self.hex_converter.hex_to_binary(bit_data[content_data_pos:content_data_pos+2], 16)
                    Identifier_bit_binary_1 = self.hex_converter.string_reverse_binary(Identifier_bit_binary_1)
                    acc = Identifier_bit_binary_1[0:1]
                    ignition = int(acc)
                    break_1 = Identifier_bit_binary_1[1:2]
                    turn_left = Identifier_bit_binary_1 [2:3]
                    turn_right = Identifier_bit_binary_1[3:4]
                    forward = Identifier_bit_binary_1[4:5]
                    backward = Identifier_bit_binary_1[5:6]
                    left_front_door = Identifier_bit_binary_1 [6:7]
                    right_front_door = Identifier_bit_binary_1[7:8]
                    content_data_pos = content_data_pos+2 # here 92 or 70

                    Identifier_bit_binary_2 = self.hex_converter.hex_to_binary(bit_data[content_data_pos:content_data_pos+2], 16)
                    Identifier_bit_binary_2 = self.hex_converter.string_reverse_binary(Identifier_bit_binary_2)
                    left_middle_door = Identifier_bit_binary_2[0:1]
                    right_middle_door = Identifier_bit_binary_2[1:2]
                    left_back_door = Identifier_bit_binary_2[2:3]
                    right_back_door = Identifier_bit_binary_2[3:4]

                    content_data_pos = content_data_pos+2 # here 94 or 72
                    content_data_pos = content_data_pos+4 # reserved and here 98 or 76 
                    
                
                if binary_content[3:4] == "1": # communication module working status
                    Identifier_bit =  bit_data[content_data_pos:content_data_pos+4]
                    content_data_pos = content_data_pos+4 # 102
                    Identifier_bit_rev = self.hex_converter.string_reverse(Identifier_bit)
                    Identifier_bit_binary = self.hex_converter.hex_to_binary(Identifier_bit_rev, 16)
                    Identifier_bit_binary = self.hex_converter.string_reverse_binary(Identifier_bit_binary)

                    mobile_net_work_data_exist = Identifier_bit_binary[0:1]
                    gps_module_data_exist = Identifier_bit_binary[1:2]
                    WIFI_module_data_exist = Identifier_bit_binary[2:3]
                    Gsensor_data_exist = Identifier_bit_binary[3:4]
                    recording_status_data_exist = Identifier_bit_binary[4:5]

                    if mobile_net_work_data_exist == "1":
                        mobile_network = bit_data[content_data_pos:content_data_pos+2]
                        mobile_network = int(mobile_network, 16)
                        content_data_pos = content_data_pos+2

                    if gps_module_data_exist == "1":
                        gps_module = bit_data[content_data_pos:content_data_pos+2]
                        gps_module = int(gps_module, 16)
                        content_data_pos = content_data_pos+2

                    if WIFI_module_data_exist == "1":
                        WIFI_module = bit_data[content_data_pos:content_data_pos+2]
                        WIFI_module = int(WIFI_module, 16)
                        content_data_pos = content_data_pos+2

                    if Gsensor_data_exist == "1":
                        Gsensor = bit_data[content_data_pos:content_data_pos+2]
                        Gsensor = int(Gsensor, 16)
                        content_data_pos = content_data_pos+2

                    if recording_status_data_exist == "1":
                        recording_status = bit_data[content_data_pos:content_data_pos+4]
                        content_data_pos = content_data_pos+4
                    
                if binary_content[4:5] == "1": # fuel consumption status bit_data 82 or 84
                    Identifier_bit = bit_data[content_data_pos:content_data_pos+2]
                    content_data_pos = content_data_pos + 2
                    Identifier_bit_binary = self.hex_converter.hex_to_binary(Identifier_bit, 16)
                    Identifier_bit_binary = self.hex_converter.string_reverse_binary(Identifier_bit_binary)

                    fuel_consumption_data_exist = Identifier_bit_binary[0:1]
                    balance_fuel_data_exist = Identifier_bit_binary[1:2]
                    if fuel_consumption_data_exist == "1":
                        fuel_consumption = int(self.hex_converter.string_reverse(bit_data[content_data_pos:content_data_pos+4]), 16)
                        content_data_pos = content_data_pos + 4
                    if balance_fuel_data_exist == "1":
                        balance_fuel = int(self.hex_converter.string_reverse(bit_data[content_data_pos:content_data_pos+4]), 16)
                        content_data_pos = content_data_pos + 4

                if binary_content[5:6] == "1": # mobile network status
                    Identifier_bit = bit_data[content_data_pos:content_data_pos+2]
                    content_data_pos = content_data_pos + 2

                    Identifier_bit_binary = self.hex_converter.hex_to_binary(Identifier_bit, 16)
                    Identifier_bit_binary = self.hex_converter.string_reverse_binary(Identifier_bit_binary)

                
                    gsm_signal = int(self.hex_converter.string_reverse(bit_data[content_data_pos:content_data_pos+2]), 16)
                    content_data_pos = content_data_pos + 2

                    network_type_temp = self.hex_converter.string_reverse(bit_data[content_data_pos:content_data_pos+2])
                    content_data_pos = content_data_pos + 2

                    reserved = self.hex_converter.string_reverse(bit_data[content_data_pos:content_data_pos+4])
                    content_data_pos = content_data_pos + 4
                

                if binary_content[6:7] == "1": # WIFI network status
                    Identifier_bit = bit_data[content_data_pos:content_data_pos+2]
                    content_data_pos = content_data_pos + 2

                    Identifier_bit_binary = self.hex_converter.hex_to_binary(Identifier_bit, 16)
                    Identifier_bit_binary = self.hex_converter.string_reverse_binary(Identifier_bit_binary)

                    signal_intensity_data_valid = Identifier_bit_binary[0:1]
                    network_address_data_valid = Identifier_bit_binary[1:2]
                    gateway_data_valid = Identifier_bit_binary[2:3]
                    Subnet_mask_data_valid = Identifier_bit_binary[3:4]
                    SSIDSSID_length_data_valid = Identifier_bit_binary[4:5]

                    if signal_intensity_data_valid == "1":
                        signal_intensity = bit_data[content_data_pos:content_data_pos+2]
                        content_data_pos = content_data_pos + 2

                    if network_address_data_valid == "1":
                        network_address = bit_data[content_data_pos:content_data_pos+8]
                        content_data_pos = content_data_pos + 8

                    if gateway_data_valid == "1":
                        gateway = bit_data[content_data_pos:content_data_pos+8]
                        content_data_pos = content_data_pos + 8
                    
                    if Subnet_mask_data_valid == "1":
                        Subnet_mask = bit_data[content_data_pos:content_data_pos+8]
                        content_data_pos = content_data_pos + 8
                    
                    if SSIDSSID_length_data_valid == "1":
                        SSIDSSID_length_temp = bit_data[content_data_pos:content_data_pos+2]
                        SSIDSSID_length = int(SSIDSSID_length_temp, 16)
                        SSID = bit_data[content_data_pos+2 : content_data_pos + 2 + SSIDSSID_length]
                        content_data_pos = content_data_pos + 4

                if binary_content[7:8] == "1":  # hard disk status
                    Identifier_bit = bit_data[content_data_pos:content_data_pos+2]
                    content_data_pos = content_data_pos + 2

                    Identifier_bit_binary = self.hex_converter.hex_to_binary(Identifier_bit, 16)
                    Identifier_bit_binary = self.hex_converter.string_reverse_binary(Identifier_bit_binary)

                    id = [""] * 8
                    hard_disk_status = [""] * 8
                    hard_disk_size = [""] * 8
                    hard_disk_balance_capacity = [""] * 8

                    for b in range(8):
                        id[b] = ""
                        hard_disk_status[b] = ""
                        hard_disk_size[b] = ""
                        hard_disk_balance_capacity[b] = ""
                        HDDataExist = Identifier_bit_binary[b]
                        
                        if HDDataExist == "1":
                            id[b] = bit_data[content_data_pos:content_data_pos + 2]
                            hard_disk_status[b] = bit_data[content_data_pos + 2:content_data_pos + 4]
                            hd_status = hard_disk_status[b]
                            hdVal = int(hard_disk_status[b], 16)
                            hard_disk_size[b] = bit_data[content_data_pos + 4:content_data_pos + 12]
                            hard_disk_size[b] = self.hex_converter.string_reverse(hard_disk_size[b])
                            hard_disk_size[b] = int(hard_disk_size[b], 16)
                            hd_size = hard_disk_size[b]
                            hard_disk_balance_capacity[b] = int(bit_data[content_data_pos + 12:content_data_pos + 20], 16)
                            hd_balance = hard_disk_balance_capacity[b]
                            content_data_pos += 20
                    if hd_status == "00":
                        hd_status = "unknown"
                    elif hd_status == "01":
                        hd_status = "recording"
                    elif hd_status == "02":
                        hd_status = "idle"
                    elif hd_status == "03":
                        hd_status = "abnormal"
                    elif hd_status == "04":
                        hd_status = "full"

                if binary_content[8:9] == "1": # alarm status

                    Identifier_bit = bit_data[content_data_pos:content_data_pos+8]
                    content_data_pos = content_data_pos + 8

                    Identifier_bit = self.hex_converter.string_reverse(Identifier_bit)

                    Identifier_bit_binary = self.hex_converter.hex_to_binary(Identifier_bit, 16)

                    Identifier_bit_binary = self.hex_converter.string_reverse_binary(Identifier_bit_binary)

                    Identifier_bit_binary = self.hex_converter.pad_right(Identifier_bit_binary, 14, '0')

                    video_loss_data_valid = Identifier_bit_binary[0:1]
                    motion_detection_data_valid = Identifier_bit_binary[1:2]
                    video_blind_data_valid = Identifier_bit_binary[2:3]
                    alarm_input_trigger_data_valid = Identifier_bit_binary[3:4]
                    over_speed_alarm = Identifier_bit_binary[4:5]
                    low_speed_alarm =  Identifier_bit_binary[5:6]
                    emergency_alarm = Identifier_bit_binary[6:7]
                    over_time_stop = Identifier_bit_binary[7:8]
                    vibration_alarm = Identifier_bit_binary[8:9]
                    out_of_GEO_fencing_alarm = Identifier_bit_binary[9:10]
                    enter_GEO_fencing_alarm = Identifier_bit_binary[10:11]
                    exist_line_alarm = Identifier_bit_binary[11:12]
                    enter_line_alarm = Identifier_bit_binary[12:13]
                    fuel_level_alarm = Identifier_bit_binary[13:14]
                    if video_loss_data_valid == "1":
                        video_loss = int(bit_data[content_data_pos:content_data_pos+4], 16)
                        content_data_pos = content_data_pos+4

                    if motion_detection_data_valid == "1":
                        motion_detection = int(bit_data[content_data_pos:content_data_pos+4], 16)
                        content_data_pos = content_data_pos+4

                    if video_blind_data_valid == "1":
                        video_blind = int(bit_data[content_data_pos:content_data_pos+4], 16)
                        content_data_pos = content_data_pos+4

                    if alarm_input_trigger_data_valid == "1":
                        alarm_input_trigger = int(bit_data[content_data_pos:content_data_pos+4], 16)
                        content_data_pos = content_data_pos+4

                if binary_content[9:10] == "1": # temperature and humidity status

                    Identifier_bit = bit_data[content_data_pos:content_data_pos+4]
                    content_data_pos = content_data_pos + 4

                    Identifier_bit = self.hex_converter.string_reverse(Identifier_bit)

                    Identifier_bit_binary = self.hex_converter.hex_to_binary(Identifier_bit, 16)

                    Identifier_bit_binary = self.hex_converter.string_reverse_binary(Identifier_bit_binary)

                    Identifier_bit_binary = self.hex_converter.pad_right(Identifier_bit_binary, 6, '0')

                    in_vehicle_temperature_data_valid = Identifier_bit_binary[0:1]
                    outside_of_vehicle_temperature_data_valid =  Identifier_bit_binary[1:2]
                    motor_temperature_data_valid = Identifier_bit_binary[2:3]
                    device_temperature_data_valid = Identifier_bit_binary[3:4]
                    in_vehicle_humidity_data_valid = Identifier_bit_binary[4:5]
                    outside_of_vehicle_humidity_data_valid = Identifier_bit_binary[5:6]

                    if in_vehicle_temperature_data_valid == "1":
                        in_vehicle_temperature = bit_data[content_data_pos:content_data_pos+4]
                        content_data_pos = content_data_pos+4
                    
                    if outside_of_vehicle_temperature_data_valid == "1":
                        outside_of_vehicle_temperature = bit_data[content_data_pos:content_data_pos+4]
                        content_data_pos = content_data_pos+4
                    
                    if motor_temperature_data_valid == "1":
                        motor_temperature = bit_data[content_data_pos:content_data_pos+4]
                        content_data_pos = content_data_pos+4
                    
                    if device_temperature_data_valid == "1":
                        device_temperature = bit_data[content_data_pos:content_data_pos+4]
                        content_data_pos = content_data_pos+4
                    
                    if in_vehicle_humidity_data_valid == "1":
                        in_vehicle_humidity = bit_data[content_data_pos:content_data_pos+2]
                        content_data_pos = content_data_pos+2
                    
                    if outside_of_vehicle_humidity_data_valid == "1":
                        outside_of_vehicle_humidity = bit_data[content_data_pos:content_data_pos+2]
                        content_data_pos = content_data_pos+2

                if binary_content[10:11] == "1": # Statistics data 
                    Identifier_bit = bit_data[content_data_pos:content_data_pos+4]
                    content_data_pos = content_data_pos + 4

                    Identifier_bit = self.hex_converter.string_reverse(Identifier_bit)

                    Identifier_bit_binary = self.hex_converter.hex_to_binary(Identifier_bit, 16)

                    Identifier_bit_binary = self.hex_converter.string_reverse_binary(Identifier_bit_binary)

                    Identifier_bit_binary = self.hex_converter.pad_right(Identifier_bit_binary, 2, '0')

                    Total_Mileage_data_valid = Identifier_bit_binary[0:1]
                    Current_day_mileage_data_valid = Identifier_bit_binary[1:2]

                    Total_Mileage =int(bit_data[content_data_pos: content_data_pos+8], 16)
                    content_data_pos = content_data_pos+8
                    Current_day_mileage = int(bit_data[content_data_pos:content_data_pos+8], 16)


                if binary_content[11:12] == "1": # ibutton
                    try:
                        Identifier_bit = bit_data[content_data_pos:content_data_pos+2]
                        content_data_pos = content_data_pos + 2

                        Identifier_bit_binary = self.hex_converter.hex_to_binary(Identifier_bit, 16)

                        Identifier_bit_binary = self.hex_converter.string_reverse_binary(Identifier_bit_binary)

                        Identifier_bit_binary = self.hex_converter.pad_right(Identifier_bit_binary, 2, '0')

                        for x in range(2):
                            ibutton_data_exist = Identifier_bit_binary[x]
                            if ibutton_data_exist == "1":
                                ibutton_id_length = int(bit_data[content_data_pos:content_data_pos+2], 16)
                                content_data_pos += 2
                                ibutton_temp = bit_data[content_data_pos:content_data_pos+ibutton_id_length * 2]
                                content_data_pos += ibutton_id_length * 2
                                ibutton_temp2 = self.hex_converter.convert_hex_to_ascii(ibutton_temp)
                                ibutton_to_send = ibutton_temp2

                    except Exception as e:
                        print(e)
            else:
                print("HEX_ERROR")
        except Exception as e:
            print(e)
        
        # raw data inserting
        self.database_manager.insert_record(unit_no, unit_no, location_type, device_date_time, direction_in_degree, satellite, speed, lat, lon, x_acceleration,
        y_acceleration, z_acceleration, tilt, impact, fuel_consumption, balance_fuel, hd_status, hd_size, hd_balance, ibutton_to_send,messageType, ignition, gsm_signal,
        polling_mode, ha, hb, panic, fuel_bar, over_speed, analog, seat_belt, previous_value, ec, tp, SD_Type, SD_Status, version,
        device_Network_Type, alert_datetime, immobilizer,IN1,IN2)

        # current data inserting
       
        


if __name__=="__main__":
    process_data = AlarmDataProcessor()
    unit_no = "91006"
    bit_data = "170B14001F09EF030000170B14001F090005000030000F00839D84050021571902000700000100000000000100010000001F0001010101030000000000001F0A000000000000000000000000010001000156DC0100000000000F0000000C000000000000003F0000000000000000000000"
    messageType = "1051"
    polling_mode = "testing"
    ha = 0
    hb = 0
    panic = 0
    fuel_bar = 0
    over_speed = 0
    analog = 0
    seat_belt = 0
    previous_value = 123
    version = "testing"
    ec = 1
    tp = 1
    event_type = 12
    SD_Type= "testing"
    SD_Status = "testing"
    device_Network_Type = "testing"
    alert_datetime = "2048-00-00 00:00:00"
    dt = 123
    Up0 = 123
    Dw0 = 123
    Up1 = 123
    Dw1 = 123
    tm = 123
    Va = 123
    Cur = 123
    Pat = 123

    process_data.process_alarm_service_data(unit_no, messageType, polling_mode, ha, hb, panic, fuel_bar,over_speed,analog,
                                    seat_belt, previous_value, bit_data,version, ec, tp, event_type, SD_Type, SD_Status, device_Network_Type, 
                                    alert_datetime,dt, Up0, Dw0, Up1, Dw1, tm, Va, Cur, Pat)
