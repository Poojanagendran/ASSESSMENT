import imaplib
import email

sender_of_interest = 'qaone.hirepro@gmail.com'
try:
    imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    imap.login('qaone.hirepro@gmail.com', 'qa@hirepro')
    imap.select('INBOX')
except Exception as e:
    print("Could not connect mail INBOX because of ERROR: %s" % str(e))

if sender_of_interest:
    status, response = imap.uid('search', None, 'UNSEEN', 'FROM {0}'.format(sender_of_interest))
else:
    status, response = imap.uid('search', None, 'UNSEEN')
if status == 'OK':
    unread_msg_nums = (response[0].split())
    unread_msg_nums.reverse()
    unread_msg_nums = unread_msg_nums[:100]
else:
    unread_msg_nums = []
# ids_to_delete = []
# logger.info('Unread_mail_ids of inbox {}: {}'.format(conn_data.get("username"), str(unread_msg_nums)))
# delete_mail_after_read = conn_data.get('delete_mail_after_read', False)
#
# for i in range(len(unread_msg_nums)):
#     try:
#         e_id = unread_msg_nums[i]
#         e_id = e_id.decode('utf-8')
#         _, response = imap.uid('fetch', e_id, '(RFC822)')
#         html = response[0][1].decode('utf-8')
#     except Exception as e:
#         print(str(e))
#         # imap.store(e_id, '+FLAGS', '\Seen')
#         # ids_to_delete.append(e_id)
#         # if delete_mail_after_read:
#         #  ParseApplicantFromMailUtils.move_read_mail_to_delete(imap, e_id)
#         continue
#
#     data_dict = {}
#     email_message = email.message_from_string(html)
#     # from_ids = ParseApplicantFromMailUtils.get_mailids_from_string(email_message['From'])
#     # data_dict['mail_subject'] = email_message['Subject']
#     # data_dict['mail_from'] = from_ids[0] if from_ids else None
#
#     # data_dict['mail_to'] = ParseApplicantFromMailUtils.get_mailids_from_string(email_message['To'])
#
#     # data_dict['mail_cc'] = ParseApplicantFromMailUtils.get_mailids_from_string(email_message['Cc'])
#     # data_dict['body'] = email_message.get_payload()
#     # data_dict['attachments'] = ParseApplicantFromMailUtils.download_email_attachments(email_message)
#     # data_dict['mail_body_data'] = ParseApplicantFromMailUtils.get_details_from_email_body(email_message)
#
#     resumes = data_dict.get('attachments', [])
#
#     imap.store(e_id, '+FLAGS', '\Seen')
#     ids_to_delete.append(e_id)
#     joined_e_ids = ",".join(e_ids)
#     imap.store(joined_e_ids, '+FLAGS', '\\Deleted')
#     imap.uid('STORE', joined_e_ids, '+X-GM-LABELS', '\\Trash')
