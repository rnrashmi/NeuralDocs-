from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from ingestion.models import Document
from doc_selection.models import SelectedDocument
from ingestion.embeddings import EmbeddingGenerator
from asgiref.sync import async_to_sync

class QAAPI(APIView):
    def post(self, request):
        question = request.data.get("question")
        user = request.user  # Get the authenticated user

        if not question:
            return Response({"error": "Question required"}, status=400)

        # Retrieve selected document titles for this user
        selected_titles = list(SelectedDocument.objects.filter(user=user).values_list("document__title", flat=True))

        if not selected_titles:
            return Response({"error": "No selected documents. Use the selection API first."}, status=400)

        # Retrieve document IDs based on selected titles
        selected_doc_ids = list(Document.objects.filter(title__in=selected_titles).values_list("id", flat=True))

        # Generate query embedding
        embedding_generator = EmbeddingGenerator()
        query_embedding = async_to_sync(embedding_generator.generate_embedding)(question)

        # Convert numpy array to SQL-compatible string format
        embedding_str = "[" + ", ".join(map(str, query_embedding.tolist())) + "]"

        # Use raw SQL with pgvector for similarity search (filter by selected documents)
        placeholders = ', '.join(['%s'] * len(selected_doc_ids))
        query = f"""
            SELECT id, title, content
            FROM ingestion_document
            WHERE id IN ({placeholders})
            ORDER BY embedding <=> %s
            LIMIT 5;
        """

        with connection.cursor() as cursor:
            cursor.execute(query, selected_doc_ids + [embedding_str])
            results = cursor.fetchall()

        retrieved_docs = [{"title": row[1], "content": row[2]} for row in results]
        return Response({"retrieved_docs": retrieved_docs}, status=200)
