"""
Generic Email Sender for Excel Files
=====================================
This script sends all Excel files from a specified folder as email attachments.

Configuration:
- Update the email configuration section below with your email credentials
- Update the folder path to point to the folder containing Excel files
- Update recipient email address(es) - supports single email or list of emails
- Update CC email address(es) - supports single email, list of emails, or None

Usage:
    python send_excel_files_email.py
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
import glob

# ============================================================================
# EMAIL CONFIGURATION - UPDATE THESE VALUES
# ============================================================================
# Gmail SMTP Configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# Sender Email Credentials
SENDER_EMAIL = 'muthumurugan.ramalingam@hirepro.in'  # Update with your email
SENDER_PASSWORD = 'ptzu xykm khiv qexr'  # Update with your Gmail app password

# Recipient Email(s) - Can be a single email string or a list of emails
# Example: RECIPIENT_EMAIL = 'recipient@example.com'
# Example: RECIPIENT_EMAIL = ['recipient1@example.com', 'recipient2@example.com']
RECIPIENT_EMAIL = ['pooja.nagendran@hirepro.in']  # Update with recipient email(s)

# CC Email(s) - Can be a single email string, a list of emails, or None/empty list
# Example: CC_EMAIL = None  # No CC
# Example: CC_EMAIL = 'cc@example.com'
# Example: CC_EMAIL = ['cc1@example.com', 'cc2@example.com']
CC_EMAIL = ['muthumurugan.ramalingam@hirepro.in', 'ashwini.bannadabhavi@hirepro.in']  # Update with CC email(s) or leave as None

# Email Subject and Body
EMAIL_SUBJECT = 'Automation Reports'
EMAIL_BODY = """
Hello,

Please find attached all Excel files from the assessment automation script.

This is an automated email.

Best regards,
Assessment Team
"""

# ============================================================================
# FOLDER CONFIGURATION - UPDATE THIS PATH
# ============================================================================
# Folder path containing Excel files to send
# Example: '/Users/senthil/Desktop/ASSESSMENT/PythonWorkingScripts_Output/dumped_questions'
FOLDER_PATH = '/Users/senthil/Desktop/ASSESSMENT/PythonWorkingScripts_Output/'  # Update this path

# Excel file extensions to look for
EXCEL_EXTENSIONS = ['.xls', '.xlsx']


class ExcelFileEmailSender:
    """Generic class to send Excel files from a folder via email"""

    def __init__(self, folder_path, sender_email, sender_password, recipient_email,
                 cc_email=None, smtp_server=SMTP_SERVER, smtp_port=SMTP_PORT):
        """
        Initialize the email sender
        
        Args:
            folder_path: Path to folder containing Excel files
            sender_email: Email address of sender
            sender_password: Password or app password for sender email
            recipient_email: Email address(es) of recipient(s) - can be string or list
            cc_email: Email address(es) for CC - can be string, list, or None
            smtp_server: SMTP server address (default: Gmail)
            smtp_port: SMTP server port (default: 587)
        """
        self.folder_path = Path(folder_path)
        self.sender_email = sender_email
        self.sender_password = sender_password
        
        # Normalize recipient_email to list
        if isinstance(recipient_email, str):
            self.recipient_emails = [recipient_email]
        elif isinstance(recipient_email, list):
            self.recipient_emails = recipient_email
        else:
            self.recipient_emails = []
        
        # Normalize cc_email to list
        if cc_email is None:
            self.cc_emails = []
        elif isinstance(cc_email, str):
            self.cc_emails = [cc_email]
        elif isinstance(cc_email, list):
            self.cc_emails = cc_email
        else:
            self.cc_emails = []
        
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def find_excel_files(self):
        """
        Find all Excel files in the specified folder
        
        Returns:
            List of Path objects for Excel files found
        """
        excel_files = []
        
        if not self.folder_path.exists():
            print(f"Error: Folder path does not exist: {self.folder_path}")
            return excel_files
        
        if not self.folder_path.is_dir():
            print(f"Error: Path is not a directory: {self.folder_path}")
            return excel_files
        
        print(f"Searching for Excel files in: {self.folder_path}")
        
        # Search for Excel files with all specified extensions
        for ext in EXCEL_EXTENSIONS:
            pattern = str(self.folder_path / f'*{ext}')
            files = glob.glob(pattern, recursive=False)
            excel_files.extend([Path(f) for f in files])
        
        # Also search in subdirectories if needed (optional)
        # Uncomment below if you want to search recursively
        # for ext in EXCEL_EXTENSIONS:
        #     pattern = str(self.folder_path / f'**/*{ext}')
        #     files = glob.glob(pattern, recursive=True)
        #     excel_files.extend([Path(f) for f in files])
        
        # Remove duplicates and sort
        excel_files = sorted(set(excel_files))
        
        print(f"Found {len(excel_files)} Excel file(s)")
        for file in excel_files:
            print(f"  - {file.name}")
        
        return excel_files

    def send_email_with_attachments(self, excel_files, subject, body):
        """
        Send email with Excel files as attachments
        
        Args:
            excel_files: List of Path objects for Excel files to attach
            subject: Email subject
            body: Email body text
        
        Returns:
            True if email sent successfully, False otherwise
        """
        if not excel_files:
            print("No Excel files found to send. Exiting.")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            
            # Set TO addresses (comma-separated string for header)
            msg['To'] = ', '.join(self.recipient_emails)
            
            # Set CC addresses if any
            if self.cc_emails:
                msg['Cc'] = ', '.join(self.cc_emails)
            
            msg['Subject'] = subject
            
            # Add body to email
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach Excel files
            for excel_file in excel_files:
                if excel_file.exists() and excel_file.is_file():
                    try:
                        with open(excel_file, 'rb') as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                        
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {excel_file.name}'
                        )
                        msg.attach(part)
                        print(f"Attached: {excel_file.name}")
                    except Exception as e:
                        print(f"Error attaching {excel_file.name}: {str(e)}")
                else:
                    print(f"Warning: File not found or not a file: {excel_file}")
            
            # Create SMTP session
            print(f"\nConnecting to SMTP server: {self.smtp_server}:{self.smtp_port}")
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Enable security
            server.login(self.sender_email, self.sender_password)
            
            # Send email
            text = msg.as_string()
            
            # Combine TO and CC recipients for sendmail
            all_recipients = self.recipient_emails + self.cc_emails
            
            print(f"Sending email to: {', '.join(self.recipient_emails)}")
            if self.cc_emails:
                print(f"CC: {', '.join(self.cc_emails)}")
            
            server.sendmail(self.sender_email, all_recipients, text)
            server.quit()
            
            print(f"\n✓ Email sent successfully!")
            print(f"  Sent {len(excel_files)} file(s)")
            print(f"  TO: {', '.join(self.recipient_emails)}")
            if self.cc_emails:
                print(f"  CC: {', '.join(self.cc_emails)}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print("Error: Authentication failed. Please check your email and password.")
            print("For Gmail, make sure you're using an App Password, not your regular password.")
            return False
        except smtplib.SMTPException as e:
            print(f"Error: SMTP error occurred: {str(e)}")
            return False
        except Exception as e:
            print(f"Error: Failed to send email: {str(e)}")
            return False

    def send_excel_files(self, subject=EMAIL_SUBJECT, body=EMAIL_BODY):
        """
        Main method to find and send Excel files
        
        Args:
            subject: Email subject (optional)
            body: Email body (optional)
        
        Returns:
            True if successful, False otherwise
        """
        print("=" * 60)
        print("Excel Files Email Sender")
        print("=" * 60)
        
        # Find Excel files
        excel_files = self.find_excel_files()
        
        if not excel_files:
            print("\nNo Excel files found in the specified folder.")
            return False
        
        # Send email
        success = self.send_email_with_attachments(excel_files, subject, body)
        
        return success


def main():
    """Main function to run the email sender"""
    
    # Validate configuration
    if SENDER_EMAIL == 'your_email@gmail.com':
        print("ERROR: Please update SENDER_EMAIL in the configuration section")
        return
    
    if SENDER_PASSWORD == 'your_app_password':
        print("ERROR: Please update SENDER_PASSWORD in the configuration section")
        return
    
    # Validate recipient email(s)
    if not RECIPIENT_EMAIL or RECIPIENT_EMAIL == 'recipient@example.com':
        print("ERROR: Please update RECIPIENT_EMAIL in the configuration section")
        return
    
    # Normalize recipient_email to check if it's a list
    if isinstance(RECIPIENT_EMAIL, list) and len(RECIPIENT_EMAIL) == 0:
        print("ERROR: RECIPIENT_EMAIL list is empty. Please add at least one recipient email.")
        return
    
    # Create email sender instance
    email_sender = ExcelFileEmailSender(
        folder_path=FOLDER_PATH,
        sender_email=SENDER_EMAIL,
        sender_password=SENDER_PASSWORD,
        recipient_email=RECIPIENT_EMAIL,
        cc_email=CC_EMAIL
    )
    
    # Send Excel files
    email_sender.send_excel_files()


if __name__ == '__main__':
    main()

