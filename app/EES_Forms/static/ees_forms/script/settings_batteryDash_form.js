function showSubCats(){
    const progress = document.getElementById('progressBar'),
    graphs = document.getElementById('graphsTile');
    if (progress.checked){
        document.getElementById('progress').style.display = 'block';
    } else {
        document.getElementById('progress').style.display = 'none';
    }

    if (graphs.checked){
        document.getElementById('graphs').style.display = 'block';
    } else {
        document.getElementById('progress').style.display = 'none';
    }
}
showSubCats();

const progOptions = ['progressDaily', 'progressWeekly', 'progressMonthly', 'progressQuarterly', 'progressAnnually']
function initital_count(){
    i=0
    for (let x=0; x < progOptions.length; x++) {
        const option = progOptions[x]
        const selObject = document.getElementById(option)
        if (selObject.checked){
            i++;
        }
    }
    console.log(i)
    document.getElementById('progress').dataset.count = i;
}
initital_count();

function stopAtFour(elem){
    const counter = document.getElementById('progress').dataset.count;
    if (elem){
        var newCount = Number(counter)+1
    } else {
        var newCount = Number(counter)-1
    }
    document.getElementById('progress').dataset.count = newCount;
    console.log(newCount);
    if (newCount == 4) {
        disableInput(true);
    } else if (newCount == 3) {
        disableInput(false);
    }
}

function disableInput(disable){
    const progOptions = ['progressDaily', 'progressWeekly', 'progressMonthly', 'progressQuarterly', 'progressAnnually']
    for (let x=0; x < progOptions.length; x++) {
        const option = progOptions[x]
        const selObject = document.getElementById(option)
        if (!selObject.checked) {
            selObject.disabled = disable;
            var label = selObject.parentNode
            if (disable){
                label.style.color = 'gray';
                label.style.textDecoration = 'line-through';
            } else {
                label.style.color = 'black';
                label.style.textDecoration = 'none';
            }
        }
    }
}

