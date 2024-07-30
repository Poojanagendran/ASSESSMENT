from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.CRPO_COMMON.credentials import *
from SCRIPTS.CRPO_COMMON.crpo_common import *
from SCRIPTS.ASSESSMENT_COMMON.assessment_common import *
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.DB_DELETE.db_cleanup import *


class ReInitiateAutomation:
    def __init__(self):
        data_clean_obj.delete_assessment_test_users_for_reinitateautomation()
        self.row_size = 2
        write_excel_object.save_result(output_path_reinitiate_automation)
        header = ["Reinitiate relogin automation"]
        write_excel_object.write_headers_for_scripts(0, 0, header,
                                                     write_excel_object.black_color_bold)
        header1 = ["Testcases", "Status", "Test ID", "Candidate ID", "Login Name", "Password", "Is Vendor Test",
                   "Is SLC Enabled", "Expected Status", "Actual Status"]
        write_excel_object.write_headers_for_scripts(1, 0, header1,
                                                     write_excel_object.black_color_bold)

    def test_user_next_test_status(self, login_response):
        print(login_response)
        if login_response.get('status') == 'KO':
            next_test_flags = login_response.get('error').get('nextTestFlags')
            if next_test_flags:
                if next_test_flags.get('isScoreFetched'):
                    if next_test_flags.get('isShortlisted'):
                        self.final_status = "Shortlisted"
                        # if next_test_flags.get('isRegistered'):
                        #     print("Candidate is registered in the vendor test")
                        #     self.final_status = "Shortlisted"
                        # else:
                        #     print("Candidate is not registered in the vendor test")
                        #     self.final_status = "Rejected"
                    else:
                        print("Score is available but not shortlisted for the next test")
                        self.final_status = "Rejected"
                else:
                    if next_test_flags.get('isHproTest') == True:
                        print("Chaining test without SLC")
                        self.final_status = "Shortlisted"
                        # if next_test_flags.get('isRegistered') == False:
                        #     self.final_status = "Rejected"
                        # else:
                        #     self.final_status = "Shortlisted"
                    else:
                        print("Score is not available")
                        self.final_status = "Rejected"
            else:
                print("Test is already submitted")
                self.final_status = "Completed"
        else:
            print("First test is not completed")
            self.final_status = "Pending"

    def excel_write(self, data):
        write_excel_object.current_status_color = write_excel_object.green_color
        write_excel_object.current_status = "Pass"
        write_excel_object.compare_results_and_write_vertically(data.get('testCaseInfo'), None, self.row_size, 0)
        write_excel_object.compare_results_and_write_vertically(data.get('primaryTestId'), None, self.row_size, 2)
        write_excel_object.compare_results_and_write_vertically(data.get('candidateId'), None, self.row_size, 3)
        write_excel_object.compare_results_and_write_vertically(data.get('loginName'), None, self.row_size, 4)
        write_excel_object.compare_results_and_write_vertically(data.get('password'), None, self.row_size, 5)
        write_excel_object.compare_results_and_write_vertically(data.get('isVendorTest'), None, self.row_size, 6)
        write_excel_object.compare_results_and_write_vertically(data.get('IsSLCEnabled'), None, self.row_size, 7)
        write_excel_object.compare_results_and_write_vertically(data.get('expectedStatus'), self.final_status,
                                                                self.row_size, 8)
        write_excel_object.compare_results_and_write_vertically(write_excel_object.current_status, None, self.row_size,
                                                                1)
        self.row_size = self.row_size + 1


re_initiate_obj = ReInitiateAutomation()
excel_read_obj.excel_read(input_path_reinitiate_automation, 0)
excel_data = excel_read_obj.details
crpo_headers = crpo_common_obj.login_to_crpo(cred_crpo_admin.get('user'), cred_crpo_admin.get('password'),
                                             cred_crpo_admin.get('tenant'))

untag_candidate_id_and_test_id = {}
for data in excel_data:
    test_id = int(data.get('primaryTestId'))
    next_test_id = int(data.get('nextTestId'))
    candiate_id = int(data.get('candidateId'))
    if data.get('isUntaggedFromT2') == 'Yes':
        tu_data = crpo_common_obj.search_test_user_by_cid_and_testid(crpo_headers, candiate_id, next_test_id)
        tu_id = tu_data.get('testUserId')
        if tu_id != 'NotExist':
            print(tu_id)
            untag_candidates_details = [{"testUserIds": [tu_id]}]
            crpo_common_obj.untag_candidate(crpo_headers, untag_candidates_details)

    crpo_common_obj.re_initiate_automation(crpo_headers, test_id, candiate_id)
    time.sleep(5)
    assessment_headers = AssessmentCommon.login_to_test(login_name=data.get('loginName'), password=data.get('password'),
                                                        tenant='automation')
    re_initiate_obj.test_user_next_test_status(assessment_headers)
    re_initiate_obj.excel_write(data)
write_excel_object.write_overall_status(testcases_count=29)
