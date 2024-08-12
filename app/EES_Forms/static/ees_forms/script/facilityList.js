show_formsList = (elem) => {
    let list = elem.parentNode.parentNode.children[1];
    if (list.style.display == 'none'){
        list.style.display = 'table';
    } else {
        list.style.display = 'none';
    }
} 

show_formsList_form = (elem) => {
    let list = elem.parentNode.children[1];
    console.log(list);
    list.style.display = 'table';
} 

open_delete_modal = (elem, packID) => {
    document.getElementById('delete'+String(packID)).style.display = 'flex';
}


exit_modal = (packID, task) => {
    var modalAdd = document.getElementById(task+String(packID));
    modalAdd.style.display = "none";
}


open_packet_modal = (elem, packID) => {
    document.getElementById('edit'+String(packID)).style.display = 'flex';
}

open_delete_facForm_modal = (elem, packID) => {
    document.getElementById('deleteFacForm'+String(packID)).style.display = 'flex';
}
exit_modal = (packID, task) => {
    var modalAdd = document.getElementById(task+String(packID));
    modalAdd.style.display = "none";
}