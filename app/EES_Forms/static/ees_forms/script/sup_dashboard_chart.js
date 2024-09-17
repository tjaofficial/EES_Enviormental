const todayDate = document.getElementById('today').dataset.today;
const chargeCanvas = document.getElementById('charges-holder'),
doorCanvas = document.getElementById('doors-holder'),
lidCanvas = document.getElementById('lids-holder');


function createGraph(selector) {
    const chartOptions = {
        legend: {display: false},
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'day',
                    parser: 'yyyy-MM-dd'
                },
                min: selector.yValues[0],
                max: selector.yValues[-1]
            },
            y: {
                min: 0,
                title: {
                    display: true
                }
                
            }
        },
        maintainAspectRatio: false
    };
    if (selector.graphID == 'charges'){
        chartOptions.scales.y.title.text = 'seconds';
    } else if (selector.graphID == 'doors'){
        chartOptions.scales.y.title.text = 'leaks';
    } else if (selector.graphID == 'lids'){
        chartOptions.scales.y.title.text = 'leaks';
    }
    const xValues = selector.xValues;
    const yValues = selector.yValues;
    const graphData = {
        labels: yValues,
        datasets: [{
            fill: false,
            lineTension: 0,
            backgroundColor: "rgba(0,0,255,1.0)",
            borderColor: "rgba(0,0,255,0.1)",
            data: xValues
        }]
    }
    const chartAreaBackgroundColor = {
        id:'chartAreaBackgroundColor',
        beforeDraw(chart, args, plugins) {
            const { ctx, chartArea: {top, bottom, left, right, width, height}, scales: {x,y} } = chart;

            ctx.save();
            var theLine = 55;
            if (y.getValueForPixel(top) > theLine) {
                var redTop = y.getValueForPixel(top);
            } else {
                var redTop = theLine;
            }
            var redBottom = theLine;
            if (y.getValueForPixel(top) > theLine) {
                var greenTop = theLine;
            } else {
                var greenTop = y.getValueForPixel(top);
            }
            if (y.getValueForPixel(bottom) > 0) {
                var greenBottom = y.getValueForPixel(bottom);
            } else {
                var greenBottom = 0;
            }
            bgColors(redBottom, redTop,"rgba(255,26,104,0.2)")
            bgColors(greenBottom, greenTop,"rgba(75,192,192,0.2)")

            function bgColors(low, high, color){
                ctx.fillStyle = color;
                ctx.fillRect(left, y.getPixelForValue(high), width, y.getPixelForValue(low) - y.getPixelForValue(high))
            }
        }
    }
    const chargesConfig = {
        type: selector.type,
        data: graphData,
        options: chartOptions,
        plugins: [chartAreaBackgroundColor]
    }
    new Chart(
        String(selector.graphID) + "-chart",
        chargesConfig
    );
}

function changeGraph(change){
    if (change.graphID == 'charges'){
        doorCanvas.style.display = 'none';
        chargeCanvas.style.display = 'block';
        lidCanvas.style.display = 'none';
    } else if (change.graphID == 'doors'){
        doorCanvas.style.display = 'block';
        chargeCanvas.style.display = 'none';
        lidCanvas.style.display = 'none';
    } else if (change.graphID == 'lids'){
        doorCanvas.style.display = 'none';
        chargeCanvas.style.display = 'none';
        lidCanvas.style.display = 'block';
    }
}