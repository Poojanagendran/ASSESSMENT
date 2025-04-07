from SCRIPTS.CRPO_COMMON.credentials import *
from SCRIPTS.DB_DELETE.question_statistics_test_delete import qs_test_del
from SCRIPTS.UI_SCRIPTS.assessment_data_verification import *
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.COMMON.io_path import *
import json


class OnlineAssessment:

    def __init__(self):
        qs_test_del.delete_question_statistics()
        self.row = 1
        write_excel_object.save_result(output_question_statistics_tests)
        header = ['Question Statics']
        write_excel_object.write_headers_for_scripts(0, 0, header, write_excel_object.black_color_bold)
        header = ['Test Cases', 'Status', 'Question Id', 'testId', 'tenant', 'Exp - Total Attempts',
                  'Act - Total Attempts',
                  'Exp - Avg response Time', 'Act - Avg response time', 'Exp-Item Difficulty', 'Act-Item Difficulty',
                  'Exp - Correct answer', 'Act - Correct answer', 'Exp - Partial Correct', 'Act - Partial Correct',
                  'Exp - Facility value', 'Act - Facility value', 'Exp - Incorrect', 'Act - Incorrect',
                  'Exp - Unattempted', 'Act - Unattempted', 'Exp - Dist index A', 'Act - Dist index A',
                  'Exp - Dist index B', 'Act - dist index B', 'Exp - Dist index C', 'Act - Dist index C',
                  'Exp - Dist index D', 'Act - Dist index D', 'Exp - Not Attempted A', 'Act - Not Attempted A',
                  'Exp - Not Attempted B', 'Act - Not Attempted B', 'Exp - Not Attempted C', 'Act - Not Attempted C',
                  'Exp - Not Attempted D', 'Act - Not Attempted D']

        write_excel_object.write_headers_for_scripts(1, 0, header, write_excel_object.black_color_bold)

    def calculate_qn_stats(self, excel_datas, automation_token):
        print(automation_token)
        automation_test_ids = []
        for i in excel_datas:
            automation_test_ids.append(int(i.get('testId')))
        automation_test_ids = set(automation_test_ids)
        automation_test_ids = list(automation_test_ids)
        if automation_test_ids:
            for test_id in automation_test_ids:
                # test_id = list[test_id]
                calculate_question_stats_context_id = CrpoCommon.calculate_question_statistics_for_tests(automation_token,
                                                                                                         test_id)
                self.task_status = CrpoCommon.job_status(automation_token, calculate_question_stats_context_id)
                self.current_task_status = self.task_status['data']['JobState']
                while self.current_task_status != 'SUCCESS':
                    self.task_status = CrpoCommon.job_status(automation_token, calculate_question_stats_context_id)
                    self.current_task_status = self.task_status['data']['JobState']
                if self.current_task_status == 'SUCCESS':
                    question_stats_results = json.loads(self.task_status['data']['Result'])
                    print(question_stats_results)
                    question_stats1 = question_stats_results['questionStats'][0]['questionStats']
                    for act_question in question_stats1:
                        write_excel_object.current_status_color = write_excel_object.green_color
                        write_excel_object.current_status = 'pass'
                        for excel_question in excel_datas:
                            if act_question.get('questionId') == int(excel_question.get('questionId')):
                                act_correct = act_question.get('correct')
                                act_incorrect = act_question.get('inCorrect')
                                act_partial_correct = act_question.get('partialCorrect')
                                act_not_attempted = act_question.get('unAttempted')
                                act_total_attempt = act_question.get('totalAttempt')
                                act_avg_response_time = round(act_question.get('avgResponseTime'), 2)
                                act_exposure_rate = act_question.get('exposureRate')
                                act_facility_value = round(act_question.get('facilityValue'), 2)
                                act_item_difficulty = round(act_question.get('itemDifficulty'), 2)
                                act_dist_index_of_a = round(act_question.get('distractorIndexOfA'), 2)
                                act_dist_index_of_b = round(act_question.get('distractorIndexOfB'), 2)
                                act_dist_index_of_c = round(act_question.get('distractorIndexOfC'), 2)
                                act_dist_index_of_d = round(act_question.get('distractorIndexOfD'), 2)
                                act_no_of_attempted_a = round(act_question.get('numberOfAttendedA'), 2)
                                act_no_of_attempted_b = round(act_question.get('numberOfAttendedB'), 2)
                                act_no_of_attempted_c = round(act_question.get('numberOfAttendedC'), 2)
                                act_no_of_attempted_d = round(act_question.get('numberOfAttendedD'), 2)
                                self.row = self.row + 1
                                write_excel_object.compare_results_and_write_vertically(excel_question.get('testCases'),
                                                                                        None, self.row, 0)
                                write_excel_object.compare_results_and_write_vertically(
                                    excel_question.get('questionId'),
                                    None, self.row, 2)
                                write_excel_object.compare_results_and_write_vertically(excel_question.get('testId'),
                                                                                        None, self.row, 3)
                                write_excel_object.compare_results_and_write_vertically(excel_question.get('tenant'),
                                                                                        None, self.row, 4)
                                write_excel_object.compare_results_and_write_vertically(
                                    int(excel_question.get('totalAttempts')), act_total_attempt, self.row, 5)
                                write_excel_object.compare_results_and_write_vertically(
                                    excel_question.get('avgResponseTime'), act_avg_response_time, self.row, 7)
                                write_excel_object.compare_results_and_write_vertically(
                                    excel_question.get('itemDifficultyLevel'), act_item_difficulty, self.row, 9)
                                write_excel_object.compare_results_and_write_vertically(
                                    int(excel_question.get('correct')),
                                    act_correct, self.row, 11)
                                write_excel_object.compare_results_and_write_vertically(
                                    excel_question.get('partialCorrect'), act_partial_correct, self.row, 13)
                                write_excel_object.compare_results_and_write_vertically(
                                    excel_question.get('facilityValue'),
                                    act_facility_value, self.row, 15)
                                write_excel_object.compare_results_and_write_vertically(
                                    int(excel_question.get('inCorrect')), act_incorrect, self.row, 17)
                                write_excel_object.compare_results_and_write_vertically(
                                    int(excel_question.get('unAttempted')), act_not_attempted, self.row, 19)
                                write_excel_object.compare_results_and_write_vertically(
                                    excel_question.get('distractorIndexA'), act_dist_index_of_a, self.row, 21)
                                write_excel_object.compare_results_and_write_vertically(
                                    excel_question.get('distractorIndexB'), act_dist_index_of_b, self.row, 23)
                                write_excel_object.compare_results_and_write_vertically(
                                    excel_question.get('distractorIndexC'), act_dist_index_of_c, self.row, 25)
                                write_excel_object.compare_results_and_write_vertically(
                                    excel_question.get('distracotrIndexD'), act_dist_index_of_d, self.row, 27)

                                write_excel_object.compare_results_and_write_vertically(
                                    int(excel_question.get('attemptedA')), act_no_of_attempted_a, self.row, 29)
                                write_excel_object.compare_results_and_write_vertically(
                                    int(excel_question.get('attemptedB')), act_no_of_attempted_b, self.row, 31)
                                write_excel_object.compare_results_and_write_vertically(
                                    int(excel_question.get('attemptedC')), act_no_of_attempted_c, self.row, 33)
                                write_excel_object.compare_results_and_write_vertically(
                                    int(excel_question.get('attemptedD')), act_no_of_attempted_d, self.row, 35)
                                write_excel_object.compare_results_and_write_vertically(
                                    write_excel_object.current_status, None, self.row, 1)
                                break


assessment_obj = OnlineAssessment()
excel_read_obj.excel_read(input_question_statistics_tests, 0)
excel_data = excel_read_obj.details

automation_token = crpo_common_obj.login_to_crpo(cred_crpo_admin.get('user'),
                                                 cred_crpo_admin.get('password'),
                                                 cred_crpo_admin.get('tenant'))
print("AT")
print(automation_token)
assessment_obj.calculate_qn_stats(excel_data, automation_token)
write_excel_object.write_overall_status(22)
