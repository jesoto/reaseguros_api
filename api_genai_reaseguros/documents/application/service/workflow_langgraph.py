import os
import json
import logging
from typing import TypedDict, List, Dict, Any, Optional
from pathlib import Path

from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser
from pypdf import PdfReader

from documents.application.service.html_to_pdf_service import HtmlToPdfService

# Configure logging
logger = logging.getLogger(__name__)

# Define State
class AgentState(TypedDict):
    poliza_path: str
    contratos_paths: List[str]
    
    # Intermediate data
    comparison_data: Dict[str, Any]
    html_content: str  # Changed from latex_content
    
    # Final output
    pdf_bytes: Optional[bytes]
    output_path: Optional[str]

class ReasegurosWorkflow:
    def __init__(self):
        # Initialize Gemini
        # Ensure GOOGLE_API_KEY is in env
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            temperature=0
        )
        self.pdf_service = HtmlToPdfService()
        self._build_graph()

    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """Helper to extract text from PDF."""
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"Error reading PDF {pdf_path}: {e}")
            return f"Error reading PDF: {e}"

    def _read_prompt(self, filename: str) -> str:
        """Read prompt file."""
        # Assuming prompts are in d:\github\reaseguros_api\prompts
        # Adjust path if running from root or elsewhere
        # We'll try to find the absolute path relative to the project root
        project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
        prompt_path = project_root / "prompts" / filename
        
        if not prompt_path.exists():
             # Fallback: try hardcoded path from context
            prompt_path = Path("d:/github/reaseguros_api/prompts") / filename
            
        return prompt_path.read_text(encoding="utf-8")

    def node_destructurer(self, state: AgentState) -> Dict:
        """Agent 1: Deconstruct and Compare."""
        logger.info("--- Node: Deconstruct & Compare ---")
        print("--- Node: Deconstruct & Compare ---")
        
        poliza_text = self._extract_text_from_pdf(state["poliza_path"])
        print(f"DEBUG: Policy Text Length: {len(poliza_text)}")
        if len(poliza_text) < 100:
            print(f"DEBUG: Policy text content (first 100): {poliza_text}")
        
        contratos_text = []
        for path in state["contratos_paths"]:
            name = Path(path).name
            content = self._extract_text_from_pdf(path)
            print(f"DEBUG: Contract {name} Text Length: {len(content)}")
            contratos_text.append(f"--- Contract: {name} ---\n{content}")
        
        contratos_combined = "\n".join(contratos_text)
        
        if len(poliza_text.strip()) == 0:
            logger.error("Policy PDF text is empty (scanned?).")
            return {"comparison_data": {"error": "Policy PDF text is empty (scanned image?)."}}

        
        prompt_template = self._read_prompt("agent3.md")
        
        # Prepare input for LLM
        # Truncate if necessary (Flash handles ~1M tokens, should be fine)
        input_text = f"""
        {prompt_template}
        
        =============
        PÓLIZA (REFERENCIA):
        {poliza_text} 
        
        =============
        CONTRATOS DE REASEGURO:
        {contratos_combined}
        """
        
        try:
            response = self.llm.invoke(input_text)
            content = response.content
            
            # Parse JSON
            # Remove markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
                
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                logger.warning("Failed to parse JSON, returning raw content wrapped")
                data = {"raw_output": content}
                
            return {"comparison_data": data}
        except Exception as e:
            logger.error(f"Error in Destructurer Node: {e}")
            print(f"CRITICAL ERROR in Destructurer Node: {e}")
            with open("error.log", "w") as f:
                f.write(f"Error: {e}\n\n")
                import traceback
                traceback.print_exc(file=f)
            return {"comparison_data": {"error": str(e)}}

    def node_report_generator(self, state: AgentState) -> Dict:
        """Agent 2: Generate HTML Report."""
        logger.info("--- Node: Legal Report ---")
        print("--- Node: Legal Report ---")
        
        comparison_data = state["comparison_data"]
        prompt_template = self._read_prompt("agent5.md")
        
        input_text = f"""
        {prompt_template}
        
        =============
        DATOS DE COMPARACIÓN (JSON):
        {json.dumps(comparison_data, indent=2, ensure_ascii=False)}
        """
        
        try:
            response = self.llm.invoke(input_text)
            content = response.content
            
            # Extract HTML
            html_content = content
            if "```html" in content:
                html_content = content.split("```html")[1].split("```")[0]
            elif "```" in content and ("<!DOCTYPE html>" in content or "<html>" in content):
                 parts = content.split("```")
                 for p in parts:
                     if "<html>" in p or "<!DOCTYPE html>" in p:
                         html_content = p
                         break
            
            return {"html_content": html_content.strip()}
        except Exception as e:
            logger.error(f"Error in Report Node: {e}")
            return {"html_content": ""}

    def node_pdf_converter(self, state: AgentState) -> Dict:
        """Convert HTML to PDF."""
        logger.info("--- Node: PDF Converter (HTML) ---")
        print("--- Node: PDF Converter (HTML) ---")
        html = state["html_content"]
        
        if not html:
            logger.error("No HTML content to convert")
            return {"pdf_bytes": None}

        try:
            pdf_bytes = self.pdf_service.compile_html_to_pdf(html, filename="report_genai")
            return {"pdf_bytes": pdf_bytes}
        except Exception as e:
            logger.error(f"PDF Conversion failed: {e}")
            return {"pdf_bytes": None}

    def _build_graph(self):
        workflow = StateGraph(AgentState)
        
        workflow.add_node("deconstruct", self.node_destructurer)
        workflow.add_node("report", self.node_report_generator)
        workflow.add_node("pdf", self.node_pdf_converter)
        
        workflow.set_entry_point("deconstruct")
        workflow.add_edge("deconstruct", "report")
        workflow.add_edge("report", "pdf")
        workflow.add_edge("pdf", END)
        
        self.app = workflow.compile()

    def run(self, poliza_path: str, contratos_paths: List[str], output_pdf_path: str = "report.pdf"):
        inputs = {
            "poliza_path": poliza_path,
            "contratos_paths": contratos_paths,
            "comparison_data": {},
            "html_content": "",
            "pdf_bytes": None,
            "output_path": output_pdf_path
        }
        
        logger.info("Starting Workflow...")
        print("Starting Workflow...")
        result = self.app.invoke(inputs)
        
        if result.get("pdf_bytes"):
            # Ensure directory exists for output
            output_dir = os.path.dirname(output_pdf_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            with open(output_pdf_path, "wb") as f:
                f.write(result["pdf_bytes"])
            logger.info(f"PDF saved to {output_pdf_path}")
            print(f"PDF saved to {output_pdf_path}")
            return result
        else:
            logger.error("No PDF bytes generated.")
            print("No PDF bytes generated.")
            return result
