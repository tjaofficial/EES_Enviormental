openInformation = (ele) => {
    const childElem = ele.parentElement.children[1];
    const elemID = ele.id;
    console.log(elemID)
    if (elemID == 'account') {
        var heightChange = '186px';
    } else if (elemID == 'company') {
        var heightChange = '162px';
    } else {
        var heightChange = '300px';
    }
    console.log(childElem.style.height)
    if (childElem.style.height == heightChange){
        childElem.style.height = '0px';
    } else {
        childElem.style.height = heightChange;
    }
}