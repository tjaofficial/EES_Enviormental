console.log("🍕 JS script loaded");
console.log("headerDropDown in global?", typeof headerDropDown);

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

document.getElementById('facility-picker').addEventListener('change', function () {
    console.log("CHicken")
    const selectedFacilityID = this.value;
    fetch("/set-facility/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie('csrftoken')
        },
        body: JSON.stringify({ id: selectedFacilityID })
    }).then(() => {
        location.reload(); // Refresh page to reflect facility change
    });
});