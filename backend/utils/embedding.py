from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from torch.cuda import is_available

load_dotenv()

device = 'cuda' if is_available() else 'cpu'
model = SentenceTransformer("sentence-transformers/all-distilroberta-v1", device=device)

def generate_desc_embedding(description: str):
    return model.encode(description)
