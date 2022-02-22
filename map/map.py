from turtle import distance
import requests
import os
import random
from math import sqrt, atan as arctan, cos, degrees, radians

class City:
    def __init__(self, name, lat, lon):
        self.name = str(name)
        self.lat = float(lat)
        self.lon = float(lon)

def delta_km(city1: City, city2: City):
    delta_lat = city1.lat - city2.lat
    delta_lon = city1.lon - city2.lon
    delta_lat_km = delta_lat * lat_conv
    delta_lon_km = delta_lon * long_conv * cos(radians((city1.lat + city2.lat)/2))
    delta_km = sqrt(delta_lat_km**2 + delta_lon_km**2)
    return delta_km

outfile = "conf.txt"
lat_conv  = 110.574
long_conv  = 111.320
if os.path.exists(outfile):
  os.remove(outfile)

cities = [
    "Jakarta",
    "Bandung",
    "Padang",
    "Medan",
    "Tasikmalaya",
    "Purwokerto",
    "Jogjakarta",
    "Magelang",
    "Semarang",
    "Klaten",
    "Jayapura",
    "Makassar",
    "Surabaya",
    "Balikpapan",
    "Manado",
    "Palembang",
    "Jayapura"
]
cities.sort()
cities_info = []
base_url = 'http://api.openweathermap.org/geo/1.0/direct'

with open(outfile,"a") as file:
    file.write("[nodes]\n")
for city in cities:
    params = {
        'q': city,
        'limit': 5,
        'appid': '874f6acc3c0bad4f9c019e59f8d8c6bc'
        }
    res = requests.get(base_url, params=params)
    data = res.json()
    try:
        name = data[0]["local_names"]["id"]
    except Exception as e:
        name = data[0]["name"]
    lat = data[0]["lat"]
    lon = data[0]["lon"]
    r = sqrt(lat**2 + lon**2)
    theta = degrees(arctan(lat/lon))
    if theta<0:
        theta = 360 - theta
        # print(f'{name+", ":>20}lat: {lat:>7.7f}, lon: {lon:>7.7f}, r: {r:>14.14f}, Θ:{theta:>14.14f}')
    with open(outfile,"a") as file:
        file.write(f'{name}: _ radius={r:>14.14f} angle={theta:>14.14f}\n')
    cities_info.append(City(name=name, lat=lat, lon=lon))

with open(outfile,"a") as file:
    file.write("\n[links]\n")
for i,city1 in enumerate(cities_info):
    for j,city2 in enumerate(cities_info):
        if j > i:
            distance = delta_km(city1, city2)
            with open(outfile,"a") as file:
                file.write(f'{city1.name}:{city2.name} delay={int(distance/299.792458+random.uniform(1,3))}ms\n')