document.addEventListener("DOMContentLoaded", function () {
    document.querySelector(".closeAdd").addEventListener("click", function (){
        document.querySelector("#selected-side").style.display = "none";
        document.querySelector("#main-side").style.display = "block";
    })
    
    
    
    const tdElements = document.querySelectorAll("td");
    tdElements.forEach(function (td) {
        td.addEventListener("click", function () {
            console.log(this)
            const allDayEvents = JSON.parse(this.dataset.allday);
            const otherEvents = JSON.parse(this.dataset.other);
            if (allDayEvents.length == 0 && otherEvents == 0) return;
            document.querySelector("#selected-side").style.display = "block";
            document.querySelector("#main-side").style.display = "none";
            const allDayCont = document.getElementById('all-day-cont');
            const newAllDay = document.createElement("div");
            newAllDay.id = "all-day-cont";
            newAllDay.classList.add("events-adjust")
            const otherEventsCont = document.getElementById('events-cont');
            const newOther = document.createElement("div");
            newOther.id = "events-cont";
            newOther.classList.add("events-adjust")
            console.log(allDayEvents)
            console.log(otherEvents)
            // Example: display in an alert
            allDayEvents.map((e) => {
                const tempDiv2 = document.createElement("div");
                tempDiv2.classList.add("event-block");
                tempDiv2.dataset.eventid = `${e.id}`
                tempDiv2.innerHTML = `
                    <div class="event-title">
                        ${e.title} - ${e.observer}
                    </div>
                    <div id="event-body-${e.id}" class="event-meta" style="display: none;">
                        <div><strong>Observer:</strong> ${e.observer}</div>
                        <div><strong>Location:</strong> 1400 Zug Island Rd,<br>Detroit, MI, United States</div>
                        <div><strong>Calendar:</strong> PICK_FACILITY</div>
                        <div><strong>Repeat:</strong> None</div>
                        <div><strong>Alerts:</strong> MethodPlus, SMS, Email</div>
                    </div>
                `
                tempDiv2.addEventListener("click", function () {
                    show_event_details(this)
                });
                newAllDay.appendChild(tempDiv2);
            })
            allDayCont.replaceWith(newAllDay);

            otherEvents.map((item) => {
                const html = `
                    <div class="event-title">
                        ${formatTimeTo12Hour(item.start_time)} - ${item.title} - ${item.observer}
                    </div>
                    <div id="event-body-${item.id}" class="event-meta" style="display: none;">
                        <div><strong>Time:</strong> ${formatTimeTo12Hour(item.start_time)} - ${formatTimeTo12Hour(item.end_time)}</div>    
                        <div><strong>Observer:</strong> ${item.observer}</div>
                        <div><strong>Location:</strong> 1400 Zug Island Rd,<br>Detroit, MI, United States</div>
                        <div><strong>Calendar:</strong> PICK_FACILITY</div>
                        <div><strong>Repeat:</strong> None</div>
                        <div><strong>Alerts:</strong> MethodPlus, SMS, Email</div>
                    </div>
                `
                const tempDiv = document.createElement("div");
                tempDiv.classList.add("event-block");
                tempDiv.innerHTML = html;
                tempDiv.dataset.eventid = `${item.id}`
                tempDiv.addEventListener("click", function () {
                    show_event_details(this)
                });
                newOther.appendChild(tempDiv);
            })
            otherEventsCont.replaceWith(newOther);
        });
    });
});

function show_event_details(elem){
    console.log(elem.dataset.eventid)
    const body = document.getElementById(`event-body-${elem.dataset.eventid}`);
    if (body.style.display == "none"){
        body.style.display = 'block';
    } else {
        body.style.display = 'none';
    }
}

function formatTimeTo12Hour(timeString) {
    const [hours, minutes] = timeString.split(":");
    const date = new Date();
    date.setHours(hours, minutes);

    return date.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    }).toUpperCase(); // optional: to match "AM"/"PM" in caps
}