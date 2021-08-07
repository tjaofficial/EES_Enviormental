function pt_averages() {
    const o1_1_reads_value  = document.getElementById('o1_1_reads').value;
    const o1_2_reads_value  = document.getElementById('o1_2_reads').value;
    const o1_3_reads_value  = document.getElementById('o1_3_reads').value;
    const o1_4_reads_value  = document.getElementById('o1_4_reads').value;
    const o1_5_reads_value  = document.getElementById('o1_5_reads').value;
    const o1_6_reads_value  = document.getElementById('o1_6_reads').value;
    const o1_7_reads_value  = document.getElementById('o1_7_reads').value;
    const o1_8_reads_value  = document.getElementById('o1_8_reads').value;
    const o1_9_reads_value  = document.getElementById('o1_9_reads').value;
    const o1_10_reads_value  = document.getElementById('o1_10_reads').value;
    const o1_11_reads_value  = document.getElementById('o1_11_reads').value;
    const o1_12_reads_value  = document.getElementById('o1_12_reads').value;
    const o1_13_reads_value  = document.getElementById('o1_13_reads').value;
    const o1_14_reads_value  = document.getElementById('o1_14_reads').value;
    const o1_15_reads_value  = document.getElementById('o1_15_reads').value;
    const o1_16_reads_value  = document.getElementById('o1_16_reads').value;

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

    let A = [
        [o1_1_reads_value, o1_2_reads_value, o1_3_reads_value, o1_4_reads_value, o1_5_reads_value, o1_6_reads_value, o1_7_reads_value, o1_8_reads_value, o1_9_reads_value, o1_10_reads_value, o1_11_reads_value, o1_12_reads_value, o1_13_reads_value, o1_14_reads_value, o1_15_reads_value, o1_16_reads_value],[o2_1_reads_value, o2_2_reads_value, o2_3_reads_value, o2_4_reads_value, o2_5_reads_value, o2_6_reads_value, o2_7_reads_value, o2_8_reads_value, o2_9_reads_value, o2_10_reads_value, o2_11_reads_value, o2_12_reads_value, o2_13_reads_value, o2_14_reads_value, o2_15_reads_value, o2_16_reads_value],[o3_1_reads_value, o3_2_reads_value, o3_3_reads_value, o3_4_reads_value, o3_5_reads_value, o3_6_reads_value, o3_7_reads_value, o3_8_reads_value, o3_9_reads_value, o3_10_reads_value, o3_11_reads_value, o3_12_reads_value, o3_13_reads_value, o3_14_reads_value, o3_15_reads_value, o3_16_reads_value],[o4_1_reads_value, o4_2_reads_value, o4_3_reads_value, o4_4_reads_value, o4_5_reads_value, o4_6_reads_value, o4_7_reads_value, o4_8_reads_value, o4_9_reads_value, o4_10_reads_value, o4_11_reads_value, o4_12_reads_value, o4_13_reads_value, o4_14_reads_value, o4_15_reads_value, o4_16_reads_value]
    ];

    
    
    const B = []
    
    for (let x in A) {
        const C = []
        for (let h in x) {
            for ( h = 0; h < A[x].length; h++){
                if(Number.isInteger(A[x][h])) {
                    C.push(A[x][h])
                }
            }
        }
        B.push("[" + C + ']')
    }
    
    const highest_avg = []

    for (let x in B) {
        if (B[x].length > 6) {
            const instances = [];
            for (let h = 0; h < (B[x].length + 1) - 6; h++) {
                let i = h;
                let r = h;
                const D = [];
                for (i; i < r + 6; i++) {
                    D.push(B[x][i])
                }
                let sum = D.reduce(function(a, b){
                    return a + b;
                }, 0);
                let avg = sum/6;
                instances.push(avg)
            }
            var max = instances.reduce(function(a, b) {
                return Math.max(a, b);
            }, 0);
            highest_avg.push(max)
        }
        else if (B[x].length <= 6) {
            let sum = B[x].reduce(function(a, b){
                return a + b;
            }, 0);
            let avg = sum/6;
            highest_avg.push(avg)
        }
    }
    
    let ha1 = highest_avg[0];
    let ha2 = highest_avg[1];
    let ha3 = highest_avg[2];
    let ha4 = highest_avg[3];
    
    document.getElementById("o1_average_6").value = ha1;
    document.getElementById("o2_average_6").value = ha2;
    document.getElementById("o3_average_6").value = ha3;
    document.getElementById("o4_average_6").value = ha4;

}