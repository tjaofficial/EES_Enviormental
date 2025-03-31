const formNameCheckTime = document.getElementById('formName').dataset.form;

function check_time(startId, endId, timePopup) {
    console.log(`${startId} & ${endId}`)
    try {
        let inputStart = document.getElementById("id_" + startId),
            inputEnd = document.getElementById("id_" + endId);
        const start = inputStart.value,
            end = inputEnd.value;
        if (end == false) {
            var popup = document.getElementById(timePopup).style.visibility = 'hidden';
            return;
        } else if (start >= end) {
            // document.getElementById(timePopup).style.visibility = 'visible';
            // inputStart.style.backgroundColor = "white";
            // inputEnd.style.backgroundColor = "white";
            inputStart.style.border = "2px solid red";
            inputStart.style.boxShadow = "inset 0 0 4px 0px red";
            inputEnd.style.border = "2px solid red";
            inputEnd.style.boxShadow = "inset 0 0 4px 0px red";
            document.getElementById(timePopup).style.display = 'block';
            return false;
        } else {
            var popup = document.getElementById(timePopup).style.visibility = 'hidden';
            // inputStart.style.backgroundColor = "#3c983c85";
            // inputEnd.style.backgroundColor = "#3c983c85";
            inputStart.style.border = "2px solid rgba(60, 152, 60, 0.52)";
            inputStart.style.boxShadow = "inset 0 0 4px 0px rgba(60, 152, 60, 0.52)";
            inputEnd.style.border = "2px solid rgba(60, 152, 60, 0.52)";
            inputEnd.style.boxShadow = "inset 0 0 4px 0px rgba(60, 152, 60, 0.52)";
            document.getElementById(timePopup).style.display = 'none';
            return true;
        }
        console.log("Times Inputed")
    } catch(err) {
        console.log("Times Not Inputed")
        console.log(err)
    }
}


/*************
 FORM 3 - OFFTAKES AND LIDS
*************/
function offtake_time() {
    check_time('id_om_start', 'id_om_stop', 'om_timePopup');
}
function lid_time() {
    check_time('id_l_start', 'id_l_stop', 'l_timePopup');
}
if (String(formNameCheckTime) == "3"){
    lid_time();
    offtake_time();
}

/*************
 FORM 2 - DOORS
*************/
function timecheck_pushDoors() {
    check_time('p_start', 'p_stop', 'p_timePopup');
}
function timecheck_cokeDoors() {
    check_time('c_start', 'c_stop', 'c_timePopup');
}
if (String(formNameCheckTime) == "2"){
    timecheck_pushDoors();
    timecheck_cokeDoors();
}

/*************
 FORM 1 - CHARGES
*************/
function formDisable(timeCheckerFunc){
    if (timeCheckerFunc == false){
        document.getElementById('submit').disabled = true;
    } else {
        document.getElementById('submit').disabled = false;
    }
    
}

function timecheck_c1() {
    let checkit = check_time('c1_start', 'c1_stop', 'c1_timePopup');
    formDisable(checkit);
    console.log(checkit)
}
function timecheck_c2() {
    check_time('c2_start', 'c2_stop', 'c2_timePopup');
    formDisable(check_time('c2_start', 'c2_stop', 'c2_timePopup'))
}
function timecheck_c3() {
    let checkit = check_time('c3_start', 'c3_stop', 'c3_timePopup');
    formDisable(checkit)
}
function timecheck_c4() {
    check_time('c4_start', 'c4_stop', 'c4_timePopup');
    //formDisable(timeCheckerFunc)
}
function timecheck_c5() {
    check_time('c5_start', 'c5_stop', 'c5_timePopup');
    //formDisable(timeCheckerFunc)
}
if (String(formNameCheckTime) == "1"){
    timecheck_c1();
    timecheck_c2();
    timecheck_c3();
    timecheck_c4();
    timecheck_c5();
}




/*************
 FORM 7 - COAL FIELD
*************/
function formC_timeCheck_area1(){
    check_time('1_start', '1_stop', 'area1_timePopup')
}
function formC_timeCheck_area2(){
    check_time('2_start', '2_stop', 'area2_timePopup')
}
function formC_timeCheck_area3(){
    check_time('3_start', '3_stop', 'area3_timePopup')
}
function formC_timeCheck_area4(){
    check_time('4_start', '4_stop', 'area4_timePopup')
}
if (String(formNameCheckTime) == "7"){
    formC_timeCheck_area1();
    formC_timeCheck_area2();
    formC_timeCheck_area3();
    formC_timeCheck_area4();
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