import re
from bs4 import BeautifulSoup
import html


def extract_string(starts_with, string):
    # extract the links between starts_with and ends with < tag.
    pattern = r"{0}\s*(\S+)(?=<)".format(starts_with)
    extracted_string = re.search(pattern, string)
    decoded_string = None
    if extracted_string:
        extracted_string = extracted_string.group(1)
        decoded_string = html.unescape(extracted_string)
    return decoded_string


def extract_http_links(starts_with, string):
    # extract the links between starts_with and ends with < tag.
    pattern = r"{}\s*(https?://\S+)(?=<)".format(starts_with)
    extracted_string = re.search(pattern, string)
    if extracted_string:
        extracted_string = extracted_string.group(1)
    return extracted_string


def convert_html_to_plain_text(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text(strip=True)


def extract_from_address(email_content):
    return email_content['From']


def extract_cc_address(email_content):
    if email_content['cc']:
        return email_content['cc']
    else:
        return "EMPTY"


def extract_mail_subject(email_content):
    return email_content['Subject']


def extract_mail_date(email_content):
    return email_content['Date']


def get_mailids_from_string(str):
    lst = re.findall('\S+@\S+', str)
    mail_ids = [e.strip("<>,") for e in lst]
    return mail_ids


def attachment_availability(email_content):
    if email_content.is_multipart():
        attachment = 'Available'
    else:
        attachment = 'Not Available'
    return attachment


def get_details_from_email_body(email_message):
    if email_message.get_content_maintype() != 'multipart':
        print(email_message.get_content_maintype())
    for part in email_message.walk():
        content_type = part.get_content_type()
        if content_type == 'text/plain':
            text = part.get_payload(decode=True).decode('utf-8')
            text = re.sub(r'(<http.*>)|(Not\s+Mentioned)', '', text)
        if content_type == 'text/html':
            payload = part.get_payload(decode=True).decode('utf-8')
            soup = BeautifulSoup(payload, "html.parser")
            text = soup.get_text(strip=True)
    return text


def get_html_payload(email_message):
    for part in email_message.walk():
        content_type = part.get_content_type()
        if content_type == 'text/plain' or content_type == 'text/html':
            payload = part.get_payload()
    return payload


def clean_urls(data):
    #Removing AWS security parameters from urls/images
    # Regex to match the AWS security parameters in the URLs
    url_pattern = re.compile(r"(\?AWSAccessKeyId=[^&]+&Signature=[^&]+&Expires=[^&]+)")

    if isinstance(data, dict):
        # If it's a dictionary, recursively clean each value
        return {key: clean_urls(value) for key, value in data.items()}
    elif isinstance(data, list):
        # If it's a list, recursively clean each element
        return [clean_urls(item) for item in data]
    elif isinstance(data, str):
        # If it's a string, clean the URL using regex
        return url_pattern.sub("", data)
    else:
        # If it's neither a dict, list, nor string, return it as is
        return data
