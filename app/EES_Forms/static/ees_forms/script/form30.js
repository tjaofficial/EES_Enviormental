document.addEventListener("DOMContentLoaded", function() {
    
    /*** 🟢 STATUS COMMENT FIELD TOGGLE ***/
    document.querySelectorAll(".status-radio").forEach(radio => {
        radio.addEventListener("change", function() {
            let commentField = this.closest(".status-item").querySelector(".status-comment");

            if (this.value === "Not OK") {
                commentField.disabled = false;
                commentField.style.background = "white";
                commentField.style.cursor = "text";
            } else {
                commentField.disabled = true;
                commentField.value = "";
                commentField.style.background = "#f5f5f5";
                commentField.style.cursor = "not-allowed";
            }
        });
    });

    /*** 🟢 OK / NOT OK TOGGLE ***/
    document.querySelectorAll(".status").forEach(select => {
        select.addEventListener("change", function() {
            let inputField = this.parentElement.querySelector(".issue-details");
            inputField.style.display = (this.value === "not_ok") ? "block" : "none";
        });
    });

    /*** 🟢 WASTE TABLE FUNCTIONALITY ***/
    let tableBody = document.getElementById("wasteTableBody");

    function updateRowListeners(row) {
        // Increment/Decrement Count
        row.querySelector(".increment").addEventListener("click", function() {
            let input = this.previousElementSibling;
            input.value = parseInt(input.value) + 1;
        });

        row.querySelector(".decrement").addEventListener("click", function() {
            let input = this.nextElementSibling;
            if (parseInt(input.value) > 1) {
                input.value = parseInt(input.value) - 1;
            }
        });

        // Remove Row
        row.querySelector(".removeRow").addEventListener("click", function() {
            row.remove();
        });

        // Add Date
        row.querySelector(".add-date").addEventListener("click", function() {
            let dateContainer = this.previousElementSibling;
            console.log(dateContainer)
            let counter = dateContainer.getAttribute("name").replace("date_container_", "").replace("[]","")
            let dateGroup = document.createElement("div");
            dateGroup.classList.add("date-group");
            let dateLength = document.querySelectorAll("input[name^='waste_dates']").length;
            dateGroup.innerHTML = `
                <input type="date" name="waste_dates_${counter}[]" required>
                <button type="button" class="remove-date" title="Remove Date">✖</button>
            `;

            dateContainer.appendChild(dateGroup);
        });

        // Remove Date (Using Event Delegation)
        row.addEventListener("click", function(event) {
            if (event.target.classList.contains("remove-date")) {
                event.target.closest(".date-group").remove();
            }
        });
    }

    /*** 🟢 ADD NEW ROW ***/
    document.getElementById("addRow").addEventListener("click", function() {
        let rowCount = tableBody.getElementsByTagName("tr").length;
        
        let newRow = document.createElement("tr");
        newRow.innerHTML = `
            <td><input type="text" name="waste_description_${rowCount}[]" required></td>
            
            <td>
                <div class="count-container">
                    <button type="button" class="decrement">−</button>
                    <input type="number" name="container_count_${rowCount}[]" value="1" min="1" required>
                    <button type="button" class="increment">+</button>
                </div>
            </td>

            <td><input type="text" name="waste_code_${rowCount}[]" required></td>

            <td>
                <div class="date-container" name="date_container_${rowCount}[]">
                    <div class="date-group">
                        <input type="date" name="waste_dates_${rowCount}[]" required>
                        <button type="button" class="remove-date" title="Remove Date">✖</button>
                    </div>
                </div>
                <button type="button" class="add-date">+ Add Date</button>
            </td>

            <td><button type="button" class="removeRow">🗑️</button></td>
        `;

        tableBody.appendChild(newRow);
        updateRowListeners(newRow);
    });

    /*** 🟢 INITIALIZE EXISTING ROWS ***/
    document.querySelectorAll("#wasteTableBody tr").forEach(updateRowListeners);
});
