import asyncio
import numpy as np
from django.core.management.base import BaseCommand
from ingestion.models import Document
from faker import Faker
from asgiref.sync import sync_to_async

fake = Faker()

class FakeEmbeddingGenerator:
    def __init__(self, embedding_dim=384):  # Adjust dimension if needed
        self.embedding_dim = embedding_dim

    async def generate_embedding(self, text):
        # Generate a random normalized embedding
        embedding = np.random.rand(self.embedding_dim)
        return embedding / np.linalg.norm(embedding)

class Command(BaseCommand):
    help = "Generate fake documents and store embeddings"

    def handle(self, *args, **options):
        asyncio.run(self.create_fake_documents_and_embeddings())

    async def create_fake_documents_and_embeddings(self):
        self.stdout.write("Checking for existing documents...")

        documents = await sync_to_async(list)(Document.objects.all())

        if not documents:
            self.stdout.write("No documents found. Creating fake documents...")
            await self.create_fake_documents(10)  # Create 10 fake documents

        self.stdout.write("Generating fake embeddings for documents...")
        documents = await sync_to_async(list)(Document.objects.filter(embedding__isnull=True))

        if not documents:
            self.stdout.write(self.style.SUCCESS("All documents already have embeddings."))
            return

        embedding_generator = FakeEmbeddingGenerator()
        tasks = [self.generate_and_save_embedding(doc, embedding_generator) for doc in documents]

        await asyncio.gather(*tasks)
        self.stdout.write(self.style.SUCCESS(f"Successfully generated embeddings for {len(documents)} documents."))

    async def create_fake_documents(self, count):
        """Generate and save fake documents."""
        for _ in range(count):
            doc = Document(title=fake.sentence(), content=fake.paragraph())
            await sync_to_async(doc.save)()
            self.stdout.write(self.style.SUCCESS(f"Created document: {doc.title}"))

    async def generate_and_save_embedding(self, document, embedding_generator):
        """Generate embeddings asynchronously and save them."""
        embedding = await embedding_generator.generate_embedding(document.content)
        await sync_to_async(self.save_document_embedding)(document, embedding)

    def save_document_embedding(self, document, embedding):
        """Runs the database operation synchronously."""
        document.embedding = embedding.tolist()  # Convert numpy array to list before saving
        document.save()
