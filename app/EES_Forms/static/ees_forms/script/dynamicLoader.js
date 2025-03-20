document.addEventListener("DOMContentLoaded", function() {
    function loadFormScripts(formNumber) {
        let scriptContainer = document.getElementById("dynamic-script-container");
        scriptContainer.innerHTML = ""; // Clear any existing scripts

        let scriptTag = document.createElement("script");
        scriptTag.src = `/static/ees_forms/script/form${formNumber}.js`; // Dynamically load JS
        scriptTag.defer = true;

        let linkTag = document.createElement("link");
        linkTag.href = `/static/ees_forms/style/form${formNumber}.css`; // Dynamically load CSS
        linkTag.rel = "stylesheet";

        // Append new files to the document
        scriptContainer.appendChild(scriptTag);
        scriptContainer.appendChild(linkTag);

        console.log(`Loaded: form${formNumber}.js & form${formNumber}.css`);
    }
    loadFormScripts(formNumber);
});