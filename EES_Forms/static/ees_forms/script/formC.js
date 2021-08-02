function sumTime() {
    const TRead1_value  = document.getElementById('TRead1').value;
    const TRead2_value  = document.getElementById('TRead2').value;
    const TRead3_value  = document.getElementById('TRead3').value;
    const TRead4_value  = document.getElementById('TRead4').value;
    const TRead5_value  = document.getElementById('TRead5').value;
    const TRead6_value  = document.getElementById('TRead6').value;
    const TRead7_value  = document.getElementById('TRead7').value;
    const TRead8_value  = document.getElementById('TRead8').value;
    const TRead9_value  = document.getElementById('TRead9').value;
    const TRead10_value  = document.getElementById('TRead10').value;
    const TRead11_value  = document.getElementById('TRead11').value;
    const TRead12_value  = document.getElementById('TRead12').value;
    
    const ARead1_value  = document.getElementById('ARead1').value;
    const ARead2_value  = document.getElementById('ARead2').value;
    const ARead3_value  = document.getElementById('ARead3').value;
    const ARead4_value  = document.getElementById('ARead4').value;
    const ARead5_value  = document.getElementById('ARead5').value;
    const ARead6_value  = document.getElementById('ARead6').value;
    const ARead7_value  = document.getElementById('ARead7').value;
    const ARead8_value  = document.getElementById('ARead8').value;
    const ARead9_value  = document.getElementById('ARead9').value;
    const ARead10_value  = document.getElementById('ARead10').value;
    const ARead11_value  = document.getElementById('ARead11').value;
    const ARead12_value  = document.getElementById('ARead12').value;

    let avgReadingT =  (parseFloat(TRead1_value) + parseFloat(TRead2_value) + parseFloat(TRead3_value) + parseFloat(TRead4_value) + parseFloat(TRead5_value) + parseFloat(TRead6_value) + parseFloat(TRead7_value) + parseFloat(TRead8_value) + parseFloat(TRead9_value) + parseFloat(TRead10_value) + parseFloat(TRead11_value) + parseFloat(TRead12_value)) / 12;
    
    let avgReadingA =  (parseFloat(ARead1_value) + parseFloat(ARead2_value) + parseFloat(ARead3_value) + parseFloat(ARead4_value) + parseFloat(ARead5_value) + parseFloat(ARead6_value) + parseFloat(ARead7_value) + parseFloat(ARead8_value) + parseFloat(ARead9_value) + parseFloat(ARead10_value) + parseFloat(ARead11_value) + parseFloat(ARead12_value)) / 12;

    document.getElementById('average_t').value = avgReadingT;
    document.getElementById('average_p').value = avgReadingA;
}