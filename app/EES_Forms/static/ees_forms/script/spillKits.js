const spill_kits_group = ['_tag_on', '_serial', '_complete', '_report', '_comment'];
function rows_true() {
    for(var i = 1; i <= 20; i++){
        const tag_on = document.getElementById('id_sk' + i + '_tag_on').value;
        const serial = document.getElementById('id_sk' + i + '_serial').value;
        const complete = document.getElementById('id_sk' + i + '_complete').value;
        const report = document.getElementById('id_sk' + i + '_report').value;
        const comment = document.getElementById('id_sk' + i + '_comment').value;
        
        if (tag_on || serial || complete || report || comment) {
            document.getElementById('id_sk' + i + '_tag_on').required = true;
            document.getElementById('id_sk' + i + '_serial').required = true;
            document.getElementById('id_sk' + i + '_complete').required = true;
            document.getElementById('id_sk' + i + '_report').required = true;
            document.getElementById('id_sk' + i + '_comment').required = true;
        } else {
            document.getElementById('id_sk' + i + '_tag_on').required = false;
            document.getElementById('id_sk' + i + '_serial').required = false;
            document.getElementById('id_sk' + i + '_complete').required = false;
            document.getElementById('id_sk' + i + '_report').required = false;
            document.getElementById('id_sk' + i + '_comment').required = false;
        }
    }
}
