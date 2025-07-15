document.addEventListener("DOMContentLoaded", () => {
    // Initialize subscription trends chart
    initializeSubscriptionTrendsChart();

    // Handle filter form submission
    document.getElementById("filterForm").addEventListener("submit", (e) => {
        e.preventDefault();
        fetchFilteredSubscriptions();
    });
});

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
    subscriptionContainer.innerHTML = `<tr><td colspan="7" class="loading">Loading subscriptions...</td></tr>`;

    try {
        const response = await fetch("/admin-pages/api/get_subscriptions/");
        if (!response.ok) throw new Error(`HTTP error ${response.status}`);
        const data = await response.json();

        // Update metrics
        document.getElementById("active-subscriptions").innerText = data.active_users;
        document.getElementById("past-due-subscriptions").innerText = data.past_due;
        document.getElementById("monthly-revenue").innerText = data.monthly_revenue;

        // Populate subscription table
        subscriptionContainer.innerHTML = "";
        const subscriptions = data.subscriptions;

        subscriptions.forEach(sub => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${sub.id}</td>
                <td>${sub.customer_name}</td>
                <td>${sub.status}</td>
                <td>${sub.plan_id}</td>
                <td>${sub.start_date}</td>
                <td>${sub.next_billing_date}</td>
                <td><button>${sub.status === "Past_due" ? "Retry Payment" : "View"}</button></td>
            `;
            subscriptionContainer.appendChild(row);
        });

    } catch (err) {
        console.error("Error fetching subscriptions:", err);
        subscriptionContainer.innerHTML = `<tr><td colspan="7">Failed to load subscriptions.</td></tr>`;
    }
}


// Call the function on page load
document.addEventListener('DOMContentLoaded', () => {
    fetchFilteredSubscriptions();
});

