from enum import Enum


class AgentCoreKey(str, Enum):
    DESESTRUCTURADOR_AGENT_KEY = "DESESTRUCTURAR_COMPARAR"
    RESUMEN_AGENT_KEY = "RESUMEN_GERENCIAL"

DEFAULT_AGENT_QUESTION = "Analiza los contratos y poliza"
#DEFAULT_ENABLE_EXTRACT_ENTITIES = False

QUESTION_AGENT_ENDPOINT = "api/agents/question"
#RETRIVAL_DOCS_ENDPOINT = "api/agents/retrival-documents"

#INVALID_AGGREGATING_DOCUMENTS = [AgentCoreKey.INITIAL_BUDGET_AGENT_KEY.value, AgentCoreKey.FINAL_BUDGET_AGENT_KEY.value]

#MAX_RETRIVAL_DOCUMENTS = 

DS_CONFIG = {
    "location": "global",
    "id": "vehicle-accident-sinister_1759985881351"
}