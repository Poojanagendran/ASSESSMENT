from SCRIPTS.UI_COMMON.assessment_ui_common_v2 import *
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.COMMON.writeExcel import *
from SCRIPTS.COMMON.io_path import *


class QPVerification:

    def __init__(self):
        self.row = 1
        write_excel_object.save_result(output_path_ui_mcqww_randomization)
        header = ['QP_Verification']
        self.overall_status = 'pass'
        self.overall_status_color = write_excel_object.green_color

        write_excel_object.write_headers_for_scripts(0, 0, header, write_excel_object.black_color_bold)
        header = ['Test Cases', 'Status', 'Test Id', 'Candidate Id', 'Testuser ID', 'User Name', 'Password',
                  'mismatched questions(in QP) - question out of the QP',
                  'mismatched S1G1- Low ', 'Exp S1G1- Low Count', 'Actual S1G1- Low Count',
                  'mismatched S1G1- Medium ', 'Exp S1G1- Medium Count', 'Actual S1G1- Medium Count',
                  'mismatched S1G1- High', 'Exp S1G1- High Count', 'Actual S1G1- High Count',
                  'mismatched S2G1- Low', 'Exp S2G1- Low Count', 'Actual S2G1- Low Count',
                  'mismatched S2G1- Medium', 'Exp S2G1- Medium Count', 'Actual S2G1- Medium Count',
                  'mismatched S2G1- High', 'Exp S2G1- High Count', 'Actual S2G1- High Count',
                  'mismatched S1G2- Low', 'Exp S1G2- Low Count', 'Actual S1G2- Low Count',
                  'mismatched S1G2- Medium', 'Exp S1G2- Medium Count', 'Actual S1G2- Medium Count',
                  'mismatched S1G2- High', 'Exp S1G2- High Count', 'Actual S1G2- High Count',
                  'mismatched S2G2- Low', 'Exp S2G2- Low Count', 'Actual S2G2- Low Count',
                  'mismatched S2G2- Medium', 'Exp S2G2- Medium Count', 'Actual S2G2- Medium Count',
                  'mismatched S2G2- High', 'Exp S2G2- High Count', 'Actual S2G2- High Count', '1st login Q1',
                  '2nd login Q1', '1st login Q2', '2nd login Q2', '1st login Q3', '2nd login Q3', '1st login Q4',
                  '2nd login Q4', '1st login Q5', '2nd login Q5', '1st login Q6', '2nd login Q6', '1st login Q7',
                  '2nd login Q7', '1st login Q8', '2nd login Q8', '1st login Q9', '2nd login Q9', '1st login Q10',
                  '2nd login Q10', '1st login Q11', '2nd login Q11', '1st login Q12', '2nd login Q12', '1st login Q13',
                  '2nd login Q13', '1st login Q14', '2nd login Q14', '1st login Q15', '2nd login Q15', '1st login Q16',
                  '2nd login Q16', '1st login Q17', '2nd login Q17', '1st login Q18', '2nd login Q18', '1st login Q19',
                  '2nd login Q19', '1st login Q20', '2nd login Q20', '1st login Q21', '2nd login Q21']
        write_excel_object.write_headers_for_scripts(1, 0, header, write_excel_object.black_color_bold)
        self.expected_low_section1_group1 = ['po q1 mcqww serverrand automation low',
                                             'po q2 mcqww serverrand automation low',
                                             'po q3 mcqww serverrand automation low']
        self.expected_medium_section1_group1 = ['po q4 mcqww serverrand automation medium',
                                                'po q5 mcqww serverrand automation medium',
                                                'po q6 mcqww serverrand automation medium']
        self.expected_high_section1_group1 = ['po q7 mcqww serverrand automation high',
                                              'po q8 mcqww serverrand automation high',
                                              'po q9 mcqww serverrand automation high']

        self.expected_low_section2_group1 = ['po q10 mcqww serverrand automation low',
                                             'po q11 mcqww serverrand automation low']
        self.expected_medium_section2_group1 = ['po q12 mcqww serverrand automation medium',
                                                'po q13 mcqww serverrand automation medium']
        self.expected_high_section2_group1 = ['po q14 mcqww serverrand automation high',
                                              'po q15 mcqww serverrand automation high']

        self.expected_low_section1_group2 = ['po q16 mcqww serverrand automation low',
                                             'po q17 mcqww serverrand automation low',
                                             'po q18 mcqww serverrand automation low',
                                             'po q19 mcqww serverrand automation low',
                                             'po q20 mcqww serverrand automation low']
        self.expected_medium_section1_group2 = ['po q21 mcqww serverrand automation medium',
                                                'po q22 mcqww serverrand automation medium',
                                                'po q23 mcqww serverrand automation medium',
                                                'po q24 mcqww serverrand automation medium',
                                                'po q25 mcqww serverrand automation medium']
        self.expected_high_section1_group2 = ['po q26 mcqww serverrand automation high',
                                              'po q27 mcqww serverrand automation high',
                                              'po q28 mcqww serverrand automation high',
                                              'po q29 mcqww serverrand automation high',
                                              'po q30 mcqww serverrand automation high']

        self.expected_low_section2_group2 = ['po q31 mcqww serverrand automation low',
                                             'po q32 mcqww serverrand automation low',
                                             'po q33 mcqww serverrand automation low',
                                             'po q34 mcqww serverrand automation low',
                                             'po q35 mcqww serverrand automation low']
        self.expected_medium_section2_group2 = ['po q36 mcqww serverrand automation medium',
                                                'po q37 mcqww serverrand automation medium',
                                                'po q38 mcqww serverrand automation medium',
                                                'po q39 mcqww serverrand automation medium',
                                                'po q40 mcqww serverrand automation medium']
        self.expected_high_section2_group2 = ['po q41 mcqww serverrand automation high',
                                              'po q42 mcqww serverrand automation high',
                                              'po q43 mcqww serverrand automation high',
                                              'po q44 mcqww serverrand automation high',
                                              'po q45 mcqww serverrand automation high']

        self.expected_section1_group1 = self.expected_low_section1_group1 + self.expected_medium_section1_group1 \
                                        + self.expected_high_section1_group1
        self.expected_section2_group1 = self.expected_low_section2_group1 + self.expected_medium_section2_group1 \
                                        + self.expected_high_section2_group1
        self.expected_section1_group2 = self.expected_low_section1_group2 + self.expected_medium_section1_group2 \
                                        + self.expected_high_section1_group2
        self.expected_section2_group2 = self.expected_low_section2_group2 + self.expected_medium_section2_group2 \
                                        + self.expected_high_section2_group2
        self.expected_questions = self.expected_section1_group1 + self.expected_section2_group1 \
                                  + self.expected_section1_group2 + self.expected_section2_group2

    def verify_questions(self, tu_details):
        self.color = write_excel_object.green_color
        self.status = 'pass'
        self.actual_low_section1_group1 = []
        self.actual_medium_section1_group1 = []
        self.actual_high_section1_group1 = []
        self.actual_low_section2_group1 = []
        self.actual_medium_section2_group1 = []
        self.actual_high_section2_group1 = []

        self.actual_low_section1_group2 = []
        self.actual_medium_section1_group2 = []
        self.actual_high_section1_group2 = []
        self.actual_low_section2_group2 = []
        self.actual_medium_section2_group2 = []
        self.actual_high_section2_group2 = []

        self.row = self.row + 1
        self.delivered_questions = []
        self.relogin_questions = []
        self.browser = assess_ui_common_obj.initiate_browser(amsin_automation_assessment_url)
        login_details = assess_ui_common_obj.ui_login_to_test(tu_details.get('userName'),
                                                              tu_details.get('password'))
        if login_details == 'SUCCESS':
            i_agreed = assess_ui_common_obj.select_i_agree()
            if i_agreed:
                start_test_status = assess_ui_common_obj.start_test_button_status()
                assess_ui_common_obj.start_test()
                for question_index in range(1, int(tu_details.get('expectedTotalQuestionsCount') + 1)):
                    assess_ui_common_obj.next_question(question_index)
                    qn_string = assess_ui_common_obj.find_question_string_v2()
                    self.delivered_questions.append(qn_string[0])
                    qn_details = {'question': qn_string[0], 'group': qn_string[1], 'section': qn_string[2]}
                    qp_verification.question_owner(qn_string)
                print("1st Login")
                self.browser.close()
                self.browser.switch_to.window(self.browser.window_handles[0])
                time.sleep(1)
                self.browser.execute_script(
                    '''window.open("https://amsin.hirepro.in/assessment/#/assess/login/eyJhbGlhcyI6ImF1dG9tYXRpb24ifQ==", "_blank");''')
                time.sleep(2)
                self.browser.switch_to.window(self.browser.window_handles[1])
                login_details = assess_ui_common_obj.ui_login_to_test(tu_details.get('userName'),
                                                                      tu_details.get('password'))
                if login_details == 'SUCCESS':
                    i_agreed = assess_ui_common_obj.select_i_agree()
                    if i_agreed:
                        start_test_status = assess_ui_common_obj.start_test_button_status()
                        assess_ui_common_obj.start_test()
                        for question_index in range(1, int(tu_details.get('expectedTotalQuestionsCount') + 1)):
                            assess_ui_common_obj.next_question(question_index)
                            qn_string = assess_ui_common_obj.find_question_string_v2()
                            self.relogin_questions.append(qn_string[0])
                            # qn_details = {'question': qn_string[0], 'group': qn_string[1], 'section': qn_string[2]}
                        self.browser.close()

                # print(delivered_questions)
                write_excel_object.ws.write(self.row, 0, tu_details.get('testCases'),
                                            write_excel_object.black_color)
                write_excel_object.ws.write(self.row, 2, tu_details.get('testID'),
                                            write_excel_object.black_color)
                write_excel_object.ws.write(self.row, 3, tu_details.get('candidateID'),
                                            write_excel_object.black_color)
                write_excel_object.ws.write(self.row, 4, tu_details.get('testUserId'),
                                            write_excel_object.black_color)
                write_excel_object.ws.write(self.row, 5, tu_details.get('userName'),
                                            write_excel_object.black_color)
                write_excel_object.ws.write(self.row, 6, tu_details.get('password'),
                                            write_excel_object.black_color)
                mismatched_questions = set(self.delivered_questions) - set(self.expected_questions)
                if len(mismatched_questions) >= 1:
                    self.color = write_excel_object.red_color
                    self.status = 'Fail'
                    self.overall_status = 'Fail'
                    self.overall_status_color = write_excel_object.red_color
                else:
                    mismatched_questions = 'No Mismatch - Expected delivery'
                write_excel_object.ws.write(self.row, 7, str(mismatched_questions), self.color)

                # qp_verification.question_matching(tu_details)
                low_s1g1 = qp_verification.mismatch_details(self.actual_low_section1_group1,
                                                            self.expected_low_section1_group1,
                                                            int(tu_details.get('expectedS1G1LowCount')), self.row,
                                                            col=8)
                medium_s1g1 = qp_verification.mismatch_details(self.actual_medium_section1_group1,
                                                               self.expected_medium_section1_group1,
                                                               int(tu_details.get('expectedS1G1MediumCount')), self.row,
                                                               col=11)

                high_s1g1 = qp_verification.mismatch_details(self.actual_high_section1_group1,
                                                             self.expected_high_section1_group1,
                                                             int(tu_details.get('expectedS1G1HighCount')), self.row,
                                                             col=14)

                low_s2g1 = qp_verification.mismatch_details(self.actual_low_section2_group1,
                                                            self.expected_low_section2_group1,
                                                            int(tu_details.get('expectedS2G1LowCount')), self.row,
                                                            col=17)

                medium_s2g1 = qp_verification.mismatch_details(self.actual_medium_section2_group1,
                                                               self.expected_medium_section2_group1,
                                                               int(tu_details.get('expectedS2G1MediumCount')), self.row,
                                                               col=20)

                high_s2g1 = qp_verification.mismatch_details(self.actual_high_section2_group1,
                                                             self.expected_high_section2_group1,
                                                             int(tu_details.get('expectedS2G1HighCount')), self.row,
                                                             col=23)

                low_s1g2 = qp_verification.mismatch_details(self.actual_low_section1_group2,
                                                            self.expected_low_section1_group2,
                                                            int(tu_details.get('expectedS1G2LowCount')), self.row,
                                                            col=26)
                medium_s1g2 = qp_verification.mismatch_details(self.actual_medium_section1_group2,
                                                               self.expected_medium_section1_group2,
                                                               int(tu_details.get('expectedS1G2MediumCount')), self.row,
                                                               col=29)
                high_s1g2 = qp_verification.mismatch_details(self.actual_high_section1_group2,
                                                             self.expected_high_section1_group2,
                                                             int(tu_details.get('expectedS1G2HighCount')), self.row,
                                                             col=32)
                low_s2g2 = qp_verification.mismatch_details(self.actual_low_section2_group2,
                                                            self.expected_low_section2_group2,
                                                            int(tu_details.get('expectedS2G2LowCount')), self.row,
                                                            col=35)
                medium_s2g2 = qp_verification.mismatch_details(self.actual_medium_section2_group2,
                                                               self.expected_medium_section2_group2,
                                                               int(tu_details.get('expectedS2G2MediumCount')), self.row,
                                                               col=38)
                high_s2g2 = qp_verification.mismatch_details(self.actual_high_section2_group2,
                                                             self.expected_high_section2_group2,
                                                             int(tu_details.get('expectedS2G2HighCount')), self.row,
                                                             col=41)
                col = 44
                print("This is Muthu")
                for index in range(0, int(tu_details.get('expectedTotalQuestionsCount'))):
                    write_excel_object.ws.write(self.row, col, self.delivered_questions[index],
                                                write_excel_object.black_color)
                    if self.delivered_questions[index] == self.relogin_questions[index]:
                        write_excel_object.ws.write(self.row, col + 1, self.relogin_questions[index],
                                                    write_excel_object.green_color)
                    else:
                        write_excel_object.ws.write(self.row, col + 1, self.relogin_questions[index],
                                                    write_excel_object.red_color)
                        self.color = write_excel_object.red_color
                        self.status = 'Fail'
                        self.overall_status = 'Fail'
                        self.overall_status_color = write_excel_object.red_color
                    col = col + 2
                write_excel_object.ws.write(self.row, 1, self.status, self.color)
                self.browser.quit()

    def question_owner(self, question_infos):
        question = question_infos[0]
        group_name = question_infos[1]
        section_name = question_infos[2]
        if group_name == 'Group 1':
            if section_name == 'Group 1Section 1':
                if question in self.expected_low_section1_group1:
                    self.actual_low_section1_group1.append(question)
                elif question in self.expected_medium_section1_group1:
                    self.actual_medium_section1_group1.append(question)
                elif question in self.expected_high_section1_group1:
                    self.actual_high_section1_group1.append(question)
                else:
                    print('S1G1 - Something went wrong ', question_infos)

            elif section_name == 'Group 1Section 2':
                if question in self.expected_low_section2_group1:
                    self.actual_low_section2_group1.append(question)
                elif question in self.expected_medium_section2_group1:
                    self.actual_medium_section2_group1.append(question)
                elif question in self.expected_high_section2_group1:
                    self.actual_high_section2_group1.append(question)
                else:
                    print('S2G1 - Something went wrong ', question_infos)

        elif group_name == 'Group 2':
            if section_name == 'Group 2Section 1':
                if question in self.expected_low_section1_group2:
                    self.actual_low_section1_group2.append(question)
                elif question in self.expected_medium_section1_group2:
                    self.actual_medium_section1_group2.append(question)
                elif question in self.expected_high_section1_group2:
                    self.actual_high_section1_group2.append(question)
                else:
                    print('S1G2 - Something went wrong ', question_infos)

            elif section_name == 'Group 2Section 2':
                if question in self.expected_low_section2_group2:
                    self.actual_low_section2_group2.append(question)
                elif question in self.expected_medium_section2_group2:
                    self.actual_medium_section2_group2.append(question)
                elif question in self.expected_high_section2_group2:
                    self.actual_high_section2_group2.append(question)
                else:
                    print('S2G2 - Something went wrong ', question_infos)
        else:
            print("Question is out of the qp ", question_infos)

    def mismatch_details(self, actual_questions, expected_questions, expected_section_difficulty_count, row, col):
        actual_question_count = len(actual_questions)
        if actual_question_count == expected_section_difficulty_count:
            count_color = write_excel_object.green_color
            mismatched_questions = set(actual_questions) - set(expected_questions)
            if len(mismatched_questions) <= 0:
                data = 'No Mismatch - Expected delivery'
                # self.color = write_excel_object.green_color
                # self.color = write_excel_object.red_color
                count_color = write_excel_object.green_color
            else:
                data = mismatched_questions
                count_color = write_excel_object.red_color
                self.color = write_excel_object.red_color
                self.status = 'Fail'
                self.overall_status = 'Fail'
                self.overall_status_color = write_excel_object.red_color
        elif actual_question_count == 0:
            data = 'No expected questions got delivered for this section and difficulty'
            # color = write_excel_object.red_color
            count_color = write_excel_object.red_color
            self.color = write_excel_object.red_color
            self.status = 'Fail'
            self.overall_status = 'Fail'
            self.overall_status_color = write_excel_object.red_color
        else:
            data = 'got lesser or higher than expected questions'
            self.color = write_excel_object.red_color
            self.status = 'Fail'
            self.overall_status = 'Fail'
            self.overall_status_color = write_excel_object.red_color
            # color = write_excel_object.red_color
            count_color = write_excel_object.red_color

        write_excel_object.ws.write(row, col, str(data), count_color)
        write_excel_object.ws.write(row, col + 1, expected_section_difficulty_count, write_excel_object.black_color)
        write_excel_object.ws.write(row, col + 2, actual_question_count, count_color)
        return data, self.color, actual_question_count

    # def question_matching(self, tu_details):


print(datetime.datetime.now())
qp_verification = QPVerification()
excel_read_obj.excel_read(input_path_ui_mcq_randomization, 4)
candidate_details = excel_read_obj.details
for current_excel_row in candidate_details:
    qp_verification.verify_questions(current_excel_row)

ended = datetime.datetime.now()
ended = "Ended:- %s" % ended.strftime("%Y-%m-%d-%H-%M-%S")
write_excel_object.ws.write(0, 1, qp_verification.overall_status, qp_verification.overall_status_color)
write_excel_object.ws.write(0, 2, 'Started:- ' + write_excel_object.started, write_excel_object.black_color_bold)
write_excel_object.ws.write(0, 3, ended, write_excel_object.black_color_bold)
write_excel_object.ws.write(0, 4, "Total_Testcase_Count:- 5", write_excel_object.black_color_bold)
write_excel_object.write_excel.close()
