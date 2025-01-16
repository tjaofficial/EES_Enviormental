let stopwatchContainer = document.getElementById("stopwatch-container");
let isDragging = false;
let offset = { x: 0, y: 0 };

stopwatchContainer.addEventListener("mousedown", (e) => {
    isDragging = true;
    offset.x = e.clientX - stopwatchContainer.getBoundingClientRect().left;
    offset.y = e.clientY - stopwatchContainer.getBoundingClientRect().top;
    stopwatchContainer.style.cursor = "grabbing";
});

document.addEventListener("mousemove", (e) => {
    if (isDragging) {
        stopwatchContainer.style.left = `${e.clientX - offset.x}px`;
        stopwatchContainer.style.top = `${e.clientY - offset.y}px`;
        stopwatchContainer.style.right = "auto"; // Clear right position for proper dragging
        stopwatchContainer.style.bottom = "auto"; // Clear bottom position for proper dragging
    }
});

document.addEventListener("mouseup", () => {
    isDragging = false;
    stopwatchContainer.style.cursor = "grab";
});

function closeStopwatch() {
    stopwatchContainer.style.display = "none";
    document.getElementById('toggle-stopwatch').checked = false;
}
























let stopwatchInterval;
let elapsedTime = 0;
let isRunning = false;

function toggleStopwatch() {
    const card = document.getElementById('card_fitter')
    const stopwatchDrawer = document.getElementById('stopWatchDrawer')
    const stopwatchContainer = document.getElementById('stopwatch-container');
    const isChecked = document.getElementById('toggle-stopwatch').checked;
    stopwatchContainer.style.display = isChecked ? 'block' : 'none';
    //stopwatchDrawer.style.display = isChecked ? 'block' : 'none';
    card.style.display = isChecked ? 'flex' : 'block';
}

function startStopwatch() {
    if (isRunning) {
        isRunning = false;
        document.getElementById('startButton').innerHTML = "Start";
        clearInterval(stopwatchInterval);
    } else {
        isRunning = true;
        const stopwatch = document.getElementById('stopwatch');
        const startTime = Date.now() - elapsedTime;
        document.getElementById('startButton').innerHTML = "Stop";
        stopwatchInterval = setInterval(() => {
            elapsedTime = Date.now() - startTime;
            stopwatch.textContent = formatTime(elapsedTime);
        }, 10); // Update every 10 milliseconds for smoother precision
    }
}

function resetStopwatch() {
    isRunning = false;
    clearInterval(stopwatchInterval);
    elapsedTime = 0;
    document.getElementById('stopwatch').textContent = '00:00:00.000';
}

function formatTime(timeInMilliseconds) {
    const totalSeconds = Math.floor(timeInMilliseconds / 1000);
    const milliseconds = String(timeInMilliseconds % 1000).padStart(3, '0');
    const hours = String(Math.floor(totalSeconds / 3600)).padStart(2, '0');
    const minutes = String(Math.floor((totalSeconds % 3600) / 60)).padStart(2, '0');
    const seconds = String(totalSeconds % 60).padStart(2, '0');
    return `${hours}:${minutes}:${seconds}.${milliseconds}`;
}

window.addEventListener('scroll', () => {
    const parent = document.getElementById('stopWatchDrawer');
    const child = document.getElementById('stopwatch-container');

    const parentRect = parent.getBoundingClientRect();
    const childHeight = child.offsetHeight;

    // Ensure the child stays within the parent's vertical bounds
    const childTop = Math.max(parentRect.top, window.innerHeight / 2 - childHeight / 2);
    const childBottom = Math.min(parentRect.bottom - childHeight, childTop);

    child.style.top = `${childBottom}px`;
});
