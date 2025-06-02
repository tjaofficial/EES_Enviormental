document.addEventListener("DOMContentLoaded", function () {
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
    //console.log(select)
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
            return fetch("/check-bat-profile/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie('csrftoken')
                },
                body: JSON.stringify({
                    facility_id: selectedFacilityID,
                    date: new Date().toISOString().split("T")[0]
                })
            });
        })
        .then(response => response.json())
        .then(data => {
            //console.log("Check result:", data);
            if (data.exists) {
                window.location.href = redirectUrl;
            } else {
                //alert("No bat profile found for today. Redirecting to create one.");
                const todays_date = new Date().toISOString().split("T")[0];
                window.location.href = `../daily_battery_profile/edit/${todays_date}`;
            }
        })
        .catch(error => {
            console.error("Something went wrong:", error);
        });
    });
});
