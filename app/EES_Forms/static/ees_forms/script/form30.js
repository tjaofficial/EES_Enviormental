document.addEventListener("DOMContentLoaded", function() {
    let area_name_check = document.getElementsByName("area_name")[0];
    if (!area_name_check.value){
        document.querySelectorAll(".waste-table")[0].style.display = "none";
        document.querySelectorAll(".status-section")[0].style.display = "none";
        document.getElementById("addRow").style.display = "none";
    }
    /*** 🟢 Ensure comments initialize correctly based on selected radio ***/
    document.querySelectorAll(".status-item").forEach(item => {
        let radios = item.querySelectorAll(".status-radio");
        let commentField = item.querySelector(".status-comment");
    
        let isNotOkSelected = false;
        let empty = false;

        radios.forEach(radio => {
            if (radio.checked){
                if (radio.value === "Not OK") {
                    isNotOkSelected = true;
                }
            } else {
                empty = true;
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
        } else if (!isNotOkSelected && !empty) {
            commentField.style.display = "none"; // ✅ Only hide if NOT "Not OK"
            commentField.disabled = true;
            commentField.style.background = "#f5f5f5";
            commentField.style.cursor = "not-allowed";
            commentField.parentElement.style.border = "2px solid rgba(60, 152, 60, 0.52)";
            commentField.parentElement.style.boxShadow = "inset 0 0 4px 0px rgba(60, 152, 60, 0.52)";
            //console.log("Changed background to gray for:", commentField); // 🔥 Debugging
        } else {
            commentField.style.display = "none"; // ✅ Only hide if NOT "Not OK"
            commentField.disabled = true;
            commentField.style.background = "#f5f5f5";
            commentField.style.cursor = "not-allowed";
            commentField.parentElement.style.border = "1px solid black";
            commentField.parentElement.style.boxShadow = "unset";
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
        let optionLength = document.querySelectorAll("#id_area_name option").length
        let optionCount = 0
        document.querySelectorAll("#id_area_name option").forEach(option => {
            if (option.getAttribute("data-submitted") === "true") {
                option.style.backgroundColor = "#d4edda"; // ✅ Light green background
                option.style.fontWeight = "bold"; // ✅ Make text bold
                option.textContent = `✔ ${option.textContent.trim()}`; // ✅ Add checkmark
                optionCount ++;
            }
        });
        let areaInput = document.getElementById("id_area_name");
        if (optionCount == (optionLength - 1)){
            //console.log("finsihed")
            areaInput.style.border = "2px solid rgba(60, 152, 60, 0.52)";
            areaInput.style.boxShadow = "inset 0 0 4px 0px rgba(60, 152, 60, 0.52)";
            document.querySelectorAll("#id_area_name option")[0].innerHTML = "All Areas Completed"
        } else {
            areaInput.style.border = "1px solid black";
            areaInput.style.boxShadow = "unset";
            document.querySelectorAll("#id_area_name option")[0].innerHTML = "Select Area"
        }
    }
});
