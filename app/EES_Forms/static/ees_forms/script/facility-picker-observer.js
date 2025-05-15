document.addEventListener("DOMContentLoaded", function () {
    const redirectUrl = document.getElementById('redirectInfo').dataset.redirectUrl;


    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    const form = document.querySelector("#obs_facility_picker");
    const select = form.querySelector("select");
    console.log(select)
    document.getElementById("submitBtn").addEventListener("click", function () {
        const selectedFacilityID = select.value;
        fetch("/set-facility/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie('csrftoken')
            },
            body: JSON.stringify({ id: selectedFacilityID })
        }).then(() => {
            window.location.href = redirectUrl;
        });
    });
});
