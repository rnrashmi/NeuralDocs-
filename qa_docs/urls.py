from django.urls import path
from qa_docs.views import QAAPI

urlpatterns = [
    path('', QAAPI.as_view(), name='qa_api'),
]