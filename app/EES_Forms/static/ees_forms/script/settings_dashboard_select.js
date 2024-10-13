function changeOptions(elem){
    const dashDict = JSON.parse(elem.dataset.dashops.replaceAll("'",'"'))
    for (const key in dashDict) {
        if (key == elem.value){
            document.getElementById(key+"Cont").style.display = "block";
        } else {
            document.getElementById(key+"Cont").style.display = "none";
        }
    }
}
changeOptions(document.getElementById('dashSelect'));