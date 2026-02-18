"""
LangGraph Workflow Definition - Wires all nodes together.
"""
from langgraph.graph import StateGraph, START, END

from src.state import InvoiceState
from src.nodes.ingest import ingest_node
from src.nodes.extraction import extraction_node
from src.nodes.validation import validation_node
from src.nodes.business_rules import business_rules_node
from src.nodes.notification import notification_node


def create_invoice_workflow() -> StateGraph:
    """
    Create and compile the invoice processing workflow.
    
    Returns:
        Compiled LangGraph workflow ready to invoke
    """
    # Create the graph builder with our state schema
    builder = StateGraph(InvoiceState)
    
    # ADD NODES
    builder.add_node("ingest", ingest_node)
    builder.add_node("extraction", extraction_node)
    builder.add_node("validation", validation_node)
    builder.add_node("business_rules", business_rules_node)
    builder.add_node("notification", notification_node)
    
    # ADD EDGES
    builder.add_edge(START, "ingest")
    builder.add_edge("ingest", "extraction")
    builder.add_edge("extraction", "validation")
    builder.add_edge("validation", "business_rules")
    builder.add_edge("business_rules", "notification")
    builder.add_edge("notification", END)
    
    # COMPILE
    workflow = builder.compile()
    
    return workflow


def process_invoice(pdf_path: str) -> dict:
    """
    Process an invoice PDF through the complete workflow
    
    Args:
        pdf_path: Path to the invoice PDF file
        
    Returns:
        Final state dict with all extracted data and processing results
    """
    # Create the workflow
    workflow = create_invoice_workflow()
    
    # Initial state
    initial_state = {
        "pdf_path": pdf_path,
        "errors": [],  # Initialize empty errors list 
    }
    
    # Invoke the workflow
    final_state = workflow.invoke(initial_state)
    
    return final_state


# Create a singleton workflow instance for reuse
_workflow_instance = None


def get_workflow():
    """
    Get or create the workflow instance (singleton pattern).
    
    Returns:
        Compiled LangGraph workflow
    """
    global _workflow_instance
    if _workflow_instance is None:
        _workflow_instance = create_invoice_workflow()
    return _workflow_instance
