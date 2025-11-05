# 국내 증시 상승 현황 확인하기

국내 증시(KOSPI, KOSDAQ) 상승 종목 정보를 웹 스크래핑하여 차트로 시각화하는 웹 애플리케이션입니다.

## 주요 기능

### 1. JSON 파일 업로드
- KOSPI와 KOSDAQ의 상승 종목 페이지 URL을 포함한 JSON 파일을 업로드
- JSON 형식:
  ```json
  {
    "markets": {
      "KOSPI": "finance.naver.com/sise/sise_rise.naver",
      "KOSDAQ": "finance.naver.com/sise/sise_rise.naver?sosok=1"
    }
  }
  ```

### 2. 웹 스크래핑
- 네이버 금융 페이지에서 상승 종목 데이터 자동 수집
- HTML 테이블 파싱을 통한 데이터 추출
- 브라우저 헤더 설정으로 봇 차단 우회

### 3. 데이터 처리
- 상위 10개 종목 자동 추출
- 종목명, 현재가, 등락률 정보 추출
- 데이터 정제 및 형식 변환 (쉼표 제거, 숫자 변환)

### 4. 차트 시각화
- **막대 그래프**: 각 종목의 현재가를 막대 그래프로 표시
- **양옆 배치**: KOSPI와 KOSDAQ 차트를 나란히 배치
- **등락률 표시**: 각 막대 상단에 등락률 텍스트 표시

## 기술 스택

- **Backend**: Flask (Python)
- **웹 스크래핑**: BeautifulSoup, requests
- **데이터 처리**: Pandas
- **Frontend**: HTML, CSS, JavaScript
- **차트 라이브러리**: Chart.js, chartjs-plugin-datalabels

## 설치 및 실행

### 필수 패키지 설치
```bash
pip install flask requests beautifulsoup4 pandas
```

### 실행
```bash
python app.py
```

브라우저에서 `http://localhost:5000` 접속

## 사용 방법

1. **홈 페이지**: 프로젝트 소개 확인
2. **업로드 페이지**: JSON 파일 업로드
3. **결과 페이지**: KOSPI와 KOSDAQ 상위 10개 종목 차트 확인