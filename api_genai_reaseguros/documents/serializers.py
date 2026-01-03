"""
Serializers for API request/response validation.
"""
from rest_framework import serializers


class Agent1DesestructurarCompararSerializer(serializers.Serializer):
    """
    Serializer for Agent 1: DESESTRUCTURAR_COMPARAR
    
    Request body:
    {
        "files": [
            "gs://bucket/path/to/poliza.pdf",
            "gs://bucket/path/to/contrato1.pdf",
            "gs://bucket/path/to/contrato2.pdf"
        ]
    }
    """
    files = serializers.ListField(
        child=serializers.CharField(),
        required=True,
        allow_empty=False,
        help_text="Lista de URIs de GCS: primero la póliza, luego los contratos de reaseguro"
    )
    
    def validate_files(self, value):
        """Validate that URIs start with gs:// and at least 2 files are provided"""
        if len(value) < 2:
            raise serializers.ValidationError(
                "Se requieren al menos 2 archivos: 1 póliza y 1+ contratos"
            )
        
        for uri in value:
            if not uri.startswith('gs://'):
                raise serializers.ValidationError(
                    f"El URI '{uri}' debe comenzar con 'gs://'"
                )
        return value


class Agent2ResumenGerencialSerializer(serializers.Serializer):
    """
    Serializer for Agent 2: RESUMEN_GERENCIAL
    
    Request body:
    {
        "comparacion_data": {...}  // Output from Agent 1
    }
    """
    comparacion_data = serializers.DictField(
        required=True,
        help_text="JSON estructurado con datos de póliza y comparación (output del Agente 1)"
    )


class EmailPdfSerializer(serializers.Serializer):
    """
    Serializer for email PDF delivery.
    
    Request body:
    {
        "trace_id": "abc123...",
        "recipient_email": "user@example.com"
    }
    """
    trace_id = serializers.CharField(
        required=True,
        help_text="Trace ID del reporte generado"
    )
    recipient_email = serializers.EmailField(
        required=True,
        help_text="Email del destinatario"
    )
