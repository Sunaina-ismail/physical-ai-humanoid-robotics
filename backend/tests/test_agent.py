#!/usr/bin/env python3
"""
Test script for RAG Agent with book-related questions
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from app.models import Query
from app.services.rag_agent import rag_agent
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

async def test_book_questions():
    """Test the RAG agent with multiple book-related questions."""

    book_questions = [
        "What is Physical AI and how does it differ from traditional AI approaches?",
        "Explain the key principles of humanoid robotics design.",
        "What are the main challenges in developing physical AI systems?",
        "How do humanoid robots differ from traditional robots?",
        "What is the significance of embodied intelligence in robotics?",
        "Explain the concept of Sim-to-Real transfer in robotics.",
        "What are the core components of a humanoid robot?",
        "How does machine learning apply to physical AI systems?"
    ]

    print("=" * 80)
    print("Testing RAG Agent with Book Questions")
    print("=" * 80)

    for i, question in enumerate(book_questions, 1):
        print(f"\nQuestion {i}: {question}")
        print("-" * 60)

        try:
            # Create query object
            query_obj = Query(query=question)

            # Process query through agent
            response = await rag_agent.query_chatbot(query_obj)

            print(f"Answer: {response.answer}")

            if response.citations:
                print(f"Citations ({len(response.citations)}):")
                for j, citation in enumerate(response.citations[:3], 1):  # Show first 3 citations
                    print(f"  {j}. {citation.format_citation()}")
                    print(f"     Snippet: {citation.snippet[:100]}...")
                    print(f"     Similarity: {citation.similarity_score:.2f}")
            else:
                print("No citations found")

            print(f"Confidence: {response.confidence}")
            print(f"Content Found: {response.content_found}")

        except Exception as e:
            print(f"Error processing question: {e}")

        print("-" * 60)

async def test_general_questions():
    """Test the RAG agent with general questions (should respond appropriately)."""

    general_questions = [
        "What's the weather like today?",
        "How do I make a cake?",
        "Tell me a joke.",
        "What is the capital of France?",
        "Explain quantum computing."
    ]

    print("\n" + "=" * 80)
    print("Testing RAG Agent with General Questions")
    print("=" * 80)

    for i, question in enumerate(general_questions, 1):
        print(f"\nGeneral Question {i}: {question}")
        print("-" * 60)

        try:
            # Create query object
            query_obj = Query(query=question)

            # Process query through agent
            response = await rag_agent.query_chatbot(query_obj)

            print(f"Answer: {response.answer}")

            if response.citations:
                print(f"Citations ({len(response.citations)}):")
                for j, citation in enumerate(response.citations[:3], 1):  # Show first 3 citations
                    print(f"  {j}. {citation.format_citation()}")
                    print(f"     Snippet: {citation.snippet[:100]}...")
                    print(f"     Similarity: {citation.similarity_score:.2f}")
            else:
                print("No citations found")

            print(f"Confidence: {response.confidence}")
            print(f"Content Found: {response.content_found}")

        except Exception as e:
            print(f"Error processing question: {e}")

        print("-" * 60)

async def main():
    """Run all tests."""
    await test_book_questions()
    await test_general_questions()

    print("\n" + "=" * 80)
    print("Testing completed!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())