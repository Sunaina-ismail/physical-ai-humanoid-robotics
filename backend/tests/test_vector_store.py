"""
Tests for the Vector Store functionality
"""

import pytest
from unittest.mock import Mock, patch
from app.services.vector_store import VectorStoreService


@pytest.fixture
def vector_store():
    """Create a vector store instance for testing"""
    with patch('app.services.vector_store.QdrantClient'):
        return VectorStoreService()


def test_vector_store_initialization(vector_store):
    """Test that the vector store initializes correctly"""
    assert vector_store is not None
    assert vector_store.collection_name == "chatkit-rag-textbook"
    assert vector_store.vector_size == 768
    assert vector_store.distance_metric is not None


def test_collection_exists_with_mock():
    """Test collection existence check with mock"""
    with patch('app.services.vector_store.QdrantClient') as mock_client:
        mock_instance = Mock()
        mock_instance.get_collections.return_value = Mock()
        mock_instance.get_collections().collections = [
            Mock(name="chatkit-rag-textbook")
        ]
        mock_client.return_value = mock_instance

        vector_store = VectorStoreService()
        result = vector_store.collection_exists()

        assert result is True