"""
Example Axon plugin - Email notifications using SMTP.
This demonstrates how to create and package an Axon plugin.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import os

def send_email(
    to: str,
    subject: str,
    body: str,
    from_email: Optional[str] = None,
    smtp_server: Optional[str] = None,
    smtp_port: int = 587
) -> str:
    """
    Send an email using SMTP.
    
    Args:
        to: Recipient email address
        subject: Email subject line
        body: Email body content
        from_email: Sender email (defaults to SMTP_FROM_EMAIL env var)
        smtp_server: SMTP server address (defaults to SMTP_SERVER env var)
        smtp_port: SMTP port (default: 587)
        
    Returns:
        Success or error message
        
    Environment Variables:
        SMTP_SERVER: SMTP server address
        SMTP_PORT: SMTP port (default: 587)
        SMTP_FROM_EMAIL: Sender email address
        SMTP_PASSWORD: SMTP password
    """
    # Get configuration from environment or parameters
    smtp_server = smtp_server or os.environ.get('SMTP_SERVER')
    from_email = from_email or os.environ.get('SMTP_FROM_EMAIL')
    password = os.environ.get('SMTP_PASSWORD')
    
    if not all([smtp_server, from_email, password]):
        return "❌ Error: Missing SMTP configuration (SMTP_SERVER, SMTP_FROM_EMAIL, SMTP_PASSWORD)"
    
    try:
        # Create message
        message = MIMEMultipart()
        message['From'] = from_email
        message['To'] = to
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        
        # Connect to SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, password)
            server.send_message(message)
        
        return f"✅ Email sent to {to}"
        
    except smtplib.SMTPAuthenticationError:
        return "❌ Error: SMTP authentication failed. Check your credentials."
    except smtplib.SMTPException as e:
        return f"❌ SMTP Error: {str(e)}"
    except Exception as e:
        return f"❌ Error sending email: {str(e)}"


def send_notification(recipient: str, message: str) -> str:
    """
    Send a simple notification email.
    
    Args:
        recipient: Email address to notify
        message: Notification message
        
    Returns:
        Success or error message
    """
    return send_email(
        to=recipient,
        subject="Notification from Axon Agent",
        body=message
    )


# Example usage
if __name__ == "__main__":
    # Set environment variables first:
    # export SMTP_SERVER="smtp.gmail.com"
    # export SMTP_FROM_EMAIL="your-email@gmail.com"  
    # export SMTP_PASSWORD="your-app-password"
    
    result = send_email(
        to="recipient@example.com",
        subject="Test from Axon Plugin",
        body="This is a test email from the Axon email plugin!"
    )
    print(result)
