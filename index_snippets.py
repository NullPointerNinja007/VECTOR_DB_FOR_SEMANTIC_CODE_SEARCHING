"""
Script to parse snippets.txt and index all snippets into the vector database.

This script:
1. Parses snippets from snippets.txt in the specified format
2. Clears the vector database
3. Indexes each snippet into ChromaDB
"""

from embedding_service import index_snippet_in_chroma, clear_vector_database
from typing import List, Dict, Optional


def parse_snippets(filename: str) -> List[Dict[str, str]]:
    """
    Parse snippets from a text file.
    
    Expected format:
    UUID: <uuid_string>
    DESCRIPTION: <description_string>
    CODE:
    <code content>
    ===END_SNIPPET===
    
    Args:
        filename: Path to the snippets file
        
    Returns:
        List of dictionaries with keys: uuid, description, code
    """
    snippets = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return snippets
    
    i = 0
    while i < len(lines):
        # Skip blank lines
        while i < len(lines) and not lines[i].strip():
            i += 1
        
        if i >= len(lines):
            break
        
        # Look for UUID line
        uuid = None
        description = None
        code_start = None
        code_lines = []
        
        # Parse UUID
        if lines[i].startswith("UUID:"):
            uuid = lines[i][5:].strip()  # Everything after "UUID:"
            i += 1
        else:
            # Skip until we find a UUID or next snippet delimiter
            while i < len(lines) and lines[i].strip() != "===END_SNIPPET===":
                i += 1
            if i < len(lines):
                i += 1  # Skip the delimiter
            continue
        
        # Skip blank lines
        while i < len(lines) and not lines[i].strip():
            i += 1
        
        if i >= len(lines):
            print(f"Warning: Snippet with UUID '{uuid}' is incomplete (missing DESCRIPTION and CODE). Skipping.")
            continue
        
        # Parse DESCRIPTION
        if lines[i].startswith("DESCRIPTION:"):
            description = lines[i][12:].strip()  # Everything after "DESCRIPTION:"
            i += 1
        else:
            print(f"Warning: Snippet with UUID '{uuid}' is missing DESCRIPTION. Skipping.")
            # Skip until delimiter
            while i < len(lines) and lines[i].strip() != "===END_SNIPPET===":
                i += 1
            if i < len(lines):
                i += 1
            continue
        
        # Skip blank lines
        while i < len(lines) and not lines[i].strip():
            i += 1
        
        if i >= len(lines):
            print(f"Warning: Snippet with UUID '{uuid}' is incomplete (missing CODE). Skipping.")
            continue
        
        # Parse CODE marker
        if lines[i].strip() == "CODE:":
            i += 1
            code_start = i
        else:
            print(f"Warning: Snippet with UUID '{uuid}' is missing CODE: marker. Skipping.")
            # Skip until delimiter
            while i < len(lines) and lines[i].strip() != "===END_SNIPPET===":
                i += 1
            if i < len(lines):
                i += 1
            continue
        
        # Collect code lines until delimiter
        while i < len(lines):
            line = lines[i]
            if line.strip() == "===END_SNIPPET===":
                break
            code_lines.append(line.rstrip('\n'))  # Remove trailing newline but preserve content
            i += 1
        
        # Check if we found the delimiter
        if i >= len(lines) or lines[i].strip() != "===END_SNIPPET===":
            print(f"Warning: Snippet with UUID '{uuid}' is missing ===END_SNIPPET=== delimiter. Skipping.")
            continue
        
        # Skip the delimiter
        i += 1
        
        # Validate we have all required fields
        if not uuid:
            print(f"Warning: Found snippet with missing UUID. Skipping.")
            continue
        
        if not description:
            print(f"Warning: Snippet with UUID '{uuid}' has missing DESCRIPTION. Skipping.")
            continue
        
        if not code_lines:
            print(f"Warning: Snippet with UUID '{uuid}' has empty CODE block. Skipping.")
            continue
        
        # Join code lines (preserve original structure, just rejoin with newlines)
        code = '\n'.join(code_lines)
        
        # Add snippet to list
        snippets.append({
            "uuid": uuid,
            "description": description,
            "code": code
        })
    
    return snippets


def main():
    """Main function to load snippets and index them into the vector database."""
    print("Starting snippet indexing process...")
    print()
    
    # Clear the vector database
    print("Clearing vector database...")
    try:
        clear_vector_database()
        print("✓ Vector database cleared successfully")
    except Exception as e:
        print(f"Error clearing vector database: {e}")
        return
    print()
    
    # Parse snippets from file
    print("Parsing snippets from snippets.txt...")
    snippets = parse_snippets("snippets.txt")
    
    if not snippets:
        print("No valid snippets found in snippets.txt")
        return
    
    print(f"✓ Found {len(snippets)} valid snippet(s) to index")
    print()
    
    # Index each snippet
    print("Indexing snippets into vector database...")
    successful = 0
    failed = 0
    
    for i, snippet in enumerate(snippets, 1):
        uuid = snippet["uuid"]
        description = snippet["description"]
        code = snippet["code"]
        
        print(f"[{i}/{len(snippets)}] Indexing UUID: {uuid}")
        
        try:
            index_snippet_in_chroma(uuid, code, description)
            successful += 1
            print(f"  ✓ Successfully indexed")
        except Exception as e:
            failed += 1
            print(f"  ✗ Failed to index: {e}")
        print()
    
    # Summary
    print("=" * 60)
    print(f"Indexing complete!")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Total: {len(snippets)}")
    print("=" * 60)


if __name__ == "__main__":
    main()

