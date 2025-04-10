function show_formsList2(elem) {
    const listContID = elem.dataset.clickbox;
    const packetForms = document.getElementById(`packetForms${listContID}`);

    // If it's open, close it
    if (packetForms.classList.contains('open')) {
        // Collapse with transition
        packetForms.style.maxHeight = packetForms.scrollHeight + 'px'; // Set the current height to allow transition
        requestAnimationFrame(() => {
            packetForms.style.maxHeight = '0px';
        });
        packetForms.classList.remove('open');
    } else {
        // Expand
        packetForms.classList.add('open');
        packetForms.style.maxHeight = packetForms.scrollHeight + 'px';

        // Optional: Remove the inline style after transition
        packetForms.addEventListener('transitionend', function cleanup(e) {
            if (packetForms.classList.contains('open')) {
                packetForms.style.maxHeight = 'none'; // Let it grow naturally now
            }
            packetForms.removeEventListener('transitionend', cleanup);
        });
    }
}

function scrollToFacility(facilityID) {
    const target = document.getElementById(`facility${facilityID}`);
    if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
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