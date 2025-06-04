import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_embedding(text):
    return model.encode([text])[0]

def compute_similarity(embedding1, embedding2):
    return cosine_similarity([embedding1], [embedding2])[0][0]

def get_hotel_embedding(hotel):
    # Combine description and amenities into one text
    amenities_text = ' '.join(hotel.amenities) if hotel.amenities else ''
    combined_text = f"{hotel.description} {amenities_text}"
    return compute_embedding(combined_text)
