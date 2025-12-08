"""
Tests for the RAG Agent functionality
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from app.services.rag_agent import RAGAgent
from app.models import Query
from app.config import settings


@pytest.fixture
def rag_agent():
    """Create a RAG agent instance for testing"""
    return RAGAgent()


@pytest.mark.asyncio
async def test_rag_agent_initialization(rag_agent):
    """Test that the RAG agent initializes correctly"""
    assert rag_agent is not None
    assert rag_agent.system_instructions is not None
    assert "Physical AI & Humanoid Robotics" in rag_agent.system_instructions


@pytest.mark.asyncio
async def test_retrieve_book_content_empty_query(rag_agent):
    """Test that retrieving content with empty query returns appropriate message"""
    result = rag_agent.retrieve_book_content("")
    assert "No relevant content found" in result or "Error" in result


@pytest.mark.asyncio
async def test_retrieve_book_content_with_mock(rag_agent):
    """Test content retrieval with mocked vector store"""
    # Mock the embedding service and vector store
    with patch.object(rag_agent.embedding_service, 'generate_query_embedding') as mock_embedding, \
         patch.object(rag_agent.vector_store, 'search_book_content') as mock_search:

        # Set up mocks
        mock_embedding.return_value = [0.1] * 768  # Mock embedding
        mock_search.return_value = [
            {
                "text": "This is a test content",
                "chapter_number": 1,
                "chapter_title": "Test Chapter",
                "section_title": "Test Section",
                "similarity_score": 0.8
            }
        ]

        # Test the method
        result = rag_agent.retrieve_book_content("test query")

        # Verify mocks were called
        mock_embedding.assert_called_once_with("test query")
        mock_search.assert_called_once()

        # Verify result contains expected content
        assert "Test Chapter" in result
        assert "This is a test content" in result


@pytest.mark.asyncio
async def test_query_chatbot_with_mock(rag_agent):
    """Test the full query chatbot flow with mocks"""
    # Create a test query
    query = Query(query="What is robotics?")

    # Mock the embedding service and vector store
    with patch.object(rag_agent.embedding_service, 'generate_query_embedding') as mock_embedding, \
         patch.object(rag_agent.vector_store, 'search_book_content') as mock_search:

        # Set up mocks
        mock_embedding.return_value = [0.1] * 768  # Mock embedding
        mock_search.return_value = [
            {
                "text": "Robotics is the field that deals with robots",
                "chapter_number": 1,
                "chapter_title": "Introduction to Robotics",
                "section_title": "What is Robotics",
                "similarity_score": 0.85
            }
        ]

        # Mock the agent runner
        with patch('app.services.rag_agent.Runner') as mock_runner:
            mock_result = MagicMock()
            mock_result.final_output = "Robotics is the field that deals with robots"
            mock_runner.run.return_value = mock_result

            # Test the method
            response = await rag_agent.query_chatbot(query)

            # Verify the response
            assert response.answer is not None
            assert len(response.citations) > 0
            assert response.content_found is True