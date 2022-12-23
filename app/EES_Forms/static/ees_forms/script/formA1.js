// Sums the times on input
 
function sumTime(){
    const totalTime = document.getElementById('total_seconds').value;
    const c1_sec_value  = document.getElementById('c1_sec').value;
    const c2_sec_value  = document.getElementById('c2_sec').value;
    const c3_sec_value  = document.getElementById('c3_sec').value;
    const c4_sec_value  = document.getElementById('c4_sec').value;
    const c5_sec_value  = document.getElementById('c5_sec').value;

    let summedTime =  parseFloat(c1_sec_value) + parseFloat(c2_sec_value) + parseFloat(c3_sec_value) + parseFloat(c4_sec_value) + parseFloat(c5_sec_value);

    if (totalTime) {
        if (parseFloat(summedTime) == parseFloat(totalTime)) {
            document.getElementById("total_seconds").style.backgroundColor = "#3c983c85";
        } else {
            document.getElementById("total_seconds").style.backgroundColor = "#F49B9B";
        }
    } else {
        document.getElementById('total_seconds').placeholder = summedTime;
        document.getElementById("total_seconds").style.backgroundColor = "#FFFA8B";
    }
}
/*function equal_start_stop() {
    let start = document.getElementById('main_start').value;
    
    document.getElementById('c1_start').value = start;
    
    let stop = document.getElementById('c5_stop').value;
    
    document.getElementById('main_stop').value = stop;
}*/

function oven_check(ovenId1, ovenId2) {
    const oven1 = parseInt(document.getElementById(ovenId1).value),
          oven2 = parseInt(document.getElementById(ovenId2).value),
          number = ovenId2.slice(1,2);
    if (oven1 == 84 && oven2 == 1 || oven1 == 85 && oven2 == 2) {
        document.getElementById("c" + number + "_popup_oven").style.visibility = 'hidden';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    } else if (oven2 == parseInt(oven1) + 2) {
        document.getElementById("c" + number + "_popup_oven").style.visibility = 'hidden';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }  
    else if (oven1 >= oven2) {
        document.getElementById("c" + number + "_popup_oven").style.visibility = 'visible';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }
    else if (oven2 == parseInt(oven1) + 1) {
        document.getElementById("c" + number + "_popup_oven").style.visibility = 'visible';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }
    else if (oven2 > parseInt(oven1) + 2) {
        document.getElementById("c" + number + "_popup_oven").style.visibility = 'hidden';
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