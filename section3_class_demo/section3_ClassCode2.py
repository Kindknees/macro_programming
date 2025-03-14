import numpy as np
import xml.etree.ElementTree as et
import os

xml_file_path = "C:/Users/gerry/Desktop/python/macro_programming/VDLive_2359.xml/"
xml_file_name = "VDLive_2359.xml"

speed_matrix = np.zeros(4)
occ_matrix = np.zeros(4)
vol_matrix = np.zeros((4, 3))  # [lane_index][vehicle_type_index]
speed_matrix_by_veh_typ = np.zeros((4, 3))

namespace = {"ns": "http://traffic.transportdata.tw/standard/traffic/schema/"}
tree = et.parse(os.path.join(xml_file_path, xml_file_name))
vd_lives = tree.findall("./ns:VDLives/ns:VDLive", namespaces=namespace)

for vd_live in vd_lives:
    vd_id = vd_live.find("./ns:VDID",  namespaces=namespace).text
    if vd_id == "VD-N1-N-92.900-M-LOOP":
        lanes = vd_live.findall(
            "./ns:LinkFlows/ns:LinkFlow/ns:Lanes/ns:Lane", namespaces=namespace)
        for lane in lanes:
            lane_id = int(lane.find("ns:LaneID", namespaces=namespace).text)
            speed_by_lane = int(
                lane.find("ns:Speed", namespaces=namespace).text)
            occupancy = int(
                lane.find("ns:Occupancy", namespaces=namespace).text)
            speed_matrix[lane_id] = speed_by_lane  # speed_matrix[車道]
            occ_matrix[lane_id] = occupancy  # occ_matrix[車道]

            vehicles = lane.findall(".//ns:Vehicle", namespaces=namespace)

            for vehicle in vehicles:
                vehicle_type = vehicle.find(
                    "ns:VehicleType", namespaces=namespace).text
                speed_by_veh = int(vehicle.find(
                    "ns:Speed", namespaces=namespace).text)
                volume = int(vehicle.find(
                    "ns:Volume", namespaces=namespace).text)
                # 將vehicle type對應到矩陣
                if vehicle_type == "S":
                    vehicle_type_index = 0
                elif vehicle_type == "L":
                    vehicle_type_index = 1
                elif vehicle_type == "T":
                    vehicle_type_index = 2
                speed_matrix_by_veh_typ[lane_id][vehicle_type_index] = speed_by_veh
                vol_matrix[lane_id][vehicle_type_index] = volume

        print('VDID, ', end='')
        for lane_index in range(4):
            for vehicle_index in ['S', 'L', 'T']:
                for type in ['spd', 'vol']:
                    print(f'Lane_{lane_index}_{
                          vehicle_index}_{type}, ', end='')
