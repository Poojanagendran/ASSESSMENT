from SCRIPTS.UI_COMMON.assessment_ui_common_v2 import *
from SCRIPTS.UI_SCRIPTS.assessment_data_verification import *
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.COMMON.writeExcel import *
from SCRIPTS.COMMON.io_path import *


class QPVerification:

    def __init__(self):
        self.row = 1

        # save_path = r"F:\qa_automation\PythonWorkingScripts_Output\UI\QP_"
        write_excel_object.save_result(output_path_ui_qp_verification)
        self.url = amsin_at_assessment_url
        # self.path = r"F:\qa_automation\chromedriver.exe"
        header = ['QP_Verification']
        write_excel_object.write_headers_for_scripts(0, 0, header, write_excel_object.black_color_bold)
        header = ['Test Cases', 'Status', 'Test Id', 'Candidate Id', 'Testuser ID', 'User Name', 'Password',
                  'Expected qn string1', 'Actual qn string1', 'Expected qn string2', 'Actual qn string2',
                  'Expected qn string3', 'Actual qn string3', 'Expected qn string4', 'Actual qn string4',
                  'Expected qn string5', 'Actual qn string5']
        write_excel_object.write_headers_for_scripts(1, 0, header, write_excel_object.black_color_bold)

    def verify_questions(self, candidate_details, qn_infos):
        self.row = self.row + 1
        delivered_questions = []
        self.browser = assess_ui_common_obj.initiate_browser(amsin_at_assessment_url)
        login_details = assess_ui_common_obj.ui_login_to_test(candidate_details.get('userName'),
                                                              candidate_details.get('password'))
        if login_details == 'SUCCESS':
            i_agreed = assess_ui_common_obj.select_i_agree()
            if i_agreed:
                start_test_status = assess_ui_common_obj.start_test_button_status()
                assess_ui_common_obj.start_test()
                qn_string = assess_ui_common_obj.find_question_string()
                delivered_questions.append({'questions': qn_string})
                assess_ui_common_obj.next_question(2)
                qn_string = assess_ui_common_obj.find_question_string()
                delivered_questions.append({'questions': qn_string})
                assess_ui_common_obj.next_question(3)
                qn_string = assess_ui_common_obj.find_question_string()
                delivered_questions.append({'questions': qn_string})
                assess_ui_common_obj.next_question(4)
                qn_string = assess_ui_common_obj.find_question_string()
                delivered_questions.append({'questions': qn_string})
                assess_ui_common_obj.next_question(5)
                qn_string = assess_ui_common_obj.find_question_string()
                delivered_questions.append({'questions': qn_string})
                print(delivered_questions)
                self.col = 7
                write_excel_object.ws.write(self.row, 0, candidate_details.get('testCases'),
                                            write_excel_object.green_color)
                write_excel_object.ws.write(self.row, 2, candidate_details.get('testID'),
                                            write_excel_object.green_color)
                write_excel_object.ws.write(self.row, 3, candidate_details.get('candidateID'),
                                            write_excel_object.green_color)
                write_excel_object.ws.write(self.row, 4, candidate_details.get('testUserId'),
                                            write_excel_object.green_color)
                write_excel_object.ws.write(self.row, 5, candidate_details.get('userName'),
                                            write_excel_object.green_color)
                write_excel_object.ws.write(self.row, 6, candidate_details.get('password'),
                                            write_excel_object.green_color)
                for excel in qn_infos:
                    for actual in delivered_questions:
                        print(actual)
                        if excel['questions'] in actual['questions']:
                            write_excel_object.ws.write(self.row, self.col, excel['questions'],
                                                        write_excel_object.green_color)
                            write_excel_object.ws.write(self.row, self.col + 1, str(actual['questions']),
                                                        write_excel_object.green_color)
                            write_excel_object.ws.write(self.row, 1, 'Pass',
                                                        write_excel_object.green_color)
                            print(excel['questions'])
                            print(actual['questions'])
                            print('Matched')
                            self.col = self.col + 2
                            break
                    else:
                        write_excel_object.ws.write(self.row, self.col, excel['questions'],
                                                    write_excel_object.green_color)
                        write_excel_object.ws.write(self.row, self.col + 1, "Question Not Available",
                                                    write_excel_object.red_color)
                        write_excel_object.ws.write(self.row, 1, 'Fail',
                                                    write_excel_object.green_color)
                        self.col = self.col + 2

        self.browser.quit()


print(datetime.datetime.now())
assessment_obj = QPVerification()
# input_file_path = r"F:\automation\PythonWorkingScripts_InputData\UI\Assessment\qp_verification.xls"
# input_file_path = r"F:\qa_automation\PythonWorkingScripts_InputData\UI\Assessment\qp_verification.xls"
excel_read_obj.excel_read(input_path_ui_qp_verification, 0)
questions = excel_read_obj.details
print(questions)
excel_read_obj.details = []
excel_read_obj.excel_read(input_path_ui_qp_verification, 1)
candidate_details = excel_read_obj.details
print(candidate_details)
# assessment_obj.verify_questions(candidate_details, questions)
for current_excel_row in candidate_details:
    print(current_excel_row)
    assessment_obj.verify_questions(current_excel_row, questions)

write_excel_object.write_excel.close()
# crpo_token = crpo_common_obj.login_to_crpo('admin', 'Email@admin', 'AT')
# time.sleep(10)
# obj_assessment_data_verification.assessment_data_report(crpo_token, excel_data)
# obj_assessment_data_verification.write_excel.close()
# print(datetime.datetime.now())
