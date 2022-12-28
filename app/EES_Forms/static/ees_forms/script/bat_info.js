document.getElementById('id_inop_ovens').addEventListener('change',inop_ovens)
document.getElementById('id_inop_numbs').addEventListener('change',inop_ovens)

function inop_ovens(){
    const oven_numbs = document.getElementById('id_inop_numbs').value;

    let ovenList = oven_numbs.replace(' ', '').split(',');

    let quant = ovenList.length;

    console.log(quant)


    // const oven = document.getElementById('id_inop_ovens').value;
    // if (oven == 0) {
    //     document.getElementById('id_inop_numbs').value = '-';
    // }
}
