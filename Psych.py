# Psych.py

import re

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

def semantic_chunking(text):
    """
    Splits the text into semantic chunks per semester.
    """
    pattern = r"(?m)^(Year\s+\d+\s*\([^)]*Semester[^)]*\))"
    parts = re.split(pattern, text)
    
    semantic_chunks = []
    i = 1
    while i < len(parts):
        header = parts[i].strip()
        if header:  # Skip if header is empty/whitespace
            content = parts[i + 1].strip() if i + 1 < len(parts) else ""
            chunk = f"{header}\n{content}".strip()
            if chunk:  # Only add non-empty chunks
                semantic_chunks.append(chunk)
        i += 2
    
    return semantic_chunks


def main():
    # Specify the path to your .txt file
    file_path = "Psych-B.A..txt"  # Replace with your .txt file path

    # Read the content of the file
    text = read_file(file_path)
    if text is None:
        return

    # Perform semantic chunking
    chunks = semantic_chunking(text)

    # Print the semantic chunks
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i + 1}:\n{chunk}\n")

if __name__ == "__main__":
    main()