function hidden_questions() {
    const q_crust_0 = document.getElementById('id_surpressant_crust_0').value;
    if (q_crust_0 == 'Yes') {
        document.getElementById('id_additional_surpressant_0').style.display = 'none';
        document.getElementById('id_comments_0').style.display = 'none';
        document.getElementById('id_additional_surpressant_0').required = false;
        document.getElementById('id_comments_0').required = false;
    }
    else if (q_crust_0 == 'No') {
        document.getElementById('id_additional_surpressant_0').style.display = 'inline-block';
        document.getElementById('id_comments_0').style.display = 'inline-block';
        document.getElementById('id_additional_surpressant_0').required = true;
        document.getElementById('id_comments_0').required = true;
    }
    else {
        document.getElementById('id_additional_surpressant_0').style.display = 'inline-block';
        document.getElementById('id_comments_0').style.display = 'inline-block';
        document.getElementById('id_additional_surpressant_0').required = false;
        document.getElementById('id_comments_0').required = false;
    }
    
    
    
    
    const q_crust_1 = document.getElementById('id_surpressant_crust_1').value;
    if (q_crust_1 == 'Yes') {
        document.getElementById('id_additional_surpressant_1').style.display = 'none';
        document.getElementById('id_comments_1').style.display = 'none';
        document.getElementById('id_additional_surpressant_1').required = false;
        document.getElementById('id_comments_1').required = false;
    }
    else if (q_crust_1 == 'No') {
        document.getElementById('id_additional_surpressant_1').style.display = 'inline-block';
        document.getElementById('id_comments_1').style.display = 'inline-block';
        document.getElementById('id_additional_surpressant_1').required = true;
        document.getElementById('id_comments_1').required = true;
    }
    else {
        document.getElementById('id_additional_surpressant_1').style.display = 'inline-block';
        document.getElementById('id_comments_1').style.display = 'inline-block';
        document.getElementById('id_additional_surpressant_1').required = false;
        document.getElementById('id_comments_1').required = false;
    }
    
    
    
    
    
    
    const q_crust_2 = document.getElementById('id_surpressant_crust_2').value;
    if (q_crust_2 == 'Yes') {
        document.getElementById('id_additional_surpressant_2').style.display = 'none';
        document.getElementById('id_comments_2').style.display = 'none';
        document.getElementById('id_additional_surpressant_2').required = false;
        document.getElementById('id_comments_2').required = false;
    }
    else if (q_crust_2 == 'No') {
        document.getElementById('id_additional_surpressant_2').style.display = 'inline-block';
        document.getElementById('id_comments_2').style.display = 'inline-block';
        document.getElementById('id_additional_surpressant_2').required = true;
        document.getElementById('id_comments_2').required = true;
    }
    else {
        document.getElementById('id_additional_surpressant_2').style.display = 'inline-block';
        document.getElementById('id_comments_2').style.display = 'inline-block';
        document.getElementById('id_additional_surpressant_2').required = false;
        document.getElementById('id_comments_2').required = false;
    }
    
    
    
    
    
    
    const q_crust_3 = document.getElementById('id_surpressant_crust_3').value;
    if (q_crust_3 == 'Yes') {
        document.getElementById('id_additional_surpressant_3').style.display = 'none';
        document.getElementById('id_comments_3').style.display = 'none';
        document.getElementById('id_additional_surpressant_3').required = false;
        document.getElementById('id_comments_3').required = false;
    }
    else if (q_crust_3 == 'No') {
        document.getElementById('id_additional_surpressant_3').style.display = 'inline-block';
        document.getElementById('id_comments_3').style.display = 'inline-block';
        document.getElementById('id_additional_surpressant_3').required = true;
        document.getElementById('id_comments_3').required = true;
    }
    else {
        document.getElementById('id_additional_surpressant_3').style.display = 'inline-block';
        document.getElementById('id_comments_3').style.display = 'inline-block';
        document.getElementById('id_additional_surpressant_3').required = false;
        document.getElementById('id_comments_3').required = false;
    }
    
    
    
    
    
    
    const q_crust_4 = document.getElementById('id_surpressant_crust_4').value;
    if (q_crust_4 == 'Yes') {
        document.getElementById('id_additional_surpressant_4').style.display = 'none';
        document.getElementById('id_comments_4').style.display = 'none';
        document.getElementById('id_additional_surpressant_4').required = false;
        document.getElementById('id_comments_4').required = false;
    }
    else if (q_crust_4 == 'No') {
        document.getElementById('id_additional_surpressant_4').style.display = 'inline-block';
        document.getElementById('id_comments_4').style.display = 'inline-block';
        document.getElementById('id_additional_surpressant_4').required = true;
        document.getElementById('id_comments_4').required = true;
    }
    else {
        document.getElementById('id_additional_surpressant_4').style.display = 'inline-block';
        document.getElementById('id_comments_4').style.display = 'inline-block';
        document.getElementById('id_additional_surpressant_4').required = false;
        document.getElementById('id_comments_4').required = false;
    }
    
}


function hidden_vessel() {
    const q_vessel_0 = document.getElementById('id_coal_vessel_0').value;
    
    if (q_vessel_0 == "No") {
        document.getElementById('id_water_sprays_0').value = 'N/A';
        document.getElementById('id_loader_lowered_0').value = 'N/A';
        document.getElementById('id_working_water_sprays_0').value = 'N/A';
    }
    else {
        document.getElementById('id_water_sprays_0').value = '';
        document.getElementById('id_loader_lowered_0').value = '';
        document.getElementById('id_working_water_sprays_0').value = '';
    }
    
    
    
    
    const q_vessel_1 = document.getElementById('id_coal_vessel_1').value;
    
    if (q_vessel_1 == "No") {
        document.getElementById('id_water_sprays_1').value = 'N/A';
        document.getElementById('id_loader_lowered_1').value = 'N/A';
        document.getElementById('id_working_water_sprays_1').value = 'N/A';
    }
    else {
        document.getElementById('id_water_sprays_1').value = '';
        document.getElementById('id_loader_lowered_1').value = '';
        document.getElementById('id_working_water_sprays_1').value = '';
    }
    
    
    
    
    const q_vessel_2 = document.getElementById('id_coal_vessel_2').value;
    
    if (q_vessel_2 == "No") {
        document.getElementById('id_water_sprays_2').value = 'N/A';
        document.getElementById('id_loader_lowered_2').value = 'N/A';
        document.getElementById('id_working_water_sprays_2').value = 'N/A';
    }
    else {
        document.getElementById('id_water_sprays_2').value = '';
        document.getElementById('id_loader_lowered_2').value = '';
        document.getElementById('id_working_water_sprays_2').value = '';
    }
    
    
    
    const q_vessel_3 = document.getElementById('id_coal_vessel_3').value;
    
    if (q_vessel_3 == "No") {
        document.getElementById('id_water_sprays_3').value = 'N/A';
        document.getElementById('id_loader_lowered_3').value = 'N/A';
        document.getElementById('id_working_water_sprays_3').value = 'N/A';
    }
    else {
        document.getElementById('id_water_sprays_3').value = '';
        document.getElementById('id_loader_lowered_3').value = '';
        document.getElementById('id_working_water_sprays_3').value = '';
    }
    
    
    
    const q_vessel_4 = document.getElementById('id_coal_vessel_4').value;
    
    if (q_vessel_4 == "No") {
        document.getElementById('id_water_sprays_4').value = 'N/A';
        document.getElementById('id_loader_lowered_4').value = 'N/A';
        document.getElementById('id_working_water_sprays_4').value = 'N/A';
    }
    else {
        document.getElementById('id_water_sprays_4').value = '';
        document.getElementById('id_loader_lowered_4').value = '';
        document.getElementById('id_working_water_sprays_4').value = '';
    }
    
}

function hidden_spills() {
    const q_spills_0 = document.getElementById('id_spills_0').value;
    
    if (q_spills_0 == "No") {
        document.getElementById('id_pushed_back_0').value = 'N/A';
    }
    else {
        document.getElementById('id_pushed_back_0').value = '';
    }
    
    
    
    const q_spills_1 = document.getElementById('id_spills_1').value;
    
    if (q_spills_1 == "No") {
        document.getElementById('id_pushed_back_1').value = 'N/A';
    }
    else {
        document.getElementById('id_pushed_back_1').value = '';
    }
    
    
    
    const q_spills_2 = document.getElementById('id_spills_2').value;
    
    if (q_spills_2 == "No") {
        document.getElementById('id_pushed_back_2').value = 'N/A';
    }
    else {
        document.getElementById('id_pushed_back_2').value = '';
    }
    
    
    
    const q_spills_3 = document.getElementById('id_spills_3').value;
    
    if (q_spills_3 == "No") {
        document.getElementById('id_pushed_back_3').value = 'N/A';
    }
    else {
        document.getElementById('id_pushed_back_3').value = '';
    }
    
    
    
    const q_spills_4 = document.getElementById('id_spills_4').value;
    
    if (q_spills_4 == "No") {
        document.getElementById('id_pushed_back_4').value = 'N/A';
    }
    else {
        document.getElementById('id_pushed_back_4').value = '';
    }
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
        })
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