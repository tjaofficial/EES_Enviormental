document.addEventListener("DOMContentLoaded", function() {
    
    /*** 🟢 Ensure comments initialize correctly based on selected radio ***/
    document.querySelectorAll(".status-item").forEach(item => {
        let radios = item.querySelectorAll(".status-radio");
        let commentField = item.querySelector(".status-comment");
    
        let isNotOkSelected = false;
    
        radios.forEach(radio => {
            if (radio.checked && radio.value === "Not OK") {
                isNotOkSelected = true;
            }
        });
    
        if (isNotOkSelected) {
            commentField.style.display = "block"; // ✅ Show comment field if "Not OK" is already selected
            commentField.disabled = false;
            commentField.style.background = "white";
            commentField.style.cursor = "text";
            commentField.parentElement.style.border = "2px solid red";
            commentField.parentElement.style.boxShadow = "inset 0 0 4px 0px red";
            //console.log("Changed background to white for:", commentField); // 🔥 Debugging
        } else {
            commentField.style.display = "none"; // ✅ Only hide if NOT "Not OK"
            commentField.disabled = true;
            commentField.style.background = "#f5f5f5";
            commentField.style.cursor = "not-allowed";
            commentField.parentElement.style.border = "2px solid rgba(60, 152, 60, 0.52)";
            commentField.parentElement.style.boxShadow = "inset 0 0 4px 0px rgba(60, 152, 60, 0.52)";
            //console.log("Changed background to gray for:", commentField); // 🔥 Debugging
        }
    });

    /*** 🟢 STATUS COMMENT FIELD TOGGLE ***/
    document.querySelectorAll(".status-radio").forEach(radio => {
        radio.addEventListener("change", function() {
            let commentField = this.closest(".status-item").querySelector(".status-comment");
    
            if (this.value === "Not OK") {
                commentField.style.display = "block";
                commentField.disabled = false;
                commentField.style.background = "white"; // ✅ Attempt to force white background
                commentField.style.cursor = "text";
                commentField.parentElement.style.border = "2px solid red";
                commentField.parentElement.style.boxShadow = "inset 0 0 4px 0px red";
                //console.log("Changed background to white for:", commentField); // 🔥 Debugging
            } else {
                commentField.style.display = "none";
                commentField.disabled = true;
                commentField.style.background = "#f5f5f5";
                commentField.style.cursor = "not-allowed";
                commentField.parentElement.style.border = "2px solid rgba(60, 152, 60, 0.52)";
                commentField.parentElement.style.boxShadow = "inset 0 0 4px 0px rgba(60, 152, 60, 0.52)";
                //console.log("Changed background to gray for:", commentField); // 🔥 Debugging
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

            <td>
                <select name="waste_code_${rowCount}[]" required>
                    <option value="">-------</option>
                    <option value="univ">UNIV</option>
                    <option value="non-haz">NON-HAZ</option>
                    <option value="haz">HAZ</option>
                </select>
            </td>

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

    /*** 🟢 DISPLAY THE COMMENT IF NOT OKAY ***/

    let statusItems = document.querySelectorAll(".status-item");

    statusItems.forEach(item => {
        let commentSection = item.querySelector(".status-comment");

        // Prevent comment from closing when clicking inside textarea
        if (commentSection) {
            commentSection.addEventListener("click", function(event) {
                event.stopPropagation(); // Stops event from bubbling to .status-item
            });
        }

        item.addEventListener("click", function(event) {
            let radioClicked = event.target.classList.contains("status-radio");
            if (!radioClicked) {
                this.classList.toggle("active"); // Toggles the active class
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function() {
    let areaSelect = document.querySelector("#id_area_name"); // 🔥 Select the area dropdown
    let fsIDInput = document.querySelector("#fsID");

    areaSelect.addEventListener("change", function() {
        let selectedArea = this.value;
        let fsID = fsIDInput ? fsIDInput.value : "";

        console.log("Area selected:", String(selectedArea));
        console.log("fsID:", fsID);

        if (!selectedArea || !fsID) return; // No area selected, exit

        fetch(`/get-existing-form/?area_name=${encodeURIComponent(selectedArea)}&fsID=${fsID}`)
            .then(response => response.json())
            .then(data => {
                console.log("Fetched form data:", data);

                if (data.form_data) {
                    populateForm(data.form_data); // Load existing form
                } else {
                    clearForm(); // Fresh form
                    new_populateForm(data.new_form_data);
                }
            })
            .catch(error => console.error("Error fetching form data:", error));
    });

    function new_populateForm(data) {
        document.querySelector("#id_observer").value = data.observer;
        document.querySelector("#id_date").value = data.date;

        console.log("New Form populated successfully!");
    }

    function populateForm(data) {
        document.querySelector("#id_observer").value = data.observer;
        document.querySelector("#id_date").value = data.date;
        document.querySelector("#id_time").value = data.time;

        // ✅ Populate Status Checks & Comments
        for (let i = 1; i <= 6; i++) {
            let statusField = document.querySelector(`input[name="check${i}"][value="${data.inspection_json[`check${i}`]?.status}"]`);
            let commentField = document.querySelector(`#id_comments${i}`);

            if (statusField) statusField.checked = true;
            if (commentField) {
                commentField.value = data.inspection_json[`check${i}`]?.comment || "";
                commentField.style.display = (data.inspection_json[`check${i}`]?.status === "Not OK") ? "block" : "none";
                commentField.parentElement.style.border = (data.inspection_json[`check${i}`]?.status === "Not OK") ? "2px solid red" : "2px solid rgba(60, 152, 60, 0.52)";
                commentField.parentElement.style.boxShadow = (data.inspection_json[`check${i}`]?.status === "Not OK") ? "inset 0 0 4px 0px red" : "inset 0 0 4px 0px rgba(60, 152, 60, 0.52)";
            }
        }




        // ✅ Populate Waste Data (containers_json)
        let tableBody = document.querySelector("#wasteTableBody");
        tableBody.innerHTML = ""; // 🔥 Clear existing rows before populating

        if (data.containers_json) {
            let containerIndex = 0; // Index for waste rows

            Object.values(data.containers_json).forEach(waste => {
                let newRow = document.createElement("tr");
                newRow.innerHTML = `
                    <td><input type="text" name="waste_description_${containerIndex}[]" value="${waste.description}" required></td>

                    <td>
                        <div class="count-container">
                            <button type="button" class="decrement">−</button>
                            <input type="number" name="container_count_${containerIndex}[]" value="${waste.count}" min="1" required>
                            <button type="button" class="increment">+</button>
                        </div>
                    </td>

                    <td>
                        <select name="waste_code_${containerIndex}[]" required>
                            <option value="">-------</option>
                            <option value="univ" ${waste.code === "univ" ? "selected" : ""}>UNIV</option>
                            <option value="non-haz" ${waste.code === "non-haz" ? "selected" : ""}>NON-HAZ</option>
                            <option value="haz" ${waste.code === "haz" ? "selected" : ""}>HAZ</option>
                        </select>
                    </td>

                    <td>
                        <div class="date-container" name="date_container_${containerIndex}[]">
                            ${waste.dates.map(date => `
                                <div class="date-group">
                                    <input type="date" name="waste_dates_${containerIndex}[]" value="${date}" required>
                                    <button type="button" class="remove-date" title="Remove Date">✖</button>
                                </div>
                            `).join("")}
                        </div>
                        <button type="button" class="add-date">+ Add Date</button>
                    </td>

                    <td><button type="button" class="removeRow">🗑️</button></td>
                `;

                tableBody.appendChild(newRow);
                containerIndex++; // Increment index for the next waste entry
            });
        }
        document.querySelectorAll("#wasteTableBody tr").forEach(updateRowListeners);

        console.log("Form populated successfully!");
    }

    function clearForm() {
        document.querySelector("#id_observer").value = "";
        document.querySelector("#id_date").value = "";
        document.querySelector("#id_time").value = "";

        for (let i = 1; i <= 6; i++) {
            let statusFields = document.querySelectorAll(`input[name="check${i}"]`);
            statusFields.forEach(field => field.checked = false);

            let commentField = document.querySelector(`#id_comments${i}`);
            if (commentField) {
                commentField.value = "";
                commentField.style.display = "none";
                commentField.parentElement.style.border = "black 1px solid";
                commentField.parentElement.style.boxShadow = "unset";
            }
        }


        // ✅ Reset Waste Table
        let tableBody = document.querySelector("#wasteTableBody");
        tableBody.innerHTML = ""; // 🔥 Remove all rows before adding default

        // ✅ Add Default Empty Row
        let newRow = document.createElement("tr");
        newRow.innerHTML = `
            <td><input type="text" name="waste_description_0[]" required></td>

            <td>
                <div class="count-container">
                    <button type="button" class="decrement">−</button>
                    <input type="number" name="container_count_0[]" value="1" min="1" required>
                    <button type="button" class="increment">+</button>
                </div>
            </td>

            <td>
                <select name="waste_code_0[]" required>
                    <option value="">-------</option>
                    <option value="univ">UNIV</option>
                    <option value="non-haz">NON-HAZ</option>
                    <option value="haz">HAZ</option>
                </select>
            </td>

            <td>
                <div class="date-container" name="date_container_0[]">
                    <div class="date-group">
                        <input type="date" name="waste_dates_0[]" required>
                        <button type="button" class="remove-date" title="Remove Date">✖</button>
                    </div>
                </div>
                <button type="button" class="add-date">+ Add Date</button>
            </td>

            <td><button type="button" class="removeRow">🗑️</button></td>
        `;

        tableBody.appendChild(newRow); // ✅ Add the default empty row
        updateRowListeners(newRow); // ✅ Reapply event listeners

            console.log("Form reset to default!");
    }

    function updateRowListeners(row) {
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
    
        row.querySelector(".removeRow").addEventListener("click", function() {
            row.remove();
        });
    
        row.querySelector(".add-date").addEventListener("click", function() {
            let dateContainer = this.previousElementSibling;
            let counter = dateContainer.getAttribute("name").replace("date_container_", "").replace("[]", "");
            let dateGroup = document.createElement("div");
            dateGroup.classList.add("date-group");
    
            dateGroup.innerHTML = `
                <input type="date" name="waste_dates_${counter}[]" required>
                <button type="button" class="remove-date" title="Remove Date">✖</button>
            `;
    
            dateContainer.appendChild(dateGroup);
        });
    
        row.addEventListener("click", function(event) {
            if (event.target.classList.contains("remove-date")) {
                event.target.closest(".date-group").remove();
            }
        });
    }
});

document.addEventListener("DOMContentLoaded", function() {
    let areaSelect = document.querySelector("#id_area_name");

    // 🔥 Fetch submitted areas from Django
    fetch("/get-submitted-areas/")
        .then(response => response.json())
        .then(data => {
            console.log("Submitted Areas:", data.submitted_areas);

            // 🔥 Loop through all options in the dropdown
            document.querySelectorAll("#id_area_name option").forEach(option => {
                if (data.submitted_areas.includes(option.value)) {
                    option.setAttribute("data-submitted", "true"); // Mark as submitted
                }
            });

            // 🔥 Apply styles after marking submitted areas
            styleDropdownOptions();
        })
        .catch(error => console.error("Error fetching submitted areas:", error));

    function styleDropdownOptions() {
        document.querySelectorAll("#id_area_name option").forEach(option => {
            if (option.getAttribute("data-submitted") === "true") {
                option.style.backgroundColor = "#d4edda"; // ✅ Light green background
                option.style.fontWeight = "bold"; // ✅ Make text bold
                option.textContent = `✔ ${option.textContent.trim()}`; // ✅ Add checkmark
            }
        });
    }
});
