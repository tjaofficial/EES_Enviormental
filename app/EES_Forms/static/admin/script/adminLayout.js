// // Toggle panels
// function showPanel(panelId) {
//     const panels = document.querySelectorAll('.panel');
//     panels.forEach(panel => panel.classList.remove('active'));
//     document.getElementById(panelId).classList.add('active');
// }

// Filter users in the User Management section
function filterUsers() {
    const searchValue = document.getElementById('user-search').value.toLowerCase();
    const userList = document.getElementById('user-list');
    const users = userList.querySelectorAll('li');
    users.forEach(user => {
        user.style.display = user.textContent.toLowerCase().includes(searchValue) ? 'block' : 'none';
    });
}

// Simulate retrying payments
function retryPayments() {
    alert("Retrying failed payments...");
}
