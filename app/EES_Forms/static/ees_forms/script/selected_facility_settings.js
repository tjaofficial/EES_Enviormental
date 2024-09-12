function openSubCategory(elem){
    const subSelector = elem.dataset.subcat;
    const subDiv = document.getElementById(subSelector);
    console.log(subSelector)
    if (elem.checked == true){
        subDiv.style.display = "block";
    } else {
        subDiv.style.display = "none";
    }
}
function showGraphDates(elem){
    const subSelector = elem.dataset.subcat;
    const subDiv = document.getElementById(subSelector);
    if (elem.value == "dates"){
        subDiv.style.display = "block";
    } else {
        subDiv.style.display = "none";
    }
}














