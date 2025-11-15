"""
Simple script to search for similar code snippets in the vector database.

Edit the QUERY variable to search for different code snippets.
"""

from embedding_service import search_similar_snippets

# Edit this variable to change your search query
QUERY = "function that computes imu accelerometer and gyro bias from sample data"

# Number of results to return (top-k)
K = 5


def main():
    """Search for similar snippets and print the UUIDs."""
    print("=" * 70)
    print(f"Query: {QUERY}")
    print(f"Requested top {K} results")
    print("=" * 70)
    print()
    
    try:
        results = search_similar_snippets(QUERY, k=K)
        
        if not results:
            print("No results found.")
        else:
            print(f"Found {len(results)} result(s):\n")
            for i, uuid in enumerate(results, 1):
                print(f"  {i}. {uuid}")
            print()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

