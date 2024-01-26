from time import sleep
import requests
from os import getenv

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

def generate_desc_embedding(description: str):
    response = requests.post(
        'https://api-inference.huggingface.co/models/BAAI/bge-large-en-v1.5',
        data={'inputs': description},
        headers={
            'Authorization': f'Bearer {getenv("INFERENCE_API_KEY")}',
            'Content-Type': 'application/json'
        }
    )
    content = response.json()

    if 'error' in content:
        if 'estimated_time' in content:
            sleep(content['estimated_time'])
            print(f'Retrying in {content["estimated_time"]} seconds')
            content = generate_desc_embedding(description)
        else:
            print(content)
    
    return content


model = SentenceTransformer("BAAI/bge-large-en-v1.5")

def local_generate_desc_embedding(description: str):
    return model.encode(description)