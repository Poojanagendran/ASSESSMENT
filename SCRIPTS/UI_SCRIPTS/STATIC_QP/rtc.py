from SCRIPTS.UI_COMMON.assessment_ui_common_v2 import *
import time
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.CRPO_COMMON.crpo_common import *
from SCRIPTS.DB_DELETE.db_cleanup import *


class OnlineAssessment:

    def __init__(self):
        # data clean up is important, b'coz we need to create a candidate everytime to check the create is working fine.
        data_clean_obj.static_ui_automation_delete()
        self.row = 1
        write_excel_object.save_result(output_path_ui_rtc_static)
        header = ["UI automation"]
        write_excel_object.write_headers_for_scripts(0, 0, header, write_excel_object.black_color_bold)
        header = ["Testcases", "Status", "Test ID", "Candidate ID", "Login Name", "Password",
                  "Q1_candidate_answer_expected_data", "Q1_candidate_answer_actual_data",
                  "Q2_candidate_answer_expected_data", "Q2_candidate_answer_actual_data",
                  "Q3_candidate_answer_expected_data", "Q3_candidate_answer_actual_data",
                  "Q4_candidate_answer_expected_data", "Q4_candidate_answer_actual_data",
                  "Q5_candidate_answer_expected_data", "Q5_candidate_answer_actual_data",
                  "Q6_candidate_answer_expected_data", "Q6_candidate_answer_actual_data",
                  "Q7_candidate_answer_expected_data", "Q7_candidate_answer_actual_data",
                  "Q8_candidate_answer_expected_data", "Q8_candidate_answer_actual_data",
                  "Q9_candidate_answer_expected_data", "Q9_candidate_answer_actual_data"]
        write_excel_object.write_headers_for_scripts(1, 0, header, write_excel_object.black_color_bold)

    def rtc_assessment(self, current_excel_data, token):
        write_excel_object.current_status = "Pass"
        write_excel_object.current_status_color = write_excel_object.green_color
        self.browser = assess_ui_common_obj.initiate_browser(amsin_at_assessment_url, chrome_driver_path)
        login_details = assess_ui_common_obj.ui_login_to_test(current_excel_data.get('loginName'),
                                                              (current_excel_data.get('password')))
        total_child_questions_count = int(current_excel_data.get('childQuestionCount'))
        if login_details == 'SUCCESS':
            i_agreed = assess_ui_common_obj.select_i_agree()
            if i_agreed:
                start_test_status = assess_ui_common_obj.start_test_button_status()
                assess_ui_common_obj.start_test()

                if current_excel_data.get('reloginRequird') == 'No':
                    # This is Single login (Re-login is not required here)
                    if current_excel_data.get('skipRequired') == "No":
                        # Skip Required No means, need to answer something.
                        for question_count in range(0, total_child_questions_count):
                            # Assessment side question starts from Number One, so below addition is required
                            assess_ui_common_obj.select_answer_for_the_question(
                                current_excel_data.get('ans_qid%d' % (question_count + 1)))
                            if question_count != (total_child_questions_count - 1):
                                assess_ui_common_obj.next_question(question_count + 2)
                        assess_ui_common_obj.end_test()
                        assess_ui_common_obj.end_test_confirmation()
                        self.browser.quit()
                        time.sleep(5)
                    elif current_excel_data.get('skipRequired') == "Yes":
                        # Skip Required No means, No need to select answer for any question.
                        assess_ui_common_obj.next_question(total_child_questions_count)
                        assess_ui_common_obj.end_test()
                        assess_ui_common_obj.end_test_confirmation()
                        time.sleep(5)
                        self.browser.quit()

                else:
                    # This is Re-login Case
                    for question_count in range(0, total_child_questions_count):
                        # Assessment side question starts from Number One, so below addition is required
                        assess_ui_common_obj.select_answer_for_the_question(
                            current_excel_data.get('ans_qid%d' % (question_count + 1)))
                        if question_count != (total_child_questions_count - 1):
                            assess_ui_common_obj.next_question(question_count + 2)
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
                            if current_excel_data.get('isAnswerChangeRequired') == "Yes":
                                for relogin_question_count in range(0, total_child_questions_count):
                                    assess_ui_common_obj.next_question(relogin_question_count + 1)
                                    # Assessment side question starts from Number One, so below addition is required
                                    assess_ui_common_obj.select_answer_for_the_question(
                                        current_excel_data.get('relogin_qid%d' % (relogin_question_count + 1)))
                                    # if relogin_question_count != (total_child_questions_count - 1):
                                    #     assess_ui_common_obj.next_question(relogin_question_count + 2)
                                assess_ui_common_obj.end_test()
                                assess_ui_common_obj.end_test_confirmation()
                                time.sleep(5)
                                self.browser.quit()
                            elif current_excel_data.get('skipRequired') == "Yes":
                                assess_ui_common_obj.next_question(total_child_questions_count)
                                assess_ui_common_obj.end_test()
                                assess_ui_common_obj.end_test_confirmation()
                                time.sleep(5)
                                self.browser.quit()
                            elif current_excel_data.get('unAnswerRequired') == "Yes":
                                for relogin_question_count in range(0, total_child_questions_count):
                                    assess_ui_common_obj.next_question(relogin_question_count + 1)
                                    assess_ui_common_obj.unanswer_question()
                                    # if relogin_question_count != (total_child_questions_count - 1):
                                    #     assess_ui_common_obj.next_question(relogin_question_count + 1)
                                assess_ui_common_obj.end_test()
                                assess_ui_common_obj.end_test_confirmation()
                                time.sleep(5)
                                self.browser.quit()
                        else:
                            print("Relogin Agrees is failed")
                    else:
                        print("Relogin Failed")
            else:
                print("I Agreed is not visible / not available - Unable to Login")
        else:
            print("login failed due to below reason")
            print(login_details)
        self.row += 1
        test_id = int(current_excel_data.get('testId'))
        test_user_id = int(current_excel_data.get('testUserId'))
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('testCases'), None,
                                                                self.row, 0)
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('testId'), None,
                                                                self.row, 2)
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('candidateId'), None,
                                                                self.row, 3)
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('loginName'), None,
                                                                self.row, 4)
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('password'), None,
                                                                self.row, 5)
        actual_data = crpo_common_obj.candidate_web_transcript(token, test_id, test_user_id)
        # data = actual_data.get('data')
        # rtc_data = data.get('referenceToContext')
        rtc_data = actual_data['data']['referenceToContext']
        column = 6
        for index in range(0, len(rtc_data)):
            actual = str(rtc_data[index].get('candidateAnswer'))
            if current_excel_data.get('reloginRequird') == 'Yes':
                expected = current_excel_data.get('relogin_qid' + str(index + 1))
            elif current_excel_data.get('unAnswerRequired') == 'Yes':
                expected = 'None'
            else:
                expected = current_excel_data.get('ans_qid' + str(index + 1))
            write_excel_object.compare_results_and_write_vertically(expected, actual, self.row, column)
            column += 2
        write_excel_object.compare_results_and_write_vertically(write_excel_object.current_status, None, self.row, 1)


print(datetime.datetime.now())
assessment_obj = OnlineAssessment()
excel_read_obj.excel_read(input_path_ui_rtc_static, 0)
excel_data = excel_read_obj.details
crpo_token = crpo_common_obj.login_to_crpo('admin', 'At@2023$$', 'AT')
for current_excel_row in excel_data:
    print(current_excel_row)
    assessment_obj.rtc_assessment(current_excel_row, crpo_token)
print(crpo_token)
write_excel_object.write_overall_status(1)
