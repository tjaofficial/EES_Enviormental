function get_average(opac_id, total_id, amount) {
    if (parseInt(amount) == 12) {
        list = [1,2,3,4,5,6,7,8,9,10,11,12]
    } else if (parseInt(amount) == 11) {
        list = [0,1,2,3,4,5,6,7,8,9,10,11]
    } else if (parseInt(amount) == 24) {
        list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
    }
    
    var the_total = 0;
    for (let i=0; i < list.length; i++){
        const opacities = list[i];
        const the_opac  = document.getElementById("id_" + opac_id + (opacities+1)).value;
        the_total += parseInt(the_opac);
    }
    if (parseInt(amount) == 12 || parseInt(amount) == 11) {
        const theAverage = (the_total / 12).toFixed(3);
        document.getElementById("id_" + total_id).placeholder = theAverage;
        const id_param = document.getElementById("id_" + total_id).id;
        stop_light(theAverage, id_param);
    } else if (parseInt(amount) == 24) {
        const theAverage = (the_total / 24).toFixed(3);
        document.getElementById(total_id).placeholder = theAverage;
        const id_param = document.getElementById(total_id).id;
        stop_light(theAverage, id_param);
    }
}
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


/*************
 FORM C - COAL FIELD
*************/
function area1_average(){
    get_average('1Read_', '1_average', 11);
}
function area2_average(){
    get_average('2Read_', '2_average', 11);
}
function area3_average(){
    get_average('3Read_', '3_average', 11);
}
function area4_average(){
    get_average('4Read_', '4_average', 11);
}
if (formName == 7) {
    console.log("Test 2")
    console.log(document.getElementById('areaCont1').style.display)
    if (document.getElementById('areaCont1').style.display == 'block'){
        area1_average();
        console.log("Test 1")
    }
    if (document.getElementById('areaCont1').style.display == 'block'){
        area2_average();
    }
    if (document.getElementById('areaCont1').style.display == 'block'){
        area3_average();
    }
    if (document.getElementById('areaCont1').style.display == 'block'){
        area4_average();
    }
}

/*************
 FORM M - ROADS AND AREAS
*************/
function paved_average(){
    get_average('id_pav_', 'id_pav_total', 12);
}
function unpaved_average(){
    get_average('id_unp_', 'id_unp_total', 12);
}
function parking_average(){
    get_average('id_par_', 'id_par_total', 12);
}

/*************
 FORM H - Combustion Stack
*************/
function comb_averages() {
    get_average('id_comb_read_', 'id_comb_average', 24);
}
if (formName == 19) {
    comb_averages()
}