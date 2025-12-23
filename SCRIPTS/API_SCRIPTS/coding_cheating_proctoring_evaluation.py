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
        header = ['Testcases', 'Status', 'Test ID', 'Candidate ID', 'Testuser ID', 'Expected Coding Cheating Status',
                  'Actual Coding Cheating Status','Expected coding state', 'Actual coding state',
                  'Expected overall proctoring status',
                  'Actual overall proctoring status', 'Expected overall rating', 'Actual overall rating',
                  'Expected Behavioural proctoring status', 'Actual Behavioural Proctoring status']
        write_excel_object.write_headers_for_scripts(1, 0, header, write_excel_object.black_color_bold)

    def proctor_detail(self, row_count, current_excel_data, token):
        write_excel_object.current_status_color = write_excel_object.green_color
        write_excel_object.current_status = "Pass"
        tu_id = int(current_excel_data.get('testUserId'))
        tu_id = {"tuId": tu_id}
        tu_proctor_details = crpo_common_obj.get_tu_proc_screen_data(token, tu_id)
        proctor_detail = tu_proctor_details['data']['getProctorDetail']
        coding_sus = proctor_detail.get('codingSuspiciousDetails')
        if coding_sus:
            coding_suspicious = coding_sus.get('codingSuspicious')
            coding_suspicious_state_name = coding_sus.get('statusName')
        else:
            coding_suspicious = 'EMPTY'
            coding_suspicious_state_name = 'EMPTY'
        # self.suspicious_or_not_supicious(device_suspicious, False)
        write_excel_object.compare_results_and_write_vertically(
            current_excel_data.get('expectedCodingCheatingStatus'), coding_suspicious, row_count, 5)
        write_excel_object.compare_results_and_write_vertically(
            current_excel_data.get('expectedCodingCheatingState'), coding_suspicious_state_name, row_count, 7)
        object_proctoring = proctor_detail.get('behaviouralSuspicious')
        # overall_proctoring_status = proctor_detail.get('finalDecision')
        overall_suspicious_value = proctor_detail.get('systemOverallDecision')
        if overall_suspicious_value >= 0.66:
            overall_proctoring_status = 'Highly Suspicious'

        elif overall_suspicious_value >= 0.35:
            overall_proctoring_status = 'Medium'

        elif overall_suspicious_value > 0:
            overall_proctoring_status = 'Low'
        else:
            overall_proctoring_status = 'Not Suspicious'
        # self.suspicious_or_not_supicious( overall_suspicious_value)
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('overallProctoringStatus'),
                                                                overall_proctoring_status, row_count, 9)
        excel_overall_suspicious_value = round(current_excel_data.get('overallSuspiciousValue'), 4)
        write_excel_object.compare_results_and_write_vertically(excel_overall_suspicious_value,
                                                                overall_suspicious_value, row_count, 11)
        write_excel_object.compare_results_and_write_vertically(object_proctoring,
                                                                current_excel_data.get('expectedBehaviouralSuspicious'),
                                                                row_count, 13)
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('testCase'), None, row_count, 0)
        write_excel_object.compare_results_and_write_vertically(write_excel_object.current_status, None, row_count, 1)
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('testId'), None, row_count, 2)
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('candidateId'), None, row_count,
                                                                3)
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('testUserId'), None, row_count,
                                                                4)


login_token = crpo_common_obj.login_to_crpo(cred_crpo_admin.get('user'),
                                            cred_crpo_admin.get('password'),
                                            cred_crpo_admin.get('tenant'))
content = json.dumps(automation_coding_cheating_proctor_eval_app_pref)
app_pref_proc_eval_id = automation_tenant_proc_eval_id
app_pref_proc_eval_type = automation_tenant_proc_eval_type
update_app_preference = CrpoCommon.save_apppreferences(login_token, content, app_pref_proc_eval_id,
                                                       app_pref_proc_eval_type)

excel_read_obj.excel_read(input_path_proctor_evaluation, 5)
excel_data = excel_read_obj.details
proctor_obj = CodingCheating()
tuids = []
over_all_status = 'Pass'
for fetch_tuids in excel_data:
    tuids.append(int(fetch_tuids.get('testUserId')))
context_id = CrpoCommon.force_evaluate_proctoring(login_token, tuids)
print("contextId : ")
print(context_id)
print("TestUserIds: ")
print(tuids)
context_id = context_id['data']['ContextId']
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
write_excel_object.write_overall_status(testcases_count=23)
