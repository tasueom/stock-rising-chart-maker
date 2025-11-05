let kospiChart = null;
let kosdaqChart = null;

// Chart.js 플러그인 등록 (스크립트 로드 직후)
if (typeof Chart !== 'undefined' && typeof ChartDataLabels !== 'undefined') {
    Chart.register(ChartDataLabels);
    console.log('ChartDataLabels plugin registered');
} else {
    console.error('Chart or ChartDataLabels not found');
}

// 페이지 로드 시 차트 생성
document.addEventListener('DOMContentLoaded', function() {
    // 플러그인 재등록 확인
    if (typeof Chart !== 'undefined' && typeof ChartDataLabels !== 'undefined') {
        Chart.register(ChartDataLabels);
    }
    
    // 디버깅: 데이터 확인
    console.log('KOSPI data:', kospiData);
    console.log('KOSDAQ data:', kosdaqData);
    console.log('KOSPI percentages:', kospiData?.percentages);
    console.log('KOSDAQ percentages:', kosdaqData?.percentages);
    
    // HTML에서 전달받은 데이터로 차트 생성 (약간의 지연을 두고 생성)
    createChart('kospi-canvas', kospiData, 'KOSPI');
    
    // 코스닥 차트는 약간의 지연 후 생성
    setTimeout(function() {
        createChart('kosdaq-canvas', kosdaqData, 'KOSDAQ');
    }, 100);
});

// 차트 생성 함수
function createChart(canvasId, data, title) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.error(`Canvas element with id "${canvasId}" not found`);
        return;
    }

    // 디버깅: 데이터 확인
    console.log(`Creating chart for ${canvasId}:`, data);
    console.log(`Percentages for ${canvasId}:`, data.percentages);

    // 기존 차트가 있으면 제거
    if (canvasId === 'kospi-canvas' && kospiChart) {
        kospiChart.destroy();
    } else if (canvasId === 'kosdaq-canvas' && kosdaqChart) {
        kosdaqChart.destroy();
    }

    // datalabels 설정
    const datalabelsConfig = {
        anchor: 'end',
        align: 'top',
        display: true,
        formatter: function(value, context) {
            // percentages 배열에서 해당 인덱스의 등락률 반환
            const percentage = data.percentages && data.percentages[context.dataIndex];
            console.log(`DataLabel formatter for ${canvasId} - index: ${context.dataIndex}, percentage:`, percentage, 'data.percentages:', data.percentages);
            if (percentage !== undefined && percentage !== null && percentage !== '') {
                return String(percentage);
            }
            return '';
        },
        color: '#333',
        font: {
            weight: 'bold',
            size: 12
        },
        padding: {
            top: 5
        }
    };
    
    // 새로운 차트 생성
    const chartConfig = {
        type: 'bar',
        plugins: [ChartDataLabels],
        data: {
            labels: data.labels,
            datasets: [{
                label: '현재가',
                data: data.values,
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: title
                },
                legend: {
                    display: false
                },
                datalabels: datalabelsConfig
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    };
    
    const chart = new Chart(ctx, chartConfig);

    // 차트 객체 저장
    if (canvasId === 'kospi-canvas') {
        kospiChart = chart;
    } else if (canvasId === 'kosdaq-canvas') {
        kosdaqChart = chart;
    }
}
