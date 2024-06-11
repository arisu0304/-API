import pandas as pd

base_url_1 = 'https://apihub.kma.go.kr/api/typ02/openApi/VilageFcstInfoService_2.0/getUltraSrtNcst?pageNo=1&numOfRows=1000&dataType=JSON&base_date=20240611&base_time=0600&nx='
base_url_2 = '&ny='
base_url_3 = '&authKey=TSUc53T-TumlHOd0_i7plA'

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

file_path = "Coordinate.xlsx"

df = open_excel_with_pandas(file_path)
print(df["3단계"].values[0])

filtered_df = df[df['1단계'] == '서울특별시']
filtered_df = filtered_df[~pd.isna(filtered_df['2단계'])]
filtered_df = filtered_df[pd.isna(filtered_df['3단계'])]

for index, row in filtered_df.iterrows():
    nx = str(row['격자 X'])
    ny = str(row['격자 Y'])
    api_url = base_url_1 + nx + base_url_2 + ny + base_url_3
    # 여기서 API를 호출하고 결과를 처리하는 코드를 추가합니다.
    print(api_url)

