function wind_placeholder(){
    const d = new Date();
    let day = d.getDay();
    let input_Id = 'id_wind_speed_' + String(day - 1);
    const weather = document.getElementById('weather').value;
    const wind_input = document.getElementById(input_Id).value;
    const weatherJson = JSON.parse(weather);
    if (!wind_input) {
        document.getElementById(input_Id).placeholder = weatherJson.wind_speed;
        document.getElementById(input_Id).style.backgroundColor = '#FFFA8B';
    } else {
        document.getElementById(input_Id).style.backgroundColor = '#3c983c85';
    }
}
wind_placeholder();

clean_up_submitted_form();

function clean_up_submitted_form() {
    individual_day();
    month_select();

    if (month_select() == '1day') {
        section_1_hidden();
        section_2_hidden();
    }
    section_3_hidden();
    section_4_hidden();
}

function individual_day() {
    const today = new Date();
    let d = today.getDay();
    let name_0 = false;
    let name_1 = false;
    let name_2 = false;
    let name_3 = false;
    let name_4 = false;
    if (d == 1){
        name_0 = true;
        name_1 = false;
        name_2 = false;
        name_3 = false;
        name_4 = false;
    } else if (d == 2){
        name_0 = true;
        name_1 = true;
        name_2 = false;
        name_3 = false;
        name_4 = false;
    } else if (d == 3){
        name_0 = true;
        name_1 = true;
        name_2 = true;
        name_3 = false;
        name_4 = false;
    } else if (d == 4){
        name_0 = true;
        name_1 = true;
        name_2 = true;
        name_3 = true;
        name_4 = false;
    } else if (d == 5){
        name_0 = true;
        name_1 = true;
        name_2 = true;
        name_3 = true;
        name_4 = true;
    }
    document.getElementById('id_observer_0').required = name_0;
    document.getElementById('id_observer_1').required = name_1;
    document.getElementById('id_observer_2').required = name_2;
    document.getElementById('id_observer_3').required = name_3;
    document.getElementById('id_observer_4').required = name_4;
    document.getElementById('id_time_0').required = name_0;
    document.getElementById('id_time_1').required = name_1;
    document.getElementById('id_time_2').required = name_2;
    document.getElementById('id_time_3').required = name_3;
    document.getElementById('id_time_4').required = name_4;
    document.getElementById('id_weather_0').required = name_0;
    document.getElementById('id_weather_1').required = name_1;
    document.getElementById('id_weather_2').required = name_2;
    document.getElementById('id_weather_3').required = name_3;
    document.getElementById('id_weather_4').required = name_4;
    document.getElementById('id_wind_speed_0').required = name_0;
    document.getElementById('id_wind_speed_1').required = name_1;
    document.getElementById('id_wind_speed_2').required = name_2;
    document.getElementById('id_wind_speed_3').required = name_3;
    document.getElementById('id_wind_speed_4').required = name_4;
    document.getElementById('id_fugitive_dust_observed_0').required = name_0;
    document.getElementById('id_fugitive_dust_observed_1').required = name_1;
    document.getElementById('id_fugitive_dust_observed_2').required = name_2;
    document.getElementById('id_fugitive_dust_observed_3').required = name_3;
    document.getElementById('id_fugitive_dust_observed_4').required = name_4;
    document.getElementById('id_supressant_applied_0').required = name_0;
    document.getElementById('id_supressant_applied_1').required = name_1;
    document.getElementById('id_supressant_applied_2').required = name_2;
    document.getElementById('id_supressant_applied_3').required = name_3;
    document.getElementById('id_supressant_applied_4').required = name_4;
    document.getElementById('id_supressant_active_0').required = name_0;
    document.getElementById('id_supressant_active_1').required = name_1;
    document.getElementById('id_supressant_active_2').required = name_2;
    document.getElementById('id_supressant_active_3').required = name_3;
    document.getElementById('id_supressant_active_4').required = name_4;
    document.getElementById('id_working_face_exceed_0').required = name_0;
    document.getElementById('id_working_face_exceed_1').required = name_1;
    document.getElementById('id_working_face_exceed_2').required = name_2;
    document.getElementById('id_working_face_exceed_3').required = name_3;
    document.getElementById('id_working_face_exceed_4').required = name_4;
    document.getElementById('id_spills_0').required = name_0;
    document.getElementById('id_spills_1').required = name_1;
    document.getElementById('id_spills_2').required = name_2;
    document.getElementById('id_spills_3').required = name_3;
    document.getElementById('id_spills_4').required = name_4;
    document.getElementById('id_pushed_back_0').required = name_0;
    document.getElementById('id_pushed_back_1').required = name_1;
    document.getElementById('id_pushed_back_2').required = name_2;
    document.getElementById('id_pushed_back_3').required = name_3;
    document.getElementById('id_pushed_back_4').required = name_4;
    document.getElementById('id_coal_vessel_0').required = name_0;
    document.getElementById('id_coal_vessel_1').required = name_1;
    document.getElementById('id_coal_vessel_2').required = name_2;
    document.getElementById('id_coal_vessel_3').required = name_3;
    document.getElementById('id_coal_vessel_4').required = name_4;
    document.getElementById('id_water_sprays_0').required = name_0;
    document.getElementById('id_water_sprays_1').required = name_1;
    document.getElementById('id_water_sprays_2').required = name_2;
    document.getElementById('id_water_sprays_3').required = name_3;
    document.getElementById('id_water_sprays_4').required = name_4;
    document.getElementById('id_loader_lowered_0').required = name_0;
    document.getElementById('id_loader_lowered_1').required = name_1;
    document.getElementById('id_loader_lowered_2').required = name_2;
    document.getElementById('id_loader_lowered_3').required = name_3;
    document.getElementById('id_loader_lowered_4').required = name_4;
    document.getElementById('id_working_water_sprays_0').required = name_0;
    document.getElementById('id_working_water_sprays_1').required = name_1;
    document.getElementById('id_working_water_sprays_2').required = name_2;
    document.getElementById('id_working_water_sprays_3').required = name_3;
    document.getElementById('id_working_water_sprays_4').required = name_4;
    document.getElementById('id_barrier_thickness_0').required = name_0;
    document.getElementById('id_barrier_thickness_1').required = name_1;
    document.getElementById('id_barrier_thickness_2').required = name_2;
    document.getElementById('id_barrier_thickness_3').required = name_3;
    document.getElementById('id_barrier_thickness_4').required = name_4;
    document.getElementById('id_surface_quality_0').required = name_0;
    document.getElementById('id_surface_quality_1').required = name_1;
    document.getElementById('id_surface_quality_2').required = name_2;
    document.getElementById('id_surface_quality_3').required = name_3;
    document.getElementById('id_surface_quality_4').required = name_4;
    document.getElementById('id_surpressant_crust_0').required = name_0;
    document.getElementById('id_surpressant_crust_1').required = name_1;
    document.getElementById('id_surpressant_crust_2').required = name_2;
    document.getElementById('id_surpressant_crust_3').required = name_3;
    document.getElementById('id_surpressant_crust_4').required = name_4;
    document.getElementById('id_additional_surpressant_0').required = name_0;
    document.getElementById('id_additional_surpressant_1').required = name_1;
    document.getElementById('id_additional_surpressant_2').required = name_2;
    document.getElementById('id_additional_surpressant_3').required = name_3;
    document.getElementById('id_additional_surpressant_4').required = name_4;
    document.getElementById('id_comments_0').required = name_0;
    document.getElementById('id_comments_1').required = name_1;
    document.getElementById('id_comments_2').required = name_2;
    document.getElementById('id_comments_3').required = name_3;
    document.getElementById('id_comments_4').required = name_4;
    document.getElementById('id_wharf_0').required = name_0;
    document.getElementById('id_wharf_1').required = name_1;
    document.getElementById('id_wharf_2').required = name_2;
    document.getElementById('id_wharf_3').required = name_3;
    document.getElementById('id_wharf_4').required = name_4;
    document.getElementById('id_breeze_0').required = name_0;
    document.getElementById('id_breeze_1').required = name_1;
    document.getElementById('id_breeze_2').required = name_2;
    document.getElementById('id_breeze_3').required = name_3;
    document.getElementById('id_breeze_4').required = name_4;
}
function month_select() {
    const freq = document.getElementById('frequency').innerText;
    if (freq == 'True') {
        auto_fill_section_1();
        auto_fill_section_2();
        //auto_fill_section_3()
        return '5days';
    } else {
        return '1day';
    }
}

function section_1_hidden() {
    list = [0,1,2,3,4];
    for (let item=0; item < list.length; item++){
        const fugitive_dust_observed = document.getElementById('id_fugitive_dust_observed_' + item);
        const supressant_applied = document.getElementById('id_supressant_applied_' + item);
        const supressant_active = document.getElementById('id_supressant_active_' + item);
        const working_face_exceed = document.getElementById('id_working_face_exceed_' + item);
        const spills = document.getElementById('id_spills_' + item);
        const pushed_back = document.getElementById('id_pushed_back_' + item);

        if ((fugitive_dust_observed.value || supressant_applied.value || supressant_active.value || working_face_exceed.value || pushed_back.value ) && spills.value == 'Yes' ) {
            list.splice(item,1);
            list.forEach((item2) => {
                console.log('DONT SHOW ' + item + ' YES')
                document.getElementById('id_fugitive_dust_observed_' + item2).style.display = 'none';
                document.getElementById('id_supressant_applied_' + item2).style.display = 'none';
                document.getElementById('id_supressant_active_' + item2).style.display = 'none';
                document.getElementById('id_working_face_exceed_' + item2).style.display = 'none';
                document.getElementById('id_spills_' + item2).style.display = 'none';
                document.getElementById('id_pushed_back_' + item2).style.display = 'none';

                document.getElementById('id_fugitive_dust_observed_' + item2).required = false;
                document.getElementById('id_supressant_applied_' + item2).required = false;
                document.getElementById('id_supressant_active_' + item2).required = false;
                document.getElementById('id_working_face_exceed_' + item2).required = false;
                document.getElementById('id_spills_' + item2).required = false;
                document.getElementById('id_pushed_back_' + item2).required = false;
            })
            break;
        } else if ((fugitive_dust_observed.value || supressant_applied.value || supressant_active.value || working_face_exceed.value) && (spills.value == '' && pushed_back.value == 'N/A')) {
            list.splice(item,1);
            list.forEach((item2) => {
                console.log('DONT SHOW ' + item + ' NONE')
                document.getElementById('id_fugitive_dust_observed_' + item2).style.display = 'none';
                document.getElementById('id_supressant_applied_' + item2).style.display = 'none';
                document.getElementById('id_supressant_active_' + item2).style.display = 'none';
                document.getElementById('id_working_face_exceed_' + item2).style.display = 'none';
                document.getElementById('id_spills_' + item2).style.display = 'none';
                document.getElementById('id_pushed_back_' + item2).style.display = 'none';

                document.getElementById('id_fugitive_dust_observed_' + item2).required = false;
                document.getElementById('id_supressant_applied_' + item2).required = false;
                document.getElementById('id_supressant_active_' + item2).required = false;
                document.getElementById('id_working_face_exceed_' + item2).required = false;
                document.getElementById('id_spills_' + item2).required = false;
                document.getElementById('id_pushed_back_' + item2).required = false;
            })
            auto_fill_section_1()
            break;
        } else if (fugitive_dust_observed.value || supressant_applied.value || supressant_active.value || working_face_exceed.value || spills.value ) {
            list.splice(item,1);
            list.forEach((item2) => {
                console.log('DONT SHOW ' + item + ' NO')
                document.getElementById('id_fugitive_dust_observed_' + item2).style.display = 'none';
                document.getElementById('id_supressant_applied_' + item2).style.display = 'none';
                document.getElementById('id_supressant_active_' + item2).style.display = 'none';
                document.getElementById('id_working_face_exceed_' + item2).style.display = 'none';
                document.getElementById('id_spills_' + item2).style.display = 'none';
                document.getElementById('id_pushed_back_' + item2).style.display = 'none';

                document.getElementById('id_fugitive_dust_observed_' + item2).required = false;
                document.getElementById('id_supressant_applied_' + item2).required = false;
                document.getElementById('id_supressant_active_' + item2).required = false;
                document.getElementById('id_working_face_exceed_' + item2).required = false;
                document.getElementById('id_spills_' + item2).required = false;
                document.getElementById('id_pushed_back_' + item2).required = false;
            })
            auto_fill_section_1()
            break;
        } else if (fugitive_dust_observed.value == '' && supressant_applied.value == '' && supressant_active.value == '' && working_face_exceed.value == '' && spills.value == '' && pushed_back.value == 'N/A') {
            list.splice(item,1);
            list.forEach((item2) => {
                console.log('DONT SHOW ' + item + ' Clear 3')
                document.getElementById('id_fugitive_dust_observed_' + item2).style.display = 'inline-block';
                document.getElementById('id_supressant_applied_' + item2).style.display = 'inline-block';
                document.getElementById('id_supressant_active_' + item2).style.display = 'inline-block';
                document.getElementById('id_working_face_exceed_' + item2).style.display = 'inline-block';
                document.getElementById('id_spills_' + item2).style.display = 'inline-block';
                document.getElementById('id_pushed_back_' + item2).style.display = 'inline-block';
            })
            auto_fill_section_1()
            break;
        } else {
            list.splice(item,1);
            list.forEach((item2) => {
                console.log('SHOW ' + item + ' CLEAR 2')
                document.getElementById('id_fugitive_dust_observed_' + item2).style.display = 'inline-block';
                document.getElementById('id_supressant_applied_' + item2).style.display = 'inline-block';
                document.getElementById('id_supressant_active_' + item2).style.display = 'inline-block';
                document.getElementById('id_working_face_exceed_' + item2).style.display = 'inline-block';
                document.getElementById('id_spills_' + item2).style.display = 'inline-block';
                document.getElementById('id_pushed_back_' + item2).style.display = 'inline-block';
            })
            list.splice(item, 0, item)
        }
    }
}
function section_2_hidden() {
    list = [0,1,2,3,4];
    for (let item=0; item < list.length; item++){
        const coal_vessel = document.getElementById('id_coal_vessel_' + item).value;
        const water_sprays = document.getElementById('id_water_sprays_' + item).value;
        const loader_lowered = document.getElementById('id_loader_lowered_' + item).value;
        const working_water_sprays = document.getElementById('id_working_water_sprays_' + item).value;
        if ( coal_vessel == 'No' ) {
            list.splice(item,1);
            list.forEach((item2) => {
                console.log('DONT SHOW ' + item + ' NO')
                document.getElementById('id_coal_vessel_' + item2).style.display = 'none';
                document.getElementById('id_water_sprays_' + item2).style.display = 'none';
                document.getElementById('id_loader_lowered_' + item2).style.display = 'none';
                document.getElementById('id_working_water_sprays_' + item2).style.display = 'none';

                document.getElementById('id_coal_vessel_' + item2).required = false;
                document.getElementById('id_water_sprays_' + item2).required = false;
                document.getElementById('id_loader_lowered_' + item2).required = false;
                document.getElementById('id_working_water_sprays_' + item2).required = false;
            })
            auto_fill_section_2();
            break;
        } else if ( (water_sprays || loader_lowered || working_water_sprays) && (coal_vessel == 'Yes') ) {
            list.splice(item,1);
            list.forEach((item2) => {
                console.log('DONT SHOW OTHER ' + item + ' YES')
                document.getElementById('id_coal_vessel_' + item2).style.display = 'none';
                document.getElementById('id_water_sprays_' + item2).style.display = 'none';
                document.getElementById('id_loader_lowered_' + item2).style.display = 'none';
                document.getElementById('id_working_water_sprays_' + item2).style.display = 'none';

                document.getElementById('id_coal_vessel_' + item2).required = false;
                document.getElementById('id_water_sprays_' + item2).required = false;
                document.getElementById('id_loader_lowered_' + item2).required = false;
                document.getElementById('id_working_water_sprays_' + item2).required = false;
            })
            break;
        } else if ( water_sprays == 'N/A' && loader_lowered == 'N/A' && working_water_sprays == 'N/A' && coal_vessel == '' ) {
            document.getElementById('id_water_sprays_' + item).value = '';
            document.getElementById('id_loader_lowered_' + item).value = '';
            document.getElementById('id_working_water_sprays_' + item).value = '';

            list.splice(item,1);
            list.forEach((item2) => {
                console.log('SHOW ' + item + ' CLEAR 2')
                document.getElementById('id_coal_vessel_' + item2).style.display = 'inline-block';
                document.getElementById('id_water_sprays_' + item2).style.display = 'inline-block';
                document.getElementById('id_loader_lowered_' + item2).style.display = 'inline-block';
                document.getElementById('id_working_water_sprays_' + item2).style.display = 'inline-block';
            })
            list.splice(item, 0, item)
        } else if ( (water_sprays || loader_lowered || working_water_sprays) && (coal_vessel == '') ) {
            list.splice(item,1);
            list.forEach((item2) => {
                console.log('DONT SHOW OTHER ' + item + ' YES')
                document.getElementById('id_coal_vessel_' + item2).style.display = 'none';
                document.getElementById('id_water_sprays_' + item2).style.display = 'none';
                document.getElementById('id_loader_lowered_' + item2).style.display = 'none';
                document.getElementById('id_working_water_sprays_' + item2).style.display = 'none';

                document.getElementById('id_coal_vessel_' + item2).required = false;
                document.getElementById('id_water_sprays_' + item2).required = false;
                document.getElementById('id_loader_lowered_' + item2).required = false;
                document.getElementById('id_working_water_sprays_' + item2).required = false;
            })
            break;
        } else if ( coal_vessel == 'Yes' ) {
            console.log(list);
            list.splice(item,1);
            console.log(list);
            list.forEach((item2) => {
                console.log('DONT SHOW ' + item + ' YES')
                document.getElementById('id_coal_vessel_' + item2).style.display = 'none';
                document.getElementById('id_water_sprays_' + item2).style.display = 'none';
                document.getElementById('id_loader_lowered_' + item2).style.display = 'none';
                document.getElementById('id_working_water_sprays_' + item2).style.display = 'none';

                document.getElementById('id_coal_vessel_' + item2).required = false;
                document.getElementById('id_water_sprays_' + item2).required = false;
                document.getElementById('id_loader_lowered_' + item2).required = false;
                document.getElementById('id_working_water_sprays_' + item2).required = false;
            })
            auto_fill_section_2();
            break;
        } else {
            document.getElementById('id_water_sprays_' + item).value = '';
            document.getElementById('id_loader_lowered_' + item).value = '';
            document.getElementById('id_working_water_sprays_' + item).value = '';

            list.splice(item,1);
            list.forEach((item2) => {
                console.log('SHOW ' + item + ' EMPTY')
                document.getElementById('id_coal_vessel_' + item2).style.display = 'inline-block';
                document.getElementById('id_water_sprays_' + item2).style.display = 'inline-block';
                document.getElementById('id_loader_lowered_' + item2).style.display = 'inline-block';
                document.getElementById('id_working_water_sprays_' + item2).style.display = 'inline-block';
            })
            list.splice(item, 0, item)
        }
    }
    
}
function section_3_hidden() {
    list = [0,1,2,3,4];
    for (let item=0; item < list.length; item++){
        const barrier_thickness = document.getElementById('id_barrier_thickness_' + item).value;
        const surface_quality = document.getElementById('id_surface_quality_' + item).value;
        const surpressant_crust = document.getElementById('id_surpressant_crust_' + item).value;
        
        if (barrier_thickness || surface_quality || surpressant_crust) {
            document.getElementById('id_barrier_thickness_' + item).required = true;
            document.getElementById('id_surface_quality_' + item).required = true;
            document.getElementById('id_surpressant_crust_' + item).required = true;
            auto_fill_section_3_each(surpressant_crust, item);
            
            list.splice(item,1);
            for (let x=0; x < list.length; x++){
                const item2 = list[x];
                document.getElementById('id_barrier_thickness_' + item2).style.display = 'none';
                document.getElementById('id_surface_quality_' + item2).style.display = 'none';
                document.getElementById('id_surpressant_crust_' + item2).style.display = 'none';
                document.getElementById('id_additional_surpressant_' + item2).style.display = 'none';
                document.getElementById('id_comments_' + item2).style.display = 'none';

                document.getElementById('id_barrier_thickness_' + item2).required = false;
                document.getElementById('id_surface_quality_' + item2).required = false;
                document.getElementById('id_surpressant_crust_' + item2).required = false;
                document.getElementById('id_additional_surpressant_' + item2).required = false;
                document.getElementById('id_comments_' + item2).required = false;
            }
            break;
        } else {
            document.getElementById('id_additional_surpressant_' + item).style.display = 'inline-block';
            document.getElementById('id_comments_' + item).style.display = 'inline-block';
            document.getElementById('id_additional_surpressant_' + item).required = false;
            document.getElementById('id_comments_' + item).required = false;

            list.splice(item,1);
            list.forEach((item2) => {
                document.getElementById('id_barrier_thickness_' + item2).style.display = 'inline-block';
                document.getElementById('id_surface_quality_' + item2).style.display = 'inline-block';
                document.getElementById('id_surpressant_crust_' + item2).style.display = 'inline-block';
                document.getElementById('id_additional_surpressant_' + item2).style.display = 'inline-block';
                document.getElementById('id_comments_' + item2).style.display = 'inline-block';
            })
            list.splice(item, 0, item);
        }
    }
}
function section_4_hidden() {
    list = [0,1,2,3,4];
    for (let item=0; item < list.length; item++){
        const wharf = document.getElementById('id_wharf_' + item).value;
        const breeze = document.getElementById('id_breeze_' + item).value;
        if (wharf || breeze) {
            document.getElementById('id_wharf_' + item).required = true;
            document.getElementById('id_breeze_' + item).required = true;
            list.splice(item,1);
            for (let x=0; x < list.length; x++){
                const item2 = list[x];
                document.getElementById('id_wharf_' + item2).style.display = 'none';
                document.getElementById('id_breeze_' + item2).style.display = 'none';

                document.getElementById('id_wharf_' + item2).required = false;
                document.getElementById('id_breeze_' + item2).required = false;
            }
            break;
        } else {
            list.splice(item,1);
            list.forEach((item2) => {
                document.getElementById('id_wharf_' + item2).style.display = 'inline-block';
                document.getElementById('id_breeze_' + item2).style.display = 'inline-block';
            })
            list.splice(item, 0, item);
        }
    }
}

function auto_fill_section_1() {
    list = [0,1,2,3,4]
    list.forEach((item) => {
        const q_spills = document.getElementById('id_spills_' + item).value;
        if (q_spills == "No") {
            document.getElementById('id_pushed_back_' + item).value = 'N/A';
        }
        else {
            document.getElementById('id_pushed_back_' + item).value = '';
        }
    })
}
function auto_fill_section_2() {
    list = [0,1,2,3,4];
    list.forEach((item) => {
        const q_vessel = document.getElementById('id_coal_vessel_' + item).value;
        
        if (q_vessel == "No") {
            document.getElementById('id_water_sprays_' + item).value = 'N/A';
            document.getElementById('id_loader_lowered_' + item).value = 'N/A';
            document.getElementById('id_working_water_sprays_' + item).value = 'N/A';
        }
    })
}
function auto_fill_section_3() {
    list = [0,1,2,3,4];
    for (let item=0; item < list.length; item++){
        const surpressant_crust = document.getElementById('id_surpressant_crust_' + item).value;
        auto_fill_section_3_each(surpressant_crust, item);
    }
}
function auto_fill_section_3_each(surpressant_crust, item) {
    if (surpressant_crust == 'Yes') {
        document.getElementById('id_additional_surpressant_' + item).style.display = 'none';
        document.getElementById('id_comments_' + item).style.display = 'none';
        document.getElementById('id_additional_surpressant_' + item).required = false;
        document.getElementById('id_comments_' + item).required = false;
    } else if (surpressant_crust == 'No') {
        document.getElementById('id_additional_surpressant_' + item).style.display = 'inline-block';
        document.getElementById('id_comments_' + item).style.display = 'inline-block';
        document.getElementById('id_additional_surpressant_' + item).required = true;
        document.getElementById('id_comments_' + item).required = true;
    } else {
        document.getElementById('id_additional_surpressant_' + item).style.display = 'inline-block';
        document.getElementById('id_comments_' + item).style.display = 'inline-block';
        document.getElementById('id_additional_surpressant_' + item).required = false;
        document.getElementById('id_comments_' + item).required = false;
    }
}

function section_2_require() {
    list = [0,1,2,3,4];
    list.forEach((item) => {
        const coal_vessel = document.getElementById('id_coal_vessel_' + item).value;

        if (coal_vessel) {
            document.getElementsById('id_coal_vessel_' + item).required = true;
            document.getElementsById('id_water_sprays_' + item).required = true;
            document.getElementsById('id_loader_lowered_' + item).required = true;
            document.getElementsById('id_working_water_sprays_' + item).required = true;

            list.splice(item,1);
            list.forEach((item2) => {
                document.getElementById('id_coal_vessel_' + item2).style.display = 'none';
                document.getElementById('id_water_sprays_' + item2).style.display = 'none';
                document.getElementById('id_loader_lowered_' + item2).style.display = 'none';
                document.getElementById('id_working_water_sprays_' + item2).style.display = 'none';
            })
        } else {
            document.getElementById('id_coal_vessel_' + item).required = false;
            document.getElementById('id_water_sprays_' + item).required = false;
            document.getElementById('id_loader_lowered_' + item).required = false;
            document.getElementById('id_working_water_sprays_' + item).required = false;

            list.splice(item,1);
            list.forEach((item2) => {
                document.getElementById('id_coal_vessel_' + item2).style.display = 'inline-block';
                document.getElementById('id_water_sprays_' + item2).style.display = 'inline-block';
                document.getElementById('id_loader_lowered_' + item2).style.display = 'inline-block';
                document.getElementById('id_working_water_sprays_' + item2).style.display = 'inline-block';
            })
        }


    })
}

