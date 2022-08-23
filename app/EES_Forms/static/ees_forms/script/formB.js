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

function run_it() {
    const freq = document.getElementById('frequency').innerText;
    if (freq == 'True') {
        auto_fill_vessel();
        auto_fill_spills();
        return '5days';
    } else {
        return '1day';
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

function info_already_entered() {
    list = [0,1,2,3,4];
    for (let item=0; item < list.length; item++){
        const barrier_thickness = document.getElementById('id_barrier_thickness_' + item).value;
        const surface_quality = document.getElementById('id_surface_quality_' + item).value;
        const surpressant_crust = document.getElementById('id_surpressant_crust_' + item).value;
        
        if (barrier_thickness || surface_quality || surpressant_crust) {
            document.getElementById('id_barrier_thickness_' + item).required = true;
            document.getElementById('id_surface_quality_' + item).required = true;
            document.getElementById('id_surpressant_crust_' + item).required = true;
            auto_hide_storage(surpressant_crust, item)
            
            list.splice(item,1);
            for (let x=0; x < list.length; x++){
                const item2 = list[x];
                console.log(item2);
                document.getElementById('id_barrier_thickness_' + item2).style.display = 'none';
                document.getElementById('id_surface_quality_' + item2).style.display = 'none';
                document.getElementById('id_surpressant_crust_' + item2).style.display = 'none';
                document.getElementById('id_additional_surpressant_' + item2).style.display = 'none';
                document.getElementById('id_comments_' + item2).style.display = 'none';
            }
            break;
        } else {
            document.getElementById('id_barrier_thickness_' + item).required = false;
            document.getElementById('id_surface_quality_' + item).required = false;
            document.getElementById('id_surpressant_crust_' + item).required = false;

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

function auto_hide_storage(surpressant_crust, item) {
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

function house_keeping() {    
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
            }
            break;
        } else {
            document.getElementById('id_wharf_' + item).required = false;
            document.getElementById('id_breeze_' + item).required = false;
            list.splice(item,1);
            list.forEach((item2) => {
                document.getElementById('id_wharf_' + item2).style.display = 'inline-block';
                document.getElementById('id_breeze_' + item2).style.display = 'inline-block';
            })
            list.splice(item, 0, item);
        }
    }
}

/*function sprayed_storage() {
    list = [0,1,2,3,4];
    for (let item=0; item < list.length; item++){
        const barrier_thick = document.getElementById('id_barrier_thickness_' + item).value;
        const surface_quality = document.getElementById('id_surface_quality_' + item).value;
        if (barrier_thick || surface_quality) {
            document.getElementById('id_barrier_thickness_' + item).required = true;
            document.getElementById('id_surface_quality_' + item).required = true;
            list.splice(item,1);
            for (let x=0; x < list.length; x++){
                const item2 = list[x];
                document.getElementById('id_barrier_thickness_' + item).style.display = 'none';
                document.getElementById('id_surface_quality_' + item).style.display = 'none';
            }
            break;
        } else {
            document.getElementById('id_barrier_thickness_' + item).required = false;
            document.getElementById('id_surface_quality_' + item).required = false;
            list.splice(item,1);
            list.forEach((item2) => {
                document.getElementById('id_barrier_thickness_' + item).style.display = 'inline-block';
                document.getElementById('id_surface_quality_' + item).style.display = 'inline-block';
            })
            list.splice(item, 0, item);
        }
    }
} */

run_it();
house_keeping();
info_already_entered();
