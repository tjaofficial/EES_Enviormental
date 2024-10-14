function mouseOverHelp(elem){
    const count = String(elem.dataset.helpcount);
    const helpPopup =  document.getElementById('help-popup'+ count)
    helpPopup.style.display = 'block';
    helpPopup.style.visibility = 'visible';
}
function mouseMoveHelp(elem, event){
    const count = String(elem.dataset.helpcount);
    const helpPopup =  document.getElementById('help-popup'+ count)
    helpPopup.style.left = event.pageX + 'px'; // Positioning relative to the cursor
    helpPopup.style.top = event.pageY + 'px';  // Positioning relative to the cursor
}
function mouseLeaveHelp(elem){
    const count = String(elem.dataset.helpcount);
    const helpPopup =  document.getElementById('help-popup'+ count)
    helpPopup.style.display = 'none';
    helpPopup.style.visibility = 'hidden';
}