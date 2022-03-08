import requests
import os
import random
import json
from math import sqrt, atan as arctan, cos, degrees, radians
import networkx as nx
import matplotlib.pyplot as plt

def delta_km(city1: str, city2: str, data: dict):
    lat1, lon1 = data[city1]["cartesian_coord"]
    lat2, lon2 = data[city2]["cartesian_coord"]
    delta_lat = lat1 - lat2
    delta_lon = lon1 - lon2
    delta_lat_km = delta_lat * lat_conv
    delta_lon_km = delta_lon * long_conv * cos(radians((lat1 + lat2)/2))
    delta_km = sqrt(delta_lat_km**2 + delta_lon_km**2)
    return delta_km

outfile = "tesis5.conf"
lat_conv  = 110.574
long_conv  = 111.320
if os.path.exists(outfile):
  os.remove(outfile)

cities = {
    "Medan": {"neighbors": ["Bengkulu", "Jambi", "Batam"]},
    "Bengkulu": {"neighbors": ["Medan", "Palembang"]},
    "Jambi": {"neighbors": ["Medan", "Palembang"]},
    "Batam": {"neighbors": ["Medan",  "Jambi"]},
    "Palembang": {"neighbors": ["Bengkulu", "Jambi"]},
}
cities_info = []
base_url = 'http://api.openweathermap.org/geo/1.0/direct'
G = nx.Graph()
pos = {}

with open(outfile,"a") as file:
    file.write("[nodes]\n")
for city in cities:
    params = {
        'q': f'{city},ID',
        'limit': 5,
        'appid': '874f6acc3c0bad4f9c019e59f8d8c6bc'
        }
    res = requests.get(base_url, params=params)
    data = res.json()
    try:
        name = data[0]["local_names"]["id"]
    except KeyError as e:
        name = data[0]["name"]
    except Exception as e:
        print(e)
    lat = data[0]["lat"]
    lon = data[0]["lon"]
    r = sqrt(lat**2 + lon**2)
    theta = degrees(arctan(lat/lon))
    if theta<0:
        theta = 360 - theta
        # print(f'{name+", ":>20}lat: {lat:>7.7f}, lon: {lon:>7.7f}, r: {r:>14.14f}, Θ:{theta:>14.14f}')
    with open(outfile,"a") as file:
        file.write(f'{name}: _ radius={r:>14.14f} angle={theta:>14.14f}\n')
    cities[city]["cartesian_coord"] = (lat,lon)
    cities[city]["polar_coord"] = (r,theta)
    G.add_node(city, pos=(lat,lon))
    pos[city] = (lon,lat)

with open("debug.json","w") as file:
    json.dump(cities, file, indent=4)

with open(outfile,"a") as file:
    file.write("\n[links]\n")

checklist = []
for src, value in cities.items():
    for dst in value["neighbors"]:
        if (src,dst) not in checklist and (dst,src) not in checklist:
            checklist.append((src,dst))
            G.add_edge(src,dst)
            distance = delta_km(src, dst, cities)
            with open(outfile,"a") as file:
                file.write(f'{src}:{dst} delay={int(distance/299.792458+random.uniform(1,3))}ms\n')
nx.draw(G,pos=pos,with_labels=True)
plt.show()