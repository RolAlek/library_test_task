document.addEventListener("DOMContentLoaded", (event) => {
    const buttons = document.querySelectorAll(".copy-btn");

    buttons.forEach(button => {
        button.addEventListener("click", function() {
            const title = this.getAttribute("data-title");
            copyToClipboard(title);
        });
    });
});

function copyToClipboard(text) {
    var tempInput = document.createElement("input");
    tempInput.style = "position: absolute; left: -1000px; top: -1000px;";
    tempInput.value = text;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand("copy");
    document.body.removeChild(tempInput);
    alert("Скопировано")
}