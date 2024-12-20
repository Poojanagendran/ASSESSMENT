from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.CRPO_COMMON.crpo_common import *
from SCRIPTS.CRPO_COMMON.credentials import *
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.ASSESSMENT_COMMON.assessment_common import *


# from SCRIPTS.DB_DELETE.db_cleanup import *


class RateControl:

    def __init__(self):
        # data_clean_obj.rate_control_delete()
        # admin_token = crpo_common_obj.login_to_crpo(cred_crpo_admin_security_automation.get('user'),
        #                                             cred_crpo_admin_security_automation.get('password'),
        #                                             cred_crpo_admin_security_automation.get('tenant'))
        requests.packages.urllib3.disable_warnings()
        self.row_count = 2
        write_excel_object.save_result(output_path_rate_control)
        self.write_headers()
        self.api_thorttle_json = {
            "ENABLED": True,
            "OAUTH_TOKEN_RESTRICTIONS": {
                "ENABLED": True,
                "FRONTEND_INTEGRATIONS": {
                    "MAX_API_COUNT_INVOCATION_PER_MINUTE": 2,
                    "MAX_API_COUNT_INVOCATION_PER_HOUR": 3
                },
                "BACKEND_INTEGRATIONS": {
                    "MAX_API_COUNT_INVOCATION_PER_MINUTE": 2,
                    "MAX_API_COUNT_INVOCATION_PER_HOUR": 3
                }
            },
            "USER_TYPE_RESTRICTIONS": {
                "CRPO_USER": {
                    "ENABLED": True,
                    "MAX_API_COUNT_INVOCATION_PER_MINUTE": 2,
                    "MAX_API_COUNT_INVOCATION_PER_HOUR": 3
                },
                "TEST_USER": {
                    "ENABLED": True,
                    "MAX_API_COUNT_INVOCATION_PER_MINUTE": 2,
                    "MAX_API_COUNT_INVOCATION_PER_HOUR": 3
                },
                "CANDIDATE_USER": {
                    "ENABLED": True,
                    "MAX_API_COUNT_INVOCATION_PER_MINUTE": 2,
                    "MAX_API_COUNT_INVOCATION_PER_HOUR": 3
                },
                "VENDOR_USER": {
                    "ENABLED": True,
                    "MAX_API_COUNT_INVOCATION_PER_MINUTE": 2,
                    "MAX_API_COUNT_INVOCATION_PER_HOUR": 3
                },
                "TPO_USER": {
                    "ENABLED": True,
                    "MAX_API_COUNT_INVOCATION_PER_MINUTE": 2,
                    "MAX_API_COUNT_INVOCATION_PER_HOUR": 3
                },
                "ALL_OTHERS": {
                    "ENABLED": True,
                    "MAX_API_COUNT_INVOCATION_PER_MINUTE": 2,
                    "MAX_API_COUNT_INVOCATION_PER_HOUR": 3
                }
            }
        }
        # update_rate_app_pref = crpo_common_obj.save_apppreferences(admin_token, json.dumps(self.api_thorttle_json), 201,
        #                                                            'api_throttle')

    def write_headers(self):
        # Writing headers in the Excel file
        headers = ["Rate Control"]
        write_excel_object.write_headers_for_scripts(0, 0, headers, write_excel_object.black_color_bold)
        headers1 = ["Testcase", "Status", "Tenant", "Type Of User", "Limit Per Minute", "Limit Per Hour",
                    "Expected - Minute before Threshold", "Actual - Minute before Threshold",
                    "Expected - Minute after Threshold", "Actual - Minute after Threshold",
                    "Expected Hour before Threshold", "Actual Hour before Threshold",
                    "Expected Hour after Threshold", "Actual Hour After Threshold"]
        write_excel_object.write_headers_for_scripts(1, 0, headers1, write_excel_object.black_color_bold)

    def rate_control(self, token, test_case_data):
        write_excel_object.current_status_color = write_excel_object.green_color
        write_excel_object.current_status = "Pass"
        test_case = test_case_data.get('testCase')
        type_of_user = test_case_data.get('typeOfUser')
        tenant_name = test_case_data.get('tenant')
        limit_per_minute = int(test_case_data.get('limitPerMinute'))
        limit_per_hour = int(test_case_data.get('limitPerHour'))
        exp_message_per_minute_till_threshold = test_case_data.get('expectedMessagPerMinuteTillThreshold')
        exp_message_per_minute_after_threshold = test_case_data.get('expectedMessagPerMinuteAfterThreshold')
        exp_message_per_hour_till_threshold = test_case_data.get('expectedMessagePerHourTillThreshold')
        exp_message_per_hour_after_threshold = test_case_data.get('expectedMessagePerHourAfterThreshold')
        total_iter = int(limit_per_hour / limit_per_minute) + 1
        count = 1
        # request = {"Type": "crpo.interviewListSearch.config", "IsTenantGlobal": True}
        request = {"Type": "crpo.tenantConfigurations", "IsTenantGlobal": True}
        for overall_iter in range(0, total_iter):
            print("This is count ", count)
            print(test_case_data.get('typeOfUser'))
            if count >= limit_per_hour:
                if test_case_data.get('typeOfUser') == 'TESTUSER':
                    act_message_per_hour_till_threshold_resp = assessment_common_obj.get_test_basic_info(token)
                    act_message_per_hour_after_threshold_resp = assessment_common_obj.get_test_basic_info(token)

                elif test_case_data.get('typeOfUser') == 'BACKEND':
                    act_message_per_hour_till_threshold_resp = crpo_common_obj.get_all_event(token)
                    act_message_per_hour_after_threshold_resp = crpo_common_obj.get_all_event(token)

                elif test_case_data.get('typeOfUser') == 'UITOKEN':
                    act_message_per_hour_till_threshold_resp = crpo_common_obj.generating_slots(token, event_id=3)
                    act_message_per_hour_after_threshold_resp = crpo_common_obj.generating_slots(token, event_id=3)

                else:
                    act_message_per_hour_till_threshold_resp = crpo_common_obj.get_app_preference_generic(token,
                                                                                                          request)
                    act_message_per_hour_after_threshold_resp = crpo_common_obj.get_app_preference_generic(token,
                                                                                                           request)
                print(act_message_per_hour_till_threshold_resp.get('status'))
                if act_message_per_hour_till_threshold_resp.get('status') in [None, 'OK']:
                    act_message_per_hour_till_threshold = 'Authorized'
                else:
                    act_message_per_hour_till_threshold = 'Unauthorized'
                if act_message_per_hour_after_threshold_resp.get('status') == 'KO':
                    act_message_per_hour_after_threshold = "Unauthorized"
                else:
                    act_message_per_hour_after_threshold = 'Authorized'
            else:
                for per_minute in range(0, limit_per_minute):
                    if test_case_data.get('typeOfUser') == 'TESTUSER':
                        act_minute_resp_till_threshold_resp = assessment_common_obj.get_test_basic_info(token)
                    elif test_case_data.get('typeOfUser') == 'BACKEND':
                        act_minute_resp_till_threshold_resp = crpo_common_obj.get_all_event(token)
                    elif test_case_data.get('typeOfUser') == 'UITOKEN':
                        act_minute_resp_till_threshold_resp = crpo_common_obj.generating_slots(token, event_id=3)
                    else:
                        act_minute_resp_till_threshold_resp = crpo_common_obj.get_app_preference_generic(token, request)
                    if act_minute_resp_till_threshold_resp.get('status') in [None, 'OK']:
                        act_minute_resp_till_threshold = 'Authorized'
                    else:
                        act_minute_resp_till_threshold = 'Unauthorized'
                    count = count + 1
                if test_case_data.get('typeOfUser') == 'TESTUSER':
                    act_minute_resp_after_threshold_resp = assessment_common_obj.get_test_basic_info(token)
                elif test_case_data.get('typeOfUser') == 'BACKEND':
                    act_minute_resp_after_threshold_resp = crpo_common_obj.get_all_event(token)
                elif test_case_data.get('typeOfUser') == 'UITOKEN':
                    act_minute_resp_after_threshold_resp = crpo_common_obj.generating_slots(token, event_id=3)
                else:
                    act_minute_resp_after_threshold_resp = crpo_common_obj.get_app_preference_generic(token, request)

                if act_minute_resp_after_threshold_resp.get('status') == 'KO':
                    act_minute_resp_after_threshold = "Unauthorized"
                else:
                    act_minute_resp_after_threshold = 'Authorized'
                time.sleep(60)
        write_excel_object.compare_results_and_write_vertically(test_case, None, self.row_count, 0)
        write_excel_object.compare_results_and_write_vertically(tenant_name, None, self.row_count, 2)
        write_excel_object.compare_results_and_write_vertically(type_of_user, None, self.row_count, 3)

        write_excel_object.compare_results_and_write_vertically(limit_per_minute, None, self.row_count, 4)

        write_excel_object.compare_results_and_write_vertically(limit_per_hour, None, self.row_count, 5)
        write_excel_object.compare_results_and_write_vertically(exp_message_per_minute_till_threshold,
                                                                act_minute_resp_till_threshold, self.row_count, 6)
        write_excel_object.compare_results_and_write_vertically(exp_message_per_minute_after_threshold,
                                                                act_minute_resp_after_threshold, self.row_count, 8)

        write_excel_object.compare_results_and_write_vertically(exp_message_per_hour_till_threshold,
                                                                act_message_per_hour_till_threshold, self.row_count, 10)
        write_excel_object.compare_results_and_write_vertically(exp_message_per_hour_after_threshold,
                                                                act_message_per_hour_after_threshold, self.row_count,
                                                                12)
        write_excel_object.compare_results_and_write_vertically(write_excel_object.current_status, None, self.row_count,
                                                                1)
        self.row_count = self.row_count + 1


sec_res_obj = RateControl()
admin_token = crpo_common_obj.login_to_crpo(cred_crpo_admin_security_automation.get('user'),
                                            cred_crpo_admin_security_automation.get('password'),
                                            cred_crpo_admin_security_automation.get('tenant'))
non_admin_token = crpo_common_obj.login_to_crpo(cred_crpo_non_admin_security_automation.get('user'),
                                                cred_crpo_non_admin_security_automation.get('password'),
                                                cred_crpo_non_admin_security_automation.get('tenant'))
tpo_token = crpo_common_obj.login_to_crpo(cred_crpo_tpo_security_automation.get('user'),
                                          cred_crpo_tpo_security_automation.get('password'),
                                          cred_crpo_tpo_security_automation.get('tenant'))
vendor_token = crpo_common_obj.login_to_crpo(cred_crpo_vendor_security_automation.get('user'),
                                             cred_crpo_vendor_security_automation.get('password'),
                                             cred_crpo_vendor_security_automation.get('tenant'))
hirepro_token = crpo_common_obj.login_to_crpo(cred_crpo_admin_hirepro.get('user'),
                                              cred_crpo_admin_hirepro.get('password'),
                                              cred_crpo_admin_hirepro.get('tenant'))
test_user_login = assessment_common_obj.login_to_test_v3('securityautomation1189', '1XTK}!',
                                                         'securityautomation', env_obj.domain)
candidate_token = crpo_common_obj.login_to_crpo(cred_crpo_candidate_security_automation.get('user'),
                                                cred_crpo_candidate_security_automation.get('password'),
                                                cred_crpo_candidate_security_automation.get('tenant'))
backend_token = crpo_common_obj.generating_backend_token(crpo_backend_token_security_automation.get('integration_id'),
                                                         crpo_backend_token_security_automation.get('client_id'),
                                                         crpo_backend_token_security_automation.get('client_secret'))
# accenture_token = crpo_common_obj.login_to_crpo(cred_crpo_user_accenturetest.get('user'),
#                                                 cred_crpo_user_accenturetest.get('password'),
#                                                 cred_crpo_user_accenturetest.get('tenant'))
ui_token = crpo_common_obj.generating_ui_token(crpo_ui_token_security_automation.get('integration_id'),
                                               crpo_ui_token_security_automation.get('client_id'), admin_token,
                                               cid=189, event_id=3, job_id=3)
print(ui_token)

test_user_token = test_user_login.get("login_token")
# assessment_common_obj.get_test_basic_info(test_user_token)
crpo_common_obj.save_apppreferences(admin_token, json.dumps(sec_res_obj.api_thorttle_json), 201, 'api_throttle')
hirepro_token.pop("X-APPLMA")
# Reading data from Excel file
excel_read_obj.excel_read(input_path_rate_control, 0)
excel_data = excel_read_obj.details
for data in excel_data:
    if data.get('rateControlConfig') == 'False':
        print("FALSE")
        sec_res_obj.api_thorttle_json['ENABLED'] = False
        crpo_common_obj.save_apppreferences(admin_token, json.dumps(sec_res_obj.api_thorttle_json), 201,
                                            'api_throttle')
    else:
        print("TRUE")
        sec_res_obj.api_thorttle_json['ENABLED'] = True
        crpo_common_obj.save_apppreferences(admin_token, json.dumps(sec_res_obj.api_thorttle_json), 201,
                                            'api_throttle')
    if data.get('typeOfUser') == 'CRPOADMIN':
        sec_res_obj.rate_control(admin_token, data)
    elif data.get('typeOfUser') == 'TESTUSER':
        sec_res_obj.rate_control(test_user_token, data)
    elif data.get('typeOfUser') == 'TPO':
        print("Hey this is TPO")
        sec_res_obj.rate_control(tpo_token, data)
    elif data.get('typeOfUser') == 'VENDOR':
        print("Hey this is VENDOR")
        sec_res_obj.rate_control(vendor_token, data)
    elif data.get('typeOfUser') == 'CANDIDATE':
        print("Hey this is CANDIDATE token")
        sec_res_obj.rate_control(candidate_token, data)
    elif data.get('typeOfUser') == 'BACKEND':
        print("Hey this is BACKEND token")
        sec_res_obj.rate_control(backend_token, data)
    elif data.get('typeOfUser') == 'UITOKEN':
        print("Hey this is UI TOKEN")
        sec_res_obj.rate_control(ui_token, data)
    else:
        sec_res_obj.rate_control(non_admin_token, data)
write_excel_object.write_overall_status(testcases_count=2)
sec_res_obj.api_thorttle_json['ENABLED'] = False
crpo_common_obj.save_apppreferences(admin_token, json.dumps(sec_res_obj.api_thorttle_json), 201, 'api_throttle')
