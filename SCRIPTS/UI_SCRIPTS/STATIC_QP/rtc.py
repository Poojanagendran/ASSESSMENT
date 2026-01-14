import datetime
from selenium.webdriver.support.ui import WebDriverWait

from SCRIPTS.UI_COMMON.assessment_ui_common_v2 import *
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.CRPO_COMMON.crpo_common import *
from SCRIPTS.DB_DELETE.db_cleanup import *


class OnlineAssessment:

    def __init__(self):
        data_clean_obj.static_ui_automation_delete()

        self.row = 1
        write_excel_object.save_result(output_path_ui_rtc_static)

        write_excel_object.write_headers_for_scripts(
            0, 0, ["UI automation"], write_excel_object.black_color_bold
        )

        headers = [
            "Testcases", "Status", "Test ID", "Candidate ID", "Login Name", "Password",
            "Q1_expected", "Q1_actual", "Q2_expected", "Q2_actual",
            "Q3_expected", "Q3_actual", "Q4_expected", "Q4_actual",
            "Q5_expected", "Q5_actual", "Q6_expected", "Q6_actual",
            "Q7_expected", "Q7_actual", "Q8_expected", "Q8_actual",
            "Q9_expected", "Q9_actual"
        ]
        write_excel_object.write_headers_for_scripts(
            1, 0, headers, write_excel_object.black_color_bold
        )

    # -------------------- COMMON HELPERS --------------------

    def answer_questions(self, total_questions, answers=None, unanswer=False):
        for i in range(total_questions):
            assess_ui_common_obj.next_question(i + 1)
            if unanswer:
                assess_ui_common_obj.unanswer_question()
            elif answers:
                assess_ui_common_obj.select_answer_for_the_question(answers[i])

    def end_test_flow(self):
        assess_ui_common_obj.end_test()
        assess_ui_common_obj.end_test_confirmation()

    # -------------------- MAIN TEST FLOW --------------------

    def rtc_assessment(self, current_excel_data, token):
        self.browser = None
        write_excel_object.current_status = "Pass"
        write_excel_object.current_status_color = write_excel_object.green_color

        try:
            self.browser = assess_ui_common_obj.initiate_browser(
                amsin_at_assessment_url
            )

            login_status = assess_ui_common_obj.ui_login_to_test(
                current_excel_data['loginName'],
                current_excel_data['password']
            )

            if login_status != 'SUCCESS':
                raise Exception(f"Login failed: {login_status}")

            if not assess_ui_common_obj.select_i_agree():
                raise Exception("I Agree not displayed")

            assess_ui_common_obj.start_test()

            total_q = int(current_excel_data['childQuestionCount'])

            # ---------------- SINGLE LOGIN ----------------
            if current_excel_data['reloginRequird'] == 'No':

                if current_excel_data['skipRequired'] == 'No':
                    answers = [
                        current_excel_data.get(f'ans_qid{i+1}')
                        for i in range(total_q)
                    ]
                    self.answer_questions(total_q, answers)

                else:
                    assess_ui_common_obj.next_question(total_q)

                self.end_test_flow()

            # ---------------- RE-LOGIN ----------------
            else:
                answers = [
                    current_excel_data.get(f'ans_qid{i+1}')
                    for i in range(total_q)
                ]
                self.answer_questions(total_q, answers)

                self.browser.close()
                self.browser.switch_to.window(self.browser.window_handles[0])

                self.browser.execute_script(
                    'window.open("https://amsin.hirepro.in/assessment/#/assess/login/eyJhbGlhcyI6ImF0In0=")'
                )
                self.browser.switch_to.window(self.browser.window_handles[-1])

                assess_ui_common_obj.ui_login_to_test(
                    current_excel_data['loginName'],
                    current_excel_data['password']
                )
                assess_ui_common_obj.select_i_agree()
                assess_ui_common_obj.start_test()

                if current_excel_data.get('isAnswerChangeRequired') == "Yes":
                    relogin_answers = [
                        current_excel_data.get(f'relogin_qid{i+1}')
                        for i in range(total_q)
                    ]
                    self.answer_questions(total_q, relogin_answers)

                elif current_excel_data.get('unAnswerRequired') == "Yes":
                    self.answer_questions(total_q, unanswer=True)

                else:
                    assess_ui_common_obj.next_question(total_q)

                self.end_test_flow()

        except Exception as e:
            print(f"❌ Test failed: {e}")
            write_excel_object.current_status = "Fail"
            write_excel_object.current_status_color = write_excel_object.red_color

        finally:
            if self.browser:
                self.browser.quit()

        self.write_results(current_excel_data, token)

    # -------------------- RESULT VALIDATION --------------------

    def write_results(self, data, token):
        self.row += 1

        write_excel_object.compare_results_and_write_vertically(
            data['testCases'], None, self.row, 0
        )
        write_excel_object.compare_results_and_write_vertically(
            data['testId'], None, self.row, 2
        )
        write_excel_object.compare_results_and_write_vertically(
            data['candidateId'], None, self.row, 3
        )
        write_excel_object.compare_results_and_write_vertically(
            data['loginName'], None, self.row, 4
        )
        write_excel_object.compare_results_and_write_vertically(
            data['password'], None, self.row, 5
        )

        actual_data = crpo_common_obj.candidate_web_transcript(
            token,
            int(data['testId']),
            int(data['testUserId'])
        )

        rtc_data = actual_data['data']['referenceToContext']
        column = 6

        for i, rtc in enumerate(rtc_data):
            actual = str(rtc.get('candidateAnswer'))

            if data.get('reloginRequird') == 'Yes':
                expected = data.get(f'relogin_qid{i+1}')
            elif data.get('unAnswerRequired') == 'Yes':
                expected = 'None'
            else:
                expected = data.get(f'ans_qid{i+1}')

            write_excel_object.compare_results_and_write_vertically(
                expected, actual, self.row, column
            )
            column += 2

        write_excel_object.compare_results_and_write_vertically(
            write_excel_object.current_status, None, self.row, 1
        )


# -------------------- EXECUTION --------------------

print(datetime.datetime.now())

assessment_obj = OnlineAssessment()
excel_read_obj.excel_read(input_path_ui_rtc_static, 0)

excel_data = excel_read_obj.details
crpo_token = crpo_common_obj.login_to_crpo(
    cred_crpo_admin_at['user'],
    cred_crpo_admin_at['password'],
    cred_crpo_admin_at['tenant']
)

for row in excel_data:
    assessment_obj.rtc_assessment(row, crpo_token)

write_excel_object.write_overall_status(1)
print(crpo_token)
