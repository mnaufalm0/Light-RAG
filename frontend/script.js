const API_URL = "http://127.0.0.1:8000";


async function uploadPDF() {
    const fileInput = document.getElementById("pdfFile");

    const formData = new FormData();

    formData.append("file", fileInput.files[0]);

    const response = await fetch(`${API_URL}/upload`, {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    alert(data.message);
}


async function askQuestion() {
    const question = document.getElementById("question").value;

    const responseDiv = document.getElementById("response");

    responseDiv.innerHTML = "Thinking...";

    const response = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ question })
    });

    const data = await response.json();

    responseDiv.innerHTML = data.answer;
}