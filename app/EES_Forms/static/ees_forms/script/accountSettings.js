openInformation = (ele) => {
    const childElem = ele.parentElement.children[1];
    const elemID = ele.id;
    console.log(elemID)
    // if (elemID == 'account') {
    //     var heightChange = '186px';
    // } else if (elemID == 'company') {
    //     var heightChange = '345px';
    // } else {
    //     var heightChange = '300px';
    // }
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