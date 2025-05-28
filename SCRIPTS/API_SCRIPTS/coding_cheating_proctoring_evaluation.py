from SCRIPTS.CRPO_COMMON.crpo_common import *
from SCRIPTS.CRPO_COMMON.credentials import *
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.CRPO_COMMON.proc_eval_config import *


class CodingCheating:
    def __init__(self):
        write_excel_object.save_result(output_path_code_cheat_proctor_evaluation)
        # 0th Row Header
        header = ['Proctoring Evaluation automation']
        # 1 Row Header
        write_excel_object.write_headers_for_scripts(0, 0, header, write_excel_object.black_color_bold)
        header = ['Testcases', 'Status', 'Test ID', 'Candidate ID', 'Testuser ID', 'Expected Liveness proct status',
                  'Actual Liveness proct status',
                  'Expected overall proctoring status',
                  'Actual overall proctoring status', 'Expected overall rating', 'Actual overall rating',
                  'Expected Video proctoring status', 'Actual Video Proctoring status']
        write_excel_object.write_headers_for_scripts(1, 0, header, write_excel_object.black_color_bold)

    def suspicious_or_not_supicious(self, data, overall_proctoring_status_value):
        if data is True:
            # only overall proctoring status has number value.
            if overall_proctoring_status_value is False:
                self.status = 'Suspicious'
            else:
                if overall_proctoring_status_value >= 0.66:
                    self.status = 'Highly Suspicious'

                elif overall_proctoring_status_value >= 0.35:
                    self.status = 'Medium'

                elif overall_proctoring_status_value > 0:
                    self.status = 'Low'
                else:
                    self.status = 'Not Suspicious'
        else:
            self.status = 'Not Suspicious'

    def proctor_detail(self, row_count, current_excel_data, token):
        write_excel_object.current_status_color = write_excel_object.green_color
        write_excel_object.current_status = "Pass"
        tu_id = int(current_excel_data.get('testUserId'))
        print(tu_id)
        tu_proctor_details = crpo_common_obj.get_tu_proc_screen_data(token, tu_id)
        print(tu_proctor_details)
        proctor_detail = tu_proctor_details['data']['getProctorDetail']
        coding_sus = proctor_detail.get('codingSuspiciousDetails')
        if coding_sus:
            coding_suspicious = coding_sus.get('codingSuspicious')
        else:
            coding_suspicious = 'EMPTY'
        # self.suspicious_or_not_supicious(device_suspicious, False)
        write_excel_object.compare_results_and_write_vertically(
            current_excel_data.get('expectedCodingCheatingStatus'), coding_suspicious, row_count, 5)
        object_proctoring = proctor_detail.get('behaviouralSuspicious')
        overall_proctoring_status = proctor_detail.get('finalDecision')
        overall_suspicious_value = proctor_detail.get('systemOverallDecision')
        self.suspicious_or_not_supicious(overall_proctoring_status, overall_suspicious_value)
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('overallProctoringStatus'),
                                                                self.status, row_count, 7)
        excel_overall_suspicious_value = round(current_excel_data.get('overallSuspiciousValue'), 4)
        write_excel_object.compare_results_and_write_vertically(excel_overall_suspicious_value,
                                                                overall_suspicious_value, row_count, 9)
        write_excel_object.compare_results_and_write_vertically(object_proctoring,
                                                                current_excel_data.get('expectedBehaviouralSuspicious'),
                                                                row_count, 11)
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('testCase'), None, row_count, 0)
        write_excel_object.compare_results_and_write_vertically(write_excel_object.current_status, None, row_count, 1)
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('testId'), None, row_count, 2)
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('candidateId'), None, row_count,
                                                                3)
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('testUserId'), None, row_count,
                                                                4)


login_token = crpo_common_obj.login_to_crpo(cred_crpo_admin_crpodemo.get('user'),
                                            cred_crpo_admin_crpodemo.get('password'),
                                            cred_crpo_admin_crpodemo.get('tenant'))
# content = json.dumps(automation_proctor_eval_app_pref)
# app_pref_proc_eval_id = automation_tenant_proc_eval_id
# app_pref_proc_eval_type = automation_tenant_proc_eval_type
# update_app_preference = CrpoCommon.save_apppreferences(login_token, content, app_pref_proc_eval_id,
#                                                        app_pref_proc_eval_type)

excel_read_obj.excel_read(input_path_proctor_evaluation, 5)
excel_data = excel_read_obj.details
proctor_obj = CodingCheating()
tuids = []
over_all_status = 'Pass'
for fetch_tuids in excel_data:
    tuids.append(int(fetch_tuids.get('testUserId')))
context_id = CrpoCommon.force_evaluate_proctoring(login_token, tuids)
print(context_id)
print(tuids)
context_id = context_id['data']['ContextId']
print(context_id)
current_job_status = 'Pending'

while current_job_status != 'SUCCESS':
    current_job_status = CrpoCommon.job_status(login_token, context_id)
    current_job_status = current_job_status['data']['JobState']
    print("_________________ Proctor Evaluation is in Progress _______________________")
    print(current_job_status)
    time.sleep(20)

row_count = 2
for data in excel_data:
    proctor_obj.proctor_detail(row_count, data, login_token)
    row_count = row_count + 1
write_excel_object.write_overall_status(testcases_count=10)
