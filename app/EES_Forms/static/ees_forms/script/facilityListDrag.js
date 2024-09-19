//on hover big div box run this fucntion 
function bang(elem){
    //console.log("hello")
    const dragItemNumber = elem.id.slice(4);

    let facilityNumber = elem.dataset.facid;//3
    let packetIDList = JSON.parse(elem.dataset.packlist);
    //console.log(elem.dataset.packlist)
    for (let i=0;i<packetIDList.length;i++){
        let packetID = packetIDList[i]
        let dropZone = document.getElementById('dropZone'+String(packetID));
        //console.log(dropZone)
        dropZone.addEventListener('dragover', function(event){
            event.preventDefault()
        })
        dropZone.addEventListener('drop', function(event){
            //console.log(event)
            //console.log(event.dataTransfer.getData("Text"))
            //show_formsList_form(dropZone)
            //console.log(event.toElement.dataset.packetid)
            document.getElementById('formSettingsID').value = String(event.dataTransfer.getData("Text"))+"-"+ event.toElement.dataset.packetid;
            document.updatePacket.submit();
        })
    }
    //console.log(facilityNumber)
    let totalForms = elem.dataset.totalforms;//29
    //console.log(totalForms)
    for (let x=1;x<=parseInt(totalForms);x++){
        //console.log(x)
        let itemBeingDraggedID = String(facilityNumber) + "drag" + String(x);
        //console.log(itemBeingDraggedID)
        const dragItem = document.getElementById(itemBeingDraggedID);
        //console.log(dragItem)
        
        dragItem.addEventListener('dragstart',function(event){
            //console.log(event);
            //console.log(event.toElement.dataset.fsid);
            event.dataTransfer.setData("Text", event.target.dataset.fsid);
        })
    }
    
}