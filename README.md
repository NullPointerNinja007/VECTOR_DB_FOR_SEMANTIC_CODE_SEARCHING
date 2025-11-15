# Embedding Service

A Python module for generating compact code descriptions using GPT-5.1 and indexing them in ChromaDB.

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

