"""
Email Service - Send notifications via Gmail SMTP.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from src.config.settings import GMAIL_ADDRESS, GMAIL_APP_PASSWORD, NOTIFICATION_EMAIL


class EmailError(Exception):
    """Raised when email sending fails."""
    pass


def send_email(subject: str, body: str, to_email: str | None = None) -> bool:
    """
    Send an email notification via Gmail SMTP.
    
    Args:
        subject: Email subject line
        body: Email body (HTML supported)
        to_email: Recipient email
        
    Returns:
        True if email sent successfully
        
    Raises:
        EmailError: If email sending fails
    """
    # Use default recipient if not specified
    recipient = to_email or NOTIFICATION_EMAIL
    
    # Validate configuration
    if not GMAIL_ADDRESS:
        raise EmailError("GMAIL_ADDRESS not configured")
    if not GMAIL_APP_PASSWORD:
        raise EmailError("GMAIL_APP_PASSWORD not configured")
    if not recipient:
        raise EmailError("No recipient email specified")
    
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = GMAIL_ADDRESS
        message["To"] = recipient
        
        # Attach HTML body
        html_part = MIMEText(body, "html")
        message.attach(html_part)
        
        # Connect to Gmail SMTP server and send
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, recipient, message.as_string())
        
        return True
        
    except smtplib.SMTPAuthenticationError:
        raise EmailError(
            "Gmail authentication failed. Check your GMAIL_ADDRESS and GMAIL_APP_PASSWORD. "
            "Make sure you're using an App Password, not your regular Gmail password."
        )
    except smtplib.SMTPException as e:
        raise EmailError(f"SMTP error: {e}")
    except Exception as e:
        raise EmailError(f"Failed to send email: {e}")


def create_approval_email(state: dict) -> tuple[str, str]:
    """
    Create email content for an approved invoice.
    
    Args:
        state: Invoice state with extracted data
        
    Returns:
        Tuple of (subject, body)
    """
    invoice_number = state.get("invoice_number", "Unknown")
    vendor_name = state.get("vendor_name", "Unknown")
    total = state.get("total", 0)
    currency = state.get("currency", "USD")
    
    subject = f"Invoice Approved: {invoice_number} from {vendor_name}"
    
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: #28a745;">Invoice Approved</h2>
        
        <table style="border-collapse: collapse; width: 100%; max-width: 500px;">
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Invoice Number:</strong></td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">{invoice_number}</td>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Vendor:</strong></td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">{vendor_name}</td>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Total Amount:</strong></td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">{currency} {total:,.2f}</td>
            </tr>
            <tr>
                <td style="padding: 10px;"><strong>Status:</strong></td>
                <td style="padding: 10px; color: #28a745; font-weight: bold;">APPROVED</td>
            </tr>
        </table>
        
        <p style="margin-top: 20px; color: #666;">
            This invoice has passed all validation checks and business rules.
        </p>
    </body>
    </html>
    """
    
    return subject, body


def create_rejection_email(state: dict) -> tuple[str, str]:
    """
    Create email content for a rejected invoice.
    
    Args:
        state: Invoice state with extracted data and errors
        
    Returns:
        Tuple of (subject, body)
    """
    invoice_number = state.get("invoice_number", "Unknown")
    vendor_name = state.get("vendor_name", "Unknown")
    total = state.get("total", 0)
    currency = state.get("currency", "USD")
    errors = state.get("errors", [])
    
    subject = f"Invoice Rejected: {invoice_number} from {vendor_name}"
    
    # Format errors as HTML list
    errors_html = "".join([f"<li style='margin: 5px 0;'>{error}</li>" for error in errors])
    
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: #dc3545;">Invoice Rejected</h2>
        
        <table style="border-collapse: collapse; width: 100%; max-width: 500px;">
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Invoice Number:</strong></td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">{invoice_number}</td>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Vendor:</strong></td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">{vendor_name}</td>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Total Amount:</strong></td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">{currency} {total:,.2f}</td>
            </tr>
            <tr>
                <td style="padding: 10px;"><strong>Status:</strong></td>
                <td style="padding: 10px; color: #dc3545; font-weight: bold;">REJECTED</td>
            </tr>
        </table>
        
        <h3 style="margin-top: 20px; color: #dc3545;">Rejection Reasons:</h3>
        <ul style="background-color: #f8d7da; padding: 15px 30px; border-radius: 5px;">
            {errors_html}
        </ul>
        
        <p style="margin-top: 20px; color: #666;">
            Please review the issues above and resubmit the invoice after corrections.
        </p>
    </body>
    </html>
    """
    
    return subject, body
