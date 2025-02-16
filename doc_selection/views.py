from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import SelectedDocument, Document

class DocumentSelectionAPI(APIView):
    def post(self, request):
        """Select documents for RAG-based Q&A by title instead of ID."""
        user = request.user  # Assuming authentication is used
        titles = request.data.get("titles", [])  # ✅ Get document titles from request

        if not titles:
            return Response({"error": "No document titles provided"}, status=400)

        # Find documents based on titles
        documents = Document.objects.filter(title__in=titles)

        if not documents.exists():
            return Response({"error": "No matching documents found"}, status=400)

        # Store selected documents for user
        SelectedDocument.objects.filter(user=user).delete()  # Clear old selections
        SelectedDocument.objects.bulk_create(
            [SelectedDocument(user=user, document=doc) for doc in documents]
        )

        return Response(
            {"message": "Documents selected successfully", "selected_titles": titles},
            status=200,
        )

    def get(self, request):
        """Retrieve the list of selected documents by title."""
        user = request.user
        selected_titles = SelectedDocument.objects.filter(user=user).values_list("document__title", flat=True)
        return Response({"selected_titles": list(selected_titles)}, status=200)

    def delete(self, request):
        """Clear selected documents for the user."""
        user = request.user
        SelectedDocument.objects.filter(user=user).delete()
        return Response({"message": "Document selection cleared"}, status=200)
