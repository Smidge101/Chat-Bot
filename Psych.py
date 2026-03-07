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
    Splits the text into semantic chunks based on patterns (e.g., course titles or semesters).
    """
    # Define a regex pattern to identify sections (e.g., "Semester 1", "Course: XYZ")
    pattern = r"(Semester\s+\d+|Course:\s+[^\n]+)"
    chunks = re.split(pattern, text)
    
    # Combine the pattern matches with their corresponding content
    semantic_chunks = []
    for i in range(1, len(chunks), 2):
        header = chunks[i].strip()
        content = chunks[i + 1].strip() if i + 1 < len(chunks) else ""
        semantic_chunks.append(f"{header}\n{content}")
    
    return semantic_chunks

def main():
    # Specify the path to your .txt file
    file_path = "C:\Users\Tyrique\Downloads\Comp Sci stuff\325\cs325_quiz2\Chat-Bot\Psych-B.A..txt"  # Replace with your .txt file path

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