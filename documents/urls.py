from django.urls import path
from .api import ProcessDocumentView

urlpatterns = [
    path("documents/process/", ProcessDocumentView.as_view()),
]
