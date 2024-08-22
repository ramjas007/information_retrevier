import os
import json
import faiss
import numpy as np
import argparse
from sentence_transformers import SentenceTransformer

# Set up argparse to handle input arguments
parser = argparse.ArgumentParser(description="Search for similar documents using a FAISS vector database.")
parser.add_argument('--json_path', type=str, required=True, help="Path to the JSON file containing transcriptions.")
parser.add_argument('--query', type=str, required=True, help="Query string to search in the FAISS index.")

args = parser.parse_args()

# Load the JSON file
with open(args.json_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extract the transcriptions and metadata from the JSON structure
documents = []
metadata = []
for video, info in data.items():
    for chunk, transcription in info[f"{video}_transcriptions"].items():
        documents.append(transcription)
        metadata.append({'document': transcription, 'video_name': video, 'chunk_name': chunk})

# Initialize the Sentence Transformer model
model_name = 'sentence-transformers/all-MiniLM-L6-v2'
sentence_model = SentenceTransformer(model_name)

# Encode the documents to get embeddings
embeddings = sentence_model.encode(documents, batch_size=16, normalize_embeddings=True, show_progress_bar=True)

# Path to the FAISS index file
index_file_path = 'transcription_faiss_index.index'

# Delete the existing index file if it exists
if os.path.exists(index_file_path):
    os.remove(index_file_path)

# Create a FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# Store metadata in a separate list
metadata = np.array(metadata)

# Save the FAISS index and metadata
faiss.write_index(index, index_file_path)
np.save('transcription_metadata.npy', metadata)

# Encode the query string
query_embedding = sentence_model.encode([args.query], normalize_embeddings=True)

# Search for similar embeddings in the FAISS index
D, I = index.search(query_embedding, k=5)  # k is the number of nearest neighbors

# Retrieve the corresponding metadata
results = []
for idx in I[0]:
    if idx != -1:
        results.append(metadata[idx])

# Print the results
for result in results:
    print(f"Document: {result['document']}")
    print(f"Video Name: {result['video_name']}")
    print(f"Chunk Name: {result['chunk_name']}\n")