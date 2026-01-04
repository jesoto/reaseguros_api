"""
Workflow View to expose LangGraph workflow.
"""
import os
import shutil
import tempfile
import uuid
import logging
from typing import List
from pathlib import Path

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.http import FileResponse

from documents.application.service.workflow_langgraph import ReasegurosWorkflow
from documents.domain.logger import get_logger
from documents.domain.constants.env_constants import LOGGING_TYPE

class WorkflowView(APIView):
    """
    API View to process the Reaseguros Workflow.
    Accepts:
    - poliza: File (PDF)
    - contratos: List of Files (PDFs)
    
    Returns:
    - PDF File (application/pdf)
    """
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):
        trace_id = str(uuid.uuid4())
        logger = get_logger("WorkflowView", LOGGING_TYPE)
        logger.set_trace(trace_id)
        
        logger.log_text(f"[API] New Workflow Request. TraceID: {trace_id}")
        
        try:
            # Validate Inputs
            poliza_file = request.FILES.get('poliza')
            contratos_files = request.FILES.getlist('contratos')
            
            if not poliza_file:
                return Response({"error": "No 'poliza' file provided"}, status=status.HTTP_400_BAD_REQUEST)
            
            if not contratos_files:
                return Response({"error": "No 'contratos' files provided"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create Temp Directory for this request
            with tempfile.TemporaryDirectory() as tmpdir:
                tmp_path = Path(tmpdir)
                
                # Save Poliza
                poliza_path = tmp_path / poliza_file.name
                with open(poliza_path, 'wb+') as f:
                    for chunk in poliza_file.chunks():
                        f.write(chunk)
                
                # Save Contratos
                contratos_paths = []
                for cf in contratos_files:
                    c_path = tmp_path / cf.name
                    with open(c_path, 'wb+') as f:
                        for chunk in cf.chunks():
                            f.write(chunk)
                    contratos_paths.append(str(c_path))
                
                # Define Output Path
                output_pdf_path = tmp_path / f"report_{trace_id}.pdf"
                
                # Run Workflow
                logger.log_text("[API] Starting Workflow...")
                workflow = ReasegurosWorkflow()
                result = workflow.run(
                    poliza_path=str(poliza_path),
                    contratos_paths=contratos_paths,
                    output_pdf_path=str(output_pdf_path)
                )
                
                # Check Result
                if result.get("pdf_bytes") and output_pdf_path.exists():
                    logger.log_text("[API] Workflow Success. Returning PDF.")
                    
                    # Open file in binary mode for streaming
                    # Note: FileResponse will close the file automatically
                    f = open(output_pdf_path, 'rb') 
                    response = FileResponse(f, content_type='application/pdf')
                    response['Content-Disposition'] = f'attachment; filename="report_reaseguros.pdf"'
                    return response
                else:
                    error_msg = "PDF was not generated."
                    if "comparison_data" in result and "error" in result["comparison_data"]:
                        error_msg = str(result["comparison_data"]["error"])
                        
                    logger.log_text(f"[API] Workflow Failed: {error_msg}", severity="ERROR")
                    return Response({
                        "error": "Workflow failed to generate PDF",
                        "details": error_msg
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            logger.log_text(f"[API] Critical Error: {str(e)}\n{error_trace}", severity="ERROR")
            
            return Response({
                "error": str(e),
                "details": error_trace,
                "trace_id": trace_id,
                "env_check": {
                    "google_api_key": "PRESENT" if os.environ.get('GOOGLE_API_KEY') else "MISSING",
                    "google_creds": "PRESENT" if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') else "MISSING"
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
