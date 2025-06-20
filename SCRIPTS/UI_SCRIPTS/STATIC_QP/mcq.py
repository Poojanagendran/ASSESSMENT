from SCRIPTS.UI_COMMON.assessment_ui_common_v2 import *
from SCRIPTS.UI_SCRIPTS.assessment_data_verification import *
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.DB_DELETE.db_cleanup import *


class OnlineAssessment:

    def __init__(self):
        self.url = amsin_at_assessment_url
        self.path = chrome_driver_path
        # data clean up is important, b'coz we need to create a candidate everytime to check the create is working fine.
        data_clean_obj.static_ui_automation_delete()

    def mcq_assessment(self, current_excel_data):
        self.browser = assess_ui_common_obj.initiate_browser(self.url, self.path)
        login_details = assess_ui_common_obj.ui_login_to_test(current_excel_data.get('loginName'),
                                                              (current_excel_data.get('password')))
        if login_details == 'SUCCESS':
            i_agreed = assess_ui_common_obj.select_i_agree()
            if i_agreed:
                start_test_status = assess_ui_common_obj.start_test_button_status()
                assess_ui_common_obj.start_test()
                if current_excel_data.get('skipRquired') == 'Yes':
                    assess_ui_common_obj.next_question(5)
                    assess_ui_common_obj.end_test()
                    assess_ui_common_obj.end_test_confirmation()
                    time.sleep(3)
                    self.browser.quit()

                elif current_excel_data.get('reloginRequird') == 'Yes':
                    assess_ui_common_obj.select_answer_for_the_question(current_excel_data.get('ans_qid1'))
                    assess_ui_common_obj.next_question(2)
                    assess_ui_common_obj.select_answer_for_the_question(current_excel_data.get('ans_qid2'))
                    assess_ui_common_obj.next_question(3)
                    assess_ui_common_obj.select_answer_for_the_question(current_excel_data.get('ans_qid3'))
                    assess_ui_common_obj.next_question(4)
                    assess_ui_common_obj.select_answer_for_the_question(current_excel_data.get('ans_qid4'))
                    assess_ui_common_obj.next_question(5)
                    assess_ui_common_obj.select_answer_for_the_question(current_excel_data.get('ans_qid5'))
                    self.browser.close()
                    self.browser.switch_to.window(self.browser.window_handles[0])
                    time.sleep(1)
                    self.browser.execute_script(
                        '''window.open("https://amsin.hirepro.in/assessment/#/assess/login/eyJhbGlhcyI6ImF0In0=", "_blank");''')
                    time.sleep(2)
                    self.browser.switch_to.window(self.browser.window_handles[1])
                    login_details = assess_ui_common_obj.ui_login_to_test(current_excel_data.get('loginName'),
                                                                          (current_excel_data.get('password')))
                    if login_details == 'SUCCESS':
                        i_agreed = assess_ui_common_obj.select_i_agree()
                        if i_agreed:
                            start_test_status = assess_ui_common_obj.start_test_button_status()
                            assess_ui_common_obj.start_test()
                            if current_excel_data.get('isAnswerChangeRequired') == 'Yes':
                                answered_status_for_q1 = assess_ui_common_obj.check_answered_status(
                                    current_excel_data.get('ans_qid1'))
                                assess_ui_common_obj.select_answer_for_the_question(current_excel_data.get('relogin_qid1'))
                                assess_ui_common_obj.next_question(2)
                                answered_status_for_q2 = assess_ui_common_obj.check_answered_status(
                                    current_excel_data.get('ans_qid1'))
                                assess_ui_common_obj.select_answer_for_the_question(current_excel_data.get('relogin_qid2'))
                                assess_ui_common_obj.next_question(3)
                                answered_status_for_q3 = assess_ui_common_obj.check_answered_status(
                                    current_excel_data.get('ans_qid1'))
                                assess_ui_common_obj.select_answer_for_the_question(current_excel_data.get('relogin_qid3'))
                                assess_ui_common_obj.next_question(4)
                                answered_status_for_q4 = assess_ui_common_obj.check_answered_status(
                                    current_excel_data.get('ans_qid1'))
                                assess_ui_common_obj.select_answer_for_the_question(current_excel_data.get('relogin_qid4'))
                                assess_ui_common_obj.next_question(5)
                                answered_status_for_q5 = assess_ui_common_obj.check_answered_status(
                                    current_excel_data.get('ans_qid1'))
                                assess_ui_common_obj.select_answer_for_the_question(current_excel_data.get('relogin_qid5'))
                                assess_ui_common_obj.end_test()
                                assess_ui_common_obj.end_test_confirmation()
                                time.sleep(5)
                            elif current_excel_data.get('unAnswerRequired') == 'Yes':
                                assess_ui_common_obj.unanswer_question()
                                assess_ui_common_obj.next_question(2)
                                assess_ui_common_obj.unanswer_question()
                                assess_ui_common_obj.next_question(3)
                                assess_ui_common_obj.unanswer_question()
                                assess_ui_common_obj.next_question(4)
                                assess_ui_common_obj.unanswer_question()
                                assess_ui_common_obj.next_question(5)
                                assess_ui_common_obj.unanswer_question()
                                assess_ui_common_obj.end_test()
                                assess_ui_common_obj.end_test_confirmation()
                                time.sleep(5)
                                # self.browser.quit()
                            else:
                                assess_ui_common_obj.next_question(5)
                                assess_ui_common_obj.end_test()
                                assess_ui_common_obj.end_test_confirmation()
                                time.sleep(5)
                            self.browser.quit()

                else:
                    if current_excel_data.get('unAnswerRequired') == 'No':
                        assess_ui_common_obj.select_answer_for_the_question(current_excel_data.get('ans_qid1'))
                        assess_ui_common_obj.next_question(2)
                        assess_ui_common_obj.select_answer_for_the_question(current_excel_data.get('ans_qid2'))
                        assess_ui_common_obj.next_question(3)
                        assess_ui_common_obj.select_answer_for_the_question(current_excel_data.get('ans_qid3'))
                        assess_ui_common_obj.next_question(4)
                        assess_ui_common_obj.select_answer_for_the_question(current_excel_data.get('ans_qid4'))
                        assess_ui_common_obj.next_question(5)
                        assess_ui_common_obj.select_answer_for_the_question(current_excel_data.get('ans_qid5'))
                        assess_ui_common_obj.end_test()
                        assess_ui_common_obj.end_test_confirmation()
                        time.sleep(5)
                        # self.browser.quit()
                    else:
                        assess_ui_common_obj.select_answer_for_the_question(current_excel_data.get('ans_qid1'))
                        assess_ui_common_obj.unanswer_question()
                        assess_ui_common_obj.next_question(2)
                        assess_ui_common_obj.select_answer_for_the_question(current_excel_data.get('ans_qid2'))
                        assess_ui_common_obj.unanswer_question()
                        assess_ui_common_obj.next_question(3)
                        assess_ui_common_obj.select_answer_for_the_question(current_excel_data.get('ans_qid3'))
                        assess_ui_common_obj.unanswer_question()
                        assess_ui_common_obj.next_question(4)
                        assess_ui_common_obj.select_answer_for_the_question(current_excel_data.get('ans_qid4'))
                        assess_ui_common_obj.unanswer_question()
                        assess_ui_common_obj.next_question(5)
                        assess_ui_common_obj.select_answer_for_the_question(current_excel_data.get('ans_qid5'))
                        assess_ui_common_obj.unanswer_question()
                        assess_ui_common_obj.end_test()
                        assess_ui_common_obj.end_test_confirmation()
                        time.sleep(5)
                    self.browser.quit()
        else:
            print("login failed due to below reason")
            print(login_details)

print(datetime.datetime.now())
assessment_obj = OnlineAssessment()

excel_read_obj.excel_read(input_path_ui_static_mcq, 0)
excel_data = excel_read_obj.details
for current_excel_row in excel_data:
    print(current_excel_row)
    assessment_obj.mcq_assessment(current_excel_row)
crpo_token = crpo_common_obj.login_to_crpo(cred_crpo_admin_at.get('user'), cred_crpo_admin_at.get('password'),
                                            cred_crpo_admin_at.get('tenant'))
print(crpo_token)
# time.sleep(10)
obj_assessment_data_verification.assessment_data_report(crpo_token, excel_data)
obj_assessment_data_verification.write_excel.close()
print(datetime.datetime.now())


