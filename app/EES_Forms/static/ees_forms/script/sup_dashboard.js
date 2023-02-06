
const labels = [
    document.getElementById('graph-xaxis-data7').innerText,
    document.getElementById('graph-xaxis-data6').innerText,
    document.getElementById('graph-xaxis-data5').innerText,
    document.getElementById('graph-xaxis-data4').innerText,
    document.getElementById('graph-xaxis-data3').innerText,
    document.getElementById('graph-xaxis-data2').innerText,
    document.getElementById('graph-xaxis-data1').innerText
];

const data = {
    labels: labels,
    datasets: [{
        label: 'Daily Total Charge Time',
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data: [
            document.getElementById('graph-yaxis-data7').innerText,
            document.getElementById('graph-yaxis-data6').innerText,
            document.getElementById('graph-yaxis-data5').innerText, 
            document.getElementById('graph-yaxis-data4').innerText, 
            document.getElementById('graph-yaxis-data3').innerText, 
            document.getElementById('graph-yaxis-data2').innerText, 
            document.getElementById('graph-yaxis-data1').innerText
        ],
        backgroundColor: [
            'rgb(255, 153, 153)',
        ],
    }]
};

const config = {
    type: 'bar',
    data: data,
    options: {
        layout: {
            padding:{
                left: 0,
                right: 0,
                top: 0,
                botttom: 0,
            }
        }
    }
};

const myChart = new Chart(document.getElementById('myChart'), config);

var height = myChart.canvas.style.height = '325px';