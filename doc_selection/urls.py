from django.urls import path
from .views import DocumentSelectionAPI

urlpatterns = [
    path('', DocumentSelectionAPI.as_view(), name='document_selection'),
]