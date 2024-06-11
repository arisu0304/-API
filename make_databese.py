import asyncio
import requests
import json
import pandas as pd

async def save_weather_data(url, file_path):
    response = await loop.run_in_executor(None, requests.get, url)
    
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print("데이터를 성공적으로 저장했습니다.")
    else:
        print("데이터를 가져오는 데 실패했습니다.")

def open_excel_with_pandas(file_path):
    try:
        df = pd.read_excel(file_path)
        print("엑셀 파일을 성공적으로 열었습니다.")
        return df
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
        return None
    except Exception as e:
        print("파일을 열다가 오류가 발생했습니다:", e)
        return None

async def main():
    file_path = "Coordinate.xlsx"
    df = open_excel_with_pandas(file_path)
    if df is None:
        return
    
    filtered_df = df[df['1단계'] == '서울특별시']
    filtered_df = filtered_df[~pd.isna(filtered_df['2단계'])]
    filtered_df = filtered_df[pd.isna(filtered_df['3단계'])]

    base_url_1 = 'https://apihub.kma.go.kr/api/typ02/openApi/VilageFcstInfoService_2.0/getUltraSrtNcst?pageNo=1&numOfRows=1000&dataType=JSON&base_date=20240611&base_time=0600&nx='
    base_url_2 = '&ny='
    base_url_3 = '&authKey=TSUc53T-TumlHOd0_i7plA'

    tasks = []
    weather_data = {}
    for index, row in filtered_df.iterrows():
        nx = str(row['격자 X'])
        ny = str(row['격자 Y'])
        url = base_url_1 + nx + base_url_2 + ny + base_url_3
        file_path = f"weather_data_{nx}_{ny}.json"
        task = save_weather_data(url, file_path)
        tasks.append(task)

    await asyncio.gather(*tasks)

    for index, row in filtered_df.iterrows():
        nx = str(row['격자 X'])
        ny = str(row['격자 Y'])
        file_path = f"weather_data_{nx}_{ny}.json"
        with open(file_path, 'r') as f:
            weather = json.load(f)
        obsrValue = weather['response']['body']['items']['item'][3]['obsrValue']
        city_name = f"{row['1단계']} {row['2단계']}"
        weather_data[city_name] = obsrValue

    with open('seoul.json', 'w', encoding='utf-8') as f:
        json.dump(weather_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
