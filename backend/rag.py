import os
from sklearn.feature_extraction.text import TfidfVectorizer
from groq import Groq
from dotenv import load_dotenv
import fitz
from docx import Document
load_dotenv()

DOCUMENTS = []

vectorizer = TfidfVectorizer(stop_words="english")

GROQ_CLIENT = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

DOCUMENT_CHUNKS = []
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    return text

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)

    text = ""

    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"

    return text

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    return text

def process_document(file_path):
    global DOCUMENT_CHUNKS

    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)

    elif file_path.endswith(".docx"):
        text = extract_text_from_docx(file_path)

    elif file_path.endswith(".txt"):
        text = extract_text_from_txt(file_path)

    else:
        raise ValueError("Unsupported file type")

    chunks = chunk_text(text)

    DOCUMENT_CHUNKS = chunks

def extract_text_from_txt(txt_path):
    with open(txt_path, "r", encoding="utf-8") as file:
        return file.read()
    

def chunk_text(text, chunk_size=150):
    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks



def process_pdf(pdf_path):
    global DOCUMENT_CHUNKS

    text = extract_text_from_pdf(pdf_path)

    chunks = chunk_text(text)

    DOCUMENT_CHUNKS = chunks

    embeddings = vectorizer.fit_transform(chunks)

    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[str(i)],
            metadatas=[{"source": pdf_path}]
        )



def retrieve_context(question, top_k=3):
    if not DOCUMENT_CHUNKS:
        return []

    all_texts = DOCUMENT_CHUNKS + [question]

    matrix = vectorizer.fit_transform(all_texts)

    question_vector = matrix[-1]

    document_vectors = matrix[:-1]

    similarities = (document_vectors @ question_vector.T).toarray()

    scores = similarities.flatten()

    top_indices = scores.argsort()[-top_k:][::-1]

    results = []

    for idx in top_indices:
        results.append(DOCUMENT_CHUNKS[idx])

    return results

def ask_question(question):
    contexts = retrieve_context(question)

    combined_context = "\n\n".join(contexts)

    prompt = f"""
You are a document assistant.

ONLY answer from the provided context.

If the answer is not found in context, say:
'I could not find that information in the document.'

Context:
{combined_context}

Question:
{question}
"""

    response = GROQ_CLIENT.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content

