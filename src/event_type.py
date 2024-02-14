from hex_converter import HexConverter
from process_data import AlarmDataProcessor
from abnormal_storage_count import RecordsCount
from db_inserting import DatabaseManager
from alarm_video_downloader import VideoDownloader
import json



class AlarmEventType:
    def __init__(self):
        self.hex_converter = HexConverter()
        self.alarm_data_processor = AlarmDataProcessor()
        self.records_count = RecordsCount()
        self.database_manager = DatabaseManager()
        self.video_downloader = VideoDownloader()

    def event_processor(self, unit_no,content_hex,bit_data,messageType,version,device_Network_Type):
        tp = 0
        ec = 0
        ha = 0
        hb = 0
        panic = 0
        fuel_bar = 0
        over_speed = 0
        analog = 0
        seat_belt = 0
        channel_no_alarm = 0
        trigger_threshold = 0
        time_threshold = 0
        max = 0
        min = 0
        average = 0
        current_value = 0
        previous_value = 0
        direction = 0
        numbering = None
        status = None
        fatigue_level = 0
        oil_tank_capacity = 0
        balance_fuel_capacity = 0
        SD_Status = "0"
        SD_Type = "0"
        Channel_NO = None
        dt = 0
        Dw0 = 0
        Dw1 = 0
        Up0 = 0
        Up1 = 0
        Pat = 0
        Va = 0
        Cur = 0
        tm = None
        polling_mode = None
        end_time = None

        # Convert hex to ASCII and load JSON data
        ascii_result = self.hex_converter.convert_hex_to_ascii(content_hex)
        
        if ascii_result:
            
            json_data = json.loads(ascii_result)
            # Extract relevant fields from JSON data
            alert_datetime = json_data.get('dtu', '')
            start_time = json_data.get('st', '')
            end_time = json_data.get('et', '')
            event_type = json_data.get('ec', '')
            alarm_description = json_data.get('det', '')
            ec = event_type
            

            # Process based on event type
            if event_type == "0":  # unknown
                polling_mode = "unknown alert start" if not end_time else "unknown alert end"
            elif event_type == "1":  # video lost
                ch = alarm_description.get('ch', '')
                channel_no_alarm = int(ch)
                ChannelNO = ch
                polling_mode = f"video lost start" if not end_time else f"video lost end"

            elif event_type == "2":  # motion detection
                ch = alarm_description.get('ch', '')
                channel_no_alarm = int(ch)
                ChannelNO = ch
                polling_mode = f"motion detection start" if not end_time else f"motion detection end"
                

            elif event_type == "3":  # video blind
                ch = alarm_description.get('ch', '')
                channel_no_alarm = int(ch)
                ChannelNO = ch
                polling_mode = f"video blind start" if not end_time else f"video blind end"

            elif event_type == "4":  # input trigger
                ch = alarm_description.get('ch', '')
                channel_no_alarm = int(ch)
                num = int(alarm_description.get('num', ''))
                ChannelNO = ch
                if num == 0:
                    polling_mode = "close"
                elif num == 1:
                    polling_mode = "Emergency/ Panic"
                elif num == 2:
                    polling_mode = "F-door open"
                elif num == 3:
                    polling_mode = "M-door open"
                elif num == 4:
                    polling_mode = "B-door open"
                elif num == 5:
                    polling_mode = "Near light"
                elif num == 6:
                    polling_mode = "Far light"
                elif num == 9:
                    polling_mode = "R-Turn (right turn)"
                elif num == 10:
                    polling_mode = "L-Turn (left turn)"
                elif num == 11:
                    polling_mode = "Braking"
                elif num == 12:
                    polling_mode = "Reverse"
                elif num == 13:
                    polling_mode = "Reserved 1"
                elif num == 14:
                    polling_mode = "F-door close"
                elif num == 15:
                    polling_mode = "M-door close"
                elif num == 16:
                    polling_mode = "B-door close"
                elif num == 17:
                    polling_mode = "Talk (start the intercom)"
                elif num == 18:
                    polling_mode = "Raise up"
                elif num == 19:
                    polling_mode = "Airtight"
                elif num == 20:
                    polling_mode = "load"
                elif num == 22:
                    polling_mode = "Custom defines"
                elif num == 23:
                    polling_mode = "Safe to load"
                if channel_no_alarm == 2:
                    fuel_bar = 1
                elif channel_no_alarm == 3:
                    seat_belt = 1
                print(f"Input Trigger ==> #{unit_no}|{event_type}|{num}|{polling_mode}", "Input Trigger")

                
            elif event_type == "5":  # emergency alarm
                ch = alarm_description.get('ch', '')
                channel_no_alarm = int(ch)
                num = alarm_description.get('num', '')
                ChannelNO = ch
                polling_mode = "panic start" if not end_time else "panic end"
                panic = 1
                print(f"Input Trigger ==> #{unit_no}|{event_type}|{num}|{polling_mode}", "Input Trigger")

            elif event_type == "6":  # low speed alarm
                trigger_threshold = int(alarm_description.get('vt', ''))
                time_threshold = int(alarm_description.get('tt', ''))
                max = int(alarm_description.get('max', ''))
                min = int(alarm_description.get('min', ''))
                average = int(alarm_description.get('avg', ''))
                current_value = int(alarm_description.get('cur', ''))
                previous_value = int(alarm_description.get('pre', '')) / 100 if alarm_description.get('pre', '') else 0
                if not end_time:
                    polling_mode = "lowspeed start"
                else:
                    polling_mode = "lowspeed end"
                
            elif event_type == "7":  # over speed alarm
                trigger_threshold = int(alarm_description.get('vt', ''))
                time_threshold = int(alarm_description.get('tt', ''))
                max_value = int(alarm_description.get('max', ''))
                min_value = int(alarm_description.get('min', ''))
                average_value = int(alarm_description.get('avg', ''))
                current_value = int(alarm_description.get('cur', ''))
                previous_value = int(alarm_description.get('pre', '')) / 100 if alarm_description.get('pre', '') else 0
                if not end_time:
                    polling_mode = "overspeed start"
                else:
                    polling_mode = "overspeed end"
                over_speed = 1
            elif event_type == "8":  # low temperature alarm
                trigger_threshold = int(alarm_description.get('vt', ''))
                time_threshold = int(alarm_description.get('tt', ''))
                max = int(alarm_description.get('max', ''))
                min = int(alarm_description.get('min', ''))
                average = int(alarm_description.get('avg', ''))
                current_value = int(alarm_description.get('cur', ''))
                previous_value = int(alarm_description.get('pre', '')) / 100 if alarm_description.get('pre', '') else 0
                if not end_time:
                    polling_mode = "low temperature start"
                else:
                    polling_mode = "low temperature end"

            elif event_type == "9":  # high temperature alarm
                trigger_threshold = int(alarm_description.get('vt', ''))
                time_threshold = int(alarm_description.get('tt', ''))
                max = int(alarm_description.get('max', ''))
                min = int(alarm_description.get('min', ''))
                average = int(alarm_description.get('avg', ''))
                current_value = int(alarm_description.get('cur', ''))
                previous_value = int(alarm_description.get('pre', '')) / 100 if alarm_description.get('pre', '') else 0
                if not end_time:
                    polling_mode = "high temperature start"
                else:
                    polling_mode = "high temperature end"

            elif event_type == "10":  # humidity alarm
                if not end_time:
                    polling_mode = "humidity start"
                else:
                    polling_mode = "humidity end"

            elif event_type == "11":  # parking over time 
                vt = alarm_description.get('vt', '')
                st = alarm_description.get('st', '')
                if not end_time:
                    polling_mode = "parking overtime start"
                else:
                    polling_mode = "parking overtime end"

            elif event_type == "12":  # acceleration alarm
                trigger_threshold = int(alarm_description.get('vt', ''))
                time_threshold = int(alarm_description.get('tt', ''))
                max = int(alarm_description.get('max', ''))
                min = int(alarm_description.get('min', ''))
                average = int(alarm_description.get('avg', ''))
                current_value = int(alarm_description.get('cur', ''))
                direction = int(alarm_description.get('dt', ''))
                previous_value = int(alarm_description.get('pre', '')) / 100 if alarm_description.get('pre', '') else 0
                dt = int(alarm_description.get('dt', '')) # same as direction = dt value
                if not end_time:
                    if direction == 1:
                        polling_mode = "xaccel start"
                    elif direction == 2:
                        polling_mode = "yaccel start"
                    elif direction == 3:
                        polling_mode = "zaccel start"
                    elif direction == 4:
                        polling_mode = "impact start"
                    elif direction == 5:
                        polling_mode = "tilt start"
                    elif direction == 6:
                        polling_mode = "turn start"
                    elif direction == 7:
                        polling_mode = "Harsh acceleration start"
                    elif direction == 8:
                        polling_mode = "harsh braking start"
                    
                elif end_time:
                    if direction == 1:
                        polling_mode = "xaccel end"
                    elif direction == 2:
                        polling_mode = "yaccel end"
                    elif direction == 3:
                        polling_mode = "zaccel end"
                    elif direction == 4:
                        polling_mode = "impact end"
                    elif direction == 5:
                        polling_mode = "tilt end" 
                    elif direction == 6:
                        polling_mode = "turn end"
                    elif direction == 7:
                        polling_mode = "Harsh acceleration end"
                    elif direction == 8:
                        polling_mode = "harsh braking end" 
                    self.video_downloader.perform_download(unit_no, dt, start_time, end_time, event_type) 

            elif event_type == "13":  # GEO fencing  
                if not end_time:
                    polling_mode = "GEO fencing start"
                else:
                    polling_mode = "GEO fencing end"

            elif event_type == "14":  # electronic route
                num = alarm_description.get('num', '')
                st = alarm_description.get('st', '')
                if st == "0":
                    status = "ENTER"
                elif st == "1":
                    status = "LEAVE"
                elif st == "2":
                    status = "over speed alarm"
                elif st == "3":
                    status = "over speed warning"
                elif st == "4":
                    status = "low speed alarm"
                elif st == "5":
                    status = "low speed warning"
                elif st == "6":
                    status = "forbidden parking engine star"
                elif st == "7":
                    status = "forbidden parking engine off"
                elif st == "8":
                    status = "overtime stay in geofence"
                elif st == "9":
                    status = "Pre-entry"
                elif st == "10":
                    status = "Pre-exit"
                if not end_time:
                    polling_mode = "GEO fencing start"
                else:
                    polling_mode = "GEO fencing end"

            elif event_type == "15":  # abnormal openclose the door 
                ch = alarm_description.get('ch', '')
                num = alarm_description.get('num', '')
                st = alarm_description.get('st', '')
                ChannelNO = ch
                if st == "0":
                    status = "CLOSE"
                elif st == "1":
                    status = "OPEN"
                if not end_time:
                    polling_mode = "abnormal openclose door start"
                else:
                    polling_mode = "abnormal openclose door end"
               
            elif event_type == "16":  # storage abnormal
                Records_count = None
                num = alarm_description.get('num', '')
                st = alarm_description.get('st', '')
                if st == "0":
                    status = "LOSS"
                elif st == "1":
                    status = "BROKEN"
                elif st == "2":
                    status = "CANNOT OVERWRITE"
                elif st == "3":
                    status = "WRITE BLOCK FAIL"
                elif st == "4":
                    status = "DISK BROKEN"
                else:
                    status = "AVAILABLE"
                
                SD_Type = num
                SD_Status = status
                if not end_time:
                    polling_mode = "storage abnormal start"
                    Records_count = self.records_count.get_or_create_count(unit_no)
                    if Records_count == "6":
                        self.database_manager.abnormal_data(unit_no, alert_datetime,SD_Type,SD_Status,polling_mode, None, "Not Updated")
                    else:
                        pass
                else:
                    polling_mode = "storage abnormal end"
                    Records_count = self.records_count.reset_count(unit_no)

            elif event_type == "17":  # fatigue driving 
                fatiguelevel = int(alarm_description.get('de', ''))
                if not end_time:
                    polling_mode = "fatigue driving start"
                else:
                    polling_mode = "fatigue driving end"
            
            elif event_type == "18":  # fuel consumption abnormal
                triggerthreshold = int(alarm_description.get('vt', ''))
                oiltankcapacity = int(alarm_description.get('to', ''))
                balancefuelcapacity = int(alarm_description.get('fr', ''))
                alarmType = alarm_description.get('dt', '')
                if alarmType == "1":
                    status = "Refuel"
                elif alarmType == "2":
                    status = "Fuel theft"

                if not end_time:
                    polling_mode = "fuel consumption abnormal start"
                else:
                    polling_mode = "fuel consumption abnormal end"
                
            elif event_type == "19" or event_type == "31":  # illegal ACC
                if not end_time:
                    polling_mode = "illegal ACC start"
                else:
                    polling_mode = "illegal ACC end"

            elif event_type == "20":  # GPS module abnormal
                if not end_time:
                    polling_mode = "GPS module abnormal start"
                else:
                    polling_mode = "GPS module abnormal end"
            
            elif event_type == "21":  # front panel open
                if not end_time:
                    polling_mode = "front panel open start"
                else:
                    polling_mode = "front panel open end"

            elif event_type == "22":  # swipe card details
                cn = alarm_description.get('cn', '')
                ht = alarm_description.get('ht', '')
                up = alarm_description.get('up', '')

                carddetails = str(cn)
                if (
                    "?" in carddetails
                    and "%" in carddetails
                    and "^" in carddetails
                    and ";" in carddetails
                    and "+" in carddetails
                    and "$" in carddetails
                ):
                    indexofFirstQuestionMark = carddetails.index("?")
                    indexofSecondQuestionMark = carddetails.index("?", indexofFirstQuestionMark + 1)
                    indexofThirdQuestionMark = carddetails.index("?", indexofSecondQuestionMark + 1)

                    drivername = carddetails[
                        carddetails.index("%") + 1 : indexofFirstQuestionMark - carddetails.index("%") - 1
                    ].replace("^", "").strip()

                    arrdrivername = drivername.split("$")
                    finaldrivername = arrdrivername[0] + " " + arrdrivername[1]
                    finaldrivername = finaldrivername.strip()

                    gender = arrdrivername[2]

                    driverID = carddetails[
                        carddetails.index(";") + 1 : carddetails.index("?", carddetails.index("?") + 1) - carddetails.index(";") - 1
                    ]
                    arrdriverID = driverID.split("=")
                    finaldriverID = arrdriverID[0]
                    finaldriverlicenseID = arrdriverID[1]

                    driverIDtype = carddetails[
                        carddetails.index("+") + 1 : indexofThirdQuestionMark - carddetails.index("+") - 1
                    ].strip()
                    finaldriverIDtype = driverIDtype[: driverIDtype.index(" ")].strip()

                    indexofFirstDollor = carddetails.index("$", indexofThirdQuestionMark) + 1
                    indexofSecondDollor = carddetails.index("$", indexofFirstDollor) + 1

                    validcard = carddetails[indexofFirstDollor]
                    loginlogout = carddetails[indexofSecondDollor]

                elif carddetails != "" and carddetails is not None:  # other than Thailand or Dallas button
                    carddetails = carddetails[::-1]

                if not end_time:
                    polling_mode = "swipe card start"
                else:
                    polling_mode = "swipe card end"

            elif event_type == "23":  # ibutton
                if not end_time:
                    polling_mode = "ibutton start"
                else:
                    polling_mode = "ibutton end"

            elif event_type == "24":  # harsh acceleration
                triggerthreshold = int(alarm_description.get('vt', ''))
                timethreshold = int(alarm_description.get('tt', ''))
                max_value = int(alarm_description.get('max', ''))
                min_value = int(alarm_description.get('min', ''))
                average = int(alarm_description.get('avg', ''))
                currentvalue = int(alarm_description.get('cur', ''))
                previousvalue = int(alarm_description.get('pre', ''))/100

                if not end_time:
                    polling_mode = "ha start"
                else:
                    polling_mode = "ha end"
                ha = 1
            elif event_type == "25":  # harsh braking
                triggerthreshold = int(alarm_description.get('vt', ''))
                timethreshold = int(alarm_description.get('tt', ''))
                max_value = int(alarm_description.get('max', ''))
                min_value = int(alarm_description.get('min', ''))
                average = int(alarm_description.get('avg', ''))
                currentvalue = int(alarm_description.get('cur', ''))
                previousvalue = int(alarm_description.get('pre', '')) / 100

                if not end_time:
                    polling_mode = "hb start"
                else:
                    polling_mode = "hb end"
                hb = 1

            elif event_type == "26":  # low speed warning
                triggerthreshold = int(alarm_description.get('vt', ''))
                timethreshold = int(alarm_description.get('tt', ''))
                max_value = int(alarm_description.get('max', ''))
                min_value = int(alarm_description.get('min', ''))
                average = int(alarm_description.get('avg', ''))
                currentvalue = int(alarm_description.get('cur', ''))
                previousvalue = int(alarm_description.get('pre', '')) / 100

                if not end_time:
                    polling_mode = "lowspeed warn start"
                else:
                    polling_mode = "lowspeed warn end"

            elif event_type == "27":  # high speed warning
                trigger_threshold = int(alarm_description.get('vt', ''))
                time_threshold = int(alarm_description.get('tt', ''))
                max_value = int(alarm_description.get('max', ''))
                min_value = int(alarm_description.get('min', ''))
                average = int(alarm_description.get('avg', ''))
                current_value = int(alarm_description.get('cur', ''))
                previous_value = int(alarm_description.get('pre', '')) / 100

                if not end_time:
                    polling_mode = "overspeed warn start"
                else:
                    polling_mode = "overspeed warn end"

            elif event_type == "28":  # low voltage or main power
                dt = int(alarm_description.get('dt', ''))
                if dt == 1:
                    polling_mode = "low voltage"
                elif dt == 2:
                    polling_mode = "high voltage"
                elif dt == 3:
                    polling_mode = "Power off"
                elif dt == 4 or dt == 7:
                    polling_mode = "Power on"
                elif dt == 5:
                    polling_mode = "Power off when moving"
                elif dt == 6:
                    polling_mode = "Low voltage shutdown"

            elif event_type == "29":  # People Counting

                Dw0 = int(alarm_description.get('dw0', ''))
                Dw1 = int(alarm_description.get('dw1', ''))
                Up0 = int(alarm_description.get('up0', ''))
                Up1 = int(alarm_description.get('up1', ''))
                Pat = int(alarm_description.get('pat', ''))
                Va = int(alarm_description.get('va', ''))
                Cur = int(alarm_description.get('cur', ''))
                tm = alarm_description.get('tm', '')

                if not end_time:
                    polling_mode = "People Counting"
                else:
                    polling_mode = "People Counting"
                print(f"People Counting ==> #{unit_no}|{alert_datetime}|{event_type}|{tp}|{polling_mode}|Up0:{Up0}|Dw0:{Dw0}|Up1:{Up1}|Dw1:{Dw1}|tm:{tm}|Pat:{Pat}|va:{Va}","People Counting")
                print(f"People Counting Ascii ==> #{unit_no}|{alert_datetime}|{ascii_result}", "People Counting")

            elif event_type == "30":  # DMS and ADAS Alarm
                tp = int(alarm_description.get('tp', ''))

                if tp == 2 or tp == 5 or tp == 19 or tp == 20:
                    polling_mode = "Lane Change"
                elif tp == 17:
                    polling_mode = "Front Collision"
                elif tp == 18:
                    polling_mode = "Head Way Monitoring"
                elif tp == 33:
                    polling_mode = "Driver Fatigue"
                elif tp == 34:
                    polling_mode = "Mobile Phone Usage"
                elif tp == 35:
                    polling_mode = "Smoking Alerts"
                elif tp == 36 or tp == 68:
                    polling_mode = "Driver Distraction"
                elif tp == 65:
                    polling_mode = "Eye closed"
                elif tp == 66:
                    polling_mode = "Yawning"
                elif tp == 67:
                    polling_mode = "Camera cover"
                elif tp == 69:
                    polling_mode = "Seat belt not closed"
                elif tp == 70:
                    polling_mode = "No driver"
                elif tp == 71:
                    polling_mode = "Liquid Drinking"
                else:
                    polling_mode = "ADAS"
                print(f"ADAS Alarm ==> #{unit_no}|{event_type}|{tp}|{polling_mode}", "ADAS Alarm")

            # elif event_type == "31":  # illegal ACC ON
            #     if not end_time:
            #         polling_mode = "illegal ACC start"
            #     else:
            #         polling_mode = "illegal ACC end"

            #     # polling_mode = "PowerOn"


            elif event_type == "32":  # idle alarm
                trigger_threshold = int(alarm_description.get('vt', ''))
                time_threshold = int(alarm_description.get('tt', ''))
                max_value = int(alarm_description.get('max', ''))
                min_value = int(alarm_description.get('min', ''))
                average_value = int(alarm_description.get('avg', ''))
                current_value = int(alarm_description.get('cur', ''))
                previous_value = int(alarm_description.get('pre', '')) / 100 if alarm_description.get('pre', '') else 0
                if not end_time:
                    polling_mode = "idle start"
                else:
                    polling_mode = "idle end"
            
            elif event_type == "33":  # Gps antenna break
                polling_mode = "Gps antenna break"

            elif event_type == "34":  # Gps antenna short
                polling_mode = "Gps antenna short"

            elif event_type == "35": # IO output
                polling_mode = "IO output"
            
            elif event_type == "36": # CAN Bus connection abnormal
                polling_mode = "CAN Bus connection abnormal"
            
            elif event_type == "37": # Towing
                polling_mode = "Towing"
            
            elif event_type == "38": # Free wheeling
                polling_mode = "Free wheeling"
            
            elif event_type == "39": # RPM exceeds
                polling_mode = "RPM exceeds"
            
            elif event_type == "40": # Vehicle Move
                polling_mode = "Vehicle Move"

            elif event_type == "41": # Trip start
                polling_mode = "Trip start"

            elif event_type == "42": # In trip
                polling_mode = "In trip"
            
            elif event_type == "43": # Trip ends (periodically report after acc off)
                polling_mode = "Trip ends (periodically report after acc off)"
            
            elif event_type == "44": # GPS location recover
                polling_mode = "GPS location recover"
            
            elif event_type == "45": # Video abnormal
                polling_mode = "Video abnormal"
            
            elif event_type == "768": # Trip notification
                polling_mode = "Trip notification"

            elif event_type == "769": # Upgrade notification
                polling_mode = "Upgrade notification"

            else:
                polling_mode = "Unknown"
                print("other Alarm ==> #" +unit_no+"|"+event_type+"|"+tp+"|"+polling_mode+"|"+content_hex+"Other Alarm")
           
            resprocessGpsServiceData = self.alarm_data_processor.process_alarm_service_data(unit_no, messageType, polling_mode, ha, hb, panic, fuel_bar,over_speed,analog,
                                                             seat_belt, previous_value, bit_data, version, ec, tp, SD_Type, SD_Status, device_Network_Type, 
                                                             alert_datetime, dt, Up0, Dw0, Up1, Dw1, tm, Va, Cur, Pat)

       


if __name__=="__main__":
    process_data = AlarmEventType()
    content_hex = "7b22646574223a7b22617667223a223638222c22637572223a223638222c226474223a2231222c226d6178223a223638222c226d696e223a223638222c22707265223a223638222c227474223a223230222c227674223a223335227d2c22647475223a22323032332d31322d30352031383a33323a3138222c226563223a223132222c226574223a22323032332d31322d30352031383a33323a3138222c227374223a22323032332d31322d30352031383a33323a3136222c2275756964223a223137303138303131333630303030313030303030303030303030303931303036227d"
    content_hex = content_hex.lower()
    unit_no = "91006"
    bit_data = "170c0512201eaf070001170c051220121a062100af010b004d454405000cdc2209000718000400000000001900010000001f000101000107000006050000010001eaed0000000000000f00000008000000000000003f00000000000000000000000100e4430000fa000000"
    messageType = "1051"
    version = "testing"
    device_Network_Type = "4G"
    process_data.event_processor(unit_no,content_hex,bit_data, messageType, version, device_Network_Type)