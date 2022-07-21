// Get the modal
var modalAdd = document.getElementById("addModal");

// Get the button that opens the modal
var addBtn = document.getElementById("addBtn");

// Get the <span> element that closes the modal
var spanAdd = document.getElementsByClassName("closeAdd")[0];

// When the user clicks the button, open the modal 
addBtn.onclick = function() {
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


document.getElementById('id_pdf_file').onchange = function () {
    const file = document.getElementById('id_pdf_file').value;
    const split_array = String(file).split("\\")
    const link = split_array[split_array.length - 1]
    const final = link.replace(/ /g, '_')
    document.getElementById('id_pdf_link').value = final;
}

