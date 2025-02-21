

// // Get the modal
// var modalAdd = document.getElementById("addModal");

// // Get the button that opens the modal
// var addBtn = document.getElementById("addBtn");

// Get the <span> element that closes the modal
var spanAdd = document.getElementsByClassName("closeAdd")[0];

// // When the user clicks the button, open the modal 
// triggerButton = (elem) => {
//   modalAdd.style.display = "block";
// }

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

document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('addModal');
  const modalTitle = document.getElementById('modalTitle');
  const sopIdField = document.getElementById('sopId');
  const sopNameField = document.getElementById('sopName');
  const sopRevisionDateField = document.getElementById('sopRevisionDate');
  const sopFileField = document.getElementById('sopFile');
  const closeBtn = document.querySelector('.closeAdd');

  // Open modal for adding
  document.getElementById('addSopBtn').addEventListener('click', () => {
      modalTitle.textContent = 'ADD SOP PDF';
      sopIdField.value = '';  // Clear ID for new entries
      sopNameField.value = '';
      sopRevisionDateField.value = '';
      sopFileField.value = '';
      modal.style.display = 'block';
  });

  // Open modal for updating
  document.querySelectorAll('.updateBtn').forEach(button => {
      button.addEventListener('click', (e) => {
          const sop = JSON.parse(button.dataset.sop);  // Parse SOP data
          modalTitle.textContent = 'UPDATE SOP PDF';
          sopIdField.value = sop.id;
          sopNameField.value = sop.name;
          sopRevisionDateField.value = sop.revision_date;
          modal.style.display = 'block';
      });
  });

  // Close the modal
  closeBtn.addEventListener('click', () => {
      modal.style.display = 'none';
  });

  // Close on outside click
  window.addEventListener('click', (e) => {
      if (e.target == modal) {
          modal.style.display = 'none';
      }
  });
});
