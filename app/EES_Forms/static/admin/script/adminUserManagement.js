document.addEventListener("DOMContentLoaded", () => {
    const tableBody = document.getElementById("user-table-body");
    const searchInput = document.getElementById("user-search");

    let users = [];
    const populateTable = (data) => {
        tableBody.innerHTML = "";
        data.forEach(user => {
            const row = document.createElement("tr");
            if (user.position == "supervisor"){
                row.innerHTML += `<td>${user.name}<a href="../admin-pages/login-as/${user.userID}/" onclick="return confirm('Are you sure you want to act as this user?')">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512">
                        <path d="M40.1 467.1l-11.2 9c-3.2 2.5-7.1 3.9-11.1 3.9C8 480 0 472 0 462.2L0 192C0 86 86 0 192 0S384 86 384 192l0 270.2c0 9.8-8 17.8-17.8 17.8c-4 0-7.9-1.4-11.1-3.9l-11.2-9c-13.4-10.7-32.8-9-44.1 3.9L269.3 506c-3.3 3.8-8.2 6-13.3 6s-9.9-2.2-13.3-6l-26.6-30.5c-12.7-14.6-35.4-14.6-48.2 0L141.3 506c-3.3 3.8-8.2 6-13.3 6s-9.9-2.2-13.3-6L84.2 471c-11.3-12.9-30.7-14.6-44.1-3.9zM160 192a32 32 0 1 0 -64 0 32 32 0 1 0 64 0zm96 32a32 32 0 1 0 0-64 32 32 0 1 0 0 64z"/>
                    </svg>
                </a></td>`
            } else {
                row.innerHTML += `<td>${user.name}</td>`
            }
            row.innerHTML += `
                <td>${user.company}</td>
                <td>${user.position}</td>
                <td>${user.number}</td>
                <td>${user.email}</td>
                <td><a href="#">${user.settings}</a></td>
                <td>${user.status}</td>
                <td class="options-menu">⋮</td>
            `;
            tableBody.appendChild(row);
        });
    };

    fetch("/admin-pages/users/json/", {
        method: "GET",
        credentials: "include", // 🔐 This is the important part
        headers: {
            "Accept": "application/json"
        }
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      users = data.users;
      populateTable(users);
    })
    .catch(error => {
      console.error("Error loading user data:", error);
      tableBody.innerHTML = `<tr><td colspan="8">Failed to load users</td></tr>`;
    });

  searchInput.addEventListener("input", (e) => {
    const term = e.target.value.toLowerCase();
    const filtered = users.filter(u =>
      u.name.toLowerCase().includes(term) || u.company.toLowerCase().includes(term)
    );
    populateTable(filtered);
  });
});

// Simple column sort
function sortTable(n) {
  const table = document.getElementById("user-table");
  let switching = true;
  let dir = "asc";
  let switchCount = 0;

  while (switching) {
    switching = false;
    const rows = table.rows;
    for (let i = 1; i < rows.length - 1; i++) {
      let x = rows[i].getElementsByTagName("TD")[n];
      let y = rows[i + 1].getElementsByTagName("TD")[n];
      let shouldSwitch = false;

      if (dir === "asc" && x.innerText.toLowerCase() > y.innerText.toLowerCase()) {
        shouldSwitch = true;
      } else if (dir === "desc" && x.innerText.toLowerCase() < y.innerText.toLowerCase()) {
        shouldSwitch = true;
      }

      if (shouldSwitch) {
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
        switchCount++;
        break;
      }
    }

    if (!switching && switchCount === 0 && dir === "asc") {
      dir = "desc";
      switching = true;
    }
  }
}
