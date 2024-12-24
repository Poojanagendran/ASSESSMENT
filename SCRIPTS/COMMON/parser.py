import re
from bs4 import BeautifulSoup
import html


def extract_string(starts_with, string):
    # extract the links between starts_with and ends with < tag.
    # pattern = r"{0}\s*([\w\d]+)(?=<)".format(starts_with)
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


def extract_mail_subject(email_content):
    return email_content['Subject']


def extract_mail_date(email_content):
    return email_content['Date']


