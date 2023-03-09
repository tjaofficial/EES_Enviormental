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
    list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16];
    var the_group = [];
    
    for (let i=0; i < list.length; i++){
        const opacities = list[i];
        const the_opac  = parseInt(document.getElementById('o' + oven + '_' + opacities + '_reads').value);
        if (Number.isInteger(the_opac)) {
            the_group.push(the_opac);
        }
    }
    console.log(the_group);
    if (the_group.length > 0) {
        const highest_avg = [];

        const highest_read = the_group.reduce(function(a, b) {
            return Math.max(a, b);
        }, 0);
        console.log('read ' + highest_read);
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
        const id_average_6 = "o" + oven + "_average_6";
        const id_high_opac = "o" + oven + "_highest_opacity";
        
        if(highest_avg) {
            document.getElementById(id_average_6).placeholder = parseFloat(ha1).toFixed(2);
            stop_light(parseFloat(ha1).toFixed(2), id_average_6);
        }
        
        if (highest_read != null) {
            console.log('CHECK 1')
            document.getElementById(id_high_opac).placeholder = highest_read;
            stop_light(parseInt(highest_read), id_high_opac);
        }


        if(highest_read > 20){
            document.getElementById("o" + oven + "_instant_over_20").value = 'Yes';
        }
        else{
            document.getElementById("o" + oven + "_instant_over_20").value = 'No';
        }
        if(highest_avg > 35){
            document.getElementById("o" + oven + "_average_6_over_35").value = 'Yes';
        }
        else{
            document.getElementById("o" + oven + "_average_6_over_35").value = 'No';
        }
    } else {
        document.getElementById("o" + oven + "_average_6").placeholder = '-';
        document.getElementById("o" + oven + "_highest_opacity").placeholder = '-';
        document.getElementById("o" + oven + "_average_6").style.backgroundColor = '#FFFA8B';
        document.getElementById("o" + oven + "_highest_opacity").style.backgroundColor = '#FFFA8B';
    }
}


function averages_pt1() {
    averages_func(1);
}
averages_pt1();
function averages_pt2() {
    averages_func(2);
}
averages_pt2();
function averages_pt3() {
    averages_func(3);
}
averages_pt3();
function averages_pt4() {
    averages_func(4);
}
averages_pt4();

function isEven(n) {
    return n % 2 == 0;
}


function pushTravelCheck(pushB) {
    const pushA = pushB - 1
    const ovenA = parseInt(document.getElementById('o' + pushA).value),
          ovenB = parseInt(document.getElementById('o' + pushB).value);
    const endingNumbers = [85, 84]
    if (ovenB && 0 < ovenB < 86) {
        if (isEven(ovenB) && isEven(ovenA) && ovenA < ovenB || !isEven(ovenB) && !isEven(ovenA) && ovenA < ovenB || ovenA == 85 && isEven(ovenB) || ovenA == 84 && !isEven(ovenB)) {
            if (ovenB >= parseInt(ovenA) + 4 || ovenB >= parseInt(ovenA) + 4 || ovenA == 85 && ovenB >= 4 || ovenA == 84 && ovenB >= 3){
                console.log('SKIPPED AN OVEN')
                document.getElementById("oven" + parseInt(pushB) + "_pop_id").style.visibility = 'hidden';
                document.getElementById("comment_skip_id").style.visibility = 'visible';
            } else {
                console.log('EVERYTHING IS FINE')
                document.getElementById("oven" + parseInt(pushB) + "_pop_id").style.visibility = 'hidden';
                document.getElementById("comment_skip_id").style.visibility = 'hidden';
            }
        } else {//if (!(parseInt(ovenA) in endingNumbers) && ovenA >= ovenB || ovenB == parseInt(ovenA) + 1 || ovenA == 85 && ovenB == 1 || ovenA == 84 && ovenB == 2) {
            console.log('NEED TO CHANGE INPUT')
            document.getElementById("oven" + parseInt(pushB) + "_pop_id").style.visibility = 'visible';
            document.getElementById("comment_skip_id").style.visibility = 'hidden';
        }
    } else {
        console.log('no input')
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
        document.getElementById("oven" + parseInt(pushB) + "_pop_id").style.visibility = 'hidden';
    }
}


function exit_pop() {
    document.getElementById("comment_skip_id").style.visibility = 'hidden';
}

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