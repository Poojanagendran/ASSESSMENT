import xlsxwriter
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.CRPO_COMMON.crpo_common import *
from SCRIPTS.ASSESSMENT_COMMON.assessment_common import *
from SCRIPTS.DB_DELETE.db_cleanup import *


class SecurityCheck:

    def __init__(self):
        # data clean up is important, b'coz we need to create a candidate everytime to check the create is working fine.
        data_clean_obj.encryption_delete()

        requests.packages.urllib3.disable_warnings()
        self.started = datetime.datetime.now()
        self.started = self.started.strftime("%Y-%M-%d-%H-%M-%S")
        excel_read_obj.excel_read(input_path_encryption_check, 0)
        self.crpo_headers = crpo_common_obj.login_to_crpo(cred_crpo_admin.get('user'),
                                                          cred_crpo_admin.get('password'),
                                                          cred_crpo_admin.get('tenant'))
        self.row_size = 2
        self.write_excel = xlsxwriter.Workbook(output_path_encryption_check + self.started + '.xls')
        self.ws = self.write_excel.add_worksheet()
        self.black_color = self.write_excel.add_format({'font_color': 'black', 'font_size': 9})
        self.red_color = self.write_excel.add_format(
            {'bg_color': 'red', 'font_color': 'black', 'bold': True, 'font_size': 9})
        self.green_color = self.write_excel.add_format({'font_color': 'green', 'font_size': 9})
        self.orange_color = self.write_excel.add_format({'font_color': 'orange', 'font_size': 9})
        self.black_color_bold = self.write_excel.add_format({'font_color': 'black', 'bold': True, 'font_size': 9})
        self.over_all_status_pass = self.write_excel.add_format({'font_color': 'green', 'bold': True, 'font_size': 9})
        self.over_all_status_failed = self.write_excel.add_format({'font_color': 'red', 'bold': True, 'font_size': 9})
        self.over_all_status_color = self.over_all_status_pass
        self.over_all_status = 'Pass'
        self.write_headers()

    def write_headers(self):
        total_headers = [['Encryption Check'],
                         ['Testcases', 'Status', 'Excel / DB / API', 'Candidate_name', 'First_Name', 'Middle_Name',
                          'Last_Name', 'Email', 'Alternate_Email', 'Mobile_Number', 'Alternate_Mobile', 'Pancard',
                          'passport', 'USN', 'Aadhar_Number', 'tu_name', 'tu_email_id', 'question_string',
                          'question_str_new', 'html_string', 'html_string_new', 'correct_answer', 'ans_html_string',
                          'ans_html_string_new', 'ans_correct_answer_new', 'choices_choice', 'choices_html_string',
                          'choices_html_string_new']]
        header_row = 0
        self.header_column = 0
        for headers in total_headers:
            col = self.header_column
            for header_name in headers:
                self.ws.write(header_row, col, header_name, self.black_color)
                col = col + 1
            header_row = header_row + 1

    def validate_encrypeted_data(self, db_data, row, col):
        # this works according to DB query if we change DB query then Column will get affect,
        # so append any field if you want.
        for db_data_column_wise in db_data:
            col = col + 1
            if db_data_column_wise and 'enc_str::' in db_data_column_wise:
                self.ws.write(row, col, db_data_column_wise, self.green_color)
            else:
                self.ws.write(row, col, db_data_column_wise, self.red_color)

    def validate_api_result_with_excel_data(self, api_data, excel_data, row_number, col_number):
        if api_data == excel_data:
            self.ws.write(row_number, col_number, api_data, self.green_color)
        else:
            self.ws.write(row_number, col_number, api_data, self.red_color)

    def encryption_check_candidate(self, excel_data, row_value):
        create_candidate_req = {
            "PersonalDetails": {"FirstName": excel_data.get('firstName'), "MiddleName": excel_data.get('middleName'),
                                "LastName": excel_data.get('lastName'),
                                "PassportNo": excel_data.get('passport'),
                                "Mobile1": str(int(excel_data.get('mobileNumber'))),
                                "PanNo": excel_data.get('panCard'), "DateOfBirth": "2021-12-21T18:30:00.000Z",
                                "PhoneOffice": str(excel_data.get('phoneOffice')),
                                "Email2": excel_data.get('alternateEmailId'),
                                "Email1": excel_data.get('emailId'), "CurrencyType": None,
                                "USN": excel_data.get('usn'), "AadhaarNo": str(int(excel_data.get('aadharNumber')))},
            "SourceDetails": {"SourceId": "3638"}}
        cid = crpo_common_obj.create_candidate_v2(self.crpo_headers, create_candidate_req)
        candidate_details = crpo_common_obj.get_candidate_by_id(self.crpo_headers, cid)
        request = request = {"questionType": 7, "difficultyLevel": 1, "subCategoryId": 3928, "categoryId": 3922,
                             "htmlString": excel_data.get('questionQuestionString'),
                             "questionStr": excel_data.get('questionQuestionString'),
                             "subTopicId": None, "authorId": 14390, "isRevised": False, "notes": "Notes1",
                             "subTopicUnitId": None,
                             "statusId": 2622, "questionFlag": 1,
                             "answers": [{"htmlString": excel_data.get("questionCorrectAnswer"), "correctAnswer": "A"}],
                             "answerChoices": [{"htmlString": excel_data.get("answerHtmlString"), "choice": "A"},
                                               {"htmlString": excel_data.get("answerHtmlString"), "choice": "B"},
                                               {"htmlString": excel_data.get("answerHtmlString"), "choice": "C"},
                                               {"htmlString": excel_data.get("answerHtmlString"), "choice": "D"}]}
        qid = crpo_common_obj.create_question(self.crpo_headers, request)
        question_details = crpo_common_obj.get_question_for_id(self.crpo_headers, qid)
        question_string = question_details['data']['questionStr']
        html_string = question_details['data']['htmlString']
        answer_choice = question_details['data']['answerChoices'][0]['htmlString']
        correct_answers = question_details['data']['answers'][0]['htmlString']
        candidate_personal_details_query = 'select candidate_name,first_name, middle_name,last_name, email1,email2,mobile1,phone_office,' \
                                           'pan_card,passport,usn,aadhaar_no from candidates where id=%d;' % cid
        print(candidate_personal_details_query)
        connection = ams_db_connection()
        cursor = connection.cursor()
        cursor.execute(candidate_personal_details_query)
        db_results = cursor.fetchone()
        self.ws.write(row_value, 2, "Excel Data", self.black_color_bold)
        self.ws.write(row_value + 1, 2, "API Data", self.black_color_bold)
        self.ws.write(row_value + 2, 2, "DB Data", self.black_color_bold)
        self.ws.write(row_value, 3, excel_data.get('candidateName'), self.black_color)
        self.ws.write(row_value, 4, excel_data.get('firstName'), self.black_color)
        self.ws.write(row_value, 5, excel_data.get('middleName'), self.black_color)
        self.ws.write(row_value, 6, excel_data.get('lastName'), self.black_color)
        self.ws.write(row_value, 7, excel_data.get('emailId'), self.black_color)
        self.ws.write(row_value, 8, excel_data.get('alternateEmailId'), self.black_color)
        self.ws.write(row_value, 9, excel_data.get('mobileNumber'), self.black_color)
        self.ws.write(row_value, 10, excel_data.get('phoneOffice'), self.black_color)
        self.ws.write(row_value, 11, excel_data.get('panCard'), self.black_color)
        self.ws.write(row_value, 12, excel_data.get('passport'), self.black_color)
        self.ws.write(row_value, 13, excel_data.get('usn'), self.black_color)
        self.ws.write(row_value, 14, excel_data.get('aadharNumber'), self.black_color)
        self.ws.write(row_value, 15, excel_data.get('candidateName'), self.black_color)
        self.ws.write(row_value, 16, excel_data.get('emailId'), self.black_color)
        self.ws.write(row_value, 17, excel_data.get('questionQuestionString'), self.black_color)
        self.ws.write(row_value, 18, excel_data.get('questionQuestionStringNew'), self.black_color)
        self.ws.write(row_value, 19, excel_data.get('questionHtmlString'), self.black_color)
        self.ws.write(row_value, 20, excel_data.get('questionHtmlStringNew'), self.black_color)
        self.ws.write(row_value, 21, excel_data.get('questionCorrectAnswer'), self.black_color)
        self.ws.write(row_value, 22, excel_data.get('answerHtmlString'), self.black_color)
        self.ws.write(row_value, 23, excel_data.get('answerHtmlStringNew'), self.black_color)
        self.ws.write(row_value, 24, excel_data.get('answerCorrectAnswerNew'), self.black_color)
        self.ws.write(row_value, 25, excel_data.get('choicesChoice'), self.black_color)
        self.ws.write(row_value, 26, excel_data.get('choicesHtmlString'), self.black_color)
        self.ws.write(row_value, 27, excel_data.get('choicesHtmlStringNew'), self.black_color)

        candidate_personal_details = candidate_details['Candidate']['PersonalDetails']
        rowvalue = row_value + 1
        encryption_obj.validate_api_result_with_excel_data(candidate_personal_details.get('Name'),
                                                           excel_data.get('candidateName'), rowvalue, 3)
        encryption_obj.validate_api_result_with_excel_data(candidate_personal_details.get('FirstName'),
                                                           excel_data.get('firstName'), rowvalue, 4)
        encryption_obj.validate_api_result_with_excel_data(candidate_personal_details.get('MiddleName'),
                                                           excel_data.get('middleName'), rowvalue, 5)
        encryption_obj.validate_api_result_with_excel_data(candidate_personal_details.get('LastName'),
                                                           excel_data.get('lastName'), rowvalue, 6)
        encryption_obj.validate_api_result_with_excel_data(candidate_personal_details.get('Email1'),
                                                           excel_data.get('emailId'), rowvalue, 7)
        encryption_obj.validate_api_result_with_excel_data(candidate_personal_details.get('Email2'),
                                                           excel_data.get('alternateEmailId'), rowvalue, 8)
        encryption_obj.validate_api_result_with_excel_data(int(candidate_personal_details.get('Mobile1')),
                                                           int(excel_data.get('mobileNumber')), rowvalue, 9)
        encryption_obj.validate_api_result_with_excel_data(int(float(candidate_personal_details.get('PhoneOffice'))),
                                                           int(excel_data.get('phoneOffice')), rowvalue, 10)
        print((candidate_personal_details.get('PanNo')))
        print(type(candidate_personal_details.get('PanNo')))
        print(excel_data.get('panCard'))
        print(type(excel_data.get('panCard')))

        encryption_obj.validate_api_result_with_excel_data((candidate_personal_details.get('PanNo')),
                                                           excel_data.get('panCard'), rowvalue, 11)

        encryption_obj.validate_api_result_with_excel_data(candidate_personal_details.get('PassportNo'),
                                                           excel_data.get('passport'), rowvalue, 12)

        encryption_obj.validate_api_result_with_excel_data(candidate_personal_details.get('USN'),
                                                           excel_data.get('usn'), rowvalue, 13)

        encryption_obj.validate_api_result_with_excel_data(str(candidate_personal_details.get('AadhaarNo')),
                                                           str(excel_data.get('aadharNumber')), rowvalue, 14)
        # encryption_obj.validate_api_result_with_excel_data(candidate_personal_details.get('AadhaarNo'),
        #                                                    excel_data.get('aadharNumber'), rowvalue, 15)
        # encryption_obj.validate_api_result_with_excel_data(candidate_personal_details.get('AadhaarNo'),
        #                                                    excel_data.get('aadharNumber'), rowvalue, 16)

        encryption_obj.validate_api_result_with_excel_data(question_string,
                                                           excel_data.get('questionQuestionString'), rowvalue, 17)
        encryption_obj.validate_api_result_with_excel_data(question_string,
                                                           excel_data.get('questionQuestionStringNew'), rowvalue, 18)
        encryption_obj.validate_api_result_with_excel_data(html_string,
                                                           excel_data.get('questionHtmlString'), rowvalue, 19)
        encryption_obj.validate_api_result_with_excel_data(html_string,
                                                           excel_data.get('questionHtmlStringNew'), rowvalue, 20)
        encryption_obj.validate_api_result_with_excel_data(correct_answers,
                                                           excel_data.get('questionCorrectAnswer'), rowvalue, 21)
        encryption_obj.validate_api_result_with_excel_data(correct_answers,
                                                           excel_data.get('answerHtmlString'), rowvalue, 22)
        encryption_obj.validate_api_result_with_excel_data(correct_answers,
                                                           excel_data.get('answerHtmlStringNew'), rowvalue, 23)
        encryption_obj.validate_api_result_with_excel_data(correct_answers,
                                                           excel_data.get('answerCorrectAnswerNew'), rowvalue, 24)
        encryption_obj.validate_api_result_with_excel_data(answer_choice,
                                                           excel_data.get('choicesChoice'), rowvalue, 25)
        encryption_obj.validate_api_result_with_excel_data(answer_choice,
                                                           excel_data.get('choicesHtmlString'), rowvalue, 26)
        encryption_obj.validate_api_result_with_excel_data(answer_choice,
                                                           excel_data.get('choicesHtmlStringNew'), rowvalue, 27)

        rowvalue = rowvalue + 1
        encryption_obj.validate_encrypeted_data(db_results, row=rowvalue, col=2)

        questions_ans_answers_query = 'select que.question_str, que.question_str_new, que.html_string, que.html_string_new, ' \
                                      'ans.correct_answer, ans.html_string, ans.html_string_new, ans.correct_answer_new, ' \
                                      'cho.choice, cho.html_string,cho.html_string_new from questions que ' \
                                      'inner join answers ans on  que.id=ans.question_id ' \
                                      'inner join answer_choices cho on ans.question_id = cho.question_id where que.id =%d;' % qid
        print(questions_ans_answers_query)
        cursor.execute(questions_ans_answers_query)
        db_results_for_questions = cursor.fetchone()

        encryption_obj.validate_encrypeted_data(db_results_for_questions, row=rowvalue, col=16)


encryption_obj = SecurityCheck()
encryption_data_excel = excel_read_obj.details
# print(encryption_data_excel)

row = 0

for data in encryption_data_excel:
    row = row + 2
    encryption_obj.encryption_check_candidate(data, row)

#     encryption_obj.security_check(iter.get('api'), iter.get('payLoad'), iter.get('expectedStatus'), iter.get('apiModule'),
#                                 crpo_headers, candidate_headers, assessment_headers, iter.get('testCaseDescription'),
#                                 source_headers)
# #
ended = datetime.datetime.now()
ended = "Ended:- %s" % ended.strftime("%Y-%M-%d-%H-%M-%S")
encryption_obj.ws.write(0, 1, encryption_obj.over_all_status, encryption_obj.over_all_status_color)
encryption_obj.ws.write(0, 2, 'Started:- ' + encryption_obj.started, encryption_obj.black_color_bold)
encryption_obj.ws.write(0, 3, ended, encryption_obj.black_color_bold)
encryption_obj.ws.write(0, 4, "Total_Testcase_Count:- 138", encryption_obj.black_color_bold)

encryption_obj.ws.write(2, 1, encryption_obj.over_all_status, encryption_obj.over_all_status_color)
encryption_obj.ws.write(3, 1, encryption_obj.over_all_status, encryption_obj.over_all_status_color)
encryption_obj.ws.write(4, 1, encryption_obj.over_all_status, encryption_obj.over_all_status_color)

encryption_obj.write_excel.close()
