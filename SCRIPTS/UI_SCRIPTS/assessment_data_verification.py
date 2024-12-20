from SCRIPTS.CRPO_COMMON.crpo_common import *
import datetime
import xlsxwriter


class AssessmentDataVerification:
    def __init__(self):

        self.started = datetime.datetime.now()
        self.started = self.started.strftime("%Y-%M-%d-%H-%M-%S")
        self.row_size = 2
        self.write_excel = xlsxwriter.Workbook(
            'F:\\ASSESSMENT\\PythonWorkingScripts_Output\\UI\\UI_Automation_MCQ_Only - ' + self.started + '.xls')
        self.final_status = ''
        self.ws = self.write_excel.add_worksheet()
        self.black_color = self.write_excel.add_format({'font_color': 'black', 'font_size': 9})
        self.red_color = self.write_excel.add_format({'font_color': 'red', 'font_size': 9})
        self.green_color = self.write_excel.add_format({'font_color': 'green', 'font_size': 9})
        self.orange_color = self.write_excel.add_format({'font_color': 'orange', 'font_size': 9})
        self.black_color_bold = self.write_excel.add_format({'font_color': 'black', 'bold': True, 'font_size': 9})
        self.over_all_status_pass = self.write_excel.add_format({'font_color': 'green', 'bold': True, 'font_size': 9})
        self.over_all_status_failed = self.write_excel.add_format({'font_color': 'red', 'bold': True, 'font_size': 9})
        self.over_all_status_color = self.over_all_status_pass
        self.over_all_status = 'Pass'
        self.ws.write(0, 0, "UI automation", self.black_color_bold)
        self.ws.write(1, 0, "Testcases", self.black_color_bold)
        self.ws.write(1, 1, "Status", self.black_color_bold)
        self.ws.write(1, 2, "Test ID", self.black_color_bold)
        self.ws.write(1, 3, "Candidate ID", self.black_color_bold)
        self.ws.write(1, 4, "Login Name", self.black_color_bold)
        self.ws.write(1, 5, "Password", self.black_color_bold)
        self.ws.write(1, 6, "Q1_candidate_answer_expected_data", self.black_color_bold)
        self.ws.write(1, 7, "Q1_candidate_answer_actual_data", self.black_color_bold)
        self.ws.write(1, 8, "Q2_candidate_answer_expected_data", self.black_color_bold)
        self.ws.write(1, 9, "Q2_candidate_answer_actual_data", self.black_color_bold)
        self.ws.write(1, 10, "Q3_candidate_answer_expected_data", self.black_color_bold)
        self.ws.write(1, 11, "Q3_candidate_answer_actual_data", self.black_color_bold)
        self.ws.write(1, 12, "Q4_candidate_answer_expected_data", self.black_color_bold)
        self.ws.write(1, 13, "Q4_candidate_answer_actual_data", self.black_color_bold)
        self.ws.write(1, 14, "Q5_candidate_answer_expected_data", self.black_color_bold)
        self.ws.write(1, 15, "Q5_candidate_answer_actual_data", self.black_color_bold)

    # Excel Data -  This is the data where the candidate is entered via assessment medium
    # Actual Data - This is the data where we fetch it from the CRPO_COMMON Application candidate_transcript api
    def assessment_data_report(self, token, excel_data):
        row_size = 2
        print(token)
        for tu_details in excel_data:
            candidate_answers = []
            test_id = int(tu_details.get('testId'))
            test_user_id = int(tu_details.get('testUserId'))
            print(test_user_id)
            actual_data = crpo_common_obj.candidate_web_transcript(token, test_id, test_user_id)
            print(actual_data)
            data = actual_data.get('data')
            mcq_data = data.get('mcq')
            for index in range(0, len(mcq_data)):
                if tu_details.get('reloginRequird') == 'Yes':
                    data = {'excel': tu_details.get('relogin_qid' + str(index + 1)),
                            'actual': str(mcq_data[index].get('candidateAnswer'))}
                elif tu_details.get('unAnswerRequired') == 'Yes':
                    data = {'excel': 'None',
                            'actual': str(mcq_data[index].get('candidateAnswer'))}
                else:
                    data = {'excel': tu_details.get('ans_qid' + str(index + 1)),
                            'actual': str(mcq_data[index].get('candidateAnswer'))}
                candidate_answers.append(data)
            obj_assessment_data_verification.write_data(tu_details, candidate_answers, row_size)
            row_size += 1
        self.ws.write(0, 1, self.over_all_status, self.over_all_status_color)

    def assessment_data_report_for_mca(self, token, excel_data):
        row_size = 2
        print(token)
        for tu_details in excel_data:
            candidate_answers = []
            test_id = int(tu_details.get('testId'))
            test_user_id = int(tu_details.get('testUserId'))
            print(test_user_id)
            actual_data = crpo_common_obj.candidate_web_transcript(token, test_id, test_user_id)
            print(actual_data)
            data = actual_data.get('data')
            mcq_data = data.get('multipleCorrectAnswer')
            for index in range(0, len(mcq_data)):
                if tu_details.get('reloginRequird') == 'Yes':
                    data = {'excel': tu_details.get('orig_answer_qid' + str(index + 1)),
                            'actual': str(mcq_data[index].get('candidateAnswer'))}
                elif tu_details.get('unAnswerRequired') == 'Yes':
                    data = {'excel': 'None',
                            'actual': str(mcq_data[index].get('candidateAnswer'))}
                else:
                    data = {'excel': tu_details.get('orig_answer_qid' + str(index + 1)),
                            'actual': str(mcq_data[index].get('candidateAnswer'))}
                candidate_answers.append(data)
            obj_assessment_data_verification.write_data(tu_details, candidate_answers, row_size)
            row_size += 1
        self.ws.write(0, 1, self.over_all_status, self.over_all_status_color)

    def write_data(self, excel_candidate_data, candidate_answers, row_value):
        col_index = 4
        status = "Pass"
        final_status_color = self.green_color
        for candidate_data in candidate_answers:
            col_index += 2
            final_status_color = self.green_color
            if candidate_data.get('excel') != candidate_data.get('actual'):
                status = "Fail"
                self.over_all_status = "Fail"
                self.over_all_status_color = self.red_color
                final_status_color = self.red_color
            self.ws.write(row_value, col_index, candidate_data.get('excel'), self.black_color)
            self.ws.write(row_value, col_index + 1, candidate_data.get('actual'), final_status_color)

        self.ws.write(row_value, 0, excel_candidate_data.get('testCases'), self.black_color_bold)
        self.ws.write(row_value, 1, status, final_status_color)
        self.ws.write(row_value, 2, excel_candidate_data.get('testId'), self.black_color)
        self.ws.write(row_value, 3, excel_candidate_data.get('candidateId'), self.black_color)
        self.ws.write(row_value, 4, excel_candidate_data.get('loginName'), self.black_color)
        self.ws.write(row_value, 5, excel_candidate_data.get('password'), self.black_color)


#
# input_file_path = "C:/Users/User/Desktop/Automation/PythonWorkingScripts_InputData/UI/Assessment/ui_relogin.xls"
# excel_read_obj.excel_read(input_file_path, 0)
# excel_data = excel_read_obj.details
# crpo_token = crpo_common_obj.login_to_crpo('admin', 'Email@admin', 'AT')
obj_assessment_data_verification = AssessmentDataVerification()
# obj_assessment_data_verification.assessment_data_report(crpo_token, excel_data)
# obj_assessment_data_verification.write_excel.close()
