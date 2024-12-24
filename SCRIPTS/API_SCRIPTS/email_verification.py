from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.CRPO_COMMON.crpo_common import *
from SCRIPTS.CRPO_COMMON.credentials import *
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.COMMON.email_validation import *
from SCRIPTS.COMMON.parser import *


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
        header = ['Usecase', 'Status', 'Tenant', 'Request Data', 'Expected From Address', 'Actual From Address',
                  'Expected CC', 'Actual CC', 'Expected Subject', 'Actual Subject', 'Expected mail Body',
                  'Actual Mail Body', 'Expected dynamic data', 'Actual Dynamic data']
        write_excel_object.write_headers_for_scripts(1, 0, header, write_excel_object.black_color_bold)
        self.row_size = 2

    def send_credentials_mail(self, test_case):
        if test_cases.get('useCase') == 'send_credentials':
            send_cred = crpo_common_obj.send_test_user_credntials(self.crpo_headers, int(test_case.get('requestData')))
            context_id = send_cred['data']['ContextId']
            job_state = crpo_common_obj.job_status_v2(self.crpo_headers, context_id)
            if job_state['data']['JobState'] == 'SUCCESS':
                email_content = mail.connect_to_mailbox(test_case.get('from'), test_case.get('subject'))
                mail_date = extract_mail_date(email_content)
                mail_html_body = email_content.get_payload()
                mail_text_body = convert_html_to_plain_text(mail_html_body)
                dynamic_actual_data = {'UserId': extract_string('UserId:', mail_html_body),
                                       'Password': extract_string('Password:', mail_html_body),
                                       'candidate_fname': extract_string('CandidateFirstName:', mail_html_body),
                                       'assessment_full_link': extract_http_links('TUAssessmentLink:', mail_html_body),
                                       'shorten_link': extract_http_links('TUAssessmentShortenedLink:', mail_html_body)}
                static_actual_data = {'mail_from': extract_from_address(email_content),
                                      'mail_subject': extract_mail_subject(email_content),
                                      'mail_text_body': mail_text_body, 'mail_cc': 'EMPTY'}
            else:
                print("Task is not completed in 3 mins")
                mail_from = 'TASK_NOT_COMPLETED'
                mail_subject = 'TASK_NOT_COMPLETED'
                mail_date = 'TASK_NOT_COMPLETED'
                dynamic_actual_data = {'UserId': 'EMPTY', 'Password': 'EMPTY', 'candidate_fname': 'EMPTY',
                                       'assessment_full_link': 'EMPTY', 'shorten_link': 'EMPTY'}
                static_actual_data = {'mail_from': 'EMPTY',
                                      'mail_subject': 'EMPTY',
                                      'mail_text_body': 'EMPTY', 'mail_cc': 'EMPTY'}
            write_excel_object.compare_results_and_write_vertically(test_case.get('useCase'), None, self.row_size, 0)
            write_excel_object.compare_results_and_write_vertically(test_case.get('tenant'), None, self.row_size, 2)
            write_excel_object.compare_results_and_write_vertically(test_case.get('requestData'), None, self.row_size,
                                                                    3)
            write_excel_object.compare_results_and_write_vertically(test_case.get('from'),
                                                                    static_actual_data.get('mail_from'), self.row_size,
                                                                    4)
            write_excel_object.compare_results_and_write_vertically(test_case.get('cc'),
                                                                    static_actual_data.get('mail_cc'), self.row_size,
                                                                    6)
            write_excel_object.compare_results_and_write_vertically(test_case.get('subject'),
                                                                    static_actual_data.get('mail_subject'),
                                                                    self.row_size, 8)
            write_excel_object.compare_results_and_write_vertically(test_case.get('mailBody'),
                                                                    static_actual_data.get('mail_text_body'),
                                                                    self.row_size, 10)
            write_excel_object.compare_results_and_write_vertically(str(test_case.get('expected_dynamic_data')),
                                                                    str(dynamic_actual_data),
                                                                    self.row_size, 12)
            write_excel_object.compare_results_and_write_vertically(
                write_excel_object.current_status, None, self.row_size, 1)
            self.row_size = self.row_size + 1
        else:
            print("Its not send_credential usecase, please check the usecase name properly")


mb = EmailChecker()
excel_read_obj.excel_read(input_path_for_email_validation, 0)
excel_data = excel_read_obj.details
diction = ()
for test_cases in excel_data:
    mb.send_credentials_mail(test_cases)
    write_excel_object.write_overall_status(testcases_count=1)
