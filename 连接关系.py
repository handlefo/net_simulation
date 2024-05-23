import math
import os
import json5
import time
from datetime import datetime
from datetime import timedelta

EARTH_RADIUS = 6371000
LIGHT_SPEED = 299792458

class Position:
    def __init__(self, longitude, latitude,identifier):
        self.longitude = longitude
        self.latitude = latitude
        self.identifier = identifier

class Setting:
    def __init__(self, time_scheduler, loss_value, delay_value, bandwidth):
        self.time_scheduler = time_scheduler
        self.loss_value = loss_value
        self.delay_value = delay_value
        self.bandwidth = bandwidth

def calculate_satellite_position(current_longitude, current_latitude, period, identifier):
    current_latitude_rad = math.radians(current_latitude)

    # Calculate satellite speed (distance per second)
    speed = 2 * math.pi * EARTH_RADIUS * math.cos(current_latitude_rad) / period
    print(" speed:", speed)
    print(" identifier:", identifier)
    a=identifier

    # Calculate new latitude
    new_latitude_rad = current_latitude_rad + identifier * speed / EARTH_RADIUS
    print(" new_latitude_rad:", new_latitude_rad)

    if new_latitude_rad > math.pi / 2:
        new_latitude_rad = math.pi / 2
        identifier = -1 if identifier == 1 else 1
    elif new_latitude_rad < -math.pi / 2:
        new_latitude_rad = -math.pi / 2
        identifier = -1 if identifier == 1 else 1
    
    new_latitude = math.degrees(new_latitude_rad)

    print(" new_latitude_rad:", new_latitude_rad)
    # Calculate new longitude based on the rules provided
    if identifier == a:
        new_longitude = current_longitude
    else:
        if current_longitude == 0:
            new_longitude = 180 
        else:
            new_longitude = -(180 - abs(current_longitude))*(current_longitude / abs(current_longitude))

    return Position(new_longitude, new_latitude , identifier)

def calculate_distance(longitude1, latitude1, longitude2, latitude2,i,j):
    longitude1_rad = math.radians(longitude1)
    latitude1_rad = math.radians(latitude1)
    longitude2_rad = math.radians(longitude2)
    latitude2_rad = math.radians(latitude2)

    delta_longitude = longitude2_rad - longitude1_rad
    delta_latitude = latitude2_rad - latitude1_rad

    a = math.sin(delta_latitude / 2) ** 2 + math.cos(latitude1_rad) * math.cos(latitude2_rad) * math.sin(delta_longitude / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = EARTH_RADIUS * c

    print("两颗卫星之间的距禯为:", i+1,j+1,distance,longitude1, latitude1, longitude2, latitude2)
    
    return distance

def calculate_satellite_params(lon1, lat1, lon2, lat2, period, time, threshold_distance,i,j):
    distance = calculate_distance(lon1, lat1, lon2, lat2,i,j)

    if distance < threshold_distance:
        loss_value = int((distance / threshold_distance) * 100)
        delay_value = int(distance*1000 / LIGHT_SPEED)
        time_scheduler = f"{int(time / 3600):02d}:{int(time / 60) % 60:02d}:00"
        bandwidth = 1/(math.log((1+(37324800/distance^2)), 2))
    else:
        loss_value = 100
        delay_value = -1
        time_scheduler = f"{int(time / 3600):02d}:{int(time / 60) % 60:02d}:00"
        bandwidth = 0

    return Setting(time_scheduler, loss_value, delay_value, bandwidth)

def write_satellite(satellite_params, satellite1, satellite2, file_path,current_time):

    time_scheduler = datetime.strptime(satellite_params.time_scheduler, "%H:%M:%S").time()
    new_time = current_time + timedelta(hours=time_scheduler.hour, minutes=time_scheduler.minute, seconds=time_scheduler.second) + timedelta(minutes=25)

    result = [
        {
        "timeScheduler": new_time.strftime("%Y-%m-%d %H:%M:%S"),
        "lossValue": satellite_params.loss_value,
        "delayValue": satellite_params.delay_value,
        "bandWidth": satellite_params.bandwidth
    }
    ]

    # 将数据转换为 JSON5 格式的字符串
    data_str = json5.dumps(result, ensure_ascii=False, indent=4,separators=(',', ':'))

    with open(file_path, "w") as file:
        file.write(data_str)

def write_satellite2(satellite_params, satellite1, satellite2, file_path,current_time):

    time_scheduler = datetime.strptime(satellite_params.time_scheduler, "%H:%M:%S").time()
    new_time = current_time + timedelta(hours=time_scheduler.hour, minutes=time_scheduler.minute, seconds=time_scheduler.second) + timedelta(minutes=15)

    result = {
        "satellite1":satellite1,
        "satellite2":satellite2,
        "timeScheduler": new_time.strftime("%Y-%m-%d %H:%M:%S"),
        "lossValue": satellite_params.loss_value,
        "delayValue": satellite_params.delay_value,
        "bandWidth": satellite_params.bandwidth
    }

    # 将数据转换为 JSON5 格式的字符串
    data_str = json5.dumps(result, ensure_ascii=False, indent=4)

    with open(file_path, "w") as file:
        file.write(data_str)

def update_satellite_position(lon, lat, period,identifier):
    return calculate_satellite_position(lon, lat, period,identifier)

def calculate_satellite_period(altitude):
    orbital_height = altitude + EARTH_RADIUS
    period = 2 * math.pi * math.sqrt(orbital_height**3 / (6.67430e-11 * 5.97219e24))
    return period

def check_same_longitude_track(lon1, lon2):
    if lon1 == lon2 or abs(lon1 + lon2) == 180:
        return 1
    else:
        return 0

def main():
    current_time = datetime.now()# 读取设备的当前时间

    #satellite_count = int(input("Please enter the number of satellites: "))
    #latitude_threshold = float(input("Please enter the latitude threshold: "))
    satellite_count = 9
    latitude_threshold = 85
    
    satellite_positions = []
    for i in range(satellite_count):
        longitude = float(input(f"Please enter the longitude of satellite {i + 1}: "))
        latitude = float(input(f"Please enter the latitude of satellite {i + 1}: "))
        identifier = float(input(f"Please enter the identifier of satellite {i + 1}: "))
        satellite_positions.append(Position(longitude, latitude,identifier))

    altitude = float(input("Please enter the altitude of the orbit (in meters): "))
    period = calculate_satellite_period(altitude)

    mytime = 0
    distance_threshold = 100000000

    file_path = input("Please enter the file path to save the satellite data: ")
    file_path2=r"D:\test\info"

    while True:
        for i in range(satellite_count):
            lon1, lat1 = satellite_positions[i].longitude, satellite_positions[i].latitude
            for j in range(i + 1, satellite_count):
                lon2, lat2 = satellite_positions[j].longitude, satellite_positions[j].latitude
                
                if (satellite_positions[i].identifier == satellite_positions[j].identifier and abs(lat1)<latitude_threshold and abs(lat2)<latitude_threshold) or (check_same_longitude_track(lon1, lon2)==1):
                    params = calculate_satellite_params(lon1, lat1, lon2, lat2, period, mytime, distance_threshold,i,j)
                else:
                    params = Setting(f"{int(mytime / 3600):02d}:{int(mytime / 60) % 60:02d}:00", 100, 0, 10)

                satellite1 = f"satellite {i + 1}"
                satellite2 = f"satellite {j + 1}"
                a=0
                file_name = f"result_{min(satellite1, satellite2)}_{max(satellite1, satellite2)}_a.json5"
                a=a+1
                file_name2 = f"result_{min(satellite1, satellite2)}_{max(satellite1, satellite2)}.json5"
                file_path_with_name = f"{file_path}/{file_name}"
                file_path_with_name2 = f"{file_path2}/{file_name2}"
                write_satellite(params, satellite1, satellite2, file_path_with_name,current_time)
                write_satellite2(params, satellite1, satellite2, file_path_with_name2,current_time)

        for k in range(satellite_count):
            lon, lat = satellite_positions[k].longitude, satellite_positions[k].latitude
            satellite_positions[k] = update_satellite_position(lon, lat, period, satellite_positions[k].identifier)
        
        mytime += 1
        time.sleep(1)  # 等待1秒


if __name__ == "__main__":
    main()