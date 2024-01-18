function hoverdiv(e){
    const divtoshow = document.getElementById('hoverModal');
    var left  = e.clientX  + "px";
    var top  = e.clientY  + "px";

    var div = divtoshow;

    div.style.left = left;
    div.style.top = top;

    $("#"+divtoshow.id).toggle();
    return false;
}

changeColor = (elem) => {
    if (elem.value == ''){
        elem.style.color = 'gray';
    } else {
        elem.style.color = 'black';
    }
}
