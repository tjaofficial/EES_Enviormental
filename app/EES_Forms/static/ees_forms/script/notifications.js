const notifNumbElem = document.getElementById('alertNotif');
console.log(document.getElementById('alertNotif'))
console.log(notifNumbElem.innerText)
const notifNumb = notifNumbElem.innerText;
const yellowDot = document.getElementsByClassName('yellowDot')[0];

if (notifNumb == 0){
    yellowDot.style.display = 'none';
    document.getElementById('notifDropdown').style.display = 'none';
}