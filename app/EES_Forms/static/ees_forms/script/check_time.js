function check_time(startId, endId, timePopup) {
    try {
        const start = document.getElementById(startId).value,
            end = document.getElementById(endId).value;

        if (end == false) {
            var popup = document.getElementById(timePopup).style.visibility = 'hidden';
        }
        else if (start >= end) {
            document.getElementById(timePopup).style.visibility = 'visible';
            document.getElementById(startId).style.backgroundColor = "white";
            document.getElementById(endId).style.backgroundColor = "white";
            document.getElementById(timePopup).style.display = 'block';
        }
        else{
            var popup = document.getElementById(timePopup).style.visibility = 'hidden';
            document.getElementById(startId).style.backgroundColor = "#3c983c85";
            document.getElementById(endId).style.backgroundColor = "#3c983c85";
            document.getElementById(timePopup).style.display = 'none';
        }
        console.log("Times Inputed")
    } catch(err) {
        console.log("Times Not Inputed")
    }
}


/*************
 FORM A-3 - OFFTAKES AND LIDS
*************/
function offtake_time() {
    check_time('id_om_start', 'id_om_stop', 'om_timePopup');
}
function lid_time() {
    check_time('id_l_start', 'id_l_stop', 'l_timePopup');
}
lid_time();
offtake_time();

/*************
 FORM A-2 - DOORS
*************/
function timecheck_pushDoors() {
    check_time('p_start', 'p_stop', 'p_timePopup');
}
function timecheck_cokeDoors() {
    check_time('c_start', 'c_stop', 'c_timePopup');
}
timecheck_pushDoors();
timecheck_cokeDoors();

/*************
 FORM A-1 - CHARGES
*************/
function timecheck_c1() {
    check_time('c1_start', 'c1_stop', 'c1_timePopup')
}
function timecheck_c2() {
    check_time('c2_start', 'c2_stop', 'c2_timePopup')
}
function timecheck_c3() {
    check_time('c3_start', 'c3_stop', 'c3_timePopup')
}
function timecheck_c4() {
    check_time('c4_start', 'c4_stop', 'c4_timePopup')
}
function timecheck_c5() {
    check_time('c5_start', 'c5_stop', 'c5_timePopup')
}

/*************
 FORM C - COAL FIELD
*************/
function formC_timeCheck_area1(){
    check_time('areaStartTime1', 'areaStopTime1', 'area1_timePopup')
}
function formC_timeCheck_area2(){
    check_time('areaStartTime2', 'areaStopTime2', 'area2_timePopup')
}
function formC_timeCheck_area3(){
    check_time('areaStartTime3', 'areaStopTime3', 'area3_timePopup')
}
function formC_timeCheck_area4(){
    check_time('areaStartTime4', 'areaStopTime4', 'area4_timePopup')
}


/*************
 FORM M - ROADS & AREAS
*************/
function timecheck_pav(){
    check_time('id_pav_start', 'id_pav_stop', 'pav_timePopup')
}
function timecheck_unpav(){
    check_time('id_unp_start', 'id_unp_stop', 'unp_timePopup')
}
function timecheck_par(){
    check_time('id_par_start', 'id_par_stop', 'par_timePopup')
}

/*************
 FORM A-5 - Push Travels
*************/
function timecheck_pt1(){
    check_time('o1_start', 'o1_stop', 'myPopup1')
}
function timecheck_pt2(){
    check_time('o2_start', 'o2_stop', 'myPopup2')
}
function timecheck_pt3(){
    check_time('o3_start', 'o3_stop', 'myPopup3')
}
function timecheck_pt4(){
    check_time('o4_start', 'o4_stop', 'myPopup4')
}

/*************
 FORM H - Combustion Stack
*************/
function timecheck_combustion(){
    check_time('comb_start', 'comb_stop', 'combPopup1')
}