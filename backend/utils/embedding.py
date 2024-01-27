from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from torch.cuda import is_available

load_dotenv()

# model = SentenceTransformer("BAAI/bge-large-en-v1.5", device='cuda')
device = 'cuda' if is_available() else 'cpu'
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2", device=device)

def generate_desc_embedding(description: str):
    return model.encode(description)
