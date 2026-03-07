# Psych.py

import pandas as pd

def read_file(file_path):
    """
    Reads the content of a .txt file and returns it as a string.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None

def chunk_text(text, chunk_size):
    """
    Splits the text into chunks of the specified size.
    """
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

def main():
    # Specify the path to your .txt file
    file_path = "example.txt"  # Replace with your .txt file path

    # Read the content of the file
    text = read_file(file_path)
    if text is None:
        return

    # Define the chunk size
    chunk_size = 100  # Adjust the chunk size as needed

    # Chunk the text
    chunks = chunk_text(text, chunk_size)

    # Print the chunks
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i + 1}:\n{chunk}\n")

if __name__ == "__main__":
    main()