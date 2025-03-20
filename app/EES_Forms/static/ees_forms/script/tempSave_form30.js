let previousArea = null;
const fsIDData = JSON.parse(document.getElementById("fsID_json").textContent);
//console.log(fsIDData)

document.addEventListener("DOMContentLoaded", function () {
    const formName = document.getElementById("formName").dataset.form;
    const tempSaveKey = formName + "_tempFormData";
    const currentDate = Date.now();
    const areaSelect = document.getElementById("id_area_name"); // Area dropdown
    let setPreviousArea = "on"
    //console.log(areaSelect.value)
    let fsIDInput = document.querySelector("#fsID");
    
    clearStorage(tempSaveKey, currentDate);
    inputEventListener();
    loadAreaData(tempSaveKey); // Load data for the selected area
    
    previousArea = areaSelect ? areaSelect.value : null;

    function repeatFunc () {
        console.log("CHECK 17")
        if (previousArea) {
            saveCurrentArea(tempSaveKey, previousArea);
        }

        previousArea = this.value;
        
        if (!previousArea){
            document.querySelectorAll(".waste-table")[0].style.display = "none";
            document.querySelectorAll(".status-section")[0].style.display = "none";
            document.getElementById("addRow").style.display = "none";
        } else {
            document.querySelectorAll(".waste-table")[0].style.display = "table";
            document.querySelectorAll(".status-section")[0].style.display = "block";
            document.getElementById("addRow").style.display = "block";
        }
        loadAreaData(tempSaveKey); // Load the new area's data

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
    }
    /*** 🟢 Listen for area changes and load respective data ***/
    if (areaSelect) {
        areaSelect.addEventListener("change", repeatFunc);
    }
});

/*** 🟢 Attach event listeners to all inputs ***/
function inputEventListener() {
    document.querySelectorAll("input, select, textarea").forEach((elem) => {
        if (elem.id) {
            elem.addEventListener("input", saveToLocal);
        }
    });
}

/*** 🟢 Save input values dynamically to localStorage ***/
function saveToLocal(event) {
    const formName = document.getElementById("formName").dataset.form;
    const tempSaveKey = formName + "_tempFormData";
    const areaSelect = document.getElementById("id_area_name");
    const areaName = areaSelect ? areaSelect.value : "default_area";

    if (!areaName) return; // Stop if no area is selected

    const currentData = JSON.parse(localStorage.getItem(tempSaveKey)) || { Experation: Date.now(), data: {} };

    // Ensure area key exists
    if (!currentData.data[areaName]) {
        currentData.data[areaName] = { containers: [], checks: {} };
    }

    const elem = event.target;
    const elemID = elem.id.replace(/_\d+$/, ""); // Remove radio input suffix (_0, _1, _2)

    // Handle radio buttons
    if (elem.type === "radio") {
        currentData.data[areaName].checks[elem.name] = elem.value;
    } 
    // Handle textareas, selects, other inputs
    else if (elem.tagName === "TEXTAREA"){
        currentData.data[areaName].checks[elemID] = elem.value;
    } else if (elem.tagName === "INPUT" || elem.tagName === "SELECT"){
        currentData.data[elemID]= elem.value;
    }
    //|| elem.tagName === "INPUT" || elem.tagName === "SELECT") {
    localStorage.setItem(tempSaveKey, JSON.stringify(currentData));
}

/*** 🟢 Save data for the current area before switching ***/
function saveCurrentArea(tempSaveKey, areaName) {
    if (!areaName) return;

    let currentData = JSON.parse(localStorage.getItem(tempSaveKey)) || { Experation: Date.now(), data: {} };

    if (!currentData.data[areaName]) {
        currentData.data[areaName] = { containers: [], checks: {} };
    }

    // Capture container data dynamically
    currentData.data[areaName].containers = [];
    document.querySelectorAll("#wasteTableBody tr").forEach((row, index) => {
        let descriptionInput = row.querySelector(`input[name^='waste_description']`);
        let countInput = row.querySelector(`input[name^='container_count']`);
        let wasteCodeSelect = row.querySelector(`select[name^='waste_code']`);

        if (!descriptionInput || !countInput || !wasteCodeSelect) return; // Skip if missing

        let containerData = {
            description: descriptionInput.value,
            count: countInput.value,
            waste_code: wasteCodeSelect.value,
            dates: []
        };

        // ✅ Collect all waste_dates inputs
        row.querySelectorAll(`input[name^='waste_dates']`).forEach(dateInput => {
            if (dateInput.value) {
                containerData.dates.push(dateInput.value);
            }
        });

        // Debugging
        console.log(`Saved container ${index + 1}:`, containerData);

        currentData.data[areaName].containers.push(containerData);
    });

    // ✅ Save to localStorage
    localStorage.setItem(tempSaveKey, JSON.stringify(currentData));

    //console.log("Stored Data for", areaName, ":", localStorage.getItem(tempSaveKey));
}

/*** 🟢 Load form data for selected area ***/
function loadAreaData(tempSaveKey) {
    console.log("CHECK 18")
    const areaSelect = document.getElementById("id_area_name");
    const areaName = areaSelect ? areaSelect.value : "default_area";
    const formTempData = JSON.parse(localStorage.getItem(tempSaveKey)) || { Experation: Date.now(), data: {} };

    if (!formTempData.data[areaName]) return; // No data for this area

    // Load check inputs
    for (const [key, value] of Object.entries(formTempData.data[areaName].checks || {})) {
        let elem = document.querySelector(`[name='${key}']`);
        if (elem) {
            if (elem.type === "radio") {
                document.querySelector(`[name='${key}'][value='${value}']`).checked = true;
            } else {
                console.log(elem)
                elem.value = value;
            }
        }
    }

    // Load waste containers
    let wasteTableBody = document.getElementById("wasteTableBody");
    wasteTableBody.innerHTML = ""; // Clear existing rows
    console.log("CHECK 19");

    (formTempData.data[areaName].containers || []).forEach((container, index) => {
        let row = document.createElement("tr");
        let cell = document.createElement("td");
        let selectElement = document.createElement("select");
        selectElement.name = `waste_description_${index}[]`;
        selectElement.required = true;
        selectElement.id = `waste_description_${index}`;
        let option1 = document.createElement("option");
        option1.value = "";
        option1.text = "Select Category";
        selectElement.appendChild(option1);
        for(const key in fsIDData){
            if (key.slice(0,3) == "cat"){
                var newOption = document.createElement("option");
                newOption.value = fsIDData[key];
                newOption.text = fsIDData[key];
                selectElement.appendChild(newOption);
            }
        }
        cell.appendChild(selectElement);
        row.appendChild(cell);
        row.innerHTML += `
            <td>
                <div class="count-container">
                    <button type="button" class="decrement">−</button>
                    <input type="number" name="container_count_${index}" value="${container.count}" min="1" required>
                    <button type="button" class="increment">+</button>
                </div>
            </td>
            <td>
                <select name="waste_code_${index}" required>
                    <option value="">-------</option>
                    <option value="empty" ${container.waste_code === "empty" ? "selected" : ""}>EMPTY</option>
                    <option value="univ" ${container.waste_code === "univ" ? "selected" : ""}>UNIV</option>
                    <option value="non-haz" ${container.waste_code === "non-haz" ? "selected" : ""}>NON-HAZ</option>
                    <option value="haz" ${container.waste_code === "haz" ? "selected" : ""}>HAZ</option>
                </select>
            </td>
        `
        row.innerHTML += `
            <td>
                <div class="date-container" name="date_container_${index}[]">
                ${container.dates.length > 0 ? container.dates.map(date => date != "false" ? `
                            <div class="date-group">
                                <input type="date" name="waste_dates_${index}[]" value="${date}" required>
                                <button type="button" class="remove-date" title="Remove Date">✖</button>
                            </div>
                        ` : `
                            <div class="date-group">
                                <div style="width: 100%;">No Date</div>
                                <input type="hidden" name="waste_dates_${index}[]" value="" required>
                            </div>
                        `
                    ).join("")
                        : `
                            <div class="date-group">
                                <div style="width: 100%;">No Date</div>
                                <input type="hidden" name="waste_dates_${index}[]" value="" required>
                            </div>
                        `
                }
                </div>
                <button type="button" class="add-date">+ Add Date</button>
            </td>
            
            <td><button type="button" class="removeRow">🗑️</button></td>
        `;
        wasteTableBody.appendChild(row);
        document.getElementById(`waste_description_${index}`).value = waste.description;
    });
}

/*** 🟢 Clear storage when expired ***/
function clearStorage(tempSaveKey, currentDate) {
    const formattedCurrentDate = new Date(currentDate);
    const formTempData = localStorage.getItem(tempSaveKey);
    if (formTempData) {
        const parsedExpiration = JSON.parse(formTempData).Experation;
        const expDate = new Date(parsedExpiration);
        if (
            formattedCurrentDate.getMonth() !== expDate.getMonth() ||
            formattedCurrentDate.getDate() !== expDate.getDate() ||
            formattedCurrentDate.getFullYear() !== expDate.getFullYear()
        ) {
            localStorage.removeItem(tempSaveKey);
        }
    }
}

function new_populateForm(data) {
    document.querySelector("#id_observer").value = data.observer;
    document.querySelector("#id_date").value = data.date;
    const sort_dict = {"OK": 0, "N/A": 1, "Not OK": 2}
    const formName = document.getElementById("formName").dataset.form;
    const tempSaveKey = formName + "_tempFormData";
    const areaSelect = document.getElementById("id_area_name");
    const areaName = areaSelect ? areaSelect.value : "default_area";
    const currentData = JSON.parse(localStorage.getItem(tempSaveKey))
    if (currentData.data[areaName]) {
        const checkData = currentData.data[areaName]['checks']
        for(const checkID in checkData){
            if (checkData.hasOwnProperty(checkID) && checkID != "id_area_name") {
                const checkValue = checkData[checkID];
                if (checkID.slice(0,5) == "check"){
                    document.querySelector(`#id_${checkID}_${sort_dict[checkValue]}`).checked = true;
                    if (sort_dict[checkValue] == 2){
                        document.querySelector(`#id_${checkID}_${sort_dict[checkValue]}`).parentElement.parentElement.parentElement.parentElement.parentElement.classList.add("active");
                    }
                } else if (checkID.slice(0,11) == "id_comments"){
                    const commentField2 = document.querySelector(`#${checkID}`)
                    if (checkValue){
                        commentField2.value = checkValue;
                        commentField2.style.display = "block"; // ✅ Show comment field if "Not OK" is already selected
                        commentField2.disabled = false;
                        commentField2.style.background = "white";
                        commentField2.style.cursor = "text";
                        commentField2.parentElement.style.border = "2px solid red";
                        commentField2.parentElement.style.boxShadow = "inset 0 0 4px 0px red";
                    } else{
                        console.log("Nope didnt wokr")
                    }
                }
            }
        }
    }
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
    console.log("CHECK 8")
    if (!("noContainers" in data.containers_json)) {
        let containerIndex = 0; // Index for waste rows

        Object.values(data.containers_json).forEach(waste => {
            let newRow = document.createElement("tr");
            let newCell = document.createElement("td");
            let selectElement = document.createElement("select");
            selectElement.name = `waste_description_${containerIndex}[]`;
            selectElement.required = true;
            selectElement.id = `waste_description_${containerIndex}`;
            let option1 = document.createElement("option");
            option1.value = "";
            option1.text = "Select Category";
            selectElement.appendChild(option1);
            for(const key in fsIDData){
                if (key.slice(0,3) == "cat"){
                    var newOption = document.createElement("option");
                    newOption.value = fsIDData[key];
                    newOption.text = fsIDData[key];
                    selectElement.appendChild(newOption);
                }
            }
            newCell.appendChild(selectElement);
            newRow.appendChild(newCell);
            newRow.innerHTML += `
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
                        <option value="empty" ${waste.code === "empty" ? "selected" : ""}>EMPTY</option>
                        <option value="univ" ${waste.code === "univ" ? "selected" : ""}>UNIV</option>
                        <option value="non-haz" ${waste.code === "non-haz" ? "selected" : ""}>NON-HAZ</option>
                        <option value="haz" ${waste.code === "haz" ? "selected" : ""}>HAZ</option>
                    </select>
                </td>
            `;
            //console.log(waste.dates)
            newRow.innerHTML += `
                <td>
                    <div class="date-container" name="date_container_${containerIndex}[]">
                    ${waste.dates.length > 0 ? waste.dates.map(date => date != "false" ? `
                                <div class="date-group">
                                    <input type="date" name="waste_dates_${containerIndex}[]" value="${date}" required>
                                    <button type="button" class="remove-date" title="Remove Date">✖</button>
                                </div>
                            ` : `
                                <div class="date-group">
                                    <div style="width: 100%;">No Date</div>
                                    <input type="hidden" name="waste_dates_${containerIndex}[]" value="" required>
                                </div>
                            `
                        ).join("")
                            : `
                                <div class="date-group">
                                    <div style="width: 100%;">No Date</div>
                                    <input type="hidden" name="waste_dates_${containerIndex}[]" value="" required>
                                </div>
                            `
                    }
                    </div>
                    <button type="button" class="add-date">+ Add Date</button>
                </td>
                
                <td><button type="button" class="removeRow">🗑️</button></td>
            `;
            tableBody.appendChild(newRow);
            document.getElementById(`waste_description_${containerIndex}`).value = waste.description;
            containerIndex++; // Increment index for the next waste entry
        });
        document.querySelectorAll("#wasteTableBody tr").forEach(updateRowListeners);
    } else {
        console.log("CHECK 9")
        let newRow = document.createElement("tr");
        newRow.innerHTML = `
                <td colspan=5>
                    <div>No Containers</div>
                    <input type="hidden" name="noContainers" value="true">
                </td>
            `
        tableBody.appendChild(newRow);
    }

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
                <option value="empty">EMPTY</option>
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
        if (document.querySelectorAll("#wasteTableBody tr").length == 1){
            row.innerHTML = `
                <td colspan=5>
                    <div>No Containers</div>
                    <input type="hidden" name="noContainers" value="true">
                </td>
            `
        } else {
            row.remove();
        }
    });

    row.querySelector(".add-date").addEventListener("click", function() {
        let dateContainer = this.previousElementSibling;
        //console.log(dateContainer)
        let counter = dateContainer.getAttribute("name").replace("date_container_", "").replace("[]", "");
        let dateGroup = document.createElement("div");
        dateGroup.classList.add("date-group");
        dateGroup.innerHTML = `
            <input type="date" name="waste_dates_${counter}[]" required>
            <button type="button" class="remove-date" title="Remove Date">✖</button>
        `;
        //console.log(dateContainer.children.length)
        //console.log(dateContainer.children[0].children[0].innerHTML)
        //console.log(dateContainer.children[0])
        if (dateContainer.children.length == 1 && dateContainer.children[0].children[0].innerHTML.trim() == "No Date"){
            dateContainer.removeChild(dateContainer.children[0]);
            dateContainer.appendChild(dateGroup);
        } else {
            console.log("check45")
            dateContainer.appendChild(dateGroup);
        }

    });

    row.addEventListener("click", function(event) {
        if (event.target.classList.contains("remove-date")) {
            let dateContainer = this.children[3].children[0];
            console.log(dateContainer)
            let counter = dateContainer.getAttribute("name").replace("date_container_", "").replace("[]", "");
            let dateGroup = document.createElement("div");
            dateGroup.classList.add("date-group");
            dateGroup.innerHTML = `
                <div style="width: 100%;">
                    No Date
                </div>
                <input type="hidden" name="waste_dates_${counter}[]" value="${false}" required>
            `;
            event.target.closest(".date-group").remove();
            console.log(dateContainer.children.length)
            if (dateContainer.children.length == 0){
                dateContainer.appendChild(dateGroup);
            }
        }
    });
}

/*** 🟢 ADD NEW ROW ***/
document.getElementById("addRow").addEventListener("click", function() {
    let tableBody = document.getElementById("wasteTableBody");
    if (tableBody.children.length == 1 && tableBody.firstElementChild.firstElementChild.firstElementChild.innerHTML.trim() == "No Containers"){
        tableBody.innerHTML = "";
    }
    let rowCount = tableBody.getElementsByTagName("tr").length;
    
    let newRow = document.createElement("tr");
    let newCell = document.createElement("td");
    let selectElement = document.createElement("select");
    selectElement.name = `waste_description_${rowCount}[]`;
    selectElement.required = true;
    selectElement.id = `waste_description_${rowCount}`;
    let option1 = document.createElement("option");
    option1.value = "";
    option1.text = "Select Category";
    selectElement.appendChild(option1);
    for(const key in fsIDData){
        if (key.slice(0,3) == "cat"){
            var newOption = document.createElement("option");
            newOption.value = fsIDData[key];
            newOption.text = fsIDData[key];
            selectElement.appendChild(newOption);
        }
    }
    newCell.appendChild(selectElement);
    newRow.appendChild(newCell);
    newRow.innerHTML += `
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
                <option value="empty">EMPTY</option>
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