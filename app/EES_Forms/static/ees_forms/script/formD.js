function freeboard_check(truck) {
    const freeboard = document.getElementById('id_freeboard' + truck).value;
    if (freeboard == 'Yes') {
        document.getElementById('id_wetted' + truck).value = 'N/A';
    } else if (freeboard == '') {
        document.getElementById('id_wetted' + truck).value = '';
    }
}
function freeboard_1() {
    freeboard_check(1);
}
function freeboard_2() {
    freeboard_check(2);
}
function freeboard_3() {
    freeboard_check(3);
}
function freeboard_4() {
    freeboard_check(4);
}
function freeboard_5() {
    freeboard_check(5);
}
