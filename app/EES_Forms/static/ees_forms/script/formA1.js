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
        
        
        //document.getElementById('total_seconds').placeholder = summedTime;
        // if (totalTime) {
        //     if (parseFloat(summedTime) == parseFloat(totalTime)) {
        //         document.getElementById("total_seconds").style.backgroundColor = "#3c983c85";
        //     } else {
        //         document.getElementById("total_seconds").style.backgroundColor = "#F49B9B";
        //     }
        // } else {
        //     if (summedTime == NaN) {
        //         document.getElementById('total_seconds').placeholder = '-';
        //     } else {
        //         document.getElementById('total_seconds').placeholder = summedTime;
        //     }
        //     document.getElementById("total_seconds").style.backgroundColor = "#FFFA8B";
        // }
    }
}
sumTime();

function check_oven_numb() {
    if (selector == 'form'){
        var commentIncluded = true;
        var commentList = [];
        for (let i=1; i<=4; i++) {
            var oven1 = document.getElementById("c"+ String(i) + "_no").value;
            var oven2 = document.getElementById("c"+ String(i+1) +"_no").value;
            if(!oven2 || !oven1){
                var oven2 = NaN;
                commentIncluded = false;
            }
            if (parseInt(oven1) == 84 && parseInt(oven2) == 1 || parseInt(oven1) == 85 && parseInt(oven2) == 2) {
                console.log("Check 1")
                console.log(commentIncluded)
                document.getElementById("c" + String(i+1) + "_popup_oven").style.visibility = 'hidden';
                document.getElementById("comment_skip_id" + String(i)).style.visibility = 'hidden';
            } else if (parseInt(oven2) == parseInt(oven1) + 2) {
                console.log("Check 2")
                console.log(commentIncluded)
                document.getElementById("c" + String(i+1) + "_popup_oven").style.visibility = 'hidden';
                document.getElementById("comment_skip_id" + String(i)).style.visibility = 'hidden';
            } else if (parseInt(oven1) >= parseInt(oven2)) {
                console.log("Check 3")
                console.log(commentIncluded)
                document.getElementById("c" + String(i+1) + "_popup_oven").style.visibility = 'visible';
                commentIncluded = false;
                document.getElementById("comment_skip_id" + String(i)).style.visibility = 'hidden';
            } else if (parseInt(oven2) == parseInt(oven1) + 1) {
                console.log("Check 4")
                console.log(commentIncluded)
                document.getElementById("c" + String(i+1) + "_popup_oven").style.visibility = 'visible';
                commentIncluded = false;
                document.getElementById("comment_skip_id" + String(i)).style.visibility = 'hidden';
            } else if (parseInt(oven2) > parseInt(oven1) + 2) {
                console.log("Check 5")
                document.getElementById("c" + String(i+1) + "_popup_oven").style.visibility = 'hidden';
                var commentSet = false;
                document.getElementById("comment_skip_id" + String(i)).style.visibility = 'visible';
                document.getElementById("comment_skip_id" + String(i)).innerHTML = 'Please change Oven No. for Charge Number ' + String(i+1) + ' or click here to comment below what oven(s) were skipped.';
                document.getElementById("comment_skip_id" + String(i)).onclick = function() {comment_add()};
                document.getElementById("comment_skip_id" + String(i)).dataset.inputValue1 = parseInt(oven1);
                document.getElementById("comment_skip_id" + String(i)).dataset.inputValue2 = parseInt(oven2);
                
                function comment_add() {
                    console.log("Check 5.1")
                    const inputValue1 = document.getElementById("comment_skip_id" + String(i)).dataset.inputValue1;
                    const inputValue2 = document.getElementById("comment_skip_id" + String(i)).dataset.inputValue2;
                    for (let x=parseInt(inputValue1)+2; x<parseInt(inputValue2); x+=2) {
                        document.getElementById("comments").value += ' Oven #' + String(x) + ' was skipped.'
                    }
                    commentSet = true
                    commentList.push(commentSet)
                    document.getElementById("comment_skip_id" + String(i)).style.visibility = 'hidden';
                    check_oven_numb();
                }

                function check_comments() {
                    console.log("Check 5.2")
                    const inputValue1 = document.getElementById("comment_skip_id" + String(i)).dataset.inputValue1;
                    const inputValue2 = document.getElementById("comment_skip_id" + String(i)).dataset.inputValue2;
                    var commentsInput = document.getElementById("comments").value;
                    
                    for (let x=parseInt(inputValue1)+2; x<parseInt(inputValue2); x+=2) {
                        if (commentsInput.includes('Oven #' + String(x) + ' was skipped.')) {
                            console.log("Check 5.2.1")
                            document.getElementById("comment_skip_id" + String(i)).style.visibility = 'hidden';
                            commentSet = true;
                        } else {
                            console.log("Check 5.2.2")
                            commentSet = false;
                        }
                    }
                    commentList.push(commentSet)
                }
                check_comments();
                console.log(commentIncluded)
            } else {
                document.getElementById("c" + String(i+1) + "_popup_oven").style.visibility = 'hidden';
                document.getElementById("comment_skip_id" + String(i)).style.visibility = 'hidden';
            }
        }
        console.log(commentList)
        if (commentIncluded && !commentList.includes(false)) {
            console.log("Check END.1")
            document.getElementById("submitButton").disabled = false;
        } else {
            console.log("Check END.2")
            document.getElementById("submitButton").disabled = true;
        }
    }
}
check_oven_numb();

// function equal_start_stop() {
//     const start = document.getElementById('main_start').value;
//     const ovenStart = document.getElementById('c1_start').value;
//     const stop = document.getElementById('c5_stop').value;
//     const ovenSop = document.getElementById('c5_stop').value;
    
//     if (start) {
//         document.getElementById('c1_start').placeholder = start;
//         document.getElementById('c1_start').style.backgroundColor = '#F49B9B';
//     } else if (ovenStart) {
//         document.getElementById('c1_start').placeholder = start;
//     }
    
    
//     document.getElementById('main_stop').value = stop;
// }
// document.getElementById("c1_no").addEventListener("load", check_oven_numb());