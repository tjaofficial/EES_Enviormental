function individual_day() {
    const today = new Date();
    let name_0 = false;
    let name_1 = false;
    let name_2 = false;
    let name_3 = false;
    let name_4 = false;
    let name_5 = false;
    let name_6 = false;
    if (today.getDay() == 6){
        name_5 = true;
        name_6 = false;
        name_0 = false;
        name_1 = false;
        name_2 = false;
        name_3 = false;
        name_4 = false;
    } else if (today.getDay() == 0){
        name_5 = true;
        name_6 = true;
        name_0 = false;
        name_1 = false;
        name_2 = false;
        name_3 = false;
        name_4 = false;
    } else if (today.getDay() == 1){
        name_5 = true;
        name_6 = true;
        name_0 = true;
        name_1 = false;
        name_2 = false;
        name_3 = false;
        name_4 = false;
    } else if (today.getDay() == 2){
        name_5 = true;
        name_6 = true;
        name_0 = true;
        name_1 = true;
        name_2 = false;
        name_3 = false;
        name_4 = false;
    } else if (today.getDay() == 3){
        name_5 = true;
        name_6 = true;
        name_0 = true;
        name_1 = true;
        name_2 = true;
        name_3 = false;
        name_4 = false;
    } else if (today.getDay() == 4){
        name_5 = true;
        name_6 = true;
        name_0 = true;
        name_1 = true;
        name_2 = true;
        name_3 = true;
        name_4 = false;
    } else if (today.getDay() == 5){
        name_5 = true;
        name_6 = true;
        name_0 = true;
        name_1 = true;
        name_2 = true;
        name_3 = true;
        name_4 = true;
    }
    document.getElementById('id_time_0').required = name_0;
    document.getElementById('id_time_1').required = name_1;
    document.getElementById('id_time_2').required = name_2;
    document.getElementById('id_time_3').required = name_3;
    document.getElementById('id_time_4').required = name_4;
    document.getElementById('id_time_5').required = name_5;
    document.getElementById('id_time_6').required = name_6;
    document.getElementById('id_obser_0').required = name_0;
    document.getElementById('id_obser_1').required = name_1;
    document.getElementById('id_obser_2').required = name_2;
    document.getElementById('id_obser_3').required = name_3;
    document.getElementById('id_obser_4').required = name_4;
    document.getElementById('id_obser_5').required = name_5;
    document.getElementById('id_obser_6').required = name_6;
    document.getElementById('id_vents_0').required = name_0;
    document.getElementById('id_vents_1').required = name_1;
    document.getElementById('id_vents_2').required = name_2;
    document.getElementById('id_vents_3').required = name_3;
    document.getElementById('id_vents_4').required = name_4;
    document.getElementById('id_vents_5').required = name_5;
    document.getElementById('id_vents_6').required = name_6;
    document.getElementById('id_mixer_0').required = name_0;
    document.getElementById('id_mixer_1').required = name_1;
    document.getElementById('id_mixer_2').required = name_2;
    document.getElementById('id_mixer_3').required = name_3;
    document.getElementById('id_mixer_4').required = name_4;
    document.getElementById('id_mixer_5').required = name_5;
    document.getElementById('id_mixer_6').required = name_6;
    document.getElementById('id_v_comments_0').required = name_0;
    document.getElementById('id_v_comments_1').required = name_1;
    document.getElementById('id_v_comments_2').required = name_2;
    document.getElementById('id_v_comments_3').required = name_3;
    document.getElementById('id_v_comments_4').required = name_4;
    document.getElementById('id_v_comments_5').required = name_5;
    document.getElementById('id_v_comments_6').required = name_6;
    document.getElementById('id_m_comments_0').required = name_0;
    document.getElementById('id_m_comments_1').required = name_1;
    document.getElementById('id_m_comments_2').required = name_2;
    document.getElementById('id_m_comments_3').required = name_3;
    document.getElementById('id_m_comments_4').required = name_4;
    document.getElementById('id_m_comments_5').required = name_5;
    document.getElementById('id_m_comments_6').required = name_6;
}

individual_day();