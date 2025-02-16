from django.db import models
from django.contrib.auth.models import User
from ingestion.models import Document

class SelectedDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "document")
