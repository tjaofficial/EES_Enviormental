const notifNumbElem = document.getElementById('alertNotif');
const notifNumb = notifNumbElem.innerText;
const yellowDot = document.getElementById('yellowDot')

if (notifNumb == 0){
    yellowDot.style.display = 'none';
    document.getElementById('notifDropdown').style.display = 'none';
}