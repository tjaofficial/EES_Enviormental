// Sums the times on input
 
function sumTime(){
    const c1_sec_value  = document.getElementById('c1_sec').value;
    const c2_sec_value  = document.getElementById('c2_sec').value;
    const c3_sec_value  = document.getElementById('c3_sec').value;
    const c4_sec_value  = document.getElementById('c4_sec').value;
    const c5_sec_value  = document.getElementById('c5_sec').value;

    let summedTime =  parseFloat(c1_sec_value) + parseFloat(c2_sec_value) + parseFloat(c3_sec_value) + parseFloat(c4_sec_value) + parseFloat(c5_sec_value);

    document.getElementById('total_seconds').value = summedTime;
}
function equal_start_stop() {
    let start = document.getElementById('main_start').value;
    
    document.getElementById('c1_start').value = start;
    
    let stop = document.getElementById('c5_stop').value;
    
    document.getElementById('main_stop').value = stop;
}
function c2_check() {
    const oven1 = parseInt(document.getElementById('c1_no').value),
          oven2 = parseInt(document.getElementById('c2_no').value);
    
    if (oven2 == parseInt(oven1) + 2) {
        document.getElementById("c2_popup_oven").style.visibility = 'hidden';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }  
    else if (oven1 >= oven2) {
        document.getElementById("c2_popup_oven").style.visibility = 'visible';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }
    else if (oven2 == parseInt(oven1) + 1) {
        document.getElementById("c2_popup_oven").style.visibility = 'visible';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }
    else if (oven2 > parseInt(oven1) + 2) {
        document.getElementById("c2_popup_oven").style.visibility = 'hidden';
        document.getElementById("comment_skip_id").style.visibility = 'visible';
        document.getElementById("comment_skip_id").innerHTML = ' Please change Oven No. for SECOND oven or click here to comment below what oven(s) were skipped.';
    } 
    
    document.getElementById("comment_skip_id").onclick = function() {
        comment_skipped()
    };
    function comment_skipped() {
        for (let x = parseInt(oven1)+2; x < parseInt(oven2); x+=2) {
            document.getElementById("comments").value += ' Oven #' + x + ' was skipped.'
        }
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }  
}
function c3_check() {
    const oven1 = parseInt(document.getElementById('c2_no').value),
          oven2 = parseInt(document.getElementById('c3_no').value);
    
    if (oven2 == parseInt(oven1) + 2) {
        document.getElementById("c3_popup_oven").style.visibility = 'hidden';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }  
    else if (oven1 >= oven2) {
        document.getElementById("c3_popup_oven").style.visibility = 'visible';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }
    else if (oven2 == parseInt(oven1) + 1) {
        document.getElementById("c3_popup_oven").style.visibility = 'visible';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }
    else if (oven2 > parseInt(oven1) + 2) {
        document.getElementById("c3_popup_oven").style.visibility = 'hidden';
        document.getElementById("comment_skip_id").style.visibility = 'visible';
        document.getElementById("comment_skip_id").innerHTML = ' Please change Oven No. for SECOND oven or click here to comment below what oven(s) were skipped.';
    } 
    
    document.getElementById("comment_skip_id").onclick = function() {
        comment_skipped()
    };
    function comment_skipped() {
        for (let x = parseInt(oven1)+2; x < parseInt(oven2); x+=2) {
            document.getElementById("comments").innerHTML += ' Oven #' + x + ' was skipped.'
        }
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }  
}
function c4_check() {
    const oven1 = parseInt(document.getElementById('c3_no').value),
          oven2 = parseInt(document.getElementById('c4_no').value);
    
    if (oven2 == parseInt(oven1) + 2) {
        document.getElementById("c4_popup_oven").style.visibility = 'hidden';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }  
    else if (oven1 >= oven2) {
        document.getElementById("c4_popup_oven").style.visibility = 'visible';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }
    else if (oven2 == parseInt(oven1) + 1) {
        document.getElementById("c4_popup_oven").style.visibility = 'visible';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }
    else if (oven2 > parseInt(oven1) + 2) {
        document.getElementById("c4_popup_oven").style.visibility = 'hidden';
        document.getElementById("comment_skip_id").style.visibility = 'visible';
        document.getElementById("comment_skip_id").innerHTML = ' Please change Oven No. for SECOND oven or click here to comment below what oven(s) were skipped.';
    } 
    document.getElementById("comment_skip_id").onclick = function() {
        comment_skipped()
    };
    function comment_skipped() {
        for (let x = parseInt(oven1)+2; x < parseInt(oven2); x+=2) {
            document.getElementById("comments").innerHTML += ' Oven #' + x + ' was skipped.'
        }
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }  
}
function c5_check() {
    const oven1 = parseInt(document.getElementById('c4_no').value),
          oven2 = parseInt(document.getElementById('c5_no').value);
    
    if (oven2 == parseInt(oven1) + 2) {
        document.getElementById("c5_popup_oven").style.visibility = 'hidden';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }  
    else if (oven1 >= oven2) {
        document.getElementById("c5_popup_oven").style.visibility = 'visible';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }
    else if (oven2 == parseInt(oven1) + 1) {
        document.getElementById("c5_popup_oven").style.visibility = 'visible';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }
    else if (oven2 > parseInt(oven1) + 2) {
        document.getElementById("c5_popup_oven").style.visibility = 'hidden';
        document.getElementById("comment_skip_id").style.visibility = 'visible';
        document.getElementById("comment_skip_id").innerHTML = ' Please change Oven No. for SECOND oven or click here to comment below what oven(s) were skipped.';
    } 
    document.getElementById("comment_skip_id").onclick = function() {
        comment_skipped()
    };
    function comment_skipped() {
        for (let x = parseInt(oven1)+2; x < parseInt(oven2); x+=2) {
            document.getElementById("comments").innerHTML += ' Oven #' + x + ' was skipped.'
        }
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }  
}
function timecheck_c1() {
    "use strict";
    
    const start = document.getElementById('c1_start').value,
          end = document.getElementById('c1_stop').value;

    if (end == false) {
        var popup = document.getElementById("c1_popup").style.visibility = 'hidden';
    }
    else if (start >= end) {
        document.getElementById("c1_popup").style.visibility = 'visible';
    }
    else{
        var popup = document.getElementById("c1_popup").style.visibility = 'hidden';
        document.getElementById("c1_start").style.backgroundColor = "#3c983c85";
        document.getElementById("c1_stop").style.backgroundColor = "#3c983c85";
    }
}
function timecheck_c2() {
    "use strict";
    const start = document.getElementById('c2_start').value,
          end = document.getElementById('c2_stop').value;

    if (end == false) {
        var popup = document.getElementById("c2_popup").style.visibility = 'hidden';
    }
    else if (start >= end) {
        document.getElementById("c2_popup").style.visibility = 'visible';
    }
    else{
        var popup = document.getElementById("c2_popup").style.visibility = 'hidden';
        document.getElementById("c2_start").style.backgroundColor = "#3c983c85";
        document.getElementById("c2_stop").style.backgroundColor = "#3c983c85";
    }
}
function timecheck_c3() {
    "use strict";
    const start = document.getElementById('c3_start').value,
          end = document.getElementById('c3_stop').value;

    if (end == false) {
        var popup = document.getElementById("c3_popup").style.visibility = 'hidden';
    }
    else if (start >= end) {
        document.getElementById("c3_popup").style.visibility = 'visible';
    }
    else{
        var popup = document.getElementById("c3_popup").style.visibility = 'hidden';
        document.getElementById("c3_start").style.backgroundColor = "#3c983c85";
        document.getElementById("c3_stop").style.backgroundColor = "#3c983c85";
    }
}
function timecheck_c4() {
    "use strict";
    const start = document.getElementById('c4_start').value,
          end = document.getElementById('c4_stop').value;

    if (end == false) {
        var popup = document.getElementById("c4_popup").style.visibility = 'hidden';
    }
    else if (start >= end) {
        document.getElementById("c4_popup").style.visibility = 'visible';
    }
    else{
        var popup = document.getElementById("c4_popup").style.visibility = 'hidden';
        document.getElementById("c4_start").style.backgroundColor = "#3c983c85";
        document.getElementById("c4_stop").style.backgroundColor = "#3c983c85";
    }
}
function timecheck_c5() {
    "use strict";
    const start = document.getElementById('c5_start').value,
          end = document.getElementById('c5_stop').value;

    if (end == false) {
        var popup = document.getElementById("c5_popup").style.visibility = 'hidden';
    }
    else if (start >= end) {
        document.getElementById("c5_popup").style.visibility = 'visible';
    }
    else{
        var popup = document.getElementById("c5_popup").style.visibility = 'hidden';
        document.getElementById("c5_start").style.backgroundColor = "#3c983c85";
        document.getElementById("c5_stop").style.backgroundColor = "#3c983c85";
    }
}