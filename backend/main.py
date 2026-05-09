from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from rag import process_document, ask_question

app = FastAPI()

# =========================
# CORS (FIXED FOR PRODUCTION)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://light-rag-omega.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}


@app.get("/")
def home():
    return {"message": "RAG Bot Running"}


# =========================
# UPLOAD ENDPOINT (FIXED)
# =========================
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        return {"error": "Only PDF, DOCX, and TXT files are allowed"}

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ✅ FIX: unified processor
    process_document(file_path)

    return {"message": f"{file.filename} uploaded and indexed successfully"}


# =========================
# ASK ENDPOINT
# =========================
@app.post("/ask")
async def ask(data: dict):
    question = data.get("question")

    if not question:
        return {"error": "Question is required"}

    answer = ask_question(question)

    return {"answer": answer}


# =========================
# RUN (LOCAL ONLY)
# =========================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)