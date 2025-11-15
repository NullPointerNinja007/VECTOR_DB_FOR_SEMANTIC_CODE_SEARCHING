# VECTOR_DB_FOR_SEMANTIC_CODE_SEARCHING

A Python-based embedding service that indexes code snippets using LLM-generated compact descriptions and stores them in ChromaDB for semantic similarity search. Includes scripts to batch-index snippets from a structured text file and query the database using natural language queries.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

```python
from embedding_service import generate_compact_code_description, index_snippet_in_chroma

# Generate a compact description
code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""

description = generate_compact_code_description(code)
print(description)

# Index a code snippet in ChromaDB
uuid = "123e4567-e89b-12d3-a456-426614174000"
description = index_snippet_in_chroma(uuid, code)
print(f"Indexed snippet {uuid} with description: {description}")
```

## Functions

### `generate_compact_code_description(code: str, user_description: str | None = None) -> str`

Generates a highly specific, space-efficient description string for a code snippet using GPT-5.1.

### `index_snippet_in_chroma(uuid: str, code: str, user_description: str | None = None) -> str`

Generates a compact description, creates an embedding, and indexes it in ChromaDB. Returns the compact description string.

### `search_similar_snippets(query: str, k: int = 5) -> list[str]`

Searches for similar code snippets in ChromaDB using a text query. Returns the UUIDs of the top-k most similar snippets.

### `clear_vector_database() -> None`

Clears all entries from the ChromaDB vector database and recreates an empty collection ready for new entries.

## Scripts

- `index_snippets.py` - Batch indexes snippets from `snippets.txt` into the vector database
- `search_snippets.py` - Simple script to search for similar code snippets using natural language queries
- `test_embedding_service.py` - Test script for the embedding service functionality
