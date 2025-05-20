const totalFacilities = document.getElementById('totalFacilities').value;

fetch('/ajax/facilityList/companyFacilityInfo/')
    .then(response => response.json())
    .then(data => {
        //console.log('Facilities:', data);
        data.forEach((item) => {
            let facilityDiv = document.getElementById('facility' + String(item.facility_id))
            //console.log(facilityDiv)
            let totalForms = facilityDiv.dataset.totalforms;//29
            let facilityNumber = facilityDiv.dataset.facid;
            let packetIDList = JSON.parse(facilityDiv.dataset.packlist);
            item.fsIDList.forEach((fsID) => {
                //console.log(x)
                let itemBeingDraggedID = String(facilityNumber) + "drag" + String(fsID);
                //console.log(itemBeingDraggedID)
                const dragItem = document.getElementById(itemBeingDraggedID);
                //console.log(dragItem)
                dragItem.addEventListener('dragstart', function(event){
                    //console.log(event.toElement.dataset.fsid);
                    let fsIDFacID = String(event.target.dataset.fsid)+'-'+String(facilityNumber)
                    event.dataTransfer.setData("Text", fsIDFacID);
                    //console.log(event.dataTransfer.getData("Text"));
                    data.forEach((elemn) => {
                        if (elemn.facility_id!=item.facility_id){
                            //console.log('CHeck 1')
                            let facilityDivBlock = document.getElementById('facility'+String(elemn.facility_id))
                            let packetIDList = JSON.parse(facilityDivBlock.dataset.packlist);
                            for (let q=0;q<packetIDList.length;q++){
                                let packetID = packetIDList[q]
                                let dropZone = document.getElementById('dropZone'+String(packetID));
                                let dropZoneFacID = dropZone.dataset.facid;
                                let dragFacID = event.dataTransfer.getData("Text").split('-');
                                //console.log(dropZoneFacID)
                                //console.log(dragFacID)
                                if (Number(dropZoneFacID) != Number(dragFacID[1])){
                                    //console.log('CHeck 2')
                                    //console.log(dropZone)
                                    dropZone.dataset.cursor = "no-drop";
                                    dropZone.style.cursor = 'no-drop';
                                }
                            }
                        }
                    })
                })
                dragItem.addEventListener('dragend',function(event){
                    for (let z=1;z<=parseInt(totalFacilities);z++){
                        //console.log('CHeck 1')
                        let facilityDivBlock = document.getElementById('facility'+String(z))
                        let packetIDList = JSON.parse(facilityDivBlock.dataset.packlist);
                        for (let q=0;q<packetIDList.length;q++){
                            let packetID = packetIDList[q]
                            let dropZone = document.getElementById('dropZone'+String(packetID));
                            
                            dropZone.dataset.cursor = "pointer";
                            dropZone.style.cursor = 'pointer';   
                        }
                    }
                })
            });
            for (let i=0;i<packetIDList.length;i++){
                let packetID = packetIDList[i]
                let dropZone = document.getElementById('dropZone'+String(packetID));
                let dropZoneFacID = dropZone.dataset.facid;
                dropZone.addEventListener('dragover', function(event){
                    event.preventDefault();
                    console.log("dragover has happened")
                    if (dropZone.dataset.cursor == 'no-drop'){
                        event.dataTransfer.dropEffect = "none";
                        event.target.style.cursor = 'no-drop';
                    }
                })
                dropZone.addEventListener('drop', function(event){
                    let dragFacID = event.dataTransfer.getData("Text").split('-');
                    //console.log(String(dropZoneFacID)+' vs '+String(dragFacID[1]))
                    console.log('Form has been dragged and released on a packet.')
                    if (Number(dropZoneFacID) == Number(dragFacID[1])){
                        console.log('Form was released on a packet in its correct facility.')
                        let dragFacID = event.dataTransfer.getData("Text").split('-');
                        document.getElementById('formSettingsID').value = String(dragFacID[0])+"-"+ event.toElement.dataset.packetid;
                        //console.log(String(event.dataTransfer.getData("Text"))+"-"+ event.toElement.dataset.packetid)
                        console.log("form has been added to Packet " + String(event.toElement.dataset.packetid)+' within facility '+ String(dropZoneFacID))
                    } else {
                        console.log('Form was not dropped into a packet in the correct facility.')
                    }
                    document.updatePacket.submit();
                })
            }
        })

    })
    .catch(error => console.error('Error loading facilities:', error));