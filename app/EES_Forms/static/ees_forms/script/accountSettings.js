function localDataSetup() {
    var tabsDict = {
        "account": "open",
        "company": "open",
        "subscription": "open",
        "facility2": "open",
    }
    let localStore = localStorage.getItem("sup_account")
    if (!localStore){
        localStorage.setItem("sup_account", JSON.stringify(tabsDict))
        // console.log(JSON.parse(localStorage.getItem("sup_account")))
    }
    localStore = JSON.parse(localStorage.getItem("sup_account"))
    return localStore
}
openInformation = (ele) => {
    const childElem = ele.parentElement.children[1];
    const elemID = ele.id;
    console.log(elemID)
    var heightChange = 'fit-content';
    console.log(childElem.style.height)
    let localStore = localDataSetup();
    if (childElem.style.height == heightChange){
        console.log("close")
        localStore[elemID] = "close";
        localStorage.setItem("sup_account", JSON.stringify(localStore))
        childElem.style.height = '0px';
        childElem.style.padding = 'unset';
    } else {
        console.log("open")
        localStore[elemID] = "open";
        localStorage.setItem("sup_account", JSON.stringify(localStore))
        childElem.style.height = heightChange;
        childElem.style.padding = '20px 0px';
    }
}
function initial_tabs() {
    let localStore = localDataSetup();
    for (x in localStore) {
        var tabID = x;
        var stateOf = localStore[x];
        console.log(tabID)
        let elem = document.getElementById(tabID)
        let chilElem = elem.parentElement.children[1];
        if (stateOf == "close"){
            chilElem.style.height = '0px';
            chilElem.style.padding = 'unset';
        } else if (stateOf == "open") {
            chilElem.style.height = 'fit-content';
            chilElem.style.padding = '20px 0px';
        }
    }
}
initial_tabs();
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