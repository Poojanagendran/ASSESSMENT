from SCRIPTS.COMMON.io_path import *
# from SCRIPTS.COMMON.writeExcel import write_excel_object
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.UI_COMMON.assessment_ui_common_v2 import *
from SCRIPTS.CRPO_COMMON.credentials import *
import time
from SCRIPTS.UI_SCRIPTS.assessment_data_verification import *


class WheeboxChaining:
    def __init__(self):
        self.driver = None
        self.url = "https://amsin.hirepro.in/assessment/#/assess/login/eyJhbGlhcyI6ImF1dG9tYXRpb24ifQ=="
        self.path = chrome_driver_path
        write_excel_object.save_result(output_path_ui_wheebox)
        # 0th Row Header
        header = ['Wheebox']
        # 1 Row Header
        write_excel_object.write_headers_for_scripts(0, 0, header, write_excel_object.black_color_bold)
        header = ['Testcases', 'Status', 'Test ID', 'Candidate ID', 'Testuser ID', 'Group1 mark', 'Group2 mark',
                  'Group3 mark', 'Group4 mark', 'Report link']
        write_excel_object.write_headers_for_scripts(1, 0, header, write_excel_object.black_color_bold)
        self.row_size = 2

    def wheebox_technical(self, login_id, password, tkn, tu_request):

        # assess_ui_common_obj.wheebox_t2start( self.path, 'https://ain.hirepro.in/t924MaYM')
        testuser_id = tu_request['testUserId']
        overall_color = write_excel_object.green_color
        browser = assess_ui_common_obj.initiate_browser(self.url)
        login_details = assess_ui_common_obj.ui_login_to_test(login_id, password)
        # self.browser.get_screenshot_as_file(self.common_path + "\\1_t1_afterlogin.png")
        # about_online_proctoring = assess_ui_common_obj.about_online_proctoring()
        assessment_terms_and_conditions = assess_ui_common_obj.assessment_terms_and_conditions()
        # selfie = assess_ui_common_obj.selfie()
        overall_status = 'pass'
        if login_details == 'SUCCESS':
            i_agreed = assess_ui_common_obj.select_i_agree()
            if i_agreed:
                start_test_status = assess_ui_common_obj.start_test_button_status()
                hirepro_start_test = assess_ui_common_obj.start_test()
                wb_agreement = assess_ui_common_obj.wheebox_starttest_checkbox()
                wb_proceed_test = assess_ui_common_obj.wheebox_proceed_test()
                wb_auto_next_qn = assess_ui_common_obj.wheebox_auto_next_qn()
                wb_click_q1 = assess_ui_common_obj.wheebox_q1_ans()
                for question_count in range(0, 10):
                    answer_qn = assess_ui_common_obj.wheebox_answer_qn()
                    print(question_count)
                time.sleep(10)
                wb_submit_test = assess_ui_common_obj.wheebox_submit_test()
                time.sleep(3)
                wb_confirm_submit = assess_ui_common_obj.wheebox_confirm_submit()
                # time.sleep(180)
                assess_ui_common_obj.chaining_shortlisting()
                # t2_wheebox_starting = assess_ui_common_obj.start_next_test()
        # about_online_proctoring = assess_ui_common_obj.about_online_proctoring()
        time.sleep(5)
        assessment_terms_and_conditions = assess_ui_common_obj.assessment_terms_and_conditions()
        # selfie = assess_ui_common_obj.selfie()
        # overall_status = 'pass'
        if login_details == 'SUCCESS':
            i_agreed = assess_ui_common_obj.select_i_agree()
            if i_agreed:
                start_test_status = assess_ui_common_obj.start_test_button_status()
                hirepro_start_test = assess_ui_common_obj.start_test()
                wb_agreement = assess_ui_common_obj.wheebox_starttest_checkbox()
                wb_proceed_test = assess_ui_common_obj.wheebox_proceed_test()
                wb_auto_next_qn = assess_ui_common_obj.wheebox_auto_next_qn()
                wb_click_q1 = assess_ui_common_obj.wheebox_q1_ans()
                for question_count in range(0, 30):
                    answer_qn = assess_ui_common_obj.wheebox_answer_qn()
                    print(question_count)
                time.sleep(10)
                wb_submit_test = assess_ui_common_obj.wheebox_submit_test()
                wb_confirm_submit = assess_ui_common_obj.wheebox_confirm_submit()
                time.sleep(60)
        browser.quit()


qs = WheeboxChaining()
token = crpo_common_obj.login_to_crpo(cred_crpo_admin.get('user'), cred_crpo_admin.get('password'),
                                      cred_crpo_admin.get('tenant'))
sprint_id = str(datetime.datetime.now())
candidate_id = crpo_common_obj.create_candidate(token, sprint_id)
test1_id = 21589
test2_id = 21591
event_id = 19191
jobrole_id = 32749
tag_candidate = crpo_common_obj.tag_candidate_to_test(token, candidate_id, test1_id, event_id, jobrole_id)
test_userid = crpo_common_obj.get_all_test_user(token, candidate_id)
tu_req_payload = {"testUserId": test_userid,
                  "requiredFlags": {"fileContentRequired": False, "isQuestionWise": True, "questionTypes": [16, 8],
                                    "isGroupSectionWiseMarks": True, "isVendorDetails": True, "isCodingSummary": False}}
tu_cred = crpo_common_obj.test_user_credentials(token, test_userid)
login_id = tu_cred['data']['testUserCredential']['loginId']
password = tu_cred['data']['testUserCredential']['password']
qs.wheebox_technical(login_id, password, token, tu_req_payload)
qs.wheebox_technical()
write_excel_object.write_overall_status(testcases_count=2)
