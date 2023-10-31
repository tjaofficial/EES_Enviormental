// Get the modal
var modalAdd = document.getElementById("modalContainer");
// Get the <span> element that closes the modal
var spanAdd = document.getElementsByClassName("closeAdd")[0];
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