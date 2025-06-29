from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def load_model():
    tokenizer = AutoTokenizer.from_pretrained("tiiuae/falcon-rw-1b")
    
    # Falcon doesn't have a default pad token, so use eos_token
    tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained("tiiuae/falcon-rw-1b")

    # Auto-detect CPU or GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    return tokenizer, model

def generate_answer(query, context, tokenizer, model):
    prompt = f"""You are a helpful assistant. Use only the information provided in the context below to answer the question.

Context:
{context}

Question: {query}
Answer:"""

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True).to(model.device)

    output = model.generate(
        **inputs,
        max_new_tokens=2000,
        do_sample=False,
        pad_token_id=tokenizer.pad_token_id  # Explicitly set padding ID
    )

    decoded = tokenizer.decode(output[0], skip_special_tokens=True)

    # Clean output to extract only the final answer
    if "Answer:" in decoded:
        return decoded.split("Answer:")[-1].strip()

    return decoded.strip()
