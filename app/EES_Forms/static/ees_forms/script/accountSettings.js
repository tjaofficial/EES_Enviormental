openInformation = (ele) => {
    const childElem = ele.parentElement.children[1];
    const elemID = ele.id;
    console.log(elemID)
    var heightChange = 'fit-content';
    console.log(childElem.style.height)
    if (childElem.style.height == heightChange){
        childElem.style.height = '0px';
        childElem.style.padding = 'unset';
    } else {
        childElem.style.height = heightChange;
        childElem.style.padding = '20px 0px';
    }
}

seeEmployees = () => {
    const seeAll = document.getElementById('seeAll');
    const employees = document.getElementById('employeesCont');
    if(seeAll.innerText == "see all"){
        employees.style.display = 'table-row';
        seeAll.innerText = 'see less';
    } else {
        employees.style.display = 'none';
        seeAll.innerText = 'see all';
    }
}