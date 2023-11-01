headerDropDown = (item) => {
    let profileMenu = document.getElementById('profileDropdown');
    let notificationMenu = document.getElementById('notifDropdown');
    if (item.id == 'notifDropdown'){
        if (notificationMenu.style.display == 'none') {
            notificationMenu.style.display = 'block';
            profileMenu.style.display = 'none';
        } else {
            notificationMenu.style.display = 'none';
        }
    } else {
        if (profileMenu.style.display == 'none') {
            profileMenu.style.display = 'block';
            notificationMenu.style.display = 'none';
        } else {
            profileMenu.style.display = 'none';
        }
    }
}

changeOtherInput = (initialInput) => {
    if (document.getElementById(initialInput.id).checked == true){
        document.getElementById('switchInput').value = 'dark';
    } else {
        document.getElementById('switchInput').value = 'light';
    }
}