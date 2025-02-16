import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework import status
from ingestion.models import Document
from ingestion.views import DocumentIngestionAPI
from ingestion.embeddings import EmbeddingGenerator

# Mock the EmbeddingGenerator
class MockEmbeddingGenerator:
    async def generate_embedding(self, content):
        return [0.1, 0.2, 0.3]  # Mock embedding

@pytest.fixture
def api_request_factory():
    return APIRequestFactory()

@pytest.fixture
def authenticated_user():
    user = User.objects.create_user(username='testuser', password='testpass123')
    return user

@pytest.fixture
def mock_embedding_generator(monkeypatch):
    monkeypatch.setattr(EmbeddingGenerator, 'generate_embedding', MockEmbeddingGenerator().generate_embedding)

@pytest.mark.django_db
def test_document_ingestion_unauthenticated(api_request_factory):
    request = api_request_factory.post('/api/documents/', {'title': 'Test Title', 'content': 'Test Content'})
    view = DocumentIngestionAPI.as_view()
    response = view(request)
    assert response.status_code == status.HTTP_403_FORBIDDEN  # Updated to 403
    assert response.data['detail'] == 'Authentication credentials were not provided.'  # Updated error message

@pytest.mark.django_db
def test_document_ingestion_authenticated_missing_fields(api_request_factory, authenticated_user):
    request = api_request_factory.post('/api/documents/', {'title': 'Test Title'})
    request.user = authenticated_user
    view = DocumentIngestionAPI.as_view()
    response = view(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['error'] == 'Title and content required'

@pytest.mark.django_db
def test_document_ingestion_success(api_request_factory, authenticated_user, mock_embedding_generator):
    request = api_request_factory.post('/api/documents/', {'title': 'Test Title', 'content': 'Test Content'})
    request.user = authenticated_user
    view = DocumentIngestionAPI.as_view()
    response = view(request)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['message'] == 'Document ingested successfully'
    assert 'doc_id' in response.data

    # Verify the document was created in the database
    document = Document.objects.get(id=response.data['doc_id'])
    assert document.title == 'Test Title'
    assert document.content == 'Test Content'
    assert document.embedding == [0.1, 0.2, 0.3]  # Mocked embedding

@pytest.mark.django_db
def test_document_ingestion_embedding_failure(api_request_factory, authenticated_user, monkeypatch):
    # Simulate an error in the embedding generator
    async def mock_generate_embedding_failure(self, content):  # Add self and make it async
        raise Exception("Embedding generation failed")

    monkeypatch.setattr(EmbeddingGenerator, 'generate_embedding', mock_generate_embedding_failure)

    request = api_request_factory.post('/api/documents/', {'title': 'Test Title', 'content': 'Test Content'})
    request.user = authenticated_user
    view = DocumentIngestionAPI.as_view()
    response = view(request)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert 'error' in response.data