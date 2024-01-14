

// Get the modal
var modalAdd = document.getElementById("tosModalCont");
console.log(modalAdd)
// Get the button that opens the modal
var addBtn = document.getElementById("addBtn");

// Get the <span> element that closes the modal
var spanAdd = document.getElementsByClassName("closeAdd")[0];

// When the user clicks the button, open the modal 
triggerButton = (elem) => {
  modalAdd.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
spanAdd.onclick = function() {
    modalAdd.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modalAdd) {
    modalAdd.style.display = "none";
  }
}

