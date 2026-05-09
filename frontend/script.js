const API_URL = "https://light-rag-production-8f5e.up.railway.app";


// =========================
// FILE UPLOAD (PDF / DOCX / TXT)
// =========================
async function uploadFile() {
    const fileInput = document.getElementById("pdfFile");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file first");
        return;
    }

    const allowedTypes = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain"
    ];

    if (!allowedTypes.includes(file.type)) {
        alert("Only PDF, DOCX, and TXT files are supported");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch(`${API_URL}/upload`, {
            method: "POST",
            body: formData
        });

        const text = await response.text();

        let data;
        try {
            data = JSON.parse(text);
        } catch (e) {
            console.log("Non-JSON response:", text);
            alert("Upload failed (server error)");
            return;
        }

        alert(data.message || "Uploaded successfully");

    } catch (error) {
        console.error(error);
        alert("Network error during upload");
    }
}


// =========================
// ASK QUESTION
// =========================
async function askQuestion() {
    const question = document.getElementById("question").value;

    if (!question.trim()) {
        alert("Enter a question");
        return;
    }

    const responseDiv = document.getElementById("response");
    responseDiv.innerHTML = "Thinking...";

    try {
        const response = await fetch(`${API_URL}/ask`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question })
        });

        const text = await response.text();

        let data;
        try {
            data = JSON.parse(text);
        } catch (e) {
            console.log("Raw response:", text);
            responseDiv.innerHTML = text;
            return;
        }

        responseDiv.innerHTML = data.answer || "No answer returned";

    } catch (error) {
        console.error(error);
        responseDiv.innerHTML = "Error connecting to server";
    }
}