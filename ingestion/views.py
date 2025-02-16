from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from asgiref.sync import async_to_sync
from .models import Document
from .embeddings import EmbeddingGenerator

class DocumentIngestionAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if request.user.is_anonymous:
            return Response({"error": "Authentication required"}, status=401)
        title = request.data.get("title")
        content = request.data.get("content")

        if not title or not content:
            return Response({"error": "Title and content required"}, status=status.HTTP_400_BAD_REQUEST)

        embedding_generator = EmbeddingGenerator()
        embedding = async_to_sync(embedding_generator.generate_embedding)(content)  # Convert async to sync

        document = Document.objects.create(title=title, content=content, embedding=embedding)
        return Response({"message": "Document ingested successfully", "doc_id": document.id}, status=status.HTTP_201_CREATED)
