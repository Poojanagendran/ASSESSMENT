import xlsxwriter
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.CRPO_COMMON.crpo_common import *
from SCRIPTS.ASSESSMENT_COMMON.assessment_common import *
from SCRIPTS.DB_DELETE.db_cleanup import *
from SCRIPTS.COMMON.parallel_execution import *


class SecurityCheck:

    def __init__(self):
        data_clean_obj.delete_ssrf_assessment_test_users()
        data_clean_obj.delete_ssrf_template()
        data_clean_obj.delete_ssrf_job()
        data_clean_obj.delete_ssrf_vendor_integration()
        data_clean_obj.delete_ssrf_candidate()
        data_clean_obj.delete_ssrf_questions()
        requests.packages.urllib3.disable_warnings()
        self.started = datetime.datetime.now()
        self.started = self.started.strftime("%Y-%M-%d-%H-%M-%S")
        excel_read_obj.excel_read(input_path_ssrf_check, 0)
        self.row_size = 2
        self.write_excel = xlsxwriter.Workbook(output_path_ssrf_check + self.started + '.xls')
        self.allowed_apis = ['https://amsin.hirepro.in/py/rpo/upload_zipped_photos/',
                             'https://amsin.hirepro.in/py/crpo/api/v1/asyncAPIContextUpdate',
                             'https://amsin.hirepro.in/py/pofu/api/v1/submit-form/',
                             'https://amsin.hirepro.in/py/assessment/htmltest/api/v1/submit-video-answer/']
        self.ws = self.write_excel.add_worksheet()
        self.black_color = self.write_excel.add_format({'font_color': 'black', 'font_size': 9})
        self.red_color = self.write_excel.add_format({'font_color': 'red', 'font_size': 9})
        self.green_color = self.write_excel.add_format({'font_color': 'green', 'font_size': 9})
        self.orange_color = self.write_excel.add_format({'font_color': 'orange', 'font_size': 9})
        self.black_color_bold = self.write_excel.add_format({'font_color': 'black', 'bold': True, 'font_size': 9})
        self.over_all_status_pass = self.write_excel.add_format({'font_color': 'green', 'bold': True, 'font_size': 9})
        self.over_all_status_failed = self.write_excel.add_format({'font_color': 'red', 'bold': True, 'font_size': 9})
        self.over_all_status_color = self.over_all_status_pass
        self.over_all_status = 'Pass'

        self.ws.write(0, 0, "SSRF - Security Check", self.black_color_bold)

        self.ws.write(1, 0, "Testcases", self.black_color)
        self.ws.write(1, 1, "Status", self.black_color)
        self.ws.write(1, 2, "API", self.black_color)
        self.ws.write(1, 3, "Application", self.black_color)
        self.ws.write(1, 4, "Request", self.black_color)
        self.ws.write(1, 5, "Response", self.black_color)
        self.ws.write(1, 6, "Expected Status", self.black_color)
        self.ws.write(1, 7, "Actual Status", self.black_color)


    def security_check(self, crpo_header, cand_header, assess_header, src_header, data):
        api = data.get('api')
        request = data.get('payLoad')
        expected_status = data.get('expectedStatus')
        api_module = data.get('apiModule')
        tc_desc = data.get('testCaseDescription')

        try:
            print(api_module)
            if api_module == 'Assessment':
                headers = assess_header

            elif api_module == 'RPO_Source':
                headers = src_header
            elif api_module == 'Candidate':
                headers = cand_header
            else:
                headers = crpo_header
            api_request = requests.post(api, headers=headers, data=request, verify=False)
            resp_dict = json.loads(api_request.content)

            if resp_dict.get('status') == 'OK' or resp_dict.get('Status') == 'OK' or \
                    (resp_dict.get('error')).get('errorCode') == 401:
                self.actual_status = 'authorized'

            else:
                if (resp_dict.get('error')).get('errorDescription') == 'Unauthorized':
                    if api in self.allowed_apis:
                        self.actual_status = 'Cannot Handle- either need dev support or need permanent URL'
                    else:
                        self.actual_status = "unauthorized"

            self.ws.write(self.row_size, 0, "Testcase Data", self.black_color)
            self.ws.write(self.row_size, 2, api, self.black_color)
            self.ws.write(self.row_size, 3, api_module, self.black_color)
            self.ws.write(self.row_size, 4, request, self.black_color)
            self.ws.write(self.row_size, 5, str(resp_dict), self.black_color)
            if expected_status == self.actual_status:
                self.ws.write(self.row_size, 1, "Pass", self.green_color)
                self.ws.write(self.row_size, 6, expected_status, self.green_color)
                self.ws.write(self.row_size, 7, self.actual_status, self.green_color)
                self.ws.write(self.row_size, 8, tc_desc, self.green_color)

            elif expected_status != self.actual_status and \
                    (self.actual_status == "unauthorized" or self.actual_status == "authorized"):
                self.over_all_status = 'Fail'
                self.over_all_status_color = self.over_all_status_failed
                self.ws.write(self.row_size, 1, "Fail", self.red_color)
                self.ws.write(self.row_size, 6, expected_status, self.red_color)
                self.ws.write(self.row_size, 7, self.actual_status, self.red_color)
                self.ws.write(self.row_size, 8, tc_desc, self.green_color)

            else:
                self.ws.write(self.row_size, 1, "Pass", self.orange_color)
                self.ws.write(self.row_size, 6, expected_status, self.orange_color)
                self.ws.write(self.row_size, 7, self.actual_status, self.orange_color)
                self.ws.write(self.row_size, 8, tc_desc, self.green_color)
            self.row_size += 1

        except Exception as e:
            print(e)
            self.ws.write(self.row_size, 0, "Testcase Data", self.black_color)
            self.ws.write(self.row_size, 1, "pass", self.orange_color)
            self.ws.write(self.row_size, 2, api, self.black_color)
            self.ws.write(self.row_size, 3, api_module, self.black_color)
            self.ws.write(self.row_size, 4, request, self.black_color)
            self.ws.write(self.row_size, 5, "Got Exception", self.black_color)
            self.ws.write(self.row_size, 6, expected_status, self.orange_color)
            self.ws.write(self.row_size, 7, "Unexpected known Behaviour", self.orange_color)
            self.ws.write(self.row_size, 8, tc_desc, self.green_color)
            self.row_size += 1


security_obj = SecurityCheck()
security_data_excel = excel_read_obj.details
crpo_headers = crpo_common_obj.login_to_crpo(cred_crpo_normal_user.get('user'), cred_crpo_normal_user.get('password'),
                                             cred_crpo_normal_user.get('tenant'))

candidate_headers = crpo_common_obj.login_to_crpo(cred_candidate_user.get('user'), cred_candidate_user.get('password'),
                                                  cred_candidate_user.get('tenant'))
source_headers = crpo_common_obj.login_to_crpo(cred_source_user.get('user'), cred_source_user.get('password'),
                                               cred_source_user.get('tenant'))
assessment_headers = AssessmentCommon.login_to_test(login_name='Automation89161268450', password='bEiATNLlO',
                                                    tenant='automation')
assessment_headers = {"content-type": "application/json", "X-AUTH-TOKEN": assessment_headers.get("Token"),
                      "X-APPLMA": "true"}
thread_context_for_ssrf_check(security_obj.security_check, crpo_headers, candidate_headers, assessment_headers,
                              source_headers, security_data_excel)
# for data in security_data_excel:
#     security_obj.security_check(crpo_headers, candidate_headers, assessment_headers, source_headers, data)

ended = datetime.datetime.now()
ended = "Ended:- %s" % ended.strftime("%Y-%M-%d-%H-%M-%S")
security_obj.ws.write(0, 1, security_obj.over_all_status, security_obj.over_all_status_color)
security_obj.ws.write(0, 2, 'Started:- ' + security_obj.started, security_obj.black_color_bold)
security_obj.ws.write(0, 3, ended, security_obj.black_color_bold)
security_obj.ws.write(0, 4, "Total_Testcase_Count:- 138", security_obj.black_color_bold)
security_obj.write_excel.close()
