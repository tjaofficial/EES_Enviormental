const modalHeaderDrop = document.getElementById('addModalHeaderDrop');
const profileMenu = document.getElementById('profileDropdown');
const notificationMenu = document.getElementById('notifDropdown');
headerDropDown = (item) => {
    if (item.id == 'notifDropdown'){
        if (notificationMenu.style.display == 'none') {
            notificationMenu.style.display = 'block';
            modalHeaderDrop.style.display = 'block';
            profileMenu.style.display = 'none';
        } else {
            notificationMenu.style.display = 'none';
            modalHeaderDrop.style.display = 'none';
        }
    } else {
        if (profileMenu.style.display == 'none') {
            profileMenu.style.display = 'block';
            modalHeaderDrop.style.display = 'block';
            notificationMenu.style.display = 'none';
        } else {
            profileMenu.style.display = 'none';
            modalHeaderDrop.style.display = 'none';
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


window.onclick = function(event) {
    if (event.target == modalHeaderDrop) {
        modalHeaderDrop.style.display = "none";
        profileMenu.style.display = "none";
        notificationMenu.style.display = "none";
    }
}