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