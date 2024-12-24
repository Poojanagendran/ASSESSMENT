import imaplib
import email
from datetime import datetime, timedelta
from SCRIPTS.COMMON import email_cred


class EmailConnectivity:

    def __init__(self):
        # imap has to be enabled in gmail settings
        # less secure apps needs to be enabled in gmain settings
        self.sender_address = 'admin@hirepro.in'
        self.subject = 'Assessment Credential mail - AMSIN AT Tenant'
        self.date_time_filter = datetime.now() - timedelta(minutes=10)
        self.time_filter = self.date_time_filter.strftime('%d-%b-%Y')

    def connect_to_mailbox(self, sender_address, subject):
        try:
            imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)
            imap.login(email_cred.receiver_address, email_cred.receiver_password)
            imap.select('INBOX')
        except Exception as e:
            print("Could not connect mail INBOX because of ERROR: %s" % str(e))
        if sender_address and subject:
            status, response = imap.uid('search', None, 'UNSEEN', 'FROM {0}'.format(sender_address),
                                        'SUBJECT "{0}"'.format(subject), 'SINCE "{0}"'.format(self.time_filter))
            print("Both sender and subject is available")
        elif sender_address:
            status, response = imap.uid('search', None, 'UNSEEN',
                                        'FROM {0}'.format(sender_address), 'SINCE "{0}"'.format(self.time_filter))
            print("only sender address is available")
        elif subject:
            status, response = imap.uid('search', None, 'UNSEEN', 'SUBJECT "{0}"'.format(subject),
                                        'SINCE "{0}"'.format(self.time_filter))
            print("only subject is available")
        else:
            status, response = imap.uid('search', None, 'UNSEEN', 'SINCE "{0}"'.format(self.time_filter))
            print("Both sender and subject is not available")
        # print(response)
        if status == 'OK':
            unread_msg_nums = (response[0].split())
            # print(unread_msg_nums)
            unread_msg_nums.reverse()
            unread_msg_nums = unread_msg_nums[:1]
        else:
            unread_msg_nums = []
        html = ''
        for i in range(len(unread_msg_nums)):
            try:
                e_id = unread_msg_nums[i]
                e_id = e_id.decode('utf-8')
                _, response = imap.uid('fetch', e_id, '(RFC822)')
                html = response[0][1].decode('utf-8')
            except Exception as e:
                print(str(e))
                continue
        email_message = email.message_from_string(html)
        return email_message


mail = EmailConnectivity()
