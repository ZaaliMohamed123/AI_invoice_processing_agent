"""
Extraction Node - Uses LLM to extract structured data from invoice text.
"""
from src.state import InvoiceState
from src.services.llm_service import extract_invoice_data, LLMExtractionError


def extraction_node(state: InvoiceState) -> dict:
    """
    Extract structured invoice data from raw text using LLM.
    
    Args:
        state: Current workflow state with pdf_text set
        
    Returns:
        Dict with state updates
    """
    # Check if pdf_text exists (ingest might have failed)
    pdf_text = state.get("pdf_text")
    
    if not pdf_text:
        return {
            "errors": ["Extraction Error: No PDF text available. Ingestion may have failed."]
        }
    
    try:
        # Call LLM to extract structured data
        invoice_data = extract_invoice_data(pdf_text)
        
        # Convert Pydantic model to dict for state update
        return invoice_data.to_state_dict()
        
    except LLMExtractionError as e:
        return {
            "errors": [f"LLM Extraction Error: {str(e)}"]
        }
    except Exception as e:
        return {
            "errors": [f"Unexpected error during extraction: {str(e)}"]
        }
