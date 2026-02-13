import requests
import numpy as np


def get_jina_embeddings(texts, api_key):
    url = "https://api.jina.ai/v1/embeddings"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "jina-embeddings-v4",
        "input": texts
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    vectors = [item["embedding"] for item in response.json()["data"]]
    return np.array(vectors).astype("float32")
