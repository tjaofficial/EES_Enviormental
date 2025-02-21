// Select/Deselect all checkboxes
function toggleSelectAll(checkbox) {
    const checkboxes = document.querySelectorAll('.sopCheckbox');
    checkboxes.forEach(cb => cb.checked = checkbox.checked);
}

// Delete selected SOPs (add endpoint logic later)
function deleteSelected() {
    const selected = document.querySelectorAll('.sopCheckbox:checked');
    
    if (selected.length === 0) {
        alert('Please select at least one SOP to delete.');
        return;
    }

    if (confirm('Are you sure you want to delete the selected SOPs?')) {
        // Collect the SOP IDs
        const sopIds = Array.from(selected).map(cb => cb.getAttribute('data-sop-id'));

        // Send a POST request to delete the selected SOPs
        fetch(`/delete_selected_sops/{{ facility }}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ selected_sops: sopIds })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                location.reload();  // Refresh the page after deletion
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }
}


// Trigger update modal
function triggerUpdateModal(id) {
    // Implement modal update logic here
    alert('Update SOP with ID: ' + id);
}
