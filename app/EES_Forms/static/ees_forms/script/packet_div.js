show_formsList = (elem) => {
    let list = elem.parentNode.parentNode.children[1];
    if (list.style.display == 'none'){
        list.style.display = 'table';
    } else {
        list.style.display = 'none';
    }
} 