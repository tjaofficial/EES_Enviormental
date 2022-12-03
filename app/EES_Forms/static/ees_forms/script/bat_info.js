document.getElementById('id_inop_ovens').addEventListener('change',inop_ovens)

function inop_ovens(){
    const oven = document.getElementById('id_inop_ovens').value;
    if (oven == 0) {
        document.getElementById('id_inop_numbs').value = '-';
    }
}