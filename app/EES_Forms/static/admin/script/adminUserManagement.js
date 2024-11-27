document.addEventListener('DOMContentLoaded', () => {
    // Populate user list
    const users = [
        "John Doe", "Jane Smith", "Alice Johnson", "Bob Brown", "Chris Davis"
    ];
    const userList = document.getElementById('user-list');
    users.forEach(user => {
        const li = document.createElement('li');
        li.textContent = user;
        userList.appendChild(li);
    });
});