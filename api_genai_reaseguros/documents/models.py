from django.db import models
from documents.application.constants.app_constants import DEFAULT_AGENT_QUESTION
# Create your models here.
class AgentGarden(models.Model):
    api_core_id = models.IntegerField(verbose_name="api_core_id")
    document_type = models.TextField(default=list, verbose_name="document_type")
    prompt = models.TextField(verbose_name="prompt", default=DEFAULT_AGENT_QUESTION)
    

    uploaded_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        db_table = "AgentGarden"   # <- nombre exacto de la tabla en la BD
        # opcional: verbose_name, ordering, etc.


    def __str__(self):
        return f"{self.api_core_id} - {self.document_type}"
