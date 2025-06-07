document.addEventListener("DOMContentLoaded", function () {
    document.querySelector(".closeAdd").addEventListener("click", function (){
        document.querySelector("#selected-side").style.display = "none";
        document.querySelector("#main-side").style.display = "block";
    })
});