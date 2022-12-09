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


function pt2_check() {
    const oven1 = parseInt(document.getElementById('o1').value),
          oven2 = parseInt(document.getElementById('o2').value);
    
    if (oven2 == parseInt(oven1) + 2) {
        document.getElementById("oven2_pop_id").style.visibility = 'hidden';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }  
    else if (oven1 >= oven2) {
        document.getElementById("oven2_pop_id").style.visibility = 'visible';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }
    else if (oven2 == parseInt(oven1) + 1) {
        document.getElementById("oven2_pop_id").style.visibility = 'visible';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }
    else if (oven2 > parseInt(oven1) + 2) {
        document.getElementById("oven2_pop_id").style.visibility = 'hidden';
        document.getElementById("comment_skip_id").style.visibility = 'visible';
    }  
}
function pt3_check() {
    const oven1 = parseInt(document.getElementById('o2').value),
          oven2 = parseInt(document.getElementById('o3').value);
    
    if (oven2 == parseInt(oven1) + 2) {
        document.getElementById("oven3_pop_id").style.visibility = 'hidden';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }  
    else if (oven1 >= oven2) {
        document.getElementById("oven3_pop_id").style.visibility = 'visible';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }
    else if (oven2 == parseInt(oven1) + 1) {
        document.getElementById("oven3_pop_id").style.visibility = 'visible';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }
    else if (oven2 > parseInt(oven1) + 2) {
        document.getElementById("oven3_pop_id").style.visibility = 'hidden';
        document.getElementById("comment_skip_id").style.visibility = 'visible';
        document.getElementById("comment_skip_id").innerHTML = '<a id="exit_pop_id" class="exit_pop_class">X</a>Please change Oven No. for THIRD oven or comment below what oven(s) were skipped.';
    }  
}
function pt4_check() {
    const oven1 = parseInt(document.getElementById('o3').value),
          oven2 = parseInt(document.getElementById('o4').value);
    
    if (oven2 == parseInt(oven1) + 2) {
        document.getElementById("oven4_pop_id").style.visibility = 'hidden';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }  
    else if (oven1 >= oven2) {
        document.getElementById("oven4_pop_id").style.visibility = 'visible';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }
    else if (oven2 == parseInt(oven1) + 1) {
        document.getElementById("oven4_pop_id").style.visibility = 'visible';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }
    else if (oven2 > parseInt(oven1) + 2) {
        document.getElementById("oven4_pop_id").style.visibility = 'hidden';
        document.getElementById("comment_skip_id").style.visibility = 'visible';
        document.getElementById("comment_skip_id").innerHTML = '<a id="exit_pop_id" class="exit_pop_class">X</a>Please change Oven No. for FORTH oven or comment below what oven(s) were skipped.';
        document.getElementById("exit_pop_id").onclick = function() {
            exit_pop()
        };
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

function reload() {
    location.reload();
}