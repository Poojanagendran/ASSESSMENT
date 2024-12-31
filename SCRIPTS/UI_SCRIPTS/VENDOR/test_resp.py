from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.CRPO_COMMON.crpo_common import *
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.COMMON.email_validation import *
from SCRIPTS.COMMON.parser import *
from SCRIPTS.DB_DELETE.db_cleanup import *
from SCRIPTS.CRPO_COMMON.requests_for_email import *
from bs4 import BeautifulSoup


class EmailChecker:

    def __init__(self):
        self.crpo_headers = crpo_common_obj.login_to_crpo(cred_crpo_admin_at.get('user'),
                                                          cred_crpo_admin_at.get('password'),
                                                          cred_crpo_admin_at.get('tenant'))
        write_excel_object.save_result(output_path_emails)
        # 0th Row Header
        header = ['Emails']
        # 1 Row Header
        write_excel_object.write_headers_for_scripts(0, 0, header, write_excel_object.black_color_bold)
        header = ['Usecase', 'Status', 'Tenant', 'Request Data', 'Expected_mail_status', 'Actual_mail_status',
                  'Expected From Address', 'Actual From Address', 'Expected CC', 'Actual CC', 'Expected Subject',
                  'Actual Subject', 'Expected mail Body', 'Actual Mail Body', 'Expected dynamic data',
                  'Actual Dynamic data']
        write_excel_object.write_headers_for_scripts(1, 0, header, write_excel_object.black_color_bold)
        self.row_size = 2

    def assessment(self):
        sprint_id = input('Enter Sprint ID')
        receiver_email = 'muthumurugan.ramalingam@hirepro.in'
        request = {"PersonalDetails": {"FirstName": "Mail Automation Candidate", "Email1": receiver_email,
                                       "USN": sprint_id, "DateOfBirth": "2022-02-08T18:30:00.000Z"}}
        candidate_id = crpo_common_obj.create_candidate_v2(self.crpo_headers, request)
        print(candidate_id)
        test_id = 13838
        event_id = 10468
        jobrole_id = 30230
        crpo_common_obj.tag_candidate_to_test(self.crpo_headers, candidate_id, test_id, event_id, jobrole_id)
        time.sleep(5)
        test_userid = crpo_common_obj.get_all_test_user(self.crpo_headers, candidate_id)
        tu_cred = crpo_common_obj.test_user_credentials(self.crpo_headers, test_userid)
        login_id = tu_cred['data']['testUserCredential']['loginId']
        password = tu_cred['data']['testUserCredential']['password']
        login_token = crpo_common_obj.login_to_test(login_id, password, "AT")
        submit_token = crpo_common_obj.final_submit(login_token, submit_test_request)
        req = {"candidateId": candidate_id, "testId": test_id}
        crpo_common_obj.initiate_automation(submit_token, req)
        time.sleep(360)

    def verify_mails(self, test_case):
        if test_cases.get('useCase') == 'send_credentials':
            cred_email_content = mail.connect_to_mailbox(test_case.get('from'), test_case.get('subject'))
            if len(cred_email_content) > 0:
                mail_date = extract_mail_date(cred_email_content)
                mail_html_body = cred_email_content.get_payload()
                mail_text_body = convert_html_to_plain_text(mail_html_body)
                attachment_status = attachment_availability(cred_email_content)
                self.dynamic_actual_data = {'UserId': extract_string('UserId:', mail_html_body),
                                            'Password': extract_string('Password:', mail_html_body),
                                            'candidate_fname': extract_string('CandidateFirstName:', mail_html_body),
                                            'assessment_full_link': extract_http_links('TUAssessmentLink:',
                                                                                       mail_html_body),
                                            'shorten_link': extract_http_links('TUAssessmentShortenedLink:',
                                                                               mail_html_body)}
                self.static_actual_data = {'mail_from': extract_from_address(cred_email_content),
                                           'mail_subject': extract_mail_subject(cred_email_content),
                                           'mail_text_body': mail_text_body,
                                           'mail_cc': extract_cc_address(cred_email_content),
                                           'attachment_status': attachment_status, 'is_mail_triggered': 'Yes'}
            else:
                print("Task is not completed in 5 mins")
                mail_from = 'TASK_NOT_COMPLETED'
                mail_subject = 'TASK_NOT_COMPLETED'
                mail_date = 'TASK_NOT_COMPLETED'
                self.dynamic_actual_data = {'UserId': 'No mail Received', 'Password': 'No mail Received',
                                            'candidate_fname': 'No mail Received',
                                            'assessment_full_link': 'No mail Received',
                                            'shorten_link': 'No mail Received'}
                self.static_actual_data = {'mail_from': 'No mail Received',
                                           'mail_subject': 'No mail Received',
                                           'mail_text_body': 'No mail Received', 'mail_cc': 'No mail Received',
                                           'attachment_status': 'No mail Received', 'is_mail_triggered': 'No'}

        elif test_cases.get('useCase') == 'candidate_thank_you_mail':
            thanks_email_content = mail.connect_to_mailbox(test_case.get('from'), test_case.get('subject'))
            if len(thanks_email_content) > 0:
                mail_date = extract_mail_date(thanks_email_content)
                mail_html_body = thanks_email_content.get_payload()
                self.mail_text_body = convert_html_to_plain_text(mail_html_body)
                self.dynamic_actual_data = {"EMPTY": "EMPTY"}
                self.static_actual_data = {'mail_from': extract_from_address(thanks_email_content),
                                           'mail_subject': extract_mail_subject(thanks_email_content),
                                           'mail_text_body': self.mail_text_body,
                                           'mail_cc': extract_cc_address(thanks_email_content),
                                           'attachment_status': attachment_availability(thanks_email_content),
                                           'is_mail_triggered': 'Yes'}
            else:
                self.dynamic_actual_data = {"EMPTY": "No mail Received"}
                self.static_actual_data = {'mail_from': "No mail Received",
                                           'mail_subject': "No mail Received",
                                           'mail_text_body': "No mail Received", 'mail_cc': 'No mail Received',
                                           'attachment_status': "No Mail Received", 'is_mail_triggered': 'No'}
                print("No mail Received for candidate thanks mail")

        elif test_cases.get('useCase') == 'candidate_transcript':
            cand_trans_email_content = mail.connect_to_mailbox(test_case.get('from'), test_case.get('subject'))
            if len(cand_trans_email_content) > 0:
                mail_date = extract_mail_date(cand_trans_email_content)
                mail_html_body = cand_trans_email_content.get_payload()
                self.mail_text_body = convert_html_to_plain_text(mail_html_body)
                self.dynamic_actual_data = {"EMPTY": "EMPTY"}
                self.static_actual_data = {'mail_from': extract_from_address(cand_trans_email_content),
                                           'mail_subject': extract_mail_subject(cand_trans_email_content),
                                           'mail_text_body': self.mail_text_body,
                                           'mail_cc': extract_cc_address(cand_trans_email_content),
                                           'attachment_status': attachment_availability(cand_trans_email_content),
                                           'is_mail_triggered': 'Yes'}
            else:
                self.dynamic_actual_data = {"EMPTY": "No mail Received"}
                self.static_actual_data = {'mail_from': "No mail Received",
                                           'mail_subject': "No mail Received",
                                           'mail_text_body': "No mail Received", 'mail_cc': 'No mail Received',
                                           'attachment_status': "No Mail Received", 'is_mail_triggered': 'No'}
                print("No mail Received for candidate Transcript")

        elif test_cases.get('useCase') == 'owner_transcript':
            owner_trans_email_content = mail.connect_to_mailbox(test_case.get('from'), test_case.get('subject'))
            if len(owner_trans_email_content) > 0:
                mail_date = extract_mail_date(owner_trans_email_content)
                # print(email_content.get_payload(0))
                mail_html_body = get_details_from_email_body(owner_trans_email_content)
                print(type(mail_html_body))
                self.mail_text_body = mail_html_body
                self.dynamic_actual_data = {"EMPTY": "EMPTY"}
                self.static_actual_data = {'mail_from': extract_from_address(owner_trans_email_content),
                                           'mail_subject': extract_mail_subject(owner_trans_email_content),
                                           'mail_text_body': self.mail_text_body,
                                           'mail_cc': extract_cc_address(owner_trans_email_content),
                                           'attachment_status': attachment_availability(owner_trans_email_content),
                                           'is_mail_triggered': 'Yes'}
            else:
                self.dynamic_actual_data = {"EMPTY": "No mail Received"}
                self.static_actual_data = {'mail_from': "No mail Received",
                                           'mail_subject': "No mail Received",
                                           'mail_text_body': "No mail Received", 'mail_cc': 'No mail Received',
                                           'attachment_status': "No Mail Received", 'is_mail_triggered': 'No'}
                print("No mail Received for Owner Transcript")

        write_excel_object.compare_results_and_write_vertically(test_case.get('useCase'), None, self.row_size, 0)
        write_excel_object.compare_results_and_write_vertically(test_case.get('tenant'), None, self.row_size, 2)
        write_excel_object.compare_results_and_write_vertically(test_case.get('requestData'), None, self.row_size, 3)
        write_excel_object.compare_results_and_write_vertically(test_case.get('mailTriggered'),
                                                                self.static_actual_data.get('is_mail_triggered'),
                                                                self.row_size, 4)
        write_excel_object.compare_results_and_write_vertically(test_case.get('from'),
                                                                self.static_actual_data.get('mail_from'), self.row_size,
                                                                6)
        write_excel_object.compare_results_and_write_vertically(test_case.get('from'),
                                                                self.static_actual_data.get('mail_from'), self.row_size,
                                                                8)
        write_excel_object.compare_results_and_write_vertically(test_case.get('cc'),
                                                                self.static_actual_data.get('mail_cc'), self.row_size,
                                                                10)
        write_excel_object.compare_results_and_write_vertically(test_case.get('subject'),
                                                                self.static_actual_data.get('mail_subject'),
                                                                self.row_size, 12)
        write_excel_object.compare_results_and_write_vertically(test_case.get('mailBody'),
                                                                self.static_actual_data.get('mail_text_body'),
                                                                self.row_size, 14)
        write_excel_object.compare_results_and_write_vertically(str(test_case.get('expected_dynamic_data')),
                                                                str(self.dynamic_actual_data),
                                                                self.row_size, 16)
        write_excel_object.compare_results_and_write_vertically(str(test_case.get('attachment')),
                                                                self.static_actual_data.get('attachment_status'),
                                                                self.row_size, 18)
        write_excel_object.compare_results_and_write_vertically(
            write_excel_object.current_status, None, self.row_size, 1)
        self.row_size = self.row_size + 1


mb = EmailChecker()
excel_read_obj.excel_read(input_path_for_email_validation, 0)
excel_data = excel_read_obj.details
# mb.assessment()
for test_cases in excel_data:
    mb.verify_mails(test_cases)
write_excel_object.write_overall_status(testcases_count=4)
