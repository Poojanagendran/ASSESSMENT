from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.CRPO_COMMON.crpo_common import *
from SCRIPTS.CRPO_COMMON.credentials import *
from SCRIPTS.COMMON.io_path import *


class ResponseEncryption:

    def __init__(self):
        requests.packages.urllib3.disable_warnings()
        self.row_count = 2
        write_excel_object.save_result(output_path_response_encryption)
        # print(output_path_allowed_extension)
        self.write_headers()

    def write_headers(self):
        # Writing headers in the Excel file
        headers = ["Response Payload Ecryption"]
        write_excel_object.write_headers_for_scripts(0, 0, headers, write_excel_object.black_color_bold)
        headers1 = ["Testcase", "Status", "Api id", "Api configuration", "Tenant Configuration", "Tenant Alias",
                    "Expected Behaviour", "Actual Behaviour", "Actual API Response"]
        write_excel_object.write_headers_for_scripts(1, 0, headers1, write_excel_object.black_color_bold)

    def check_payload_encryption(self, token, test_case_data):

        write_excel_object.current_status_color = write_excel_object.green_color
        write_excel_object.current_status = "Pass"
        test_case = test_case_data.get('testCase')
        api_id = int(test_case_data.get('apiId'))
        encryption_config = test_case_data.get('apiAuditUpdate')
        tenant_alias = test_case_data.get('tenantAlias')
        tenant_id = int(test_case_data.get('tenantId'))
        # tenant_enc_config = test_case_data.get('tenantUpdate')
        if test_case_data.get('tenantUpdate') == 'True':
            tenant_enc_config = True
        else:
            tenant_enc_config = False
        expected_behaviour = test_case_data.get('expectedBehaviour')

        if encryption_config == "True":
            api_enc_conf = {"responsePayload": {"enabled": True}}
        elif encryption_config == "False":
            api_enc_conf = {"responsePayload": {"enabled": False}}
        else:
            api_enc_conf = None

        api_audit_config = {"id": api_id, "doNotAudit": False,
                            "responseCaching": {"isEnabled": False, "sleepFor": None},
                            "ssrfConfig": {"isByPassOutgoingAPI": False, "isByPassIncomingAPI": False},
                            "urlSigningConfig": {"IC_JSON": {"NEUTRALISE_SIGNED_URLS_IN_IC_JSON": False},
                                                 "OG_JSON": {"MAKE_READABLE_URLS_IN_OG_JSON": False,
                                                             "SIGNED_URL_TIMEOUT_IN_SECONDS": 0},
                                                 "idorConfig": {"isEnabledForAMSUser": False}},
                            "encryptionConfig": api_enc_conf,
                            "idorConfig": None, "doNotAuditRequestPayload": False, "doNotAuditResponsePayload": False,
                            "auditPayloadsInS3": False, "requestPayloadSizeConfig": None, "httpMethodsConfig": None,
                            "ipThrottlingConfig": None}
        update_config = crpo_common_obj.update_tenant_config(token, tenant_id, tenant_enc_config)
        payload_enc = crpo_common_obj.update_api_audit(token, api_audit_config)
        remove_cache = crpo_common_obj.clear_tenant_cache(token, tenant_alias)
        res = crpo_common_obj.security_login_to_crpo(cred_crpo_admin_security_automation.get('user'),
                                                     cred_crpo_admin_security_automation.get('password'),
                                                     cred_crpo_admin_security_automation.get('tenant'))
        print(res)
        if "Token" in str(res):
            actual_behaviour = "Not Encrypted"
        else:
            actual_behaviour = "Encrypted"

        if actual_behaviour == expected_behaviour:
            status = "Pass"
        else:
            status = "Fail"

        write_excel_object.compare_results_and_write_vertically(test_case, None, self.row_count, 0)
        write_excel_object.compare_results_and_write_vertically(api_id, None, self.row_count, 2)
        write_excel_object.compare_results_and_write_vertically(encryption_config, None, self.row_count, 3)
        write_excel_object.compare_results_and_write_vertically(tenant_enc_config, None, self.row_count, 4)
        write_excel_object.compare_results_and_write_vertically(tenant_alias, None, self.row_count, 5)
        write_excel_object.compare_results_and_write_vertically(expected_behaviour, actual_behaviour, self.row_count, 6)
        write_excel_object.compare_results_and_write_vertically(write_excel_object.current_status, None, self.row_count,
                                                                1)
        write_excel_object.compare_results_and_write_vertically(str(res), None, self.row_count, 8)
        self.row_count = self.row_count + 1


sec_res_obj = ResponseEncryption()
login_token = crpo_common_obj.login_to_crpo(cred_crpo_admin_hirepro.get('user'),
                                            cred_crpo_admin_hirepro.get('password'),
                                            cred_crpo_admin_hirepro.get('tenant'))
login_token.pop("X-APPLMA")
# Reading data from Excel file
excel_read_obj.excel_read(input_path_response_encryption, 0)
excel_data = excel_read_obj.details

# Validating files and writing results
for data in excel_data:
    sec_res_obj.check_payload_encryption(login_token, data)
write_excel_object.write_overall_status(testcases_count=2)
