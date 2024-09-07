const charges = document.getElementById('charge-btn'),
doors = document.getElementById('door-btn'),
lids = document.getElementById('lid-btn'),
chargeCanvas = document.getElementById('charges-holder'),
doorCanvas = document.getElementById('doors-holder'),
lidCanvas = document.getElementById('lids-holder'),
chargeX = JSON.parse(document.getElementById('charge-values').dataset.xvalues),
doorX = JSON.parse(document.getElementById('door-values').dataset.xvalues),
lidX = JSON.parse(document.getElementById('lid-values').dataset.xvalues),
chargeY = JSON.parse(document.getElementById('charge-values').dataset.yvalues),
doorY = JSON.parse(document.getElementById('door-values').dataset.yvalues),
lidY = JSON.parse(document.getElementById('lid-values').dataset.yvalues),
last7days = document.getElementById('last7days').dataset.sevendays,
today = document.getElementById('today').dataset.today;
charges.addEventListener('click', changeCharge)
doors.addEventListener('click', changeDoor)
lids.addEventListener('click', changeLid)

const chartOptions = {
    legend: {display: false},
    scales: {
        x: {
            type: 'time',
            time: {
                unit: 'day',
                parser: 'yyyy-MM-dd'
            },
            min: last7days,
            max: today
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

function createChargeChart(){
    chartOptions.scales.y.title.text = 'seconds';
    const CxValues = chargeX;
    const CyValues = chargeY;
    const chargesData = {
        labels: CyValues,
        datasets: [{
            fill: false,
            lineTension: 0,
            backgroundColor: "rgba(0,0,255,1.0)",
            borderColor: "rgba(0,0,255,0.1)",
            data: CxValues
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
        type: "bar",
        data: chargesData,
        options: chartOptions,
        plugins: [chartAreaBackgroundColor]
    }
    new Chart(
        "charges-chart",
        chargesConfig
    );
}
createChargeChart();
function createDoorChart(){
    chartOptions.scales.y.title.text = 'leaks';
    const DxValues = doorX;
    const DyValues = doorY;
    const doorsData = {
        labels: DyValues,
        datasets: [{
            fill: false,
            lineTension: 0,
            backgroundColor: "rgba(0,0,255,1.0)",
            borderColor: "rgba(0,0,255,0.1)",
            data: DxValues,
        }]
    }
    const chartAreaBackgroundColorD = {
        id:'chartAreaBackgroundColorD',
        beforeDraw(chart, args, plugins) {
            const { ctx, chartArea: {top, bottom, left, right, width, height}, scales: {x,y} } = chart;

            ctx.save();
            var theLine = 8;
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
    const doorsConfig = {
        type: "bar",
        data: doorsData,
        options: chartOptions,
        plugins: [chartAreaBackgroundColorD]
    }
    new Chart(
        "doors-chart",
        doorsConfig
    );
}
createDoorChart();
function createLidChart(){
    chartOptions.scales.y.title.text = 'leaks';
    const LxValues = lidX;
    const LyValues = lidY;
    const lidsData = {
        labels: LyValues,
        datasets: [{
            fill: false,
            lineTension: 0,
            backgroundColor: "rgba(0,0,255,1.0)",
            borderColor: "rgba(0,0,255,0.1)",
            data: LxValues
        }]
    }
    const chartAreaBackgroundColorL = {
        id:'chartAreaBackgroundColorL',
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
    const lidsConfig = {
        type: "bar",
        data: lidsData,
        options: chartOptions,
        plugins: [chartAreaBackgroundColorL]
    };
    new Chart(
        "lids-chart",
        lidsConfig
    );
}
createLidChart();

function changeCharge(){
    doorCanvas.style.display = 'none';
    chargeCanvas.style.display = 'block';
    lidCanvas.style.display = 'none';
}
function changeDoor(){
    doorCanvas.style.display = 'block';
    chargeCanvas.style.display = 'none';
    lidCanvas.style.display = 'none';
}
function changeLid(){
    doorCanvas.style.display = 'none';
    chargeCanvas.style.display = 'none';
    lidCanvas.style.display = 'block';
}