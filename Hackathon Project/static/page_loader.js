
document.getElementById("summaryForm").addEventListener("submit", function() {
    // Show loader
    const loaderModal = document.getElementById("loaderModal");
    const loadingText = document.getElementById("loadingText");

    loaderModal.style.display = "flex";

    // Update text in phases
    let messages = ["🔍 Reading the document...", "🤖 Analyzing content...", "✍️ Summarizing key points...", "🚀 Almost done..."];
    let index = 0;

    const interval = setInterval(() => {
        loadingText.innerText = messages[index];
        index = (index + 1) % messages.length;
    }, 2000);

    // Hide loader after processing (handled by server response)
    window.addEventListener("load", () => {
        clearInterval(interval);
        loaderModal.style.display = "none";
    });
});
