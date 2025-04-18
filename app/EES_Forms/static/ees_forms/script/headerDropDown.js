console.log("✅ headerDropDown.js loaded");
document.addEventListener("DOMContentLoaded", function () {
    document.querySelector(".notification").addEventListener("click", function () {
        headerDropDown(document.getElementById("notifDropdown"));
    });
});

var modalHeaderDrop = document.getElementById('addModalHeaderDrop');
var profileMenu = document.getElementById('profileDropdown');
var notificationMenu = document.getElementById('notifDropdown');

window.addEventListener('click', closeModel);

function closeModel(event) {
    if (event.target == modalHeaderDrop) {
        modalHeaderDrop.style.display = "none";
        profileMenu.style.display = "none";
        notificationMenu.style.display = "none";
    }
}

function headerDropDown(item) {
    if (!item) return;
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
    if (!initialInput) return;
    if (document.getElementById(initialInput.id).checked == true){
        document.getElementById('switchInput').value = 'dark';
    } else {
        document.getElementById('switchInput').value = 'light';
    }
}


