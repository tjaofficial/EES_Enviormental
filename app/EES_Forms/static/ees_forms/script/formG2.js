function stop_light(average, id_param) {
    const inputAverage = document.getElementById(id_param).value;
    if (inputAverage) {
        if (parseFloat(inputAverage) == parseFloat(average)) {
            document.getElementById(id_param).style.backgroundColor = '#3c983c85';
        } else {
            document.getElementById(id_param).style.backgroundColor = '#F49B9B';
        }
    } else {
        document.getElementById(id_param).style.backgroundColor = '#FFFA8B';
    }
}

function averages_func(oven) {
    list = [1,2,3,4,5,6,7,8];
    var the_group = [];
    for (let i=0; i < list.length; i++){
        const opacities = list[i];
        const the_opac  = parseInt(document.getElementById('id_PEC_read_' + oven + '_' + opacities).value);
        if (Number.isInteger(the_opac)) {
            the_group.push(the_opac);
        }
    }
    if (the_group.length > 0) {
        const highest_avg = [];

        const highest_read = the_group.reduce(function(a, b) {
            return Math.max(a, b);
        }, 0);
        if (the_group.length > 6) {
            const instances = [];
            for (let h = 0; h < (the_group.length + 1) - 6; h++) {
                let i = h;
                let r = h;
                const D = [];
                for (i; i < r + 6; i++) {
                    D.push(parseInt(the_group[i])) 
                }
                let sum = D.reduce(function(a, b){
                    return a + b;
                }, 0);
                let avg = sum / 6;
                    instances.push(avg)
                }
                
                var max = instances.reduce(function(a, b) {
                    return Math.max(a, b);
                }, 0);
                highest_avg.push(max)

            }
        else if (the_group.length <= 6) {
            let sum = the_group.reduce(function(a, b){
                return parseInt(a) + parseInt(b);
            }, 0);
            let avg = sum / 6;
            highest_avg.push(avg)
        }

        let ha1 = highest_avg;
        const id_average_6 = "id_PEC_average_" + oven;
        
        if(highest_avg) {
            document.getElementById(id_average_6).placeholder = parseFloat(ha1).toFixed(2);
            stop_light(parseFloat(ha1).toFixed(2), id_average_6);
        }

    } else {
        document.getElementById("id_PEC_average_" + oven).placeholder = '-';
        document.getElementById("id_PEC_average_" + oven).style.backgroundColor = '#FFFA8B';
    }
}
function main_avg() {
    const avg_a = document.getElementById('id_PEC_average_a').value;
    const avg_b = document.getElementById('id_PEC_average_b').value;
    const avg_c = document.getElementById('id_PEC_average_c').value;
    const value_avg_main = document.getElementById('id_PEC_average_main').value;

    if (!avg_a || !avg_b || !avg_c) {
        document.getElementById('id_PEC_average_main').placeholder = '-';
    } else {
        const main_avg = (parseFloat(avg_a) + parseFloat(avg_b) + parseFloat(avg_c))/3;
        document.getElementById('id_PEC_average_main').placeholder = main_avg.toFixed(2);
        stop_light(main_avg.toFixed(2), 'id_PEC_average_main')
    }
}


function avg_a() {
    averages_func('a')
    main_avg()
}
function avg_b() {
    averages_func('b')
    main_avg()
}
function avg_c() {
    averages_func('c')
    main_avg()
}
avg_a()
avg_b()
avg_c()

function weatherStoplight() {
    const weatherJson = JSON.parse(document.getElementById('weather').value);
    const wind_speed_start = document.getElementById('id_wind_speed_start').value;
    const wind_speed_stop = document.getElementById('id_wind_speed_stop').value;
    const ambient_temp_start = document.getElementById('id_ambient_temp_start').value;
    const ambient_temp_stop = document.getElementById('id_ambient_temp_stop').value;
    const sky_conditions = document.getElementById('id_sky_conditions').value;
    const wind_direction = document.getElementById('id_wind_direction').value;
    const humidity = document.getElementById('id_humidity').value;

    if (!sky_conditions){
        document.getElementById('id_sky_conditions').placeholder = weatherJson.description;
        document.getElementById('id_sky_conditions').style.backgroundColor = '#FFFA8B';
    } else {
        document.getElementById('id_sky_conditions').style.backgroundColor = '#3c983c85';
    }

    if (!wind_direction){
        document.getElementById('id_wind_direction').placeholder = weatherJson.wind_direction;
        document.getElementById('id_wind_direction').style.backgroundColor = '#FFFA8B';
    } else {
        document.getElementById('id_wind_direction').style.backgroundColor = '#3c983c85';
    }

    if (!humidity){
        document.getElementById('id_humidity').placeholder = weatherJson.humidity;
        document.getElementById('id_humidity').style.backgroundColor = '#FFFA8B';
    } else {
        document.getElementById('id_humidity').style.backgroundColor = '#3c983c85';
    }

    if (!wind_speed_start) {
        document.getElementById('id_wind_speed_start').placeholder = weatherJson.wind_speed;
        document.getElementById('id_wind_speed_start').style.backgroundColor = '#FFFA8B';
    } else {
        document.getElementById('id_wind_speed_start').style.backgroundColor = '#3c983c85';
    }
    if (!ambient_temp_start) {
        document.getElementById('id_ambient_temp_start').placeholder = weatherJson.temperature;
        document.getElementById('id_ambient_temp_start').style.backgroundColor = '#FFFA8B';
    } else {
        document.getElementById('id_ambient_temp_start').style.backgroundColor = '#3c983c85';
    }
}
weatherStoplight();