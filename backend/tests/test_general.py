#!/usr/bin/env python3
"""
Test script for RAG Agent with general/out-of-scope questions
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

async def test_general_question():
    """Test a general question to see how agent handles out-of-scope queries."""

    question = "What is the capital of France?"

    print("=" * 80)
    print("Testing RAG Agent - General Question (Out of Scope)")
    print("=" * 80)
    print(f"Question: {question}")
    print("-" * 60)

    try:
        # Create query object
        query_obj = Query(query=question)

        # Process query through agent
        response = await rag_agent.query_chatbot(query_obj)

        print(f"Answer: {response.answer}")

        if response.citations:
            print(f"Citations ({len(response.citations)}):")
            for j, citation in enumerate(response.citations, 1):
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
    print("Test completed!")

if __name__ == "__main__":
    asyncio.run(test_general_question())