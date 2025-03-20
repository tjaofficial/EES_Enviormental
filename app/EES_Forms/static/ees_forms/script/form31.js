document.addEventListener("DOMContentLoaded", function() {
    let tableRows = document.querySelectorAll(".tank-table tbody tr");

    tableRows.forEach(row => {
        let radios = row.querySelectorAll(".status-radio");
        let commentField = row.querySelector(".tank-comment");

        radios.forEach(radio => {
            radio.addEventListener("change", function() {
                if (this.value === "OK") {
                    row.classList.add("ok");
                    row.classList.remove("not-ok");
                } else {
                    row.classList.add("not-ok");
                    row.classList.remove("ok");
                }
            });
        });

        // Ensure comments are always editable
        commentField.addEventListener("click", function(event) {
            event.stopPropagation(); // Prevent row click from interfering
        });
    });
});


function toggleTable() {
    let table = document.getElementById("inspection-table");
    let arrow = document.getElementById("toggle-arrow");

    if (table.classList.contains("hidden")) {
        table.classList.remove("hidden");
        arrow.innerHTML = "&#9650;"; // Up Arrow
    } else {
        table.classList.add("hidden");
        arrow.innerHTML = "&#9660;"; // Down Arrow
    }
}
