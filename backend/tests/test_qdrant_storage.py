"""
Test script to verify book content is stored in Qdrant and test chatbot functionality
"""

import asyncio
import os
from pathlib import Path

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import settings
from app.services.vector_store import VectorStoreService
from app.services.rag_agent import rag_agent
from app.models import Query


def test_qdrant_connection():
    """Test connection to Qdrant and check collection info"""
    print("Testing Qdrant connection...")

    try:
        vector_store = VectorStoreService()

        # Check if collection exists
        exists = vector_store.collection_exists()
        print(f"Collection '{settings.qdrant_collection_name}' exists: {exists}")

        if exists:
            # Get collection info
            info = vector_store.get_collection_info()
            print(f"Collection info: {info}")

            # Count total points in collection
            total_points = vector_store.count_points()
            print(f"Total points in collection: {total_points}")

            # Count points by chapter if any exist
            if total_points > 0:
                # Try to get a sample of points to see the content
                sample_points = vector_store.client.scroll(
                    collection_name=settings.qdrant_collection_name,
                    limit=5  # Get first 5 points
                )

                print(f"\nSample of first {min(5, total_points)} points:")
                for i, point in enumerate(sample_points[0]):
                    payload = point.payload
                    print(f"  Point {i+1}:")
                    print(f"    Chapter: {payload.get('chapter_number', 'N/A')}")
                    print(f"    Section: {payload.get('section_title', 'N/A')}")
                    print(f"    Text snippet: {payload.get('text', '')[:100]}...")
                    print()

            return True, info
        else:
            print("Collection does not exist. You need to run setup_qdrant.py and ingest.py first.")
            return False, None

    except Exception as e:
        print(f"Error testing Qdrant connection: {e}")
        return False, None


def test_content_retrieval():
    """Test that we can retrieve content from the vector store"""
    print("\nTesting content retrieval...")

    try:
        # Test with a simple query
        test_query = "What is robotics?"
        print(f"Testing retrieval for query: '{test_query}'")

        retrieved_content = rag_agent.retrieve_book_content(test_query)
        print(f"Retrieved content: {retrieved_content[:200]}...")

        # If no content found, it might mean the collection is empty
        if "No relevant content found" in retrieved_content:
            print("No relevant content found - collection might be empty")
            return False
        else:
            print("Content retrieval successful")
            return True

    except Exception as e:
        print(f"Error retrieving content: {e}")
        return False


async def test_chatbot_response():
    """Test the chatbot response with a book-related question"""
    print("\nTesting chatbot response...")

    try:
        # Create a test query
        query = Query(query="What is Physical AI?")

        print(f"Testing chatbot with query: '{query.query}'")

        # Get response from the RAG agent
        response = await rag_agent.query_chatbot(query)

        print(f"Answer: {response.answer}")
        print(f"Content found: {response.content_found}")
        print(f"Confidence: {response.confidence}")
        print(f"Number of citations: {len(response.citations)}")

        if response.citations:
            print("\nCitations:")
            for i, citation in enumerate(response.citations, 1):
                print(f"  {i}. Chapter {citation.chapter_number}: {citation.chapter_title}")
                print(f"     Section: {citation.section_title}")
                print(f"     Snippet: {citation.snippet[:100]}...")

        return True

    except Exception as e:
        print(f"Error testing chatbot: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_ingestion_script():
    """Test the ingestion script by checking if book content exists"""
    print("\nTesting if book content exists in the expected location...")

    # Check if frontend/docs directory exists (source of book content)
    docs_path = Path(__file__).parent.parent.parent / "frontend" / "docs"

    if docs_path.exists():
        md_files = list(docs_path.glob("**/*.md"))
        print(f"Found {len(md_files)} markdown files in {docs_path}")

        if md_files:
            print("Sample files:")
            for file in md_files[:5]:  # Show first 5 files
                print(f"  - {file}")

        return len(md_files) > 0
    else:
        print(f"Directory {docs_path} does not exist")
        return False


def main():
    """Main test function"""
    print("="*60)
    print("Testing ChatKit RAG System")
    print("="*60)

    # Test 1: Qdrant connection and content
    qdrant_ok, collection_info = test_qdrant_connection()

    # Test 2: Content retrieval
    if qdrant_ok:
        retrieval_ok = test_content_retrieval()
    else:
        retrieval_ok = False
        print("Skipping content retrieval test due to Qdrant connection issues")

    # Test 3: Chatbot response
    if qdrant_ok:
        chatbot_ok = asyncio.run(test_chatbot_response())
    else:
        chatbot_ok = False
        print("Skipping chatbot test due to Qdrant connection issues")

    # Test 4: Check if book content exists for ingestion
    content_exists = test_ingestion_script()

    print("\n" + "="*60)
    print("Test Results:")
    print(f"  Qdrant Connection: {'PASS' if qdrant_ok else 'FAIL'}")
    print(f"  Content Retrieval: {'PASS' if retrieval_ok else 'FAIL'}")
    print(f"  Chatbot Response: {'PASS' if chatbot_ok else 'FAIL'}")
    print(f"  Book Content Exists: {'PASS' if content_exists else 'FAIL'}")
    print("="*60)

    if qdrant_ok and content_exists:
        print("\nTo populate the Qdrant database with book content, run:")
        print("1. python scripts/setup_qdrant.py")
        print("2. python scripts/ingest.py --source ../../frontend/docs")
        print("\nThen restart the backend and test again.")
    elif not qdrant_ok:
        print("\nQdrant is not configured properly. Check your .env file and run setup_qdrant.py")
    elif not content_exists:
        print("\nBook content not found. Make sure the frontend/docs directory contains markdown files.")


if __name__ == "__main__":
    main()