# rag-chatbot
# 🤖 Document-based RAG Chatbot

## 📌 Project Overview
This project is a **Retrieval-Augmented Generation (RAG) Chatbot** designed to answer questions based on content from uploaded PDF or DOCX documents. It integrates document chunking, semantic embedding, vector search using **Qdrant**, and an offline **Falcon LLM** model to provide relevant, accurate answers.

The user interacts via a polished **Streamlit interface**, supporting both pre-loaded and dynamically uploaded documents.

---

## 🎯 Problem Statement
The task was to build a **domain-specific chatbot** using offline models, capable of retrieving contextually relevant information from technical documents and generating human-like responses. The solution had to run on CPU (due to hardware constraints) while supporting GPU if available.

---

## ✅ Features Implemented
- 📚 Supports **PDF/DOCX document loading** from both:
  - `data/` directory (default documents)
  - Sidebar upload interface (dynamic documents)
- 🧠 **Text chunking** with overlap for better retrieval context.
- 🔍 **Semantic embedding** using `BAAI/bge-small-en` (Sentence Transformers).
- 💃 **Qdrant (in-memory)** vector DB for fast context retrieval.
- 🧾 **Falcon-RW-1B** LLM for generating answers (offline, via HuggingFace Transformers).
- 🌐 **Streamlit UI** with:
  - Chat-style interface (user left, bot right)
  - Avatar icons, timestamps, color-coded bubbles
  - Auto-scrolling and dark theme
- 🧹 Modular architecture with:
  - `app.py` (UI)
  - `main.py` (pipeline logic)
  - `loader.py` (file reading + chunking)
  - `embed_store.py` (embedding + search)
  - `answer_generator.py` (LLM answer logic)

---

## ⚙️ Technologies Used
| Component        | Stack/Tool                             |
|------------------|----------------------------------------|
| UI               | Streamlit                              |
| Document Parsing | PyMuPDF, python-docx                   |
| Embedding        | SentenceTransformer (`bge-small-en`)   |
| Vector Store     | Qdrant (in-memory mode)                |
| Language Model   | Falcon-RW-1B (offline, Transformers)   |
| Model Hosting    | Hugging Face Hub (1-time download)     |

---

## ⚠️ Why CPU is Used Instead of GPU
- The project requirement initially asked for **T4 GPU support**.
- **Colab runtime memory constraints**, frequent session timeouts, and download failures made GPU testing unreliable.
- Therefore, we switched to a **local CPU environment** for development and testing.
- ✅ However, the code is **GPU-compatible**. If a GPU is available, it **automatically uses it**:
```python
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
```
- This ensures the solution **meets the GPU-readiness requirement** despite CPU-only validation.

---

## 📂 Folder Structure
```
rag-chatbot/
│
├── app.py                  # Streamlit frontend
├── main.py                 # RAG pipeline logic
├── loader.py               # Document loader & chunker
├── embed_store.py          # Embedding & Qdrant logic
├── answer_generator.py     # Offline Falcon model
├── requirements.txt
├── data/                   # Default documents (PDF/DOCX)
|── output/                 # Screenshots + Q&A PDF

```

---

## 📄 Sample Questions (Used in Demo)
1. What is the function of the LINAK OpenBus interface?
2. How can you configure the virtual I/O channels in the LINAK system?
3. What is the function of the LINAK I/O interface?
4. What are the default input and output signals supported by the I/O actuator?
5. How does the LINAK I/O actuator handle fault detection and reporting?
6. How does the actuator communicate status?
7. What type of IO link is supported in the Techline system?
8. Which page describes position feedback methods?
9. What are the default baud rate settings?
10. What is the use of COM port diagnostics?


---

## 📸 Screenshots & Responses
Please refer to the `/output/` folder which contains:
- 10 questions & answers PDF with screenshots
- Final UI preview

---

## 🚀 How to Run
```bash
# 1. Create environment
python -m venv venv
source venv/bin/activate (or venv\Scripts\activate)

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch Streamlit app
streamlit run app.py
```

---

## 👤 Team & Contact
**Name**: Monika A. D  
**Program**: B.Tech, Artificial Intelligence and Data Science  
**Institution**: [Your College Name Here]  
**Email**: monika@example.com  *(replace with your real ID)*

---

## ✅ Evaluation Checklist
| Task Requirement                   | Status         |
|------------------------------------|----------------|
| RAG architecture implementation    | ✅ Done        |
| Offline model usage (Falcon)       | ✅ Done        |
| Document upload + parsing          | ✅ Done        |
| Vector DB + semantic search        | ✅ Done        |
| UI: Streamlit chatbot w/ avatars   | ✅ Done        |
| CPU/GPU compatibility              | ✅ Done (CPU)  |
| 10 Q&A with screenshots            | ✅ Included    |
| README with justification          | ✅ Provided    |

---

## 🙌 Acknowledgements
Thanks to the hackathon organizers and reviewers for the opportunity to explore real-world RAG applications. The project was inspired by HuggingFace Transformers, Qdrant, and the Streamlit open-source ecosystem.
