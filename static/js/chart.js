let kospiChart = null;
let kosdaqChart = null;

// 페이지 로드 시 차트 생성
document.addEventListener('DOMContentLoaded', function() {
    // HTML에서 전달받은 데이터로 차트 생성
    createChart('kospi-canvas', kospiData, 'KOSPI');
    createChart('kosdaq-canvas', kosdaqData, 'KOSDAQ');
});

// 차트 생성 함수
function createChart(canvasId, data, title) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.error(`Canvas element with id "${canvasId}" not found`);
        return;
    }

    // 기존 차트가 있으면 제거
    if (canvasId === 'kospi-canvas' && kospiChart) {
        kospiChart.destroy();
    } else if (canvasId === 'kosdaq-canvas' && kosdaqChart) {
        kosdaqChart.destroy();
    }

    // 새로운 차트 생성
    const chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: '현재가',
                data: data.values,
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: title
                },
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // 차트 객체 저장
    if (canvasId === 'kospi-canvas') {
        kospiChart = chart;
    } else if (canvasId === 'kosdaq-canvas') {
        kosdaqChart = chart;
    }
}
