import xml.etree.ElementTree as et
import requests
import os
import gzip
import shutil
import matplotlib.pyplot as plt
import csv


def get_vdlive_speed(id):
    temp = []
    speed_matrix = []
    namespace = {
        "ns": "http://traffic.transportdata.tw/standard/traffic/schema/"}
    for hour in range(17, 21, 1):
        for i in range(6):
            for j in range(0, 10, 1):
                vdlive_tree = et.parse(
                    f'./vd_uncompressed_data/{hour}{i}{j}.xml')
                vd_lives = vdlive_tree.findall(
                    "./ns:VDLives/ns:VDLive", namespace)
                for vd_live in vd_lives:
                    link_id = vd_live.find(
                        './ns:LinkFlows/ns:LinkFlow/ns:LinkID', namespaces=namespace).text
                    if link_id == id:
                        sum = 0
                        temp = []
                        lanes = vd_live.findall(
                            "./ns:LinkFlows/ns:LinkFlow/ns:Lanes/ns:Lane", namespace)
                        for lane in lanes:
                            speed_by_lane = int(
                                lane.find("ns:Speed", namespaces=namespace).text)
                            if speed_by_lane != 0:
                                temp.append(speed_by_lane)  # speed_matrix[車道]
                        for a in temp:
                            sum = sum + a
                        avg = sum / len(temp)
                        speed_matrix.append(avg)
    return speed_matrix


def get_live_traffic_speed(id):
    live_traffic_matrix = []
    namespace = {
        "ns": "http://traffic.transportdata.tw/standard/traffic/schema/"}
    for hour in range(17, 21, 1):
        for i in range(0, 6, 1):
            for j in range(0, 10, 1):
                trafficlive_tree = et.parse(
                    f'./livetraffic_uncompressed_data/{hour}{i}{j}.xml')
                live_traffics = trafficlive_tree.findall(
                    "./ns:LiveTraffics/ns:LiveTraffic", namespaces=namespace)
                for live_traffic in live_traffics:
                    section_id = live_traffic.find(
                        "./ns:SectionID",  namespaces=namespace).text
                    if section_id == id:
                        travel_speed = int(live_traffic.find(
                            "ns:TravelSpeed",  namespaces=namespace).text)
                        live_traffic_matrix.append(travel_speed)
    return (live_traffic_matrix)


# 偽裝成瀏覽器
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
os.mkdir('vd_compressed_data')
os.mkdir('vd_uncompressed_data')
os.mkdir('livetraffic_compressed_data')
os.mkdir('livetraffic_uncompressed_data')
for hour in range(17, 21, 1):
    for i in range(6):
        for j in range(0, 10, 1):
            # 讀VD動態資料
            url = f'https://tisvcloud.freeway.gov.tw/history/motc20/VD/20231229/VDLive_{hour}{i}{j}.xml.gz'
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                with open(f'./vd_compressed_data/{hour}{i}{j}.xml.gz', "wb") as file:
                    # 防止記憶體爆滿，改成以每102400 bytes的資料量讀進來
                    for chunk in response.iter_content(102400):
                        file.write(chunk)
                with gzip.open(f'./vd_compressed_data/{hour}{i}{j}.xml.gz', 'rb') as gz_file, open(
                        f'./vd_uncompressed_data/{hour}{i}{j}.xml', 'wb') as uncompressed_file:
                    shutil.copyfileobj(gz_file, uncompressed_file)
            else:
                print(f'VD {hour}{i}{j}:{response.status_code}')

for hour in range(17, 21, 1):
    for i in range(6):
        for j in range(0, 10, 1):
            # 即時路況
            url = f'https://tisvcloud.freeway.gov.tw/history/motc20/Section/20231229/LiveTraffic_{hour}{i}{j}.xml.gz'
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                with open(f'./livetraffic_compressed_data/{hour}{i}{j}.xml.gz', "wb") as file:
                    for chunk in response.iter_content(102400):
                        file.write(chunk)
                with gzip.open(f'./livetraffic_compressed_data/{hour}{i}{j}.xml.gz', 'rb') as gz_file, open(f'./livetraffic_uncompressed_data/{hour}{i}{j}.xml', 'wb') as uncompressed_file:
                    shutil.copyfileobj(gz_file, uncompressed_file)
            else:
                print(f'live:{hour}{i}{j}:{response.status_code}')

# # 載section對照檔:section0000, sectionlink_0000
url = 'https://tisvcloud.freeway.gov.tw/history/motc20/Section/20231229/SectionLink_0000.xml.gz'
response = requests.get(url, headers=headers)
with open('SectionLink_0000.xml.gz', "wb") as file:
    for chunk in response.iter_content(102400):
        file.write(chunk)
with gzip.open('SectionLink_0000.xml.gz', 'rb') as gz_file, open('SectionLink_0000.xml', 'wb') as uncompressed_file:
    shutil.copyfileobj(gz_file, uncompressed_file)

url = 'https://tisvcloud.freeway.gov.tw/history/motc20/Section/20231229/Section_0000.xml.gz'
response = requests.get(url, headers=headers)
with open('Section_0000.xml.gz', "wb") as file:
    for chunk in response.iter_content(102400):
        file.write(chunk)
with gzip.open('Section_0000.xml.gz', 'rb') as gz_file, open('Section_0000.xml', 'wb') as uncompressed_file:
    shutil.copyfileobj(gz_file, uncompressed_file)

# -----竹北-----
# 開始用vd資料，找到我們想要的路段資料速度

vd_speed_matrix1 = get_vdlive_speed('0000100108900J')  # 竹北
vd_speed_matrix2 = get_vdlive_speed('0000100102700F')  # 三重
vd_speed_matrix3 = get_vdlive_speed('0000100109860J')  # 寶山

live_traffic_matrix1 = get_live_traffic_speed('0056')  # 竹北
live_traffic_matrix2 = get_live_traffic_speed('0024')  # 三重
live_traffic_matrix3 = get_live_traffic_speed('0060')  # 寶山


for i, matrix in enumerate([vd_speed_matrix1, vd_speed_matrix2, vd_speed_matrix3]):
    plt.plot(range(len(matrix)), matrix)
    plt.xlabel('time')
    plt.ylabel('speed')
    plt.title(f'VD_data_average_speed_{i+1}')
    if i == 0:
        district = '竹北'
    elif i == 1:
        district = '三重'
    else:
        district = '寶山'
    plt.savefig(f'VD_speed_{district}.png')
    plt.clf()

for i, matrix in enumerate([live_traffic_matrix1, live_traffic_matrix2, live_traffic_matrix3]):
    plt.plot(range(len(matrix)), matrix)
    plt.xlabel('time')
    plt.ylabel('speed')
    plt.title(f'live_traffic_data_average_speed_{i+1}')
    if i == 0:
        district = '竹北'
    elif i == 1:
        district = '三重'
    else:
        district = '寶山'
    plt.savefig(f'live_traffic_speed_{district}.png')
    plt.clf()

with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['竹北_vd_speed', '竹北_live_traffic_speed', '三重_vd_speed',
                    '三重_live_traffic_speed', '寶山_vd_speed', '寶山_live_traffic_speed'])
    for a, b, c, d, e, f in zip(vd_speed_matrix1, live_traffic_matrix1, vd_speed_matrix2, live_traffic_matrix2, vd_speed_matrix3, live_traffic_matrix3):
        writer.writerow([a, b, c, d, e, f])
