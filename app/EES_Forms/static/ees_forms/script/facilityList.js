show_formsList = (elem) => {
    let list = elem.parentNode.children[2];
    list.style.display = 'table';
} 

show_formsList_form = (elem) => {
    let list = elem.parentNode.children[2];
    console.log(list);
    list.style.display = 'table';
} 

open_packet_modal = (elem, packID) => {
    const getID = elem.parentNode.parentNode.dataset.selector;
    document.getElementById(packID).style.display = 'flex';
}


exit_modal = (packID) => {
    var modalAdd = document.getElementById(packID);
    modalAdd.style.display = "none";
}