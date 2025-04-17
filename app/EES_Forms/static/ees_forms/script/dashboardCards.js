document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".dash-card").forEach(card => {
        const url = card.dataset.url;

        fetch(url)
            .then(res => res.json())
            .then(data => {
                card.innerHTML = data.html;
            })
            .catch(err => {
                console.error("Error loading card:", err);
                card.innerHTML = "<p class='error'>Failed to load card</p>";
            });
    });
});
