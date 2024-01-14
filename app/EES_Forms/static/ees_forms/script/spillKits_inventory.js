
function selectType(){
    const selector = document.getElementById("selector").dataset.selector;
    if (selector == "form" || selector == "edit") {
        var skType = document.getElementById("skType").value;
    } else {
        var skType = document.getElementById("skTypeDiv").firstChild.nodeValue;
    }
    console.log(skType);
     if (skType == "universal drum"){
        document.getElementById("table2").style.visibility = "visible";
        document.getElementById("table1").style.visibility = "collapse";
        if (selector == "form" || selector == "edit") {
            document.getElementById("submitHere").style.visibility = "visible";

            document.getElementById("t2count1").placeholder = 16;
            document.getElementById("t2count2").placeholder = 10;
            document.getElementById("t2count3").placeholder = 60;
            document.getElementById("t2count4").placeholder = 8;
            document.getElementById("t2count5").placeholder = 56;
            document.getElementById("t2count6").placeholder = 10;
            document.getElementById("t2count7").placeholder = 1;
            document.getElementById("t2count8").placeholder = 1;
            document.getElementById("t2count9").placeholder = 6;
        }
    } else if (skType == "oil XL cart"){
        document.getElementById("table1").style.visibility = "visible";
        document.getElementById("table2").style.visibility = "collapse";
        if (selector == "form" || selector == "edit") {
            document.getElementById("submitHere").style.visibility = "visible";

            document.getElementById("t1count1").placeholder = 2;
            document.getElementById("t1count2").placeholder = 3;
            document.getElementById("t1count3").placeholder = 15;
            document.getElementById("t1count4").placeholder = 6;
            document.getElementById("t1count5").placeholder = 150;
            document.getElementById("t1count6").placeholder = 2;
            document.getElementById("t1count7").placeholder = 30;
            document.getElementById("t1count8").placeholder = 1;
            document.getElementById("t1count9").placeholder = 1;
            document.getElementById("t1count10").placeholder = 6;
        }
        
    } else {
        if (selector == "form" || selector == "edit") {
            document.getElementById("table1").style.visibility = "collapse";
            document.getElementById("table2").style.visibility = "collapse";
            document.getElementById("submitHere").style.visibility = "collapse";
        }
     }
}
selectType();
function t1mathItems(){
    for (let i=1; i<=10; i++){
        const theCount = document.getElementById("t1count" + String(i)).value;
        const theActual = document.getElementById("t1count" + String(i)).placeholder;
        if (theCount) {
            document.getElementById("t1miss" + String(i)).value = theActual - theCount;
        } else {
            document.getElementById("t1miss" + String(i)).value = null;
        }
    }
}

function t2mathItems(){
    for (let i=1; i<=9; i++){
        const theCount = document.getElementById("t2count" + String(i)).value;
        const theActual = document.getElementById("t2count" + String(i)).placeholder;
        if (theCount) {
            document.getElementById("t2miss" + String(i)).value = theActual - theCount;
        } else {
            document.getElementById("t2miss" + String(i)).value = null;
        }
    }
}

if (selector == "form") {
    t1mathItems();
    t2mathItems();
}