function get_average(opac_id, total_id) {
    list = [1,2,3,4,5,6,7,8,9,10,11,12]
    var the_total = 0;
    for (let i=0; i < list.length; i++){
        const opacities = list[i];
        const the_opac  = document.getElementById(opac_id + opacities).value;
        the_total += parseInt(the_opac);
    }
    const theAverage = (the_total / 12).toFixed(3);
    document.getElementById(total_id).placeholder = theAverage;
    const id_param = document.getElementById(total_id).id;
    stop_light(theAverage, id_param);
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
    get_average('TRead', 'average_t');
}
function area_average(){
    get_average('ARead', 'average_p');
}
function storage_average(){
    get_average('storage_', 'average_storage');
}
function salt_average(){
    get_average('salt_', 'average_salt');
}


/*************
 FORM M - ROADS AND AREAS
*************/
function paved_average(){
    get_average('id_pav_', 'id_pav_total');
}
function unpaved_average(){
    get_average('id_unp_', 'id_unp_total');
}
function parking_average(){
    get_average('id_par_', 'id_par_total');
}