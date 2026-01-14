from SCRIPTS.CRPO_COMMON.credentials import cred_crpo_admin
from SCRIPTS.UI_COMMON.assessment_ui_common_v2 import *
import time
from SCRIPTS.UI_SCRIPTS.assessment_data_verification import *
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.COMMON.io_path import *


class OnlineAssessment:

    def __init__(self):
        self.row = 1
        write_excel_object.save_result(output_path_ui_mca_marking_schema)
        header = ['mca test marking']
        write_excel_object.write_headers_for_scripts(0, 0, header, write_excel_object.black_color_bold)
        header = ['Test Cases', 'Status', 'Test Id', 'Candidate Id', 'Testuser ID', 'User Name', 'Password',
                  'Expected total score', 'Actual total score', 'Expected group1 mark', 'Actual group1 mark',
                  'Expected group2 mark', 'Actual group2 mark', 'Expected group1 section1 mark',
                  'Actual group1 section1 mark', 'Expected group1 section2 mark', 'Actual group1 section2 mark',
                  'Expected group2 section1 mark', 'Actual group2 section1 mark', 'Expected Qn id1', 'Actual Qn id1',
                  'Expected Qn1 mark', 'Actual Qn1 mark',
                  'Expected Qn id2', 'Actual Qn id2', 'Expected Qn2 mark', 'Actual Qn2 mark', 'Expected Qn id3',
                  'Actual Qn id3', 'Expected Qn3 mark', 'Actual Qn3 mark', 'Expected Qn id4',
                  'Actual Qn id4', 'Expected Qn4 mark', 'Actual Qn4 mark', 'Expected Qn id5', 'Actual Qn id5',
                  'Expected Qn5 mark', 'Actual Qn5 mark', 'Expected Qn id6', 'Actual Qn id6', 'Expected Qn6 mark',
                  'Actual Qn6 mark',
                  'Expected Qn id7', 'Actual Qn id7', 'Expected Qn7 mark', 'Actual Qn7 mark', 'Expected Qn id8',
                  'Actual Qn id8', 'Expected Qn8 mark', 'Actual Qn8 mark', 'Expected Qn id9',
                  'Actual Qn id9', 'Expected Qn9 mark', 'Actual Qn9 mark', 'Expected Qn id10', 'Actual Qn id10',
                  'Expected Qn10 mark', 'Actual Qn10 mark',
                  'Expected Qn id11', 'Actual Qn id11', 'Expected Qn11 mark', 'Actual Qn11 mark',
                  'Expected Qn id12', 'Actual Qn id12', 'Expected Qn12 mark', 'Actual Qn12 mark', 'Expected Qn id13',
                  'Actual Qn id13', 'Expected Qn13 mark', 'Actual Qn13 mark', 'Expected Qn id14',
                  'Actual Qn id14', 'Expected Qn14 mark', 'Actual Qn14 mark', 'Expected Qn id15', 'Actual Qn id15',
                  'Expected Qn15 mark', 'Actual Qn15 mark', 'Expected Qn id16', 'Actual Qn id16', 'Expected Qn16 mark',
                  'Actual Qn16 mark',
                  'Expected Qn id17', 'Actual Qn id17', 'Expected Qn17 mark', 'Actual Qn17 mark', 'Expected Qn id18',
                  'Actual Qn id18', 'Expected Qn18 mark', 'Actual Qn18 mark', 'Expected Qn id19',
                  'Actual Qn id19', 'Expected Qn19 mark', 'Actual Qn19 mark', 'Expected Qn id20', 'Actual Qn id20',
                  'Expected Qn20 mark', 'Actual Qn20 mark', 'Expected Qn id21', 'Actual Qn id21', 'Expected Qn21 mark',
                  'Actual Qn21 mark'
                  ]

        write_excel_object.write_headers_for_scripts(1, 0, header, write_excel_object.black_color_bold)

    def mca_marking(self, tu_details, token):
        write_excel_object.current_status_color = write_excel_object.green_color
        write_excel_object.current_status = 'pass'
        self.browser = assess_ui_common_obj.initiate_browser(amsin_automation_assessment_url)
        login_details = assess_ui_common_obj.ui_login_to_test(tu_details.get('loginName'), (tu_details.get('password')))
        if login_details == 'SUCCESS':
            i_agreed = assess_ui_common_obj.select_i_agree()
            if i_agreed:
                start_test_status = assess_ui_common_obj.start_test_button_status()
                assess_ui_common_obj.start_test()
                assess_ui_common_obj.select_answer_for_mca_question(tu_details.get('ans_qid1'))
                assess_ui_common_obj.next_question(2)
                assess_ui_common_obj.select_answer_for_mca_question(tu_details.get('ans_qid2'))
                assess_ui_common_obj.next_question(3)
                assess_ui_common_obj.select_answer_for_mca_question(tu_details.get('ans_qid3'))
                assess_ui_common_obj.next_question(4)
                assess_ui_common_obj.select_answer_for_mca_question(tu_details.get('ans_qid4'))
                assess_ui_common_obj.next_question(5)
                assess_ui_common_obj.select_answer_for_mca_question(tu_details.get('ans_qid5'))
                assess_ui_common_obj.next_question(6)
                assess_ui_common_obj.select_answer_for_mca_question(tu_details.get('ans_qid6'))
                assess_ui_common_obj.next_question(7)
                assess_ui_common_obj.select_answer_for_mca_question(tu_details.get('ans_qid7'))
                assess_ui_common_obj.next_question(8)
                assess_ui_common_obj.select_answer_for_mca_question(tu_details.get('ans_qid8'))
                assess_ui_common_obj.next_question(9)
                assess_ui_common_obj.select_answer_for_mca_question(tu_details.get('ans_qid9'))
                assess_ui_common_obj.next_question(10)
                assess_ui_common_obj.select_answer_for_mca_question(tu_details.get('ans_qid10'))
                assess_ui_common_obj.next_question(11)
                assess_ui_common_obj.select_answer_for_mca_question(tu_details.get('ans_qid11'))
                assess_ui_common_obj.next_question(12)
                assess_ui_common_obj.select_answer_for_mca_question(tu_details.get('ans_qid12'))
                assess_ui_common_obj.next_question(13)
                assess_ui_common_obj.select_answer_for_mca_question(tu_details.get('ans_qid13'))
                assess_ui_common_obj.next_question(14)
                assess_ui_common_obj.select_answer_for_mca_question(tu_details.get('ans_qid14'))
                assess_ui_common_obj.next_question(15)
                assess_ui_common_obj.select_answer_for_mca_question(tu_details.get('ans_qid15'))
                assess_ui_common_obj.next_question(16)
                assess_ui_common_obj.select_answer_for_mca_question(tu_details.get('ans_qid16'))
                assess_ui_common_obj.next_question(17)
                assess_ui_common_obj.select_answer_for_mca_question(tu_details.get('ans_qid17'))
                assess_ui_common_obj.next_question(18)
                assess_ui_common_obj.select_answer_for_mca_question(tu_details.get('ans_qid18'))
                assess_ui_common_obj.next_question(19)
                assess_ui_common_obj.select_answer_for_mca_question(tu_details.get('ans_qid19'))
                assess_ui_common_obj.next_question(20)
                assess_ui_common_obj.select_answer_for_mca_question(tu_details.get('ans_qid20'))
                assess_ui_common_obj.next_question(21)
                assess_ui_common_obj.select_answer_for_mca_question(tu_details.get('ans_qid21'))
                # assess_ui_common_obj.unanswer_question()
                assess_ui_common_obj.end_test()
                assess_ui_common_obj.end_test_confirmation()
                time.sleep(5)
                self.browser.quit()
                time.sleep(5)
        else:
            print("login failed due to below reason")
            print(login_details)
        mark_details = crpo_common_obj.candidate_web_transcript(token, int(tu_details.get('testId')),
                                                                int(tu_details.get('testUserId')))
        total_obtained_mark = mark_details['data']['assessment']['marksObtained']
        group1_obtained_mark = mark_details['data']['groupAndSectionWiseMarks'][0]['obtainedMarks']
        group2_obtained_mark = mark_details['data']['groupAndSectionWiseMarks'][1]['obtainedMarks']
        group1_section1_obtained_mark = mark_details['data']['groupAndSectionWiseMarks'][0]['sectionInfo'][0][
            'obtainedMarks']
        group1_section2_obtained_mark = mark_details['data']['groupAndSectionWiseMarks'][0]['sectionInfo'][1][
            'obtainedMarks']
        group2_section1_obtained_mark = mark_details['data']['groupAndSectionWiseMarks'][1]['sectionInfo'][0][
            'obtainedMarks']
        all_questions = mark_details['data']['multipleCorrectAnswer']
        # id = 121404

        self.row = self.row + 1
        write_excel_object.compare_results_and_write_vertically(tu_details.get('testCases'), None, self.row, 0)
        write_excel_object.compare_results_and_write_vertically(tu_details.get('testId'), None, self.row, 2)
        write_excel_object.compare_results_and_write_vertically(tu_details.get('candidateId'), None, self.row, 3)
        write_excel_object.compare_results_and_write_vertically(tu_details.get('testUserId'), None, self.row, 4)
        write_excel_object.compare_results_and_write_vertically(tu_details.get('loginName'), None, self.row, 5)
        write_excel_object.compare_results_and_write_vertically(tu_details.get('password'), None, self.row, 6)
        write_excel_object.compare_results_and_write_vertically(tu_details.get('totalObtainedMark'),
                                                                total_obtained_mark, self.row, 7)
        write_excel_object.compare_results_and_write_vertically(tu_details.get('group1ObtainedMark'),
                                                                group1_obtained_mark, self.row, 9)
        write_excel_object.compare_results_and_write_vertically(tu_details.get('group2ObtainedMark'),
                                                                group2_obtained_mark, self.row, 11)
        write_excel_object.compare_results_and_write_vertically(tu_details.get('group1Section1ObtainedMark'),
                                                                group1_section1_obtained_mark, self.row, 13)
        write_excel_object.compare_results_and_write_vertically(tu_details.get('group1Section2ObtainedMark'),
                                                                group1_section2_obtained_mark, self.row, 15)
        write_excel_object.compare_results_and_write_vertically(tu_details.get('group2Section1ObtainedMark'),
                                                                group2_section1_obtained_mark, self.row, 17)
        # write_excel_object.compare_results_and_write_vertically(tu_details.get('totalObtainedMark'),
        #                                                         total_obtained_mark, self.row, 15)
        question_index = 0
        col = 19
        for question in all_questions:
            question_index = question_index + 1
            question_id = 'qid' + str(question_index)
            expected_qn_wise_obtained_mark = 'mark_qid' + str(question_index)
            if int(tu_details.get(question_id)) == question.get('id'):
                actual_qn_wise_obtained_mark = question['obtainedMark']
                write_excel_object.compare_results_and_write_vertically(int(tu_details.get(question_id)),
                                                                        question.get('id'), self.row, col)
                write_excel_object.compare_results_and_write_vertically(tu_details.get(expected_qn_wise_obtained_mark),
                                                                        actual_qn_wise_obtained_mark, self.row, col + 2)

                col = col + 4
        write_excel_object.compare_results_and_write_vertically(write_excel_object.current_status, None,
                                                                self.row, 1)


print(datetime.datetime.now())
assessment_obj = OnlineAssessment()
# input_file_path = r"F:\qa_automation\PythonWorkingScripts_InputData\UI\Assessment\ui_relogin.xls"
excel_read_obj.excel_read(input_path_ui_marking_schema, 4)
excel_data = excel_read_obj.details
crpo_token = crpo_common_obj.login_to_crpo(cred_crpo_admin.get('user'), cred_crpo_admin.get('password'),
                                           cred_crpo_admin.get('tenant'))
for current_excel_row in excel_data:
    print(current_excel_row)
    assessment_obj.mca_marking(current_excel_row, crpo_token)

print(crpo_token)
write_excel_object.write_overall_status(1)
print(datetime.datetime.now())
