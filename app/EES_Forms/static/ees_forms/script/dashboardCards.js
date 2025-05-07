document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".dash-card").forEach(card => {
        const url = card.dataset.url;

        fetch(url)
            .then(res => res.json())
            .then(data => {
                card.innerHTML = data.html;
                // Re-execute any <script> tags inside the injected card
                card.querySelectorAll("script").forEach(oldScript => {
                    const newScript = document.createElement("script");
                    if (oldScript.src) {
                        newScript.src = oldScript.src;
                        newScript.defer = true;
                    } else {
                        newScript.textContent = oldScript.textContent;
                    }
                    document.body.appendChild(newScript);
                    document.body.removeChild(newScript);
                });
            })
            .catch(err => {
                console.error("Error loading card:", err);
                card.innerHTML = "<p class='error'>Failed to load card</p>";
            });
    });
});
