const settingsDays = JSON.parse(document.getElementById('settings-days-json').textContent);

function individual_day() {
    const dayNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    function dayNameToNumber(dayName) {
        return dayNames.indexOf(dayName);
    }
    const today = new Date();
    const dayIndex = today.getDay();

    settingsDays.forEach((i) => {
        let day_num = dayNameToNumber(i);
        const required = day_num <= (dayIndex - 1); // Adjust since your IDs start at 0 for Monday
        document.getElementById(`id_time_${day_num}`).required = required;
        document.getElementById(`id_obser_${day_num}`).required = required;
        document.getElementById(`id_time_${day_num}`).closest('.day-card').style.backgroundColor = '#F49B9B';
    })
}

const container = document.getElementById('daysContainer');
let i = 0;
settingsDays.forEach(day => {
    const card = document.createElement('div');
    card.className = 'day-card';
    card.innerHTML = `
        <div class="day-title">
            ${day}
            <button class="toggle-btn" aria-label="Toggle Inputs" type="button">+</button>
        </div>
        <div class="field-group">
            <input type="text" placeholder="Inspector Name" name="obser_${i}" id="id_obser_${i}">
            <input type="time" placeholder="Sample Time" name="time_${i}" id="id_time_${i}">
        </div>
    `;
    container.appendChild(card);
    i++;
});

individual_day();

document.querySelectorAll('.field-group input').forEach(input => {
    input.addEventListener('change', function() {
        const group = this.closest('.field-group');
        const inspector = group.querySelector("input[type='text']").value;
        const sample = group.querySelector("input[type='time']").value;
        const toggleBtn = group.parentElement.querySelector('.toggle-btn');
        const title = group.parentElement.querySelector('.day-title');
        const weekDayIndex = this.name.slice(-1);
        if (inspector && sample) {
            toggleBtn.style.display = 'inline';
            group.style.display = 'none';
            title.style.marginBottom = 'unset';
            group.parentElement.style.backgroundColor = '#3c983c85';
        } else {
            toggleBtn.style.display = 'none';
            const today = new Date();
            const dayIndex = today.getDay();
            if (Number(weekDayIndex) <= (dayIndex - 1)) {
                group.parentElement.style.backgroundColor = '#F49B9B';
            }
        }
    });
});

document.querySelectorAll('.toggle-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const group = this.closest('.day-card').querySelector('.field-group');
        const title = this.closest('.day-card').querySelector('.day-title');
        if (group.style.display === 'none') {
            group.style.display = 'flex';
            this.textContent = '-';
            title.style.marginBottom = '15px';
        } else {
            group.style.display = 'none';
            this.textContent = '+';
            title.style.marginBottom = 'unset';
        }
    });
});

document.getElementById('submitBtn').addEventListener('click', () => {
    // handle submission logic here
    alert("Form submitted (mockup)");
});