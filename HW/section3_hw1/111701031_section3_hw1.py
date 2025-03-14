import requests

for i in range(6):
    for j in range(0, 6, 5):
        url = f'https://tisvcloud.freeway.gov.tw/history/TDCS/M03A/20231218/23/TDCS_M03A_20231218_23{
            i}{j}00.csv'
        response = requests.get(url)
        if response.status_code == 200:
            file_name = f'C:/Users/gerry/Desktop/python/macro_programming/section3_hw1/23{
                i}{j}.csv'
            with open(file_name, 'wb') as file:
                file.write(response.content)
