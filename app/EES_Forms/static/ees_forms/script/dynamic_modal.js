var spanAdd = document.getElementsByClassName("closeAdd")[0];
var modalAdd = document.getElementById("addModal");

spanAdd.onclick = function() {
    modalAdd.style.display = "none";
}

triggerButton = (elem) => {
    modalAdd.style.display = "block";
    window.addEventListener('click', (e) => {
        if (e.target == modalAdd) {
            modalAdd.style.display = 'none';
        }
    });
}