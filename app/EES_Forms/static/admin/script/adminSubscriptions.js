document.addEventListener("DOMContentLoaded", () => {
    // Fetch and display metrics
    fetchMetrics();

    // Initialize subscription trends chart
    initializeSubscriptionTrendsChart();

    // Handle filter form submission
    document.getElementById("filterForm").addEventListener("submit", (e) => {
        e.preventDefault();
        fetchFilteredSubscriptions();
    });
});

function fetchMetrics() {
    var active_users = document.getElementById("active_users").dataset.activeusers;
    var past_due = document.getElementById("past_due").dataset.pastdue;
    document.getElementById("filterForm")
    // Simulate an API call to fetch metrics
    setTimeout(() => {
        document.getElementById("active-subscriptions").innerText = "active_users";
        document.getElementById("past-due-subscriptions").innerText = "past_due";
        document.getElementById("monthly-revenue").innerText = "$get new category";
    }, 1000);
}

function initializeSubscriptionTrendsChart() {
    const ctx = document.getElementById("subscriptionTrendsChart").getContext("2d");
    new Chart(ctx, {
        type: "line",
        data: {
            labels: ["January", "February", "March", "April", "May"],
            datasets: [
                {
                    label: "Active Subscriptions",
                    data: [100, 120, 130, 125, 140],
                    borderColor: "rgba(0, 123, 255, 0.8)",
                    fill: false,
                },
                {
                    label: "Past Due Subscriptions",
                    data: [10, 12, 15, 10, 8],
                    borderColor: "rgba(255, 99, 132, 0.8)",
                    fill: false,
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: "top",
                },
            },
        },
    });
}

async function fetchFilteredSubscriptions() {
    const subscriptionContainer = document.getElementById("subscriptionContainer");
    subscriptionContainer.innerHTML = `<div class="loading">Loading subscriptions...</div>`;
    
    try {
        const response = await fetch('/api/get_subscriptions/');
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();

        if (data.error) {
            subscriptionContainer.innerHTML = `<div class="error">Error: ${data.error}</div>`;
            return;
        }

        // Populate the subscription data
        subscriptionContainer.innerHTML = '';
        const subscriptions = data.subscriptions;

        subscriptions.forEach(subscription => {
            const subscriptionDiv = document.createElement('tr');
            subscriptionDiv.classList.add('subscription');
            subscriptionDiv.innerHTML = `
                <td>${subscription.id}</td>
                <td>${subscription.customer_name}</td>
                <td>${subscription.status}</td>
                <td>${subscription.plan_id}</td>
                <td>${subscription.start_date}</td>
                <td>${subscription.next_billing_date}</td>
            `;
            if (subscription.status != "Past Due"){
                subscriptionDiv.innerHTML += `<td><button>View</button></td>`
            } else {
                subscriptionDiv.innerHTML += `<td><button>Retry Payment</button></td>`
            }
            subscriptionContainer.appendChild(subscriptionDiv);
        });
    } catch (error) {
        console.error('Error fetching subscriptions:', error);
        subscriptionContainer.innerHTML = `<div class="error">Failed to load subscriptions.</div>`;
    }
}

// Call the function on page load
document.addEventListener('DOMContentLoaded', () => {
    fetchFilteredSubscriptions();
});

