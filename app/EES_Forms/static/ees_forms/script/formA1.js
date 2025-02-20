for (let x = 1; x <= 5; x++) {
    document.getElementById(`c${x}_no`).addEventListener("change", check_ovens_inop);
}

async function check_ovens_inop() {
    let ovenNumbers = [];

    // Collect all entered oven numbers
    for (let x = 1; x <= 5; x++) {
        let input = document.getElementById(`c${x}_no`);
        if (input && input.value) {
            ovenNumbers.push(input.value.trim());
        }
    }

    if (ovenNumbers.length === 0) return; // Don't fetch if no ovens are entered

    let queryParams = `/api/get-inop/`;

    try {
        let response = await fetch(queryParams);
        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }
        let inopData = await response.json();

        // Check and highlight inop ovens
        let flagged = false
        for (let x = 1; x <= 5; x++) {
            let input = document.getElementById(`c${x}_no`);
            if (input) {
                if (inopData.includes(input.value.trim())) {
                    flagged = true
                }
            }
        }
        if (flagged){
            document.getElementById("inop_ovenPopup").style.visibility = "visible";  // Flag as inop
        } else {
            document.getElementById("inop_ovenPopup").style.visibility = "hidden";  // Reset if not inop
        }
    } catch (error) {
        console.error("Error fetching inop ovens:", error);
    }
}

// Sums the times on input
const selector = document.getElementById('selector').dataset.selector;
 
function sumTime(){
    if (selector == 'form'){
        const totalTime = document.getElementById('total_seconds').value;
        const c1_sec_value  = document.getElementById('c1_sec').value;
        const c2_sec_value  = document.getElementById('c2_sec').value;
        const c3_sec_value  = document.getElementById('c3_sec').value;
        const c4_sec_value  = document.getElementById('c4_sec').value;
        const c5_sec_value  = document.getElementById('c5_sec').value;
        const emissionsList = [
            c1_sec_value,
            c2_sec_value,
            c3_sec_value,
            c4_sec_value,
            c5_sec_value
        ]
        var green = true;
        for (let x=0; x<emissionsList.length; x++) {
            if (!emissionsList[x]) {
                green = false;
                emissionsList[x] = 0;
            }
        }
        let summedTime =  parseFloat(emissionsList[0]) + parseFloat(emissionsList[1]) + parseFloat(emissionsList[2]) + parseFloat(emissionsList[3]) + parseFloat(emissionsList[4]);

        if (green) {
            document.getElementById("total_seconds").style.backgroundColor = "#3c983c85";
            document.getElementById('total_seconds').value = summedTime;
        } else {
            document.getElementById('total_seconds').value = '';
            document.getElementById("total_seconds").style.backgroundColor = "gray";
        }
    }
}
sumTime();

function check_oven_numb() {
    function isEven(number) {
        return number % 2 === 0;
    }
    if (selector == 'form') {
        let commentIncluded = true;
        let commentList = [];

        for (let i = 1; i <= 4; i++) {
            let input1 = document.getElementById(`c${i}_no`);
            let input2 = document.getElementById(`c${i + 1}_no`);
            let oven1 = input1.value.trim();
            let oven2 = input2 ? input2.value.trim() : "";
    
            if (i == 1) {
                if (oven1){
                    input1.style.border = "2px solid rgba(60, 152, 60, 0.52)";
                    input1.style.boxShadow = "inset 0 0 4px 0px rgba(60, 152, 60, 0.52)";
                } else {
                    input1.style.border = "1px solid #b0bec5";
                    input1.style.boxShadow = "unset";
                }
            }
            if (!oven1 && !oven2) {
                // Empty inputs should be neutral (gray)
                input1.style.border = "1px solid #b0bec5";
                input1.style.boxShadow = "unset";
                // document.getElementById(`c${i}_popup_oven`).style.visibility = "hidden";
                // document.getElementById(`comment_skip_id${i}`).style.visibility = "hidden";
                if (input2) {
                    input2.style.border = "1px solid #b0bec5";
                    input2.style.boxShadow = "unset";
                }
                continue;
            }

            let num1 = parseInt(oven1);
            let num2 = parseInt(oven2);

            if (isNaN(num1) || (!isNaN(num2) && isNaN(num1))) {
                if (input2) {
                    input2.style.border = "2px solid rgba(60, 152, 60, 0.52)";
                    input2.style.boxShadow = "inset 0 0 4px 0px rgba(60, 152, 60, 0.52)";
                    // document.getElementById(`c${i + 1}_popup_oven`).style.visibility = "hidden";
                    // document.getElementById(`comment_skip_id${i}`).style.visibility = "hidden";
                    input1.style.border = "1px solid #b0bec5";
                    input1.style.boxShadow = "unset";
                    // document.getElementById(`c${i}_popup_oven`).style.visibility = "hidden";
                }
                continue; // Skip if oven number is not valid
            }

            let validSequence = false;
            let skippedOvens = false;
            if (num2) {
                if ((num1 === 84 && num2 === 1) || (num1 === 85 && num2 === 2)) {
                    validSequence = true;
                } else if (num2 === num1 + 2) {
                    validSequence = true;
                } else if (num1 === 84){
                    if (!isEven(num2) && num2 !== 1){
                        validSequence = true;
                        skippedOvens = true
                    }
                } else if (num1 === 85){
                    if (isEven(num2) && num2 !== 2){
                        validSequence = true;
                        skippedOvens = true
                    }
                }
            }
            //console.log(`In this set number 1: ${num1} & number 2: ${num2}`)
            if (validSequence) {
                // console.log("valid 1")
                input2.style.border = "2px solid rgba(60, 152, 60, 0.52)";
                input2.style.boxShadow = "inset 0 0 4px 0px rgba(60, 152, 60, 0.52)";
                // document.getElementById(`c${i + 1}_popup_oven`).style.visibility = "hidden";
            } else if (num2 && num2 < num1) {
                //console.log("invalid 1")
                input2.style.border = "2px solid red";
                input2.style.boxShadow = "inset 0 0 4px 0px red";
                // document.getElementById(`c${i + 1}_popup_oven`).style.visibility = "visible";
                commentIncluded = false;
            } else if (num2 && num2 === num1 + 1) {
                //console.log("invalid 2")
                input2.style.border = "2px solid red";
                // document.getElementById(`c${i + 1}_popup_oven`).style.visibility = "visible";
                commentIncluded = false;
            } else if (num2 && num2 > num1 + 2 && (isEven(num1) && isEven(num2) || !isEven(num1) && !isEven(num2))) {
                //console.log("invalid 3")
                input2.style.border = "2px solid red";
                skippedOvens = true
            } else if (num1 && num1 === num2 + 1) {
                //console.log("invalid 4")
                input2.style.border = "2px solid red";
                // document.getElementById(`c${i + 1}_popup_oven`).style.visibility = "visible";
                commentIncluded = false;
            } else if (num1 && num2 && num1 === num2){
                //console.log("invalid 6")
                input2.style.border = "2px solid red";
                // document.getElementById(`c${i + 1}_popup_oven`).style.visibility = "visible";
                commentIncluded = false;
            } else {
                if (i>1){
                    let oven0 = document.getElementById(`c${i - 1}_no`) ? document.getElementById(`c${i - 1}_no`).value.trim() : "";
                    if (num1 && oven0 && num1 == oven0 + 1) {
                        //console.log("invalid 5")
                        input2.style.border = "2px solid red";
                        // document.getElementById(`c${i + 1}_popup_oven`).style.visibility = "visible";
                        commentIncluded = false;
                    }
                }
            }
            if (skippedOvens){
                document.getElementById(`comment_skip_id${i}`).style.visibility = "visible";
                document.getElementById(`comment_skip_id${i}`).innerHTML =
                    `Please change Oven No. for Charge Number ${i + 1} or click here to comment below what oven(s) were skipped.`;
                document.getElementById(`comment_skip_id${i}`).onclick = function () {
                    comment_add(i, num1, num2);
                };
                document.getElementById(`comment_skip_id${i}`).dataset.inputvalue1 = num1;
                document.getElementById(`comment_skip_id${i}`).dataset.inputvalue2 = num2;
                check_comments(i, num1, num2);
            } else {
                document.getElementById(`comment_skip_id${i}`).style.visibility = "hidden";
            }
        }
    }
}

function comment_add(i, num1, num2) {
    //console.log("Test 1")
    //console.log(`i: ${i}, num1: ${num1}, num2: ${num2}`)
    if (num1 === 85){
        for (let x = 2; x < num2; x += 2) {
            //console.log(`Comments were: ${document.getElementById("comments").value}`)
            document.getElementById("comments").value += ` Oven #${x} was skipped and left empty.`;
        }
    } else if (num1 === 84){
        for (let x = 1; x < num2; x += 2) {
            //console.log(`Comments were: ${document.getElementById("comments").value}`)
            document.getElementById("comments").value += ` Oven #${x} was skipped and left empty.`;
        }
    } else {
        for (let x = num1 + 2; x < num2; x += 2) {
            //console.log(`Comments were: ${document.getElementById("comments").value}`)
            document.getElementById("comments").value += ` Oven #${x} was skipped and left empty.`;
        }
    }
    document.getElementById(`comment_skip_id${i}`).style.visibility = "hidden";
    let storedData = localStorage.getItem("1_tempFormData"); 

    if (storedData) {
        let parsedData = JSON.parse(storedData); // Convert to object
        
        // Modify the "comments" field
        parsedData.data.comments = document.getElementById("comments").value; 

        // Save it back to localStorage
        localStorage.setItem("1_tempFormData", JSON.stringify(parsedData));
    }
}

function check_comments(i, num1, num2) {
    //console.log("Test 1")
    //console.log(`i: ${i}, num1: ${num1}, num2: ${num2}`)
    let commentsInput = document.getElementById("comments").value;
    //console.log(commentsInput)
    let commentSet = false;

    if (num1 === 85){
        for (let x = 2; x < num2; x += 2) {
            if (commentsInput.toLowerCase().includes(`Oven #${x} was skipped and left empty.`.toLowerCase())) {
                document.getElementById(`comment_skip_id${i}`).style.visibility = "hidden";
                commentSet = true;
            }
        }
    } else if (num1 === 84){
        for (let x = 1; x < num2; x += 2) {
            if (commentsInput.toLowerCase().includes(`Oven #${x} was skipped and left empty.`.toLowerCase())) {
                document.getElementById(`comment_skip_id${i}`).style.visibility = "hidden";
                commentSet = true;
            }
        }
    } else {
        for (let x = num1 + 2; x < num2; x += 2) {
            if (commentsInput.toLowerCase().includes(`Oven #${x} was skipped and left empty.`.toLowerCase())) {
                document.getElementById(`comment_skip_id${i}`).style.visibility = "hidden";
                commentSet = true;
            }
        }
    }
}

document.addEventListener("DOMContentLoaded", check_oven_numb);

