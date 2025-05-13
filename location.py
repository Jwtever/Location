import requests
import openpyxl
import pandas as pd
import time
import sys

KEY = '6b3b39139eef2be3c1390650012586af'

# def Get_location(address):
#     url = 'https://restapi.amap.com/v3/geocode/geo'
#     params = {
#         "address": address,
#         "key": KEY,
#         "output": "json"
#     }
#     response = requests.get(url, params=params)
#     data = response.json()
#     if data['status'] == '1' and len(data['geocodes']) > 0:
#         location = data['geocodes'][0]['location'].split(',')
#         return float(location[1]), float(location[0])
#     else:
#         return None, None


class LocationInfo:
    def __init__(self):
        self.latitude = 0.0
        self.longtude = 0.0
        self.area = []
    def ShowInfo(self):
        print(f"Lat: {self.latitude}  Lon: {self.longtude} Area: {self.area}")


def FuzzySearch(address, city=None):
    url = "https://restapi.amap.com/v3/assistant/inputtips"
    params = {
        "keywords": address,
        "key": KEY,
        "output": "json"
    }
    if city:
        params["city"] = city
    
    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] == "1" and int(data["count"]) > 0:
        tips = data["tips"]
        return tips[0]["location"], tips[0]["address"]
    else:
        return None, None


def GetAreaInfoByLocation(location, address):
    url = "https://restapi.amap.com/v3/geocode/regeo"
    params = {
        "key": KEY,
        "location": location,
        "extensions": "base",
        "poitype": "",
        "radius": 1000,
        "batch": False,
        "roadlevel": 0
    }
    response = requests.get(url, params=params).json()
    if response["status"] != "1":
        return None
    
    address_component = response["regeocode"]["addressComponent"]
    locInfo = LocationInfo()
    locInfo.area.append(address_component["province"])
    locInfo.area.append(address_component["city"])
    locInfo.area.append(address_component["district"])
    locInfo.area.append(address)
    location_parts = location.split(",")
    locInfo.latitude = float(location_parts[0])
    locInfo.longtude = float(location_parts[1])
    return locInfo

# def GetAreaInfoByAdcode(adcode):
#     url = "https://restapi.amap.com/v3/config/district"
#     params = {
#         "key": KEY,
#         "keywords": adcode,
#         "subdistrict": 2,
#         "extensions": "base"
#     }
#
#     response = requests.get(url, params=params)
#     data = response.json()
#
#     if data["status"] == "1" and int(data["count"]) > 0:
#         print(data)
#         district = data["districts"][0]
#         province = district["name"]
#         city = district["districts"][0]["name"] if district["districts"] else ""
#         area = district["districts"][0]["districts"][0]["name"] if district["districts"] and district["districts"][0]["districts"] else ""
#         print(f"{province} {city} {area}")
#         return province, city, area
#
#     return None, None, None


if __name__ == '__main__':
    inputs = input("Inputs : ")
    location,address = FuzzySearch(inputs, city=None)
    assert(location and address)
    location_info = GetAreaInfoByLocation(location, address)
    location_info.ShowInfo()
