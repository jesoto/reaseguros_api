"""
URL configuration for documents app.
"""
from django.urls import path
from documents.views.workflow_view import WorkflowView

urlpatterns = [
    path("process-workflow", WorkflowView.as_view(), name="process-workflow"),
]
