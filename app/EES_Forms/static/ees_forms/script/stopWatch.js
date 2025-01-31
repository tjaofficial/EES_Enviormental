let stopwatchContainer = document.getElementById("stopwatch-container");
let isDragging = false;
let dragThreshold = 10; // Minimum movement (in pixels) to trigger dragging
let startPosition = { x: 0, y: 0 };
let offset = { x: 0, y: 0 };

function startDrag(e) {
    isDragging = false; // Reset dragging state
    stopwatchContainer.style.cursor = "grab";

    // Get the starting position for touch or mouse
    if (e.type === "touchstart") {
        startPosition.x = e.touches[0].clientX;
        startPosition.y = e.touches[0].clientY;
        offset.x = e.touches[0].clientX - stopwatchContainer.getBoundingClientRect().left;
        offset.y = e.touches[0].clientY - stopwatchContainer.getBoundingClientRect().top;
    } else {
        startPosition.x = e.clientX;
        startPosition.y = e.clientY;
        offset.x = e.clientX - stopwatchContainer.getBoundingClientRect().left;
        offset.y = e.clientY - stopwatchContainer.getBoundingClientRect().top;
    }

    document.addEventListener("mousemove", duringDrag);
    document.addEventListener("touchmove", duringDrag);
    document.addEventListener("mouseup", stopDrag);
    document.addEventListener("touchend", stopDrag);
}

function duringDrag(e) {
    let clientX = e.type === "touchmove" ? e.touches[0].clientX : e.clientX;
    let clientY = e.type === "touchmove" ? e.touches[0].clientY : e.clientY;

    // Check if movement exceeds threshold to enable dragging
    if (!isDragging) {
        if (
            Math.abs(clientX - startPosition.x) > dragThreshold ||
            Math.abs(clientY - startPosition.y) > dragThreshold
        ) {
            isDragging = true;
            stopwatchContainer.style.cursor = "grabbing";
        }
    }

    // If dragging, move the stopwatch
    if (isDragging) {
        e.preventDefault(); // Prevent scrolling while dragging
        stopwatchContainer.style.left = `${clientX - offset.x}px`;
        stopwatchContainer.style.top = `${clientY - offset.y}px`;
        stopwatchContainer.style.right = "auto"; // Clear right position for proper dragging
        stopwatchContainer.style.bottom = "auto"; // Clear bottom position for proper dragging
    }
}

function stopDrag() {
    isDragging = false;
    stopwatchContainer.style.cursor = "grab";

    document.removeEventListener("mousemove", duringDrag);
    document.removeEventListener("touchmove", duringDrag);
    document.removeEventListener("mouseup", stopDrag);
    document.removeEventListener("touchend", stopDrag);
}

// Add event listeners for mouse and touch
stopwatchContainer.addEventListener("mousedown", startDrag);
stopwatchContainer.addEventListener("touchstart", startDrag);

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
    document.getElementById('startButton').innerHTML = "Start";
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
