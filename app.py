from flask import Flask, render_template, request, redirect, url_for
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)

def not_a_robot():
    # ▶ 웹 요청 시, 브라우저처럼 보이게 하기 위한 HTTP 헤더 설정
    #   (requests로 직접 접속하면 '봇'으로 차단당할 수 있으므로)
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    return headers

def get_chart(url):
    # URL에 프로토콜이 없으면 https:// 추가
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    
    headers = not_a_robot()
    response = requests.get(url, headers=headers)
    # 깨짐방지
    response.encoding = "euc-kr"
    soup = BeautifulSoup(response.text, "html.parser")
    
    table = soup.find("table", class_="type_2")
    
    if not table:
        print("table not found")
    else:
        print("table found")
        tbody = table.find("tbody")
        if tbody:
            rows = tbody.find_all("tr")
        else:
            rows = table.find_all("tr")
        
        data = []
        # 모든 행 순회하며 데이터 추출
        for row in rows:
            cols = [col.get_text(strip=True) for col in row.find_all("td")]
            data.append(cols)
        
        # 최대 행 길이 확인
        if not data:
            print("data가 비어있습니다")
        
        max_length = max(len(row) for row in data)
        # 첫 번째 tr만 선택해서 헤더 추출
        if tbody:
            first_row = tbody.find("tr")
            if first_row:
                headers = [
                    th.get_text(strip=True)
                    for th in first_row.find_all("th")
                ]
            else:
                headers = []
        else:
            # tbody가 없으면 직접 첫 번째 tr 찾기
            first_row = table.find("tr")
            headers = [
                th.get_text(strip=True)
                for th in first_row.find_all("th")
            ] if first_row else []
        
        print(f"디버그 - max_length: {max_length}, headers 길이: {len(headers)}")
        print(f"디버그 - headers: {headers}")
        
        #헤더 수와 실제 데이터 열 수가 다를 경우 자동 보정
        if len(headers) != max_length:
            print("최대 행 길이: ", max_length)
            print("원래 헤더 길이: ", len(headers))
            headers = [f"컬럼{i+1}" for i in range(max_length)]
            print("조정된 헤더: ", headers)
        else:
            print("헤더 조정 없음")
        
        df = pd.DataFrame(data, columns=headers)
        df.dropna(inplace=True)
        df.reset_index(drop=True, inplace=True)
        print(df.head())
        
        if "종목명" not in df.columns:
            # 만약 컬럼명이 조정되었다면 두번째 컬럼을 종목명으로 설정
            df.rename(columns={1: "종목명"}, inplace=True)
        
        # 현재가 컬럼 숫자 변환
        if "현재가" in df.columns:
            # 쉼표 제거 후 정수화
            df["현재가"] = df["현재가"].str.replace(",", "").astype(int)
        else:
            # 만약 컬럼명이 조정되었다면 세번째 컬럼을 현재가로 설정
            df.iloc[:, 2] = df.iloc[:, 2].str.replace(",", "").astype(int)
            df.rename(columns={2: "현재가"}, inplace=True)
        
        if "등락률" not in df.columns:
            # 만약 컬럼명이 조정되었다면 다섯번째 컬럼을 등락률로 설정
            df.rename(columns={4: "등락률"}, inplace=True)
        
        df = df[["종목명","현재가","등락률"]].head(10)
        
        labels = df["종목명"].tolist()
        values = df["현재가"].tolist()
        percentages = df["등락률"].tolist()
        
        return labels, values, percentages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        # JSON 파일을 직접 파싱해서 딕셔너리로 사용
        data = json.load(file)
        markets = data["markets"]
        # 주소 저장
        kospi_url = markets["KOSPI"]
        kosdaq_url = markets["KOSDAQ"]
        
        kospi_labels, kospi_values, kospi_percentages = get_chart(kospi_url)
        kosdaq_labels, kosdaq_values, kosdaq_percentages = get_chart(kosdaq_url)
        
        kospi_data = {
            "labels": kospi_labels,
            "values": kospi_values,
            "percentages": kospi_percentages
        }
        kosdaq_data = {
            "labels": kosdaq_labels,
            "values": kosdaq_values,
            "percentages": kosdaq_percentages
        }
        
        return render_template('chart.html', kospi_data=kospi_data, kosdaq_data=kosdaq_data)
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)