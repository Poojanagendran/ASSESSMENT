from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.CRPO_COMMON.credentials import *
from SCRIPTS.CRPO_COMMON.crpo_common import *
from SCRIPTS.COMMON.io_path import *
from Logging.Logging import logging_config
import time
import logging


class ReuseScore:

    def __init__(self):
        logging_config(log_reuse_score)
        logging.info('Initialized successfully')
        self.test_login_informations = {}
        write_excel_object.save_result(output_path_reuse_score)
        header = ["Chaining Of Two Tests"]
        write_excel_object.write_headers_for_scripts(0, 0, header, write_excel_object.black_color_bold)
        header1 = ["Test cases", "Test case status", "Candidate Id", "Old Event Id", "New Event Id", "Old Test1 Id",
                   "New Test1 Id", "Applicant Id", "Expected Total Score in New T1", "Actual Total Score in New T1",
                   "Expected Test user status in New T1", "Actual Test user status in New T1",
                   "Are you Expecting Test report in new T1?", "Is test report available in new T1",
                   "Expected applicant current status", "Actual applicant current status",
                   "Expected applicant previous status", "Actual applicant previous status",
                   "Expected applicant previous2 status", "Actual applicant previous2 status",
                   " Are you expecting test user in T2?", "is candidate available in T2?"]
        write_excel_object.write_headers_for_scripts(1, 0, header1, write_excel_object.black_color_bold)

    def make_report(self, row_count, current_excel_data, total_mark, third_party_test_link, test_status,
                    last_three_stage_status, new_test2_userid):
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('testCase'), None, row_count, 0)
        write_excel_object.compare_results_and_write_vertically(int(current_excel_data.get('candidateId')), None,
                                                                row_count, 2)
        write_excel_object.compare_results_and_write_vertically(int(current_excel_data.get('oldEventId')), None,
                                                                row_count, 3)
        write_excel_object.compare_results_and_write_vertically(int(current_excel_data.get('newEventId')), None,
                                                                row_count, 4)
        write_excel_object.compare_results_and_write_vertically(int(current_excel_data.get('oldEventTest1Id')), None,
                                                                row_count, 5)
        write_excel_object.compare_results_and_write_vertically(int(current_excel_data.get('newEventTest1Id')), None,
                                                                row_count, 6)
        write_excel_object.compare_results_and_write_vertically(int(current_excel_data.get('newEventApplicantId')),
                                                                None, row_count, 7)
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('expectedTest1OverallScore'),
                                                                total_mark, row_count, 8)
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('expectedT1Status'), test_status,
                                                                row_count, 10)
        write_excel_object.compare_results_and_write_vertically(
            current_excel_data.get('areYouExpectingTestLinkForNewT1?'), None, row_count, 12)

        write_excel_object.compare_results_and_write_vertically(None, third_party_test_link, row_count, 13)
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('expectedstatus1InEvent2'),
                                                                last_three_stage_status[2], row_count, 14)
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('expectedstatus2InEvent2'),
                                                                last_three_stage_status[1], row_count, 16)
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('expectedstatus3InEvent2'),
                                                                last_three_stage_status[0], row_count, 18)

        if new_test2_userid != 'NotExist':
            t2_candidate_availability = 'Yes'
        else:
            t2_candidate_availability = 'No'

        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('expectedNextTestStatus'),
                                                                t2_candidate_availability, row_count, 20)

        write_excel_object.compare_results_and_write_vertically(write_excel_object.current_status, None, row_count, 1)


reuse_score = ReuseScore()
login_token = crpo_common_obj.login_to_crpo(cred_crpo_admin_at.get('user'), cred_crpo_admin_at.get('password'),
                                            cred_crpo_admin_at.get('tenant'))
excel_read_obj.excel_read(input_path_ui_reuse_score, 0)
excel_data = excel_read_obj.details
reuse_score_excel = excel_read_obj.details
logging.info('Successfully Read excel input')
# print(reuse_score_excel)
row_count = 1
for current_excel_data in reuse_score_excel:
    logging.info('Testcase info:- %s' % current_excel_data)
    row_count = row_count + 1
    candidate_id = int(current_excel_data.get('candidateId'))
    event_id = int(current_excel_data.get('newEventId'))
    job_id = int(current_excel_data.get('newJobId'))
    test1_id = int(current_excel_data.get('newEventTest1Id'))
    applicant_id = int(current_excel_data.get('newEventApplicantId'))
    to_status_id = int(current_excel_data.get('toStatusId'))
    test_user_details = crpo_common_obj.search_test_user_by_cid_and_testid(login_token, candidate_id, test1_id)
    old_tu_id_tuid = test_user_details.get('testUserId')
    untag_candidate = crpo_common_obj.force_untag_testuser(login_token, old_tu_id_tuid)
    change_candidate_status = crpo_common_obj.change_applicant_status(login_token, applicant_id, event_id, job_id,
                                                                      to_status_id)
    tag_to_test = crpo_common_obj.tag_candidate_to_test(login_token, candidate_id, test1_id, event_id, job_id)
    test_user_details = crpo_common_obj.search_test_user_by_cid_and_testid(login_token, candidate_id, test1_id)
    new_tu_tuid = test_user_details.get('testUserId')
    time.sleep(5)
    test2_id = int(current_excel_data.get('newEventTest2Id'))
    test_user_details = crpo_common_obj.search_test_user_by_cid_and_testid(login_token, candidate_id, test2_id)
    new_test2_userid = test_user_details.get('testUserId')
    if new_tu_tuid != 'NotExist':
        applicant_stage_status = []
        test_user_infos = crpo_common_obj.get_test_user_infos_v2(login_token, new_tu_tuid)
        # print(test_user_infos)
        total_mark = test_user_infos['data']['assessment']['marksObtained']
        print(test_user_infos)
        third_party_test_link = test_user_infos['data']['vendorDetails']['reportLink']
        test_status = test_user_infos['data']['assessment']['testUserStatus']
        get_applicant_status = crpo_common_obj.get_applicant_infos(login_token, candidate_id)
        for all_applicants_infos in (get_applicant_status['data'][0]['ApplicantDetails']):
            if all_applicants_infos.get('Id') == applicant_id:
                applicant_history = all_applicants_infos.get('ApplicantHistory')
                for stage_status in applicant_history[-3:]:
                    stage = stage_status.get('Stage')
                    status = stage_status.get('Status')
                    stage_status = {'stage': stage, 'status': status}
                    applicant_stage_status.append(stage_status)
            else:
                print("Applicant History Not Available in this object")
            print(applicant_stage_status)
            last_three_stage_status = []
            for data in applicant_stage_status:
                t1_status = data.get("stage") + "-" + data.get("status").strip()
                last_three_stage_status.append(t1_status)
        reuse_score.make_report(row_count, current_excel_data, total_mark, third_party_test_link,
                                test_status, last_three_stage_status, new_test2_userid)
    else:
        print("Test user is not exist")

write_excel_object.write_overall_status(testcases_count=1)
