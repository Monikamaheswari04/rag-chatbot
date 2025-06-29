def rag_pipeline(query, uploaded_files=None):
    # Load docs from uploaded files or fallback to local data/
    if uploaded_files:
        import tempfile
        import os
        from docx import Document
        import fitz

        docs = []
        for file in uploaded_files:
            file_path = os.path.join(tempfile.gettempdir(), file.name)
            with open(file_path, "wb") as f:
                f.write(file.read())
            if file.name.endswith(".pdf"):
                pdf = fitz.open(file_path)
                for i in range(len(pdf)):
                    page = pdf[i]
                    docs.append({
                        "content": page.get_text(),
                        "source": file.name,
                        "page": i + 1
                    })
            elif file.name.endswith(".docx"):
                doc = Document(file_path)
                text = "\n".join([p.text for p in doc.paragraphs])
                docs.append({
                    "content": text,
                    "source": file.name,
                    "page": 1
                })
    else:
        from loader import load_documents
        docs = load_documents()

    from loader import chunk_documents
    chunks = chunk_documents(docs)

    # Index and search
    from embed_store import create_qdrant_client, create_collection, index_chunks, retrieve_context
    from sentence_transformers import SentenceTransformer
    embed_model = SentenceTransformer("BAAI/bge-small-en")
    client = create_qdrant_client()
    create_collection(client)
    index_chunks(client, embed_model, chunks)

    from answer_generator import load_model, generate_answer
    tokenizer, model = load_model()

    hits = retrieve_context(client, embed_model, query)
    if not hits:
        return "Answer not found in the documents.", None

    top = hits[0].payload
    context = top["content"]
    answer = generate_answer(query, context, tokenizer, model)
    source = f"{top['source']} | Page {top.get('page', '?')}"
    return answer, source
