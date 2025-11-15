"""
Test script for embedding_service module.

This script demonstrates how to use the generate_compact_code_description
and index_snippet_in_chroma functions.
"""

import uuid
from embedding_service import generate_compact_code_description, index_snippet_in_chroma


def test_generate_description():
    """Test generating compact descriptions for different code snippets."""
    print("=" * 80)
    print("TEST 1: Generate Compact Description - Simple Function")
    print("=" * 80)
    
    code1 = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
    
    try:
        description = generate_compact_code_description(code1)
        print(f"Code:\n{code1}")
        print(f"\nCompact Description:\n{description}\n")
    except Exception as e:
        print(f"Error: {e}\n")
    
    print("=" * 80)
    print("TEST 2: Generate Compact Description - FastAPI Endpoint")
    print("=" * 80)
    
    code2 = """
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session

@app.post("/users")
async def create_user(user_data: dict, db: Session):
    if not user_data.get("email"):
        raise HTTPException(status_code=400, detail="Email required")
    user = User(**user_data)
    db.add(user)
    db.commit()
    return {"user_id": user.id}
"""
    
    try:
        description = generate_compact_code_description(code2)
        print(f"Code:\n{code2}")
        print(f"\nCompact Description:\n{description}\n")
    except Exception as e:
        print(f"Error: {e}\n")
    
    print("=" * 80)
    print("TEST 3: Generate Compact Description - With User Description")
    print("=" * 80)
    
    code3 = """
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
"""
    
    user_desc = "This is a binary search algorithm for finding elements in a sorted array"
    
    try:
        description = generate_compact_code_description(code3, user_description=user_desc)
        print(f"Code:\n{code3}")
        print(f"User Description: {user_desc}")
        print(f"\nCompact Description:\n{description}\n")
    except Exception as e:
        print(f"Error: {e}\n")


def test_index_in_chroma():
    """Test indexing code snippets in ChromaDB."""
    print("=" * 80)
    print("TEST 4: Index Code Snippet in ChromaDB")
    print("=" * 80)
    
    test_uuid = str(uuid.uuid4())
    code = """
import requests

def fetch_user_data(user_id: int) -> dict:
    response = requests.get(f"https://api.example.com/users/{user_id}", timeout=5)
    response.raise_for_status()
    return response.json()
"""
    
    try:
        description = index_snippet_in_chroma(test_uuid, code)
        print(f"UUID: {test_uuid}")
        print(f"Code:\n{code}")
        print(f"\nIndexed with description:\n{description}\n")
        print("✓ Successfully indexed in ChromaDB!")
    except Exception as e:
        print(f"Error: {e}\n")
    
    print("=" * 80)
    print("TEST 5: Index Multiple Snippets")
    print("=" * 80)
    
    snippets = [
        {
            "code": """
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
""",
            "desc": "Quick sort implementation"
        },
        {
            "code": """
async def send_email(to: str, subject: str, body: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.email.com/send",
            json={"to": to, "subject": subject, "body": body}
        ) as resp:
            return await resp.json()
""",
            "desc": None
        }
    ]
    
    for i, snippet in enumerate(snippets, 1):
        test_uuid = str(uuid.uuid4())
        try:
            description = index_snippet_in_chroma(
                test_uuid,
                snippet["code"],
                user_description=snippet["desc"]
            )
            print(f"\nSnippet {i} (UUID: {test_uuid})")
            print(f"Description: {description}")
            print("✓ Indexed successfully!")
        except Exception as e:
            print(f"\nSnippet {i} - Error: {e}")


def test_verify_chroma_collection():
    """Verify that items were stored in ChromaDB by querying the collection."""
    print("\n" + "=" * 80)
    print("TEST 6: Verify ChromaDB Collection")
    print("=" * 80)
    
    try:
        import chromadb
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_collection("snippets")
        
        count = collection.count()
        print(f"Total snippets in collection: {count}")
        
        if count > 0:
            # Get a few samples
            results = collection.get(limit=min(3, count))
            print(f"\nSample entries:")
            for i, (uuid_val, metadata) in enumerate(zip(results["ids"], results["metadatas"]), 1):
                print(f"\n  {i}. UUID: {uuid_val}")
                print(f"     Description: {metadata.get('compact_description', 'N/A')[:100]}...")
    except Exception as e:
        print(f"Error querying collection: {e}")


def main():
    """Run all tests."""
    print("\n" + "🚀 Starting Embedding Service Tests" + "\n")
    
    # Test description generation
    test_generate_description()
    
    # Test indexing
    test_index_in_chroma()
    
    # Verify ChromaDB
    test_verify_chroma_collection()
    
    print("\n" + "=" * 80)
    print("✅ All tests completed!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()

