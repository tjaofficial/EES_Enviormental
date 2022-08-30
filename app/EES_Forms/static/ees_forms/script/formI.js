function individual_day() {
    const today = new Date();
    let name_0 = false;
    let name_1 = false;
    let name_2 = false;
    let name_3 = false;
    let name_4 = false;
    if (today.getDay() == 1){
        name_0 = true;
        name_1 = false;
        name_2 = false;
        name_3 = false;
        name_4 = false;
    } else if (today.getDay() == 2){
        name_0 = true;
        name_1 = true;
        name_2 = false;
        name_3 = false;
        name_4 = false;
    } else if (today.getDay() == 3){
        name_0 = true;
        name_1 = true;
        name_2 = true;
        name_3 = false;
        name_4 = false;
    } else if (today.getDay() == 4){
        name_0 = true;
        name_1 = true;
        name_2 = true;
        name_3 = true;
        name_4 = false;
    } else if (today.getDay() == 5){
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
    document.getElementById('id_obser_0').required = name_0;
    document.getElementById('id_obser_1').required = name_1;
    document.getElementById('id_obser_2').required = name_2;
    document.getElementById('id_obser_3').required = name_3;
    document.getElementById('id_obser_4').required = name_4;
}

individual_day();