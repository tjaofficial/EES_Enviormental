const type2 = document.getElementById('tableChoice').value;
console.log(type2);
if (type2 == 'meth9'){
    document.getElementById('formG1method9').style.display = 'inline-block';
    document.getElementById('formG1Non').style.display = 'none';
    document.getElementById('method9').style.backgroundColor = 'gray';
    document.getElementById('nonCert').style.backgroundColor = 'white';
} else if (type2 == 'non') {
    document.getElementById('formG1Non').style.display = 'inline-block';
    document.getElementById('formG1method9').style.display = 'none';
    document.getElementById('method9').style.backgroundColor = 'white';
    document.getElementById('nonCert').style.backgroundColor = 'gray';
} else {
    const type = document.getElementById('id_PEC_type').value;
    if (type == 'meth9'){
        method9();
    } else if (type == 'non') {
        nonCert();
    }


    document.getElementById("method9").onclick = function() {method9(), meth9_input()};
    function method9() {
        document.getElementById('formG1method9').style.display = 'inline-block';
        document.getElementById('formG1Non').style.display = 'none';
        document.getElementById('method9').style.backgroundColor = 'gray';
        document.getElementById('nonCert').style.backgroundColor = 'white';
        
        document.getElementById('id_PEC_start').required = true;
        document.getElementById('id_PEC_stop').required = true;
        document.getElementById('id_PEC_average').required = true;
        list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24];
        list.forEach((item) => {
            document.getElementById('id_PEC_read_' + item).required = true;
        });
        document.getElementById('id_PEC_push_oven').required = false;
        document.getElementById('id_PEC_push_time').required = false;
        document.getElementById('id_PEC_observe_time').required = false;
        document.getElementById('id_PEC_emissions_present').required = false;  
    }
    function meth9_input(){
        document.getElementById('id_PEC_type').value = 'meth9';
    }

    document.getElementById("nonCert").onclick = function() {nonCert(), nonCert_input()};
    function nonCert() {
        document.getElementById('formG1Non').style.display = 'inline-block';
        document.getElementById('formG1method9').style.display = 'none';
        document.getElementById('method9').style.backgroundColor = 'white';
        document.getElementById('nonCert').style.backgroundColor = 'gray';

        

        document.getElementById('id_PEC_start').required = false;
        document.getElementById('id_PEC_stop').required = false;
        document.getElementById('id_PEC_average').required = false;
        list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24];
        list.forEach((item) => {
            document.getElementById('id_PEC_read_' + item).required = false;
        });
        console.log(document.getElementById('id_PEC_read_1').required);
        document.getElementById('id_PEC_push_oven').required = true;
        document.getElementById('id_PEC_push_time').required = true;
        document.getElementById('id_PEC_observe_time').required = true;
    }
    function nonCert_input(){
        document.getElementById('id_PEC_type').value = 'non';
    }
}