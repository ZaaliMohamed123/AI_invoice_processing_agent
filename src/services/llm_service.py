"""
LLM Service - OpenAI integration for invoice data extraction.
"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from src.config.settings import OPENAI_API_KEY, OPENAI_BASE_URL
from src.models.invoice import InvoiceData


class LLMExtractionError(Exception):
    """Raised when LLM extraction fails."""
    pass


def get_llm(model: str = "gpt-4o-mini", temperature: float = 0) -> ChatOpenAI:
    """
    Create and return a configured ChatOpenAI instance.
    
    Args:
        model: OpenAI model name (default: gpt-4o-mini for cost efficiency)
        temperature: Randomness (0 = deterministic, good for extraction)
        
    Returns:
        Configured ChatOpenAI instance
    """
    if not OPENAI_API_KEY:
        raise LLMExtractionError(
            "OPENAI_API_KEY not set. Please add it to your .env file."
        )
    
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
    )


# Prompt template for invoice extraction
EXTRACTION_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an expert invoice data extractor. Your task is to extract 
structured data from invoice text with high accuracy.

Guidelines:
- Extract all available information from the invoice
- For dates, use YYYY-MM-DD format
- For currency, use standard codes (USD, EUR, GBP, etc.)
- Calculate tax_rate as a decimal (e.g., 0.10 for 10%)
- If a field is not present in the invoice, use null/None
- Ensure line item totals match quantity * unit_price
- Be precise with numbers - don't round unless necessary"""
    ),
    (
        "human",
        """Please extract all invoice data from the following text:

---
{invoice_text}
---

Extract the invoice number, vendor details, customer details, dates, 
line items, and all totals."""
    )
])


def extract_invoice_data(invoice_text: str) -> InvoiceData:
    """
    Extract structured invoice data from raw text using LLM.
    
    Args:
        invoice_text: Raw text extracted from invoice PDF
        
    Returns:
        InvoiceData object with all extracted fields
        
    Raises:
        LLMExtractionError: If extraction fails
    """
    try:
        # Get LLM with structured output
        llm = get_llm()
        
        # Create chain: prompt -> LLM with structured output
        # with_structured_output forces the LLM to return an InvoiceData object
        structured_llm = llm.with_structured_output(InvoiceData)
        
        # Create the chain
        chain = EXTRACTION_PROMPT | structured_llm
        
        # Invoke the chain with invoice text
        result = chain.invoke({"invoice_text": invoice_text})
        
        return result
        
    except Exception as e:
        raise LLMExtractionError(f"Failed to extract invoice data: {e}")


def get_extraction_chain():
    """
    Get the complete extraction chain for use in LangGraph nodes.
    
    Returns a chain that can be invoked with {"invoice_text": "..."}.
    """
    llm = get_llm()
    structured_llm = llm.with_structured_output(InvoiceData)
    return EXTRACTION_PROMPT | structured_llm
