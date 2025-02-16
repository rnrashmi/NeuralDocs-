from django.urls import path
from .views import DocumentIngestionAPI

urlpatterns = [
    path('ingest/', DocumentIngestionAPI.as_view(), name='document_ingestion'),
]