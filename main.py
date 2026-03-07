import tensorflow as tf
import tensorflow_hub as hub
from sklearn.cluster import KMeans
import numpy as np

def embed_sentences(sentences):
    """
    Embed sentences using the Universal Sentence Encoder.
    
    Parameters:
    sentences (list): A list of sentences to be embedded.
    
    Returns:
    np.array: An array of sentence embeddings.
    """
    embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
    embeddings = embed(sentences)
    return np.array(embeddings)

def semantic_chunk(sentences, num_clusters):
    """
    Perform semantic chunking by clustering sentences based on their embeddings.
    
    Parameters:
    sentences (list): A list of sentences to be chunked.
    num_clusters (int): The number of clusters to form.
    
    Returns:
    list: A list of clusters, each containing similar sentences.
    """
    # Embed the sentences
    embeddings = embed_sentences(sentences)
    
    # Perform KMeans clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(embeddings)
    
    # Group sentences by clusters
    clusters = [[] for _ in range(num_clusters)]
    for i, label in enumerate(kmeans.labels_):
        clusters[label].append(sentences[i])
    
    return clusters

# Sample text
file_path = 'sample.txt'
try:
    with open(file_path, 'r') as file:
        content = file.read()
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")

# Split text into sentences
sentences = content.split('. ')
sentences[-1] = sentences[-1].rstrip('.')

# Perform semantic chunking
num_clusters = 3
clusters = semantic_chunk(sentences, num_clusters)

# Print the clusters
for i, cluster in enumerate(clusters):
    print(f"Cluster {i+1}:")
    for sentence in cluster:
        print(f"- {sentence}")
    print()


