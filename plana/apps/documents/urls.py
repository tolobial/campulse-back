"""List of URLs directly linked to operations that can be done on documents."""
from django.urls import path

from .views.document import DocumentList, DocumentRetrieveDestroy
from .views.document_upload import DocumentUploadListCreate

urlpatterns = [
    path("", DocumentList.as_view(), name="document_list"),
    path(
        "<int:pk>", DocumentRetrieveDestroy.as_view(), name="document_retrieve_destroy"
    ),
    path(
        "uploads",
        DocumentUploadListCreate.as_view(),
        name="document_upload_list_create",
    ),
]
