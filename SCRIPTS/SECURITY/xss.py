from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.CRPO_COMMON.crpo_common import *
from SCRIPTS.CRPO_COMMON.credentials import *
from SCRIPTS.COMMON.io_path import *


class XSSCharEncoding:

    def __init__(self):
        requests.packages.urllib3.disable_warnings()
        self.row_count = 2
        write_excel_object.save_result(output_path_xss)
        self.write_headers()

    def write_headers(self):
        # Writing headers in the Excel file
        headers = ["Response Payload Ecryption"]
        write_excel_object.write_headers_for_scripts(0, 0, headers, write_excel_object.black_color_bold)
        headers1 = ["Testcase", "Status", "API", "Tenant XSS Config", "API audit Config", "Tenant Alias",
                    "Expected Behaviour", "Actual Behaviour"]
        write_excel_object.write_headers_for_scripts(1, 0, headers1, write_excel_object.black_color_bold)

    def xss_char_encoding(self, token, test_case_data, hirepro_tkn):
        now = datetime.datetime.now()
        usn = now.strftime("%d-%m-%Y-%H-%M-%S-%f")
        write_excel_object.current_status_color = write_excel_object.green_color
        write_excel_object.current_status = "Pass"
        test_case = test_case_data.get('testCase')
        api_url = test_case_data.get('apiUrl')
        api_id = int(test_case_data.get('apiId'))
        app_pref_id = int(test_case_data.get('appPreferenceID'))
        expected_behaviour = test_case_data.get('expectedResult')
        if test_case_data.get('xssConfig') == 'True':
            xss_content = {"isEnabled": True}
            app_pref_type = "xss.config"
        elif test_case_data.get('xssConfig') == 'False':
            xss_content = {"isEnabled": False}
            app_pref_type = "xss.config"
        else:
            xss_content = {"isEnabled": False}
            app_pref_type = "xss.config_deleted"
        update_xss_app_pref = crpo_common_obj.save_apppreferences(token, json.dumps(xss_content), app_pref_id,
                                                                  app_pref_type)
        remove_cache = crpo_common_obj.clear_tenant_cache(hirepro_tkn, 'securityautomation')
        if test_case_data.get('api_audit_config') == 'True':
            audit_request = {"apiUrl": api_url, "xssConfig": {"isEnabled": True}, "id": api_id}
        elif test_case_data.get('api_audit_config') == 'False':
            audit_request = {"apiUrl": api_url, "xssConfig": {"isEnabled": False}, "id": api_id}
        else:
            audit_request = {"apiUrl": api_url, "xssConfig": None, "id": api_id}

        update_api_audit_configurations = crpo_common_obj.update_api_audit(hirepro_tkn, audit_request)
        # remove_cache = crpo_common_obj.clear_tenant_cache(hirepro_tkn, 'hirepro')
        create_cand_req = {"PersonalDetails": {"Name": "<script>alert(1)</script>", "PhoneOffice": None,
                                               "Email1": "qaonehirepro@gmail.com", "USN": usn},
                           "SourceDetails": {"SourceId": "1"}}

        candidate_id = crpo_common_obj.create_candidate_v2(token, create_cand_req)
        candidate_details = crpo_common_obj.get_candidate_by_id(token, candidate_id)
        print(candidate_details)
        if "&lt;script&gt;alert(1)&lt;/script&gt;" in candidate_details["Candidate"]["PersonalDetails"]["Name"]:
            actual_behaviour = "XSS encoded"
        else:
            actual_behaviour = "XSS not encoded"
        write_excel_object.compare_results_and_write_vertically(test_case, None, self.row_count, 0)
        write_excel_object.compare_results_and_write_vertically(api_url, None, self.row_count, 2)
        write_excel_object.compare_results_and_write_vertically(test_case_data.get('xssConfig'), None, self.row_count,
                                                                3)

        write_excel_object.compare_results_and_write_vertically(test_case_data.get('api_audit_config'), None,
                                                                self.row_count, 4)

        write_excel_object.compare_results_and_write_vertically(test_case_data.get('tenantAlias'), None, self.row_count,
                                                                5)
        write_excel_object.compare_results_and_write_vertically(expected_behaviour, actual_behaviour, self.row_count, 6)
        write_excel_object.compare_results_and_write_vertically(write_excel_object.current_status, None, self.row_count,
                                                                1)
        self.row_count = self.row_count + 1


sec_res_obj = XSSCharEncoding()
admin_token = crpo_common_obj.login_to_crpo(cred_crpo_admin_security_automation.get('user'),
                                            cred_crpo_admin_security_automation.get('password'),
                                            cred_crpo_admin_security_automation.get('tenant'))
non_admin_token = crpo_common_obj.login_to_crpo(cred_crpo_non_admin_security_automation.get('user'),
                                                cred_crpo_non_admin_security_automation.get('password'),
                                                cred_crpo_non_admin_security_automation.get('tenant'))
hirepro_token = crpo_common_obj.login_to_crpo(cred_crpo_admin_hirepro.get('user'),
                                              cred_crpo_admin_hirepro.get('password'),
                                              cred_crpo_admin_hirepro.get('tenant'))
hirepro_token.pop("X-APPLMA")
# Reading data from Excel file
excel_read_obj.excel_read(input_path_xss_encoding, 0)
excel_data = excel_read_obj.details

# Validating files and writing results
for data in excel_data:
    if data.get("isAdmin") == "Yes":
        sec_res_obj.xss_char_encoding(admin_token, data, hirepro_token)
    else:
        sec_res_obj.xss_char_encoding(non_admin_token, data, hirepro_token)
write_excel_object.write_overall_status(testcases_count=10)
