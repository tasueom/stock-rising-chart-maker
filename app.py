from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

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
        
        return render_template('chart.html', kospi_url=kospi_url, kosdaq_url=kosdaq_url)
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)