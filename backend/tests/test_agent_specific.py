#!/usr/bin/env python3
"""
Test script for RAG Agent with specific robotics questions
"""

import asyncio
import sys
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from app.models import Query
from app.services.rag_agent import rag_agent
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

async def test_specific_questions():
    """Test the RAG agent with specific robotics-related questions."""

    # Questions that might be more likely to find matches in the existing content
    specific_questions = [
        "What is Navigation2 (Nav2) in ROS 2?",
        "Explain ROS 2 navigation system",
        "What is the significance of Why This Matters section?",
        "Tell me about autonomous navigation in robotics",
        "What is the relationship between ROS and navigation?",
        "Explain the navigation stack for ROS 2",
        "What are the key components of ROS 2 navigation?",
        "How does autonomous navigation work in ROS 2?"
    ]

    print("=" * 80)
    print("Testing RAG Agent with Specific Robotics Questions")
    print("=" * 80)

    for i, question in enumerate(specific_questions, 1):
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
            # If it's a rate limit error, wait before continuing
            if "429" in str(e) or "quota" in str(e).lower():
                print("Rate limit hit, waiting 60 seconds before continuing...")
                await asyncio.sleep(60)

        print("-" * 60)

async def test_simple_questions():
    """Test the RAG agent with simpler questions."""

    simple_questions = [
        "What is robotics?",
        "Explain humanoid robots",
        "What is embodied intelligence?",
        "How do robots navigate?",
        "What are the components of a robot?"
    ]

    print("\n" + "=" * 80)
    print("Testing RAG Agent with Simple Questions")
    print("=" * 80)

    for i, question in enumerate(simple_questions, 1):
        print(f"\nSimple Question {i}: {question}")
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
            # If it's a rate limit error, wait before continuing
            if "429" in str(e) or "quota" in str(e).lower():
                print("Rate limit hit, waiting 60 seconds before continuing...")
                await asyncio.sleep(60)

        print("-" * 60)

async def main():
    """Run all tests."""
    await test_specific_questions()
    await test_simple_questions()

    print("\n" + "=" * 80)
    print("Testing completed!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())