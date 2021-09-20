function sumTime1() {
    const pav_1_value  = document.getElementById('id_pav_1').value,
          pav_2_value  = document.getElementById('id_pav_2').value,
          pav_3_value  = document.getElementById('id_pav_3').value,
          pav_4_value  = document.getElementById('id_pav_4').value,
          pav_5_value  = document.getElementById('id_pav_5').value,
          pav_6_value  = document.getElementById('id_pav_6').value,
          pav_7_value  = document.getElementById('id_pav_7').value,
          pav_8_value  = document.getElementById('id_pav_8').value,
          pav_9_value  = document.getElementById('id_pav_9').value,
          pav_10_value  = document.getElementById('id_pav_10').value,
          pav_11_value  = document.getElementById('id_pav_11').value,
          pav_12_value  = document.getElementById('id_pav_12').value;
    
    let avgReadingPAV =  (parseFloat(pav_1_value) + parseFloat(pav_2_value) + parseFloat(pav_3_value) + parseFloat(pav_4_value) + parseFloat(pav_5_value) + parseFloat(pav_6_value) + parseFloat(pav_7_value) + parseFloat(pav_8_value) + parseFloat(pav_9_value) + parseFloat(pav_10_value) + parseFloat(pav_11_value) + parseFloat(pav_12_value)) / 12;
    
    document.getElementById('id_pav_total').value = avgReadingPAV;
}
    
function sumTime2() {    
    const unp_1_value  = document.getElementById('id_unp_1').value,
          unp_2_value  = document.getElementById('id_unp_2').value,
          unp_3_value  = document.getElementById('id_unp_3').value,
          unp_4_value  = document.getElementById('id_unp_4').value,
          unp_5_value  = document.getElementById('id_unp_5').value,
          unp_6_value  = document.getElementById('id_unp_6').value,
          unp_7_value  = document.getElementById('id_unp_7').value,
          unp_8_value  = document.getElementById('id_unp_8').value,
          unp_9_value  = document.getElementById('id_unp_9').value,
          unp_10_value  = document.getElementById('id_unp_10').value,
          unp_11_value  = document.getElementById('id_unp_11').value,
          unp_12_value  = document.getElementById('id_unp_12').value;
    
    let avgReadingUNP =  (parseFloat(unp_1_value) + parseFloat(unp_2_value) + parseFloat(unp_3_value) + parseFloat(unp_4_value) + parseFloat(unp_5_value) + parseFloat(unp_6_value) + parseFloat(unp_7_value) + parseFloat(unp_8_value) + parseFloat(unp_9_value) + parseFloat(unp_10_value) + parseFloat(unp_11_value) + parseFloat(unp_12_value)) / 12;
    
    document.getElementById('id_unp_total').value = avgReadingUNP;
}

function sumTime3() {  
    const par_1_value  = document.getElementById('id_par_1').value,
          par_2_value  = document.getElementById('id_par_2').value,
          par_3_value  = document.getElementById('id_par_3').value,
          par_4_value  = document.getElementById('id_par_4').value,
          par_5_value  = document.getElementById('id_par_5').value,
          par_6_value  = document.getElementById('id_par_6').value,
          par_7_value  = document.getElementById('id_par_7').value,
          par_8_value  = document.getElementById('id_par_8').value,
          par_9_value  = document.getElementById('id_par_9').value,
          par_10_value  = document.getElementById('id_par_10').value,
          par_11_value  = document.getElementById('id_par_11').value,
          par_12_value  = document.getElementById('id_par_12').value;
    
    let avgReadingPAR =  (parseFloat(par_1_value) + parseFloat(par_2_value) + parseFloat(par_3_value) + parseFloat(par_4_value) + parseFloat(par_5_value) + parseFloat(par_6_value) + parseFloat(par_7_value) + parseFloat(par_8_value) + parseFloat(par_9_value) + parseFloat(par_10_value) + parseFloat(par_11_value) + parseFloat(par_12_value)) / 12;
    
    document.getElementById('id_par_total').value = avgReadingPAR;
}

function sumTime4() {
    const storage_1_value  = document.getElementById('id_storage_1').value,
          storage_2_value  = document.getElementById('id_storage_2').value,
          storage_3_value  = document.getElementById('id_storage_3').value,
          storage_4_value  = document.getElementById('id_storage_4').value,
          storage_5_value  = document.getElementById('id_storage_5').value,
          storage_6_value  = document.getElementById('id_storage_6').value,
          storage_7_value  = document.getElementById('id_storage_7').value,
          storage_8_value  = document.getElementById('id_storage_8').value,
          storage_9_value  = document.getElementById('id_storage_9').value,
          storage_10_value  = document.getElementById('id_storage_10').value,
          storage_11_value  = document.getElementById('id_storage_11').value,
          storage_12_value  = document.getElementById('id_storage_12').value;

    let avgReadingSTORAGE =  (parseFloat(storage_1_value) + parseFloat(storage_2_value) + parseFloat(storage_3_value) + parseFloat(storage_4_value) + parseFloat(storage_5_value) + parseFloat(storage_6_value) + parseFloat(storage_7_value) + parseFloat(storage_8_value) + parseFloat(storage_9_value) + parseFloat(storage_10_value) + parseFloat(storage_11_value) + parseFloat(storage_12_value)) / 12;

    document.getElementById('id_storage_total').value = avgReadingSTORAGE;
}

function timecheck_1() {
    "use strict";
    const start1 = document.getElementById('id_pav_start').value,
          end1 = document.getElementById('id_pav_stop').value;

    if (end1 == false) {
        
    }
    else if (start1 >= end1) {
        var popup = document.getElementById("pav_popup").style.visibility = 'visible';
        document.getElementById("id_pav_start").style.backgroundColor = "#ffffff";
        document.getElementById("id_pav_stop").style.backgroundColor = "#ffffff";
    }
    else{
        var popup = document.getElementById("pav_popup").style.visibility = 'hidden';
        document.getElementById("id_pav_start").style.backgroundColor = "#3c983c85";
        document.getElementById("id_pav_stop").style.backgroundColor = "#3c983c85";
    }
}

function timecheck_2() {
    "use strict";
    const start1 = document.getElementById('id_unp_start').value,
          end1 = document.getElementById('id_unp_stop').value;

    if (end1 == false) {
        
    }
    else if (start1 >= end1) {
        var popup = document.getElementById("unp_popup").style.visibility = 'visible';
        document.getElementById("id_unp_start").style.backgroundColor = "#ffffff";
        document.getElementById("id_unp_stop").style.backgroundColor = "#ffffff";
    }
    else{
        var popup = document.getElementById("unp_popup").style.visibility = 'hidden';
        document.getElementById("id_unp_start").style.backgroundColor = "#3c983c85";
        document.getElementById("id_unp_stop").style.backgroundColor = "#3c983c85";
    }
}

function timecheck_3() {
    "use strict";
    const start1 = document.getElementById('id_par_start').value,
          end1 = document.getElementById('id_par_stop').value;

    if (end1 == false) {
        
    }
    else if (start1 >= end1) {
        var popup = document.getElementById("par_popup").style.visibility = 'visible';
        document.getElementById("id_par_start").style.backgroundColor = "#ffffff";
        document.getElementById("id_par_stop").style.backgroundColor = "#ffffff";
    }
    else{
        var popup = document.getElementById("par_popup").style.visibility = 'hidden';
        document.getElementById("id_par_start").style.backgroundColor = "#3c983c85";
        document.getElementById("id_par_stop").style.backgroundColor = "#3c983c85";
    }
}

function timecheck_4() {
    "use strict";
    const start1 = document.getElementById('id_sto_start').value,
          end1 = document.getElementById('id_sto_stop').value;

    if (end1 == false) {
        
    }
    else if (start1 >= end1) {
        var popup = document.getElementById("storage_popup").style.visibility = 'visible';
        document.getElementById("id_sto_start").style.backgroundColor = "#ffffff";
        document.getElementById("id_sto_stop").style.backgroundColor = "#ffffff";
    }
    else{
        var popup = document.getElementById("storage_popup").style.visibility = 'hidden';
        document.getElementById("id_sto_start").style.backgroundColor = "#3c983c85";
        document.getElementById("id_sto_stop").style.backgroundColor = "#3c983c85";
    }
}