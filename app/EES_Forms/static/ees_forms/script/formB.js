function hidden_material() {
    run_it();

    if (run_it() == '1day') {
        list = [0,1,2,3,4];
        for (let item=0; item < list.length; item++){
            const fugitive_dust_observed = document.getElementById('id_fugitive_dust_observed_' + item).value;
            const supressant_applied = document.getElementById('id_supressant_applied_' + item).value;
            const supressant_active = document.getElementById('id_supressant_active_' + item).value;
            const working_face_exceed = document.getElementById('id_working_face_exceed_' + item).value;
            const spills = document.getElementById('id_spills_' + item).value;
            const pushed_back = document.getElementById('id_pushed_back_' + item).value;

            if ((fugitive_dust_observed || supressant_applied || supressant_active || working_face_exceed || pushed_back ) && spills == 'Yes' ) {
                list.splice(item,1);
                list.forEach((item2) => {
                    console.log('DONT SHOW ' + item + ' YES')
                    document.getElementById('id_fugitive_dust_observed_' + item2).style.display = 'none';
                    document.getElementById('id_supressant_applied_' + item2).style.display = 'none';
                    document.getElementById('id_supressant_active_' + item2).style.display = 'none';
                    document.getElementById('id_working_face_exceed_' + item2).style.display = 'none';
                    document.getElementById('id_spills_' + item2).style.display = 'none';
                    document.getElementById('id_pushed_back_' + item2).style.display = 'none';
                })
                break;
            } else if ((fugitive_dust_observed || supressant_applied || supressant_active || working_face_exceed) && (spills == '' && pushed_back == 'N/A')) {
                list.splice(item,1);
                list.forEach((item2) => {
                    console.log('DONT SHOW ' + item + ' NONE')
                    document.getElementById('id_fugitive_dust_observed_' + item2).style.display = 'none';
                    document.getElementById('id_supressant_applied_' + item2).style.display = 'none';
                    document.getElementById('id_supressant_active_' + item2).style.display = 'none';
                    document.getElementById('id_working_face_exceed_' + item2).style.display = 'none';
                    document.getElementById('id_spills_' + item2).style.display = 'none';
                    document.getElementById('id_pushed_back_' + item2).style.display = 'none';
                })
                auto_fill_spills()
                break;
            } else if (fugitive_dust_observed || supressant_applied || supressant_active || working_face_exceed || spills ) {
                list.splice(item,1);
                list.forEach((item2) => {
                    console.log('DONT SHOW ' + item + ' NO')
                    document.getElementById('id_fugitive_dust_observed_' + item2).style.display = 'none';
                    document.getElementById('id_supressant_applied_' + item2).style.display = 'none';
                    document.getElementById('id_supressant_active_' + item2).style.display = 'none';
                    document.getElementById('id_working_face_exceed_' + item2).style.display = 'none';
                    document.getElementById('id_spills_' + item2).style.display = 'none';
                    document.getElementById('id_pushed_back_' + item2).style.display = 'none';
                })
                auto_fill_spills()
                break;
            } else if (fugitive_dust_observed == '' && supressant_applied == '' && supressant_active == '' && working_face_exceed == '' && spills == '' && pushed_back == 'N/A') {
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
                auto_fill_spills()
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
    
}

function hidden_vessel() {
    run_it();

    if (run_it() == '1day') {
        list = [0,1,2,3,4];
        console.log(list);
        for (let item=0; item < list.length; item++){
            const coal_vessel = document.getElementById('id_coal_vessel_' + item).value;
            const water_sprays = document.getElementById('id_water_sprays_' + item).value;
            const loader_lowered = document.getElementById('id_loader_lowered_' + item).value;
            const working_water_sprays = document.getElementById('id_working_water_sprays_' + item).value;
            console.log(item);
            if ( coal_vessel == 'No' ) {
                list.splice(item,1);
                list.forEach((item2) => {
                    console.log('DONT SHOW ' + item + ' NO')
                    document.getElementById('id_coal_vessel_' + item2).style.display = 'none';
                    document.getElementById('id_water_sprays_' + item2).style.display = 'none';
                    document.getElementById('id_loader_lowered_' + item2).style.display = 'none';
                    document.getElementById('id_working_water_sprays_' + item2).style.display = 'none';
                })
                auto_fill_vessel();
                break;
            } else if ( (water_sprays || loader_lowered || working_water_sprays) && (coal_vessel == 'Yes') ) {
                list.splice(item,1);
                list.forEach((item2) => {
                    console.log('DONT SHOW OTHER ' + item + ' YES')
                    document.getElementById('id_coal_vessel_' + item2).style.display = 'none';
                    document.getElementById('id_water_sprays_' + item2).style.display = 'none';
                    document.getElementById('id_loader_lowered_' + item2).style.display = 'none';
                    document.getElementById('id_working_water_sprays_' + item2).style.display = 'none';
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
                })
                auto_fill_vessel();
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
}

function auto_fill_vessel() {
    list = [0,1,2,3,4];
    list.forEach((item) => {
        const q_vessel = document.getElementById('id_coal_vessel_' + item).value;
        
        if (q_vessel == "No") {
            document.getElementById('id_water_sprays_' + item).value = 'N/A';
            document.getElementById('id_loader_lowered_' + item).value = 'N/A';
            document.getElementById('id_working_water_sprays_' + item).value = 'N/A';
        } else {
            document.getElementById('id_water_sprays_' + item).value = '';
            document.getElementById('id_loader_lowered_' + item).value = '';
            document.getElementById('id_working_water_sprays_' + item).value = '';
        }
    })
}

function auto_fill_spills() {
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

function info_already_entered_0() {
    run_it();

    if (run_it() == '1day') {
        const barrier_thickness_0 = document.getElementById('id_barrier_thickness_0').value;
        const surface_quality_0 = document.getElementById('id_surface_quality_0').value;
        const surpressant_crust_0 = document.getElementById('id_surpressant_crust_0').value;
        
        
        if (barrier_thickness_0 || surface_quality_0 || surpressant_crust_0) {
            document.getElementById('id_barrier_thickness_0').required = true;
            document.getElementById('id_surface_quality_0').required = true;
            document.getElementById('id_surpressant_crust_0').required = true;

            document.getElementById('id_barrier_thickness_1').style.display = 'none';
            document.getElementById('id_barrier_thickness_2').style.display = 'none';
            document.getElementById('id_barrier_thickness_3').style.display = 'none';
            document.getElementById('id_barrier_thickness_4').style.display = 'none';
            document.getElementById('id_surface_quality_1').style.display = 'none';
            document.getElementById('id_surface_quality_2').style.display = 'none';
            document.getElementById('id_surface_quality_3').style.display = 'none';
            document.getElementById('id_surface_quality_4').style.display = 'none';
            document.getElementById('id_surpressant_crust_1').style.display = 'none';
            document.getElementById('id_surpressant_crust_2').style.display = 'none';
            document.getElementById('id_surpressant_crust_3').style.display = 'none';
            document.getElementById('id_surpressant_crust_4').style.display = 'none';
            document.getElementById('id_additional_surpressant_1').style.display = 'none';
            document.getElementById('id_additional_surpressant_2').style.display = 'none';
            document.getElementById('id_additional_surpressant_3').style.display = 'none';
            document.getElementById('id_additional_surpressant_4').style.display = 'none';
            document.getElementById('id_comments_1').style.display = 'none';
            document.getElementById('id_comments_2').style.display = 'none';
            document.getElementById('id_comments_3').style.display = 'none';
            document.getElementById('id_comments_4').style.display = 'none';
            if (surpressant_crust_0 == 'Yes') {
                document.getElementById('id_additional_surpressant_0').style.display = 'none';
                document.getElementById('id_comments_0').style.display = 'none';
                document.getElementById('id_additional_surpressant_0').required = false;
                document.getElementById('id_comments_0').required = false;
            } else if (surpressant_crust_0 == 'No') {
                document.getElementById('id_additional_surpressant_0').style.display = 'inline-block';
                document.getElementById('id_comments_0').style.display = 'inline-block';
                document.getElementById('id_additional_surpressant_0').required = true;
                document.getElementById('id_comments_0').required = true;
            } else {
                document.getElementById('id_additional_surpressant_0').style.display = 'inline-block';
                document.getElementById('id_comments_0').style.display = 'inline-block';
                document.getElementById('id_additional_surpressant_0').required = false;
                document.getElementById('id_comments_0').required = false;
            }
        } else {
            document.getElementById('id_barrier_thickness_1').style.display = 'inline-block';
            document.getElementById('id_barrier_thickness_2').style.display = 'inline-block';
            document.getElementById('id_barrier_thickness_3').style.display = 'inline-block';
            document.getElementById('id_barrier_thickness_4').style.display = 'inline-block';
            document.getElementById('id_surface_quality_1').style.display = 'inline-block';
            document.getElementById('id_surface_quality_2').style.display = 'inline-block';
            document.getElementById('id_surface_quality_3').style.display = 'inline-block';
            document.getElementById('id_surface_quality_4').style.display = 'inline-block';
            document.getElementById('id_surpressant_crust_1').style.display = 'inline-block';
            document.getElementById('id_surpressant_crust_2').style.display = 'inline-block';
            document.getElementById('id_surpressant_crust_3').style.display = 'inline-block';
            document.getElementById('id_surpressant_crust_4').style.display = 'inline-block';
            document.getElementById('id_additional_surpressant_1').style.display = 'inline-block';
            document.getElementById('id_additional_surpressant_2').style.display = 'inline-block';
            document.getElementById('id_additional_surpressant_3').style.display = 'inline-block';
            document.getElementById('id_additional_surpressant_4').style.display = 'inline-block';
            document.getElementById('id_comments_1').style.display = 'inline-block';
            document.getElementById('id_comments_2').style.display = 'inline-block';
            document.getElementById('id_comments_3').style.display = 'inline-block';
            document.getElementById('id_comments_4').style.display = 'inline-block';

            document.getElementById('id_barrier_thickness_0').required = false;
            document.getElementById('id_surface_quality_0').required = false;
            document.getElementById('id_surpressant_crust_0').required = false;

            document.getElementById('id_additional_surpressant_0').style.display = 'inline-block';
            document.getElementById('id_comments_0').style.display = 'inline-block';
            document.getElementById('id_additional_surpressant_0').required = false;
            document.getElementById('id_comments_0').required = false;
        }
    }
}

function info_already_entered_1() {
    run_it();

    if (run_it() == '1day') {
        const barrier_thickness_1 = document.getElementById('id_barrier_thickness_1').value;
        const surface_quality_1 = document.getElementById('id_surface_quality_1').value;
        const surpressant_crust_1 = document.getElementById('id_surpressant_crust_1').value;

        if (barrier_thickness_1 || surface_quality_1 || surpressant_crust_1) {
            document.getElementById('id_barrier_thickness_1').required = true;
            document.getElementById('id_surface_quality_1').required = true;
            document.getElementById('id_surpressant_crust_1').required = true;

            document.getElementById('id_barrier_thickness_0').style.display = 'none';
            document.getElementById('id_barrier_thickness_2').style.display = 'none';
            document.getElementById('id_barrier_thickness_3').style.display = 'none';
            document.getElementById('id_barrier_thickness_4').style.display = 'none';
            document.getElementById('id_surface_quality_0').style.display = 'none';
            document.getElementById('id_surface_quality_2').style.display = 'none';
            document.getElementById('id_surface_quality_3').style.display = 'none';
            document.getElementById('id_surface_quality_4').style.display = 'none';
            document.getElementById('id_surpressant_crust_0').style.display = 'none';
            document.getElementById('id_surpressant_crust_2').style.display = 'none';
            document.getElementById('id_surpressant_crust_3').style.display = 'none';
            document.getElementById('id_surpressant_crust_4').style.display = 'none';
            document.getElementById('id_additional_surpressant_0').style.display = 'none';
            document.getElementById('id_additional_surpressant_2').style.display = 'none';
            document.getElementById('id_additional_surpressant_3').style.display = 'none';
            document.getElementById('id_additional_surpressant_4').style.display = 'none';
            document.getElementById('id_comments_0').style.display = 'none';
            document.getElementById('id_comments_2').style.display = 'none';
            document.getElementById('id_comments_3').style.display = 'none';
            document.getElementById('id_comments_4').style.display = 'none';
            
            if (surpressant_crust_1 == 'Yes') {
                document.getElementById('id_additional_surpressant_1').style.display = 'none';
                document.getElementById('id_comments_1').style.display = 'none';
                document.getElementById('id_additional_surpressant_1').required = false;
                document.getElementById('id_comments_1').required = false;
            } else if (surpressant_crust_1 == 'No') {
                document.getElementById('id_additional_surpressant_1').style.display = 'inline-block';
                document.getElementById('id_comments_1').style.display = 'inline-block';
                document.getElementById('id_additional_surpressant_1').required = true;
                document.getElementById('id_comments_1').required = true;
            } else {
                document.getElementById('id_additional_surpressant_1').style.display = 'inline-block';
                document.getElementById('id_comments_1').style.display = 'inline-block';
                document.getElementById('id_additional_surpressant_1').required = false;
                document.getElementById('id_comments_1').required = false;
            }
        } else {
            document.getElementById('id_barrier_thickness_0').style.display = 'inline-block';
            document.getElementById('id_barrier_thickness_2').style.display = 'inline-block';
            document.getElementById('id_barrier_thickness_3').style.display = 'inline-block';
            document.getElementById('id_barrier_thickness_4').style.display = 'inline-block';
            document.getElementById('id_surface_quality_0').style.display = 'inline-block';
            document.getElementById('id_surface_quality_2').style.display = 'inline-block';
            document.getElementById('id_surface_quality_3').style.display = 'inline-block';
            document.getElementById('id_surface_quality_4').style.display = 'inline-block';
            document.getElementById('id_surpressant_crust_0').style.display = 'inline-block';
            document.getElementById('id_surpressant_crust_2').style.display = 'inline-block';
            document.getElementById('id_surpressant_crust_3').style.display = 'inline-block';
            document.getElementById('id_surpressant_crust_4').style.display = 'inline-block';
            document.getElementById('id_additional_surpressant_0').style.display = 'inline-block';
            document.getElementById('id_additional_surpressant_2').style.display = 'inline-block';
            document.getElementById('id_additional_surpressant_3').style.display = 'inline-block';
            document.getElementById('id_additional_surpressant_4').style.display = 'inline-block';
            document.getElementById('id_comments_0').style.display = 'inline-block';
            document.getElementById('id_comments_2').style.display = 'inline-block';
            document.getElementById('id_comments_3').style.display = 'inline-block';
            document.getElementById('id_comments_4').style.display = 'inline-block';

            document.getElementById('id_barrier_thickness_1').required = false;
            document.getElementById('id_surface_quality_1').required = false;
            document.getElementById('id_surpressant_crust_1').required = false;

            document.getElementById('id_additional_surpressant_1').style.display = 'inline-block';
            document.getElementById('id_comments_1').style.display = 'inline-block';
            document.getElementById('id_additional_surpressant_1').required = false;
            document.getElementById('id_comments_1').required = false;
        }
    }
}

function info_already_entered_2() {
    run_it();

    if (run_it() == '1day') {
        const barrier_thickness_2 = document.getElementById('id_barrier_thickness_2').value;
        const surface_quality_2 = document.getElementById('id_surface_quality_2').value;
        const surpressant_crust_2 = document.getElementById('id_surpressant_crust_2').value;

        if (barrier_thickness_2 || surface_quality_2 || surpressant_crust_2) {
            document.getElementById('id_barrier_thickness_2').required = true;
            document.getElementById('id_surface_quality_2').required = true;
            document.getElementById('id_surpressant_crust_2').required = true;

            document.getElementById('id_barrier_thickness_0').style.display = 'none';
            document.getElementById('id_barrier_thickness_1').style.display = 'none';
            document.getElementById('id_barrier_thickness_3').style.display = 'none';
            document.getElementById('id_barrier_thickness_4').style.display = 'none';
            document.getElementById('id_surface_quality_0').style.display = 'none';
            document.getElementById('id_surface_quality_1').style.display = 'none';
            document.getElementById('id_surface_quality_3').style.display = 'none';
            document.getElementById('id_surface_quality_4').style.display = 'none';
            document.getElementById('id_surpressant_crust_0').style.display = 'none';
            document.getElementById('id_surpressant_crust_1').style.display = 'none';
            document.getElementById('id_surpressant_crust_3').style.display = 'none';
            document.getElementById('id_surpressant_crust_4').style.display = 'none';
            document.getElementById('id_additional_surpressant_0').style.display = 'none';
            document.getElementById('id_additional_surpressant_1').style.display = 'none';
            document.getElementById('id_additional_surpressant_3').style.display = 'none';
            document.getElementById('id_additional_surpressant_4').style.display = 'none';
            document.getElementById('id_comments_0').style.display = 'none';
            document.getElementById('id_comments_1').style.display = 'none';
            document.getElementById('id_comments_3').style.display = 'none';
            document.getElementById('id_comments_4').style.display = 'none';
            if (surpressant_crust_2 == 'Yes') {
                document.getElementById('id_additional_surpressant_2').style.display = 'none';
                document.getElementById('id_comments_2').style.display = 'none';
                document.getElementById('id_additional_surpressant_2').required = false;
                document.getElementById('id_comments_2').required = false;
            } else if (surpressant_crust_2 == 'No') {
                document.getElementById('id_additional_surpressant_2').style.display = 'inline-block';
                document.getElementById('id_comments_2').style.display = 'inline-block';
                document.getElementById('id_additional_surpressant_2').required = true;
                document.getElementById('id_comments_2').required = true;
            } else {
                document.getElementById('id_additional_surpressant_2').style.display = 'inline-block';
                document.getElementById('id_comments_2').style.display = 'inline-block';
                document.getElementById('id_additional_surpressant_2').required = false;
                document.getElementById('id_comments_2').required = false;
            }
        } else {
            document.getElementById('id_barrier_thickness_0').style.display = 'inline-block';
            document.getElementById('id_barrier_thickness_1').style.display = 'inline-block';
            document.getElementById('id_barrier_thickness_3').style.display = 'inline-block';
            document.getElementById('id_barrier_thickness_4').style.display = 'inline-block';
            document.getElementById('id_surface_quality_0').style.display = 'inline-block';
            document.getElementById('id_surface_quality_1').style.display = 'inline-block';
            document.getElementById('id_surface_quality_3').style.display = 'inline-block';
            document.getElementById('id_surface_quality_4').style.display = 'inline-block';
            document.getElementById('id_surpressant_crust_0').style.display = 'inline-block';
            document.getElementById('id_surpressant_crust_1').style.display = 'inline-block';
            document.getElementById('id_surpressant_crust_3').style.display = 'inline-block';
            document.getElementById('id_surpressant_crust_4').style.display = 'inline-block';
            document.getElementById('id_additional_surpressant_0').style.display = 'inline-block';
            document.getElementById('id_additional_surpressant_1').style.display = 'inline-block';
            document.getElementById('id_additional_surpressant_3').style.display = 'inline-block';
            document.getElementById('id_additional_surpressant_4').style.display = 'inline-block';
            document.getElementById('id_comments_0').style.display = 'inline-block';
            document.getElementById('id_comments_1').style.display = 'inline-block';
            document.getElementById('id_comments_3').style.display = 'inline-block';
            document.getElementById('id_comments_4').style.display = 'inline-block';

            document.getElementById('id_barrier_thickness_2').required = false;
            document.getElementById('id_surface_quality_2').required = false;
            document.getElementById('id_surpressant_crust_2').required = false;

            document.getElementById('id_additional_surpressant_2').style.display = 'inline-block';
            document.getElementById('id_comments_2').style.display = 'inline-block';
            document.getElementById('id_additional_surpressant_2').required = false;
            document.getElementById('id_comments_2').required = false;
        }
    }
}

function info_already_entered_3() {
    run_it();

    if (run_it() == '1day') {
        const barrier_thickness_3 = document.getElementById('id_barrier_thickness_3').value;
        const surface_quality_3 = document.getElementById('id_surface_quality_3').value;
        const surpressant_crust_3 = document.getElementById('id_surpressant_crust_3').value;

        if (barrier_thickness_3 || surface_quality_3 || surpressant_crust_3) {
            document.getElementById('id_barrier_thickness_3').required = true;
            document.getElementById('id_surface_quality_3').required = true;
            document.getElementById('id_surpressant_crust_3').required = true;
            document.getElementById('id_barrier_thickness_0').style.display = 'none';
            document.getElementById('id_barrier_thickness_1').style.display = 'none';
            document.getElementById('id_barrier_thickness_2').style.display = 'none';
            document.getElementById('id_barrier_thickness_4').style.display = 'none';
            document.getElementById('id_surface_quality_0').style.display = 'none';
            document.getElementById('id_surface_quality_1').style.display = 'none';
            document.getElementById('id_surface_quality_2').style.display = 'none';
            document.getElementById('id_surface_quality_4').style.display = 'none';
            document.getElementById('id_surpressant_crust_0').style.display = 'none';
            document.getElementById('id_surpressant_crust_1').style.display = 'none';
            document.getElementById('id_surpressant_crust_2').style.display = 'none';
            document.getElementById('id_surpressant_crust_4').style.display = 'none';
            document.getElementById('id_additional_surpressant_0').style.display = 'none';
            document.getElementById('id_additional_surpressant_1').style.display = 'none';
            document.getElementById('id_additional_surpressant_2').style.display = 'none';
            document.getElementById('id_additional_surpressant_4').style.display = 'none';
            document.getElementById('id_comments_0').style.display = 'none';
            document.getElementById('id_comments_1').style.display = 'none';
            document.getElementById('id_comments_2').style.display = 'none';
            document.getElementById('id_comments_4').style.display = 'none';
            if (surpressant_crust_3 == 'Yes') {
                document.getElementById('id_additional_surpressant_3').style.display = 'none';
                document.getElementById('id_comments_3').style.display = 'none';
                document.getElementById('id_additional_surpressant_3').required = false;
                document.getElementById('id_comments_3').required = false;
            } else if (surpressant_crust_3 == 'No') {
                document.getElementById('id_additional_surpressant_3').style.display = 'inline-block';
                document.getElementById('id_comments_3').style.display = 'inline-block';
                document.getElementById('id_additional_surpressant_3').required = true;
                document.getElementById('id_comments_3').required = true;
            } else {
                document.getElementById('id_additional_surpressant_3').style.display = 'inline-block';
                document.getElementById('id_comments_3').style.display = 'inline-block';
                document.getElementById('id_additional_surpressant_3').required = false;
                document.getElementById('id_comments_3').required = false;
            }
        } else {
            document.getElementById('id_barrier_thickness_0').style.display = 'inline-block';
            document.getElementById('id_barrier_thickness_1').style.display = 'inline-block';
            document.getElementById('id_barrier_thickness_2').style.display = 'inline-block';
            document.getElementById('id_barrier_thickness_4').style.display = 'inline-block';
            document.getElementById('id_surface_quality_0').style.display = 'inline-block';
            document.getElementById('id_surface_quality_1').style.display = 'inline-block';
            document.getElementById('id_surface_quality_2').style.display = 'inline-block';
            document.getElementById('id_surface_quality_4').style.display = 'inline-block';
            document.getElementById('id_surpressant_crust_0').style.display = 'inline-block';
            document.getElementById('id_surpressant_crust_1').style.display = 'inline-block';
            document.getElementById('id_surpressant_crust_2').style.display = 'inline-block';
            document.getElementById('id_surpressant_crust_4').style.display = 'inline-block';
            document.getElementById('id_additional_surpressant_0').style.display = 'inline-block';
            document.getElementById('id_additional_surpressant_1').style.display = 'inline-block';
            document.getElementById('id_additional_surpressant_2').style.display = 'inline-block';
            document.getElementById('id_additional_surpressant_4').style.display = 'inline-block';
            document.getElementById('id_comments_0').style.display = 'inline-block';
            document.getElementById('id_comments_1').style.display = 'inline-block';
            document.getElementById('id_comments_2').style.display = 'inline-block';
            document.getElementById('id_comments_4').style.display = 'inline-block';

            document.getElementById('id_barrier_thickness_3').required = false;
            document.getElementById('id_surface_quality_3').required = false;
            document.getElementById('id_surpressant_crust_3').required = false;

            document.getElementById('id_additional_surpressant_3').style.display = 'inline-block';
            document.getElementById('id_comments_3').style.display = 'inline-block';
            document.getElementById('id_additional_surpressant_3').required = false;
            document.getElementById('id_comments_3').required = false;
        }
    }
}

function info_already_entered_4() {
    run_it();

    if (run_it() == '1day') {
        const barrier_thickness_4 = document.getElementById('id_barrier_thickness_4').value;
        const surface_quality_4 = document.getElementById('id_surface_quality_4').value;
        const surpressant_crust_4 = document.getElementById('id_surpressant_crust_4').value;

        if (barrier_thickness_4 || surface_quality_4 || surpressant_crust_4) {
            document.getElementById('id_barrier_thickness_4').required = true;
            document.getElementById('id_surface_quality_4').required = true;
            document.getElementById('id_surpressant_crust_4').required = true;

            document.getElementById('id_barrier_thickness_0').style.display = 'none';
            document.getElementById('id_barrier_thickness_1').style.display = 'none';
            document.getElementById('id_barrier_thickness_2').style.display = 'none';
            document.getElementById('id_barrier_thickness_3').style.display = 'none';
            document.getElementById('id_surface_quality_0').style.display = 'none';
            document.getElementById('id_surface_quality_1').style.display = 'none';
            document.getElementById('id_surface_quality_2').style.display = 'none';
            document.getElementById('id_surface_quality_3').style.display = 'none';
            document.getElementById('id_surpressant_crust_0').style.display = 'none';
            document.getElementById('id_surpressant_crust_1').style.display = 'none';
            document.getElementById('id_surpressant_crust_2').style.display = 'none';
            document.getElementById('id_surpressant_crust_3').style.display = 'none';
            document.getElementById('id_additional_surpressant_0').style.display = 'none';
            document.getElementById('id_additional_surpressant_1').style.display = 'none';
            document.getElementById('id_additional_surpressant_2').style.display = 'none';
            document.getElementById('id_additional_surpressant_3').style.display = 'none';
            document.getElementById('id_comments_0').style.display = 'none';
            document.getElementById('id_comments_1').style.display = 'none';
            document.getElementById('id_comments_2').style.display = 'none';
            document.getElementById('id_comments_3').style.display = 'none';
            if (surpressant_crust_4 == 'Yes') {
                document.getElementById('id_additional_surpressant_4').style.display = 'none';
                document.getElementById('id_comments_4').style.display = 'none';
                document.getElementById('id_additional_surpressant_4').required = false;
                document.getElementById('id_comments_4').required = false;
            } else if (surpressant_crust_4 == 'No') {
                document.getElementById('id_additional_surpressant_4').style.display = 'inline-block';
                document.getElementById('id_comments_4').style.display = 'inline-block';
                document.getElementById('id_additional_surpressant_4').required = true;
                document.getElementById('id_comments_4').required = true;
            } else {
                document.getElementById('id_additional_surpressant_4').style.display = 'inline-block';
                document.getElementById('id_comments_4').style.display = 'inline-block';
                document.getElementById('id_additional_surpressant_4').required = false;
                document.getElementById('id_comments_4').required = false;
            }
        } else {
            document.getElementById('id_barrier_thickness_0').style.display = 'inline-block';
            document.getElementById('id_barrier_thickness_1').style.display = 'inline-block';
            document.getElementById('id_barrier_thickness_2').style.display = 'inline-block';
            document.getElementById('id_barrier_thickness_3').style.display = 'inline-block';
            document.getElementById('id_surface_quality_0').style.display = 'inline-block';
            document.getElementById('id_surface_quality_1').style.display = 'inline-block';
            document.getElementById('id_surface_quality_2').style.display = 'inline-block';
            document.getElementById('id_surface_quality_3').style.display = 'inline-block';
            document.getElementById('id_surpressant_crust_0').style.display = 'inline-block';
            document.getElementById('id_surpressant_crust_1').style.display = 'inline-block';
            document.getElementById('id_surpressant_crust_2').style.display = 'inline-block';
            document.getElementById('id_surpressant_crust_3').style.display = 'inline-block';
            document.getElementById('id_additional_surpressant_0').style.display = 'inline-block';
            document.getElementById('id_additional_surpressant_1').style.display = 'inline-block';
            document.getElementById('id_additional_surpressant_2').style.display = 'inline-block';
            document.getElementById('id_additional_surpressant_3').style.display = 'inline-block';
            document.getElementById('id_comments_0').style.display = 'inline-block';
            document.getElementById('id_comments_1').style.display = 'inline-block';
            document.getElementById('id_comments_2').style.display = 'inline-block';
            document.getElementById('id_comments_3').style.display = 'inline-block';

            document.getElementById('id_barrier_thickness_4').required = false;
            document.getElementById('id_surface_quality_4').required = false;
            document.getElementById('id_surpressant_crust_4').required = false;

            document.getElementById('id_additional_surpressant_4').style.display = 'inline-block';
            document.getElementById('id_comments_4').style.display = 'inline-block';
            document.getElementById('id_additional_surpressant_4').required = false;
            document.getElementById('id_comments_4').required = false;
        }
    }
}

function run_it() {
    const freq = document.getElementById('frequency').innerText;
    if (freq == 'True') {
        const list = [0,1,2,3,4];
        list.forEach((item) => {
            const surpressant_crust = document.getElementById('id_surpressant_crust_' + item).value;
            const coal_vessel = document.getElementById('id_coal_vessel_' + item).value;

            if (surpressant_crust) {
                if (surpressant_crust == 'Yes'){
                    document.getElementById('id_additional_surpressant_' + item).style.display = 'none';
                    document.getElementById('id_comments_' + item).style.display = 'none';
                    document.getElementById('id_additional_surpressant_' + item).required = false;
                    document.getElementById('id_comments_' + item).required = false;
                } else {
                    document.getElementById('id_additional_surpressant_' + item).style.display = 'inline-block';
                    document.getElementById('id_comments_' + item).style.display = 'inline-block';
                    document.getElementById('id_additional_surpressant_' + item).required = true;
                    document.getElementById('id_comments_' + item).required = true;
                }
            } else {
                document.getElementById('id_additional_surpressant_' + item).style.display = 'inline-block';
                document.getElementById('id_comments_' + item).style.display = 'inline-block';
                document.getElementById('id_additional_surpressant_' + item).required = false;
                document.getElementById('id_comments_' + item).required = false;
            }
        })
        auto_fill_vessel();
        auto_fill_spills();
        return '5days';
    } else {
        return '1day';
    }
}

function house_keeping_0() {
    run_it();

    if (run_it() == '1day') {
        const wharf_0 = document.getElementById('id_wharf_0').value;
        const breeze_0 = document.getElementById('id_breeze_0').value;

        if (wharf_0 || breeze_0) {
            document.getElementById('id_wharf_0').required = true;
            document.getElementById('id_breeze_0').required = true;

            document.getElementById('id_wharf_1').style.display = 'none';
            document.getElementById('id_breeze_1').style.display = 'none';
            document.getElementById('id_wharf_2').style.display = 'none';
            document.getElementById('id_breeze_2').style.display = 'none';
            document.getElementById('id_wharf_3').style.display = 'none';
            document.getElementById('id_breeze_3').style.display = 'none';
            document.getElementById('id_wharf_4').style.display = 'none';
            document.getElementById('id_breeze_4').style.display = 'none';
        } else {
            document.getElementById('id_wharf_1').style.display = 'inline-block';
            document.getElementById('id_breeze_1').style.display = 'inline-block';
            document.getElementById('id_wharf_2').style.display = 'inline-block';
            document.getElementById('id_breeze_2').style.display = 'inline-block';
            document.getElementById('id_wharf_3').style.display = 'inline-block';
            document.getElementById('id_breeze_3').style.display = 'inline-block';
            document.getElementById('id_wharf_4').style.display = 'inline-block';
            document.getElementById('id_breeze_4').style.display = 'inline-block';
            

            document.getElementById('id_wharf_0').required = false;
            document.getElementById('id_breeze_0').required = false;
        }
    }
}

function house_keeping_1() {
    run_it();

    if (run_it() == '1day') {
        const wharf_1 = document.getElementById('id_wharf_1').value;
        const breeze_1 = document.getElementById('id_breeze_1').value;

        if (wharf_1 || breeze_1) {
            document.getElementById('id_wharf_1').required = true;
            document.getElementById('id_breeze_1').required = true;

            document.getElementById('id_wharf_0').style.display = 'none';
            document.getElementById('id_breeze_0').style.display = 'none';
            document.getElementById('id_wharf_2').style.display = 'none';
            document.getElementById('id_breeze_2').style.display = 'none';
            document.getElementById('id_wharf_3').style.display = 'none';
            document.getElementById('id_breeze_3').style.display = 'none';
            document.getElementById('id_wharf_4').style.display = 'none';
            document.getElementById('id_breeze_4').style.display = 'none';
        } else {
            document.getElementById('id_wharf_0').style.display = 'inline-block';
            document.getElementById('id_breeze_0').style.display = 'inline-block';
            document.getElementById('id_wharf_2').style.display = 'inline-block';
            document.getElementById('id_breeze_2').style.display = 'inline-block';
            document.getElementById('id_wharf_3').style.display = 'inline-block';
            document.getElementById('id_breeze_3').style.display = 'inline-block';
            document.getElementById('id_wharf_4').style.display = 'inline-block';
            document.getElementById('id_breeze_4').style.display = 'inline-block';
            

            document.getElementById('id_wharf_1').required = false;
            document.getElementById('id_breeze_1').required = false;
        }
    }
}

function house_keeping_2() {
    run_it();

    if (run_it() == '1day') {
        const wharf_2 = document.getElementById('id_wharf_2').value;
        const breeze_2 = document.getElementById('id_breeze_2').value;

        if (wharf_2 || breeze_2) {
            document.getElementById('id_wharf_2').required = true;
            document.getElementById('id_breeze_2').required = true;

            document.getElementById('id_wharf_0').style.display = 'none';
            document.getElementById('id_breeze_0').style.display = 'none';
            document.getElementById('id_wharf_1').style.display = 'none';
            document.getElementById('id_breeze_1').style.display = 'none';
            document.getElementById('id_wharf_3').style.display = 'none';
            document.getElementById('id_breeze_3').style.display = 'none';
            document.getElementById('id_wharf_4').style.display = 'none';
            document.getElementById('id_breeze_4').style.display = 'none';
        } else {
            document.getElementById('id_wharf_0').style.display = 'inline-block';
            document.getElementById('id_breeze_0').style.display = 'inline-block';
            document.getElementById('id_wharf_1').style.display = 'inline-block';
            document.getElementById('id_breeze_1').style.display = 'inline-block';
            document.getElementById('id_wharf_3').style.display = 'inline-block';
            document.getElementById('id_breeze_3').style.display = 'inline-block';
            document.getElementById('id_wharf_4').style.display = 'inline-block';
            document.getElementById('id_breeze_4').style.display = 'inline-block';
            

            document.getElementById('id_wharf_2').required = false;
            document.getElementById('id_breeze_2').required = false;
        }
    }
}

function house_keeping_3() {
    run_it();

    if (run_it() == '1day') {
        const wharf_3 = document.getElementById('id_wharf_3').value;
        const breeze_3 = document.getElementById('id_breeze_3').value;

        if (wharf_3 || breeze_3) {
            document.getElementById('id_wharf_3').required = true;
            document.getElementById('id_breeze_3').required = true;

            document.getElementById('id_wharf_0').style.display = 'none';
            document.getElementById('id_breeze_0').style.display = 'none';
            document.getElementById('id_wharf_1').style.display = 'none';
            document.getElementById('id_breeze_1').style.display = 'none';
            document.getElementById('id_wharf_2').style.display = 'none';
            document.getElementById('id_breeze_2').style.display = 'none';
            document.getElementById('id_wharf_4').style.display = 'none';
            document.getElementById('id_breeze_4').style.display = 'none';
        } else {
            document.getElementById('id_wharf_0').style.display = 'inline-block';
            document.getElementById('id_breeze_0').style.display = 'inline-block';
            document.getElementById('id_wharf_1').style.display = 'inline-block';
            document.getElementById('id_breeze_1').style.display = 'inline-block';
            document.getElementById('id_wharf_2').style.display = 'inline-block';
            document.getElementById('id_breeze_2').style.display = 'inline-block';
            document.getElementById('id_wharf_4').style.display = 'inline-block';
            document.getElementById('id_breeze_4').style.display = 'inline-block';
            

            document.getElementById('id_wharf_3').required = false;
            document.getElementById('id_breeze_3').required = false;
        }
    }
}

function house_keeping_4() {
    run_it();

    if (run_it() == '1day') {
        const wharf_4 = document.getElementById('id_wharf_4').value;
        const breeze_4 = document.getElementById('id_breeze_4').value;

        if (wharf_4 || breeze_4) {
            document.getElementById('id_wharf_4').required = true;
            document.getElementById('id_breeze_4').required = true;

            document.getElementById('id_wharf_0').style.display = 'none';
            document.getElementById('id_breeze_0').style.display = 'none';
            document.getElementById('id_wharf_1').style.display = 'none';
            document.getElementById('id_breeze_1').style.display = 'none';
            document.getElementById('id_wharf_2').style.display = 'none';
            document.getElementById('id_breeze_2').style.display = 'none';
            document.getElementById('id_wharf_3').style.display = 'none';
            document.getElementById('id_breeze_3').style.display = 'none';
        } else {
            document.getElementById('id_wharf_0').style.display = 'inline-block';
            document.getElementById('id_breeze_0').style.display = 'inline-block';
            document.getElementById('id_wharf_1').style.display = 'inline-block';
            document.getElementById('id_breeze_1').style.display = 'inline-block';
            document.getElementById('id_wharf_2').style.display = 'inline-block';
            document.getElementById('id_breeze_2').style.display = 'inline-block';
            document.getElementById('id_wharf_3').style.display = 'inline-block';
            document.getElementById('id_breeze_3').style.display = 'inline-block';
            

            document.getElementById('id_wharf_4').required = false;
            document.getElementById('id_breeze_4').required = false;
        }
    }
}

function loading() {
    run_it();

    if (run_it() == '1day') {
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
                    document.getElementsById('id_coal_vessel_' + item2).style.display = 'none';
                    document.getElementsById('id_water_sprays_' + item2).style.display = 'none';
                    document.getElementsById('id_loader_lowered_' + item2).style.display = 'none';
                    document.getElementsById('id_working_water_sprays_' + item2).style.display = 'none';
                })
            } else {
                document.getElementsById('id_coal_vessel_' + item).required = false;
                document.getElementsById('id_water_sprays_' + item).required = false;
                document.getElementsById('id_loader_lowered_' + item).required = false;
                document.getElementsById('id_working_water_sprays_' + item).required = false;

                list.splice(item,1);
                list.forEach((item2) => {
                    document.getElementsById('id_coal_vessel_' + item2).style.display = 'inline-block';
                    document.getElementsById('id_water_sprays_' + item2).style.display = 'inline-block';
                    document.getElementsById('id_loader_lowered_' + item2).style.display = 'inline-block';
                    document.getElementsById('id_working_water_sprays_' + item2).style.display = 'inline-block';
                })
            }


        })
    }
}