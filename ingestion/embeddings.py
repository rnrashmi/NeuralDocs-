from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

class EmbeddingGenerator:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    async def generate_embedding(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            output = self.model(**inputs)
        embedding = output.last_hidden_state.mean(dim=1).squeeze().numpy()
        return embedding / np.linalg.norm(embedding)
