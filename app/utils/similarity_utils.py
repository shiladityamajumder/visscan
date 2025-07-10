# File: app/utils/similarity_utils.py
# Description: Utility functions for computing semantic similarity between text strings using sentence-transformers.

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_text(text: str):
    """
    Generates a semantic embedding for a given string.
    """
    return model.encode([text])[0]


def compute_similarity(text1: str, text2: str) -> float:
    """
    Computes cosine similarity between two strings using sentence-transformers.
    """
    emb1 = embed_text(text1)
    emb2 = embed_text(text2)
    sim = cosine_similarity([emb1], [emb2])[0][0]
    return round(float(sim), 4)  # return float rounded
