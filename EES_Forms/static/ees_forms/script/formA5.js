function timecheck_1() {
    "use strict";
    const start1 = document.getElementById('o1_start').value,
          end1 = document.getElementById('o1_stop').value;

    if (end1 == false) {
        
    }
    else if (start1 > end1) {
        var popup = document.getElementById("myPopup1").style.visibility = 'visible';
        document.getElementById("o1_start").style.backgroundColor = "#ffffff";
        document.getElementById("o1_stop").style.backgroundColor = "#ffffff";
    }
    else{
        var popup = document.getElementById("myPopup1").style.visibility = 'hidden';
        document.getElementById("o1_start").style.backgroundColor = "#3c983c85";
        document.getElementById("o1_stop").style.backgroundColor = "#3c983c85";
    }
}
function pt1_averages() {
    "use strict";
    const o1_1_reads_value  = document.getElementById('o1_1_reads').value,
          o1_2_reads_value  = document.getElementById('o1_2_reads').value,
          o1_3_reads_value  = document.getElementById('o1_3_reads').value,
          o1_4_reads_value  = document.getElementById('o1_4_reads').value,
          o1_5_reads_value  = document.getElementById('o1_5_reads').value,
          o1_6_reads_value  = document.getElementById('o1_6_reads').value,
          o1_7_reads_value  = document.getElementById('o1_7_reads').value,
          o1_8_reads_value  = document.getElementById('o1_8_reads').value,
          o1_9_reads_value  = document.getElementById('o1_9_reads').value,
          o1_10_reads_value  = document.getElementById('o1_10_reads').value,
          o1_11_reads_value  = document.getElementById('o1_11_reads').value,
          o1_12_reads_value  = document.getElementById('o1_12_reads').value,
          o1_13_reads_value  = document.getElementById('o1_13_reads').value,
          o1_14_reads_value  = document.getElementById('o1_14_reads').value,
          o1_15_reads_value  = document.getElementById('o1_15_reads').value,
          o1_16_reads_value  = document.getElementById('o1_16_reads').value;

    

    let A = [o1_1_reads_value, o1_2_reads_value, o1_3_reads_value, o1_4_reads_value, o1_5_reads_value, o1_6_reads_value, o1_7_reads_value, o1_8_reads_value, o1_9_reads_value, o1_10_reads_value, o1_11_reads_value, o1_12_reads_value, o1_13_reads_value, o1_14_reads_value, o1_15_reads_value, o1_16_reads_value];

    const B = []

    const highest_avg = []

    
    for (let x in A) {
        
      	let home = parseInt(A[x]);
        if(Number.isInteger(home)) {
            B.push(A[x])
        }
        else{
        
        }
    }
    var highest_read = B.reduce(function(a, b) {
        return Math.max(a, b);
    }, 0);
    
    if (B.length > 6) {
        const instances = [];
        for (let h = 0; h < (B.length + 1) - 6; h++) {
            let i = h;
            let r = h;
            const D = [];
            for (i; i < r + 6; i++) {
                D.push(parseInt(B[i])) 
            }
            let sum = D.reduce(function(a, b){
                return a + b;
            }, 0);
            let avg = sum / 6;
                instances.push(avg)
            }
            
            var max = instances.reduce(function(a, b) {
                return Math.max(a, b);
            }, 0);
            highest_avg.push(max)

        }
    else if (B.length <= 6) {
        let sum = B.reduce(function(a, b){
            return parseInt(a) + parseInt(b);
        }, 0);
        let avg = sum / 6;
        highest_avg.push(avg)
    }
    
    let ha1 = highest_avg;
    
    if(highest_avg) {
        document.getElementById("o1_average_6").value = parseFloat(ha1).toFixed(2);
    }
    else{
        document.getElementById("o1_average_6").value = '-';
    }
    document.getElementById("o1_highest_opacity").value = highest_read;
    
    if(highest_read > 20){
        document.getElementById("o1_instant_over_20").value = 'Yes';
    }
    else{
        document.getElementById("o1_instant_over_20").value = 'No';
    }
    if(highest_avg > 35){
        document.getElementById("o1_average_6_over_35").value = 'Yes';
    }
    else{
        document.getElementById("o1_average_6_over_35").value = 'No';
    }
    
        
    
}
function pt2_check() {
    const oven1 = parseInt(document.getElementById('o1').value),
          oven2 = parseInt(document.getElementById('o2').value);
    
    if (oven2 == parseInt(oven1) + 2) {
        document.getElementById("oven2_pop_id").style.visibility = 'hidden';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }  
    else if (oven1 >= oven2) {
        document.getElementById("oven2_pop_id").style.visibility = 'visible';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }
    else if (oven2 == parseInt(oven1) + 1) {
        document.getElementById("oven2_pop_id").style.visibility = 'visible';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }
    else if (oven2 > parseInt(oven1) + 2) {
        document.getElementById("oven2_pop_id").style.visibility = 'hidden';
        document.getElementById("comment_skip_id").style.visibility = 'visible';
    }  
}
function timecheck_2() {
    "use strict";
    const start_2 = document.getElementById('o2_start').value,
          end_2 = document.getElementById('o2_stop').value;
    
    if (end_2 == false) {
        
    }
    else if (start_2 > end_2) {
        var popup = document.getElementById("myPopup2").style.visibility = 'visible';
        document.getElementById("o2_start").style.backgroundColor = "#ffffff";
        document.getElementById("o2_stop").style.backgroundColor = "#ffffff";
    }
    else{
        var popup = document.getElementById("myPopup2").style.visibility = 'hidden';
        document.getElementById("o2_start").style.backgroundColor = "#3c983c85";
        document.getElementById("o2_stop").style.backgroundColor = "#3c983c85";
    }
}
function pt2_averages() {
    "use strict";
    const o2_1_reads_value  = document.getElementById('o2_1_reads').value;
    const o2_2_reads_value  = document.getElementById('o2_2_reads').value;
    const o2_3_reads_value  = document.getElementById('o2_3_reads').value;
    const o2_4_reads_value  = document.getElementById('o2_4_reads').value;
    const o2_5_reads_value  = document.getElementById('o2_5_reads').value;
    const o2_6_reads_value  = document.getElementById('o2_6_reads').value;
    const o2_7_reads_value  = document.getElementById('o2_7_reads').value;
    const o2_8_reads_value  = document.getElementById('o2_8_reads').value;
    const o2_9_reads_value  = document.getElementById('o2_9_reads').value;
    const o2_10_reads_value  = document.getElementById('o2_10_reads').value;
    const o2_11_reads_value  = document.getElementById('o2_11_reads').value;
    const o2_12_reads_value  = document.getElementById('o2_12_reads').value;
    const o2_13_reads_value  = document.getElementById('o2_13_reads').value;
    const o2_14_reads_value  = document.getElementById('o2_14_reads').value;
    const o2_15_reads_value  = document.getElementById('o2_15_reads').value;
    const o2_16_reads_value  = document.getElementById('o2_16_reads').value;

    

    let A = [o2_1_reads_value, o2_2_reads_value, o2_3_reads_value, o2_4_reads_value, o2_5_reads_value, o2_6_reads_value, o2_7_reads_value, o2_8_reads_value, o2_9_reads_value, o2_10_reads_value, o2_11_reads_value, o2_12_reads_value, o2_13_reads_value, o2_14_reads_value, o2_15_reads_value, o2_16_reads_value];

    const B = []

    const highest_avg = []

    
    for (let x in A) {
        
      	let home = parseInt(A[x]);
        if(Number.isInteger(home)) {
            B.push(A[x])
        }
        else{
        
        }
    }
    var highest_read = B.reduce(function(a, b) {
        return Math.max(a, b);
    }, 0);
    
    if (B.length > 6) {
        const instances = [];
        for (let h = 0; h < (B.length + 1) - 6; h++) {
            let i = h;
            let r = h;
            const D = [];
            for (i; i < r + 6; i++) {
                D.push(parseInt(B[i])) 
            }
            let sum = D.reduce(function(a, b){
                return a + b;
            }, 0);
            let avg = sum / 6;
                instances.push(avg)
            }
            
            var max = instances.reduce(function(a, b) {
                return Math.max(a, b);
            }, 0);
            highest_avg.push(max)

        }
    else if (B.length <= 6) {
        let sum = B.reduce(function(a, b){
            return parseInt(a) + parseInt(b);
        }, 0);
        let avg = sum / 6;
        highest_avg.push(avg)
    }
    
    let ha1 = highest_avg;
    
    if(highest_avg) {
        document.getElementById("o2_average_6").value = parseFloat(ha1).toFixed(2);
    }
    else{
        document.getElementById("o2_average_6").value = '-';
    }
    document.getElementById("o2_highest_opacity").value = highest_read;
    
    if(highest_read > 20){
        document.getElementById("o2_instant_over_20").value = 'Yes';
    }
    else{
        document.getElementById("o2_instant_over_20").value = 'No';
    }
    if(highest_avg > 35){
        document.getElementById("o2_average_6_over_35").value = 'Yes';
    }
    else{
        document.getElementById("o2_average_6_over_35").value = 'No';
    }
    
}
function pt3_check() {
    const oven1 = parseInt(document.getElementById('o2').value),
          oven2 = parseInt(document.getElementById('o3').value);
    
    if (oven2 == parseInt(oven1) + 2) {
        document.getElementById("oven3_pop_id").style.visibility = 'hidden';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }  
    else if (oven1 >= oven2) {
        document.getElementById("oven3_pop_id").style.visibility = 'visible';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }
    else if (oven2 == parseInt(oven1) + 1) {
        document.getElementById("oven3_pop_id").style.visibility = 'visible';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }
    else if (oven2 > parseInt(oven1) + 2) {
        document.getElementById("oven3_pop_id").style.visibility = 'hidden';
        document.getElementById("comment_skip_id").style.visibility = 'visible';
        document.getElementById("comment_skip_id").innerHTML = '<a id="exit_pop_id" class="exit_pop_class">X</a>Please change Oven No. for THIRD oven or comment below what oven(s) were skipped.';
    }  
}
function timecheck_3() {
    "use strict";
    const start_3 = document.getElementById('o3_start').value,
          end_3 = document.getElementById('o3_stop').value;
    
    if (end_3 == false) {
        
    }
    else if (start_3 > end_3) {
        var popup = document.getElementById("myPopup3").style.visibility = 'visible';
        document.getElementById("o3_start").style.backgroundColor = "#ffffff";
        document.getElementById("o3_stop").style.backgroundColor = "#ffffff";
    }
    else{
        var popup = document.getElementById("myPopup3").style.visibility = 'hidden';
        document.getElementById("o3_start").style.backgroundColor = "#3c983c85";
        document.getElementById("o3_stop").style.backgroundColor = "#3c983c85";
    }
}
function pt3_averages() {
    const o3_1_reads_value  = document.getElementById('o3_1_reads').value;
    const o3_2_reads_value  = document.getElementById('o3_2_reads').value;
    const o3_3_reads_value  = document.getElementById('o3_3_reads').value;
    const o3_4_reads_value  = document.getElementById('o3_4_reads').value;
    const o3_5_reads_value  = document.getElementById('o3_5_reads').value;
    const o3_6_reads_value  = document.getElementById('o3_6_reads').value;
    const o3_7_reads_value  = document.getElementById('o3_7_reads').value;
    const o3_8_reads_value  = document.getElementById('o3_8_reads').value;
    const o3_9_reads_value  = document.getElementById('o3_9_reads').value;
    const o3_10_reads_value  = document.getElementById('o3_10_reads').value;
    const o3_11_reads_value  = document.getElementById('o3_11_reads').value;
    const o3_12_reads_value  = document.getElementById('o3_12_reads').value;
    const o3_13_reads_value  = document.getElementById('o3_13_reads').value;
    const o3_14_reads_value  = document.getElementById('o3_14_reads').value;
    const o3_15_reads_value  = document.getElementById('o3_15_reads').value;
    const o3_16_reads_value  = document.getElementById('o3_16_reads').value;

    

    let A = [o3_1_reads_value, o3_2_reads_value, o3_3_reads_value, o3_4_reads_value, o3_5_reads_value, o3_6_reads_value, o3_7_reads_value, o3_8_reads_value, o3_9_reads_value, o3_10_reads_value, o3_11_reads_value, o3_12_reads_value, o3_13_reads_value, o3_14_reads_value, o3_15_reads_value, o3_16_reads_value];

    const B = []

    const highest_avg = []
    
    
    for (let x in A) {
        
      	let home = parseInt(A[x]);
        if(Number.isInteger(home)) {
            B.push(parseInt(A[x]))
        }
        else{
        
        }
    }
    var highest_read = B.reduce(function(a, b) {
        return Math.max(a, b);
    }, 0);
    
    if (B.length > 6) {
        const instances = [];
        for (let h = 0; h < (B.length + 1) - 6; h++) {
            let i = h;
            let r = h;
            const D = [];
            for (i; i < r + 6; i++) {
                D.push(parseInt(B[i])) 
            }
            let sum = D.reduce(function(a, b){
                return a + b;
            }, 0);
            let avg = sum / 6;
                instances.push(avg)
            }
            
            var max = instances.reduce(function(a, b) {
                return Math.max(a, b);
            }, 0);
            highest_avg.push(max)

        }
    else if (B.length <= 6) {
        let sum = B.reduce(function(a, b){
            return parseInt(a) + parseInt(b);
        }, 0);
        let avg = sum / 6;
        highest_avg.push(avg)
    }
    
    let ha1 = highest_avg;
    
    if(highest_avg) {
        document.getElementById("o3_average_6").value = parseFloat(ha1).toFixed(2);
    }
    else{
        document.getElementById("o3_average_6").value = '-';
    }
    document.getElementById("o3_highest_opacity").value = highest_read;
    
    if(highest_read > 20){
        document.getElementById("o3_instant_over_20").value = 'Yes';
    }
    else{
        document.getElementById("o3_instant_over_20").value = 'No';
    }
    if(highest_avg > 35){
        document.getElementById("o3_average_6_over_35").value = 'Yes';
    }
    else{
        document.getElementById("o3_average_6_over_35").value = 'No';
    }
}
function pt4_check() {
    const oven1 = parseInt(document.getElementById('o3').value),
          oven2 = parseInt(document.getElementById('o4').value);
    
    if (oven2 == parseInt(oven1) + 2) {
        document.getElementById("oven4_pop_id").style.visibility = 'hidden';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }  
    else if (oven1 >= oven2) {
        document.getElementById("oven4_pop_id").style.visibility = 'visible';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }
    else if (oven2 == parseInt(oven1) + 1) {
        document.getElementById("oven4_pop_id").style.visibility = 'visible';
        document.getElementById("comment_skip_id").style.visibility = 'hidden';
    }
    else if (oven2 > parseInt(oven1) + 2) {
        document.getElementById("oven4_pop_id").style.visibility = 'hidden';
        document.getElementById("comment_skip_id").style.visibility = 'visible';
        document.getElementById("comment_skip_id").innerHTML = '<a id="exit_pop_id" class="exit_pop_class">X</a>Please change Oven No. for FORTH oven or comment below what oven(s) were skipped.';
    } 
}
function timecheck_4() {
    "use strict";
    const start_4 = document.getElementById('o4_start').value,
          end_4 = document.getElementById('o4_stop').value;
    
    if (end_4 == false) {
        
    }
    else if (start_4 > end_4) {
        var popup = document.getElementById("myPopup4").style.visibility = 'visible';
        document.getElementById("o4_start").style.backgroundColor = "#ffffff";
        document.getElementById("o4_stop").style.backgroundColor = "#ffffff";
    }
    else{
        var popup = document.getElementById("myPopup4").style.visibility = 'hidden';
        document.getElementById("o4_start").style.backgroundColor = "#3c983c85";
        document.getElementById("o4_stop").style.backgroundColor = "#3c983c85";
    }
}
function pt4_averages() {
    "use strict";
    const o4_1_reads_value  = document.getElementById('o4_1_reads').value;
    const o4_2_reads_value  = document.getElementById('o4_2_reads').value;
    const o4_3_reads_value  = document.getElementById('o4_3_reads').value;
    const o4_4_reads_value  = document.getElementById('o4_4_reads').value;
    const o4_5_reads_value  = document.getElementById('o4_5_reads').value;
    const o4_6_reads_value  = document.getElementById('o4_6_reads').value;
    const o4_7_reads_value  = document.getElementById('o4_7_reads').value;
    const o4_8_reads_value  = document.getElementById('o4_8_reads').value;
    const o4_9_reads_value  = document.getElementById('o4_9_reads').value;
    const o4_10_reads_value  = document.getElementById('o4_10_reads').value;
    const o4_11_reads_value  = document.getElementById('o4_11_reads').value;
    const o4_12_reads_value  = document.getElementById('o4_12_reads').value;
    const o4_13_reads_value  = document.getElementById('o4_13_reads').value;
    const o4_14_reads_value  = document.getElementById('o4_14_reads').value;
    const o4_15_reads_value  = document.getElementById('o4_15_reads').value;
    const o4_16_reads_value  = document.getElementById('o4_16_reads').value;

    

    let A = [o4_1_reads_value, o4_2_reads_value, o4_3_reads_value, o4_4_reads_value, o4_5_reads_value, o4_6_reads_value, o4_7_reads_value, o4_8_reads_value, o4_9_reads_value, o4_10_reads_value, o4_11_reads_value, o4_12_reads_value, o4_13_reads_value, o4_14_reads_value, o4_15_reads_value, o4_16_reads_value];

    const B = []

    const highest_avg = []

    
    for (let x in A) {
        
      	let home = parseInt(A[x]);
        if(Number.isInteger(home)) {
            B.push(A[x])
        }
        else{
        
        }
    }
    var highest_read = B.reduce(function(a, b) {
        return Math.max(a, b);
    }, 0);
    
    if (B.length > 6) {
        const instances = [];
        for (let h = 0; h < (B.length + 1) - 6; h++) {
            let i = h;
            let r = h;
            const D = [];
            for (i; i < r + 6; i++) {
                D.push(parseInt(B[i])) 
            }
            let sum = D.reduce(function(a, b){
                return a + b;
            }, 0);
            let avg = sum / 6;
                instances.push(avg)
            }
            
            var max = instances.reduce(function(a, b) {
                return Math.max(a, b);
            }, 0);
            highest_avg.push(max)

        }
    else if (B.length <= 6) {
        let sum = B.reduce(function(a, b){
            return parseInt(a) + parseInt(b);
        }, 0);
        let avg = sum / 6;
        highest_avg.push(avg)
    }
    
    let ha1 = highest_avg;
    
    if(highest_avg) {
        document.getElementById("o4_average_6").value = parseFloat(ha1).toFixed(2);
    }
    else{
        document.getElementById("o4_average_6").value = '-';
    }
    document.getElementById("o4_highest_opacity").value = highest_read;
    
    if(highest_read > 20){
        document.getElementById("o4_instant_over_20").value = 'Yes';
    }
    else{
        document.getElementById("o4_instant_over_20").value = 'No';
    }
    if(highest_avg > 35){
        document.getElementById("o4_average_6_over_35").value = 'Yes';
    }
    else{
        document.getElementById("o4_average_6_over_35").value = 'No';
    }
    
}

document.getElementById("exit_pop_id").onclick = function() {
    exit_pop()
};

function exit_pop() {
    document.getElementById("comment_skip_id").style.visibility = 'hidden';
}