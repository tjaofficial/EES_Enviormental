function get_average(opac_id, total_id, amount) {
    if (parseInt(amount) == 12) {
        list = [1,2,3,4,5,6,7,8,9,10,11,12]
    } else if (parseInt(amount) == 24) {
        list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
    }
    
    var the_total = 0;
    for (let i=0; i < list.length; i++){
        const opacities = list[i];
        const the_opac  = document.getElementById(opac_id + opacities).value;
        the_total += parseInt(the_opac);
    }
    if (parseInt(amount) == 12) {
        const theAverage = (the_total / 12).toFixed(3);
        document.getElementById(total_id).placeholder = theAverage;
        const id_param = document.getElementById(total_id).id;
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
function truck_average(){
    const TRead1 = document.getElementById('TRead1').value;
    if (TRead1 == 'fil'){
        for (i=1;i<13;i+=1){
            document.getElementById('TRead'+i).value = 0;
        }
    } 
    get_average('TRead', 'average_t', 12);
}
function area_average(){
    const ARead = document.getElementById('ARead1').value;
    if (ARead == 'fil'){
        for (i=1;i<13;i+=1){
            document.getElementById('ARead'+i).value = 0;
        }
    } 
    get_average('ARead', 'average_p', 12);
}
function storage_average(){
    const Storage = document.getElementById('storage_1').value;
    if (Storage == 'fil'){
        for (i=1;i<13;i+=1){
            document.getElementById('storage_'+i).value = 0;
        }
    } 
    get_average('storage_', 'average_storage', 12);
}
function salt_average(){
    const Salt = document.getElementById('salt_1').value;
    if (Salt == 'fil'){
        for (i=1;i<13;i+=1){
            document.getElementById('salt_'+i).value = 0;
        }
    } 
    get_average('salt_', 'average_salt', 12);
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
comb_averages()