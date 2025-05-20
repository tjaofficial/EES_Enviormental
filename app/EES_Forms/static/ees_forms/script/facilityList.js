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
    //console.log(facilityID)
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

openDeletePacketModal = (elem, packID) => {
    document.getElementById('deletePacForm'+String(packID)).style.display = 'flex';
}

exit_modal = (packID, task) => {
    var modalAdd = document.getElementById(task+String(packID));
    modalAdd.style.display = "none";
}

function addFacilityForm(elem){
    const selectedFacilityID = elem.dataset.facility;
    const link = elem.dataset.link;
    fetch("/set-facility/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie('csrftoken')
        },
        body: JSON.stringify({ id: selectedFacilityID })
    }).then(() => {
        window.location.href = link;
    });
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function changePacketFormLabel(packetID, fsID){
    console.log("Show Label Input")
    const formLabelElement = document.querySelector(`#packet-form-label-${packetID}-${fsID}`);
    const changeLabelButton = document.querySelector(`#change-label-btn-${packetID}-${fsID}`);
    const deletePacketButton = document.querySelector(`#delete-packet-btn-${packetID}-${fsID}`);
    const outterPacketFormCont = document.querySelector(`#outter-packet-forms-cont-${packetID}-${fsID}`);
    //Create input
    const labelInput = document.createElement('input');
    labelInput.name = "labelInput";
    labelInput.type = "text";
    labelInput.classList.add('new-label-input');
    labelInput.required = true;
    //adds new input to new span element
    const newLabelInputCont = document.createElement('span');
    newLabelInputCont.id = `label-input-cont-${packetID}-${fsID}`;
    newLabelInputCont.innerHTML = "Form: "
    newLabelInputCont.appendChild(labelInput);
    
    
    

    if (changeLabelButton.textContent === 'Change Label') {
        //hides the exisiting form label cont
        formLabelElement.style.display = 'none';
        //puts new span element first inside the exisiting forms container
        outterPacketFormCont.prepend(newLabelInputCont);
        labelInput.focus()
        changeLabelButton.innerHTML = "Save";
        deletePacketButton.style.display = 'none';
    } else {
        const updatedlabelInput = document.querySelector(`#label-input-cont-${packetID}-${fsID} input`);
        const newLabel = updatedlabelInput.value;
        fetch('/ajax/packets/update-label/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                packet_ID: packetID,
                fs_ID: fsID,
                newLabel: newLabel
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const halfOfLabel = formLabelElement.textContent.slice(formLabelElement.textContent.indexOf('-'));
                const fullLabel = `Form ${data.new_label} ${halfOfLabel}`;
                formLabelElement.textContent = fullLabel;
                formLabelElement.style.display = 'inline-block';
                changeLabelButton.textContent = 'Change Label';
                deletePacketButton.style.display = 'inline-block';
                const removeNewLabelInputCont = outterPacketFormCont.querySelector(`#label-input-cont-${packetID}-${fsID}`);
                removeNewLabelInputCont.remove();
            } else {
                alert('ERROR: ID-11850008. Label was not updated, try again or contact Support Team.');
            }
        });
    }
}