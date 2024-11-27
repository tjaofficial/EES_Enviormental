document.addEventListener('DOMContentLoaded', () => {
    var active_users = document.getElementById('active_users').dataset.activeusers;
    var mmr_total = document.getElementById('mmr').dataset.mmr;
    var past_due = document.getElementById('past_due').dataset.pastdue;
    // Simulate loading data for the overview cards
    document.getElementById('active-users').innerText = String(active_users);
    document.getElementById('mrr').innerText = "$" + String(mmr_total);
    document.getElementById('past-due').innerText = past_due;

    // Render the traffic chart
    renderTrafficChart();
});

// Render a traffic chart using Chart.js
function renderTrafficChart() {
    const ctx = document.getElementById('traffic-chart').getContext('2d');
    const trafficData = {
        labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        datasets: [{
            label: 'Site Traffic (Visitors)',
            data: [1200, 1500, 1100, 900, 1600, 2000, 1700],
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 2,
            tension: 0.4, // Smooth lines
        }]
    };

    const trafficChart = new Chart(ctx, {
        type: 'line', // Chart type
        data: trafficData,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Website Traffic (Last 7 Days)'
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Days of the Week',
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Visitors',
                    }
                }
            }
        }
    });
}                