from SCRIPTS.CRPO_COMMON.credentials import *
from SCRIPTS.DB_DELETE.question_stats_new_cron_delete import qs_new_cron_del
from SCRIPTS.UI_SCRIPTS.assessment_data_verification import *
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.COMMON.io_path import *


class QuestionStatistics:

    def __init__(self):
        self.row = 1
        qs_new_cron_del.delete_question_statistics()
        write_excel_object.save_result(output_question_statistics_new_cron)
        header = ['Question Statics']
        write_excel_object.write_headers_for_scripts(0, 0, header, write_excel_object.black_color_bold)
        header = ['Test Cases', 'Status', 'Question Id', 'Exp - Total Attempts', 'Act - Total Attempts',
                  'Exp - Avg response Time', 'Act - Avg response time', 'Exp-Item Difficulty', 'Act-Item Difficulty',
                  'Exp - Correct answer', 'Act - Correct answer', 'Exp - Partial Correct', 'Act - Partial Correct',
                  'Exp - Facility value', 'Act - Facility value', 'Exp - Incorrect', 'Act - Incorrect',
                  'Exp - Unattempted', 'Act - Unattempted', 'Exp - Dist index A', 'Act - Dist index A',
                  'Exp - Dist index B', 'Act - dist index B', 'Exp - Dist index C', 'Act - Dist index C',
                  'Exp - Dist index D', 'Act - Dist index D', 'Exp - Qn usage', 'Act - Qn usage', 'Exp - qn papers',
                  'Act - Qn papers']

        write_excel_object.write_headers_for_scripts(1, 0, header, write_excel_object.black_color_bold)

    def calculate_qn_stats(self, excel_datas, hirepro_token):
        hirepro_question_ids = []
        for i in excel_datas:
            if i.get('tenant') == 'hirepro':
                hirepro_question_ids.append(int(i.get('question_id_for_api')))
            else:
                print("Please include only hirepro questions")

        if hirepro_question_ids:
            calculate_question_stats_context_id = CrpoCommon.calculate_hirepro_question_statistics(hirepro_token,
                                                                                                   hirepro_question_ids)
            task_status = CrpoCommon.job_status(hirepro_token, calculate_question_stats_context_id)
            current_task_status = task_status['data']['JobState']
            while current_task_status != 'SUCCESS':
                task_status = CrpoCommon.job_status(hirepro_token, calculate_question_stats_context_id)
                current_task_status = task_status['data']['JobState']

    def question_statistics(self, current_excel_data, hirepro_token):
        write_excel_object.current_status_color = write_excel_object.green_color
        write_excel_object.current_status = 'pass'
        excel_question_id = int(current_excel_data.get('questionId'))
        print(current_excel_data.get('tenant'))
        if current_excel_data.get('tenant') == "hirepro":
            qn_infos = CrpoCommon.get_question_for_id(hirepro_token, excel_question_id)
            print(qn_infos)
        else:
            print("Only hirepro questions are supported")

        qn_statistics = qn_infos['data']['questionAttributes']['statistics']
        question_usage = qn_infos['data']['questionReuse']
        question_papers = len(qn_infos['data']['questionAttributes']['questionPaperInfos'])
        total_attempts = qn_statistics.get('totalAttempt')
        avg_res_time = round(qn_statistics.get('avgResponseTime'), 4)
        item_difficulty_level = round(qn_statistics.get('itemDifficulty'), 4)
        correct = qn_statistics.get('correct')
        partial_correct = qn_statistics.get('partialCorrect')
        facility_value = round(qn_statistics.get('facilityValue'), 4)
        in_correct = qn_statistics.get('inCorrect')
        un_attempted = qn_statistics.get('unAttempted')
        dist_index_a = round(qn_statistics.get('distractorIndexOfA'), 4)
        dist_index_b = round(qn_statistics.get('distractorIndexOfB'), 4)
        dist_index_c = round(qn_statistics.get('distractorIndexOfC'), 4)
        dist_index_d = round(qn_statistics.get('distractorIndexOfD'), 4)

        self.row = self.row + 1
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('testCases'), None, self.row, 0)
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('questionId'), None, self.row, 2)
        write_excel_object.compare_results_and_write_vertically(int(current_excel_data.get('totalAttempts')),
                                                                total_attempts, self.row, 3)
        write_excel_object.compare_results_and_write_vertically(round(current_excel_data.get('avgResponseTime'), 4),
                                                                avg_res_time, self.row, 5)
        write_excel_object.compare_results_and_write_vertically(round(current_excel_data.get('itemDifficultyLevel'), 4),
                                                                item_difficulty_level, self.row, 7)
        write_excel_object.compare_results_and_write_vertically(int(current_excel_data.get('correct')),
                                                                correct, self.row, 9)
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('partialCorrect'),
                                                                partial_correct, self.row, 11)
        write_excel_object.compare_results_and_write_vertically(round(current_excel_data.get('facilityValue'), 4),
                                                                facility_value, self.row, 13)
        write_excel_object.compare_results_and_write_vertically(int(current_excel_data.get('inCorrect')),
                                                                in_correct, self.row, 15)
        write_excel_object.compare_results_and_write_vertically(int(current_excel_data.get('unAttempted')),
                                                                un_attempted, self.row, 17)
        write_excel_object.compare_results_and_write_vertically(round(current_excel_data.get('distractorIndexA'), 4),
                                                                dist_index_a, self.row, 19)
        write_excel_object.compare_results_and_write_vertically(round(current_excel_data.get('distractorIndexB'), 4),
                                                                dist_index_b, self.row, 21)
        write_excel_object.compare_results_and_write_vertically(round(current_excel_data.get('distractorIndexC'), 4),
                                                                dist_index_c, self.row, 23)
        write_excel_object.compare_results_and_write_vertically(round(current_excel_data.get('distracotrIndexD'), 4),
                                                                dist_index_d, self.row, 25)
        write_excel_object.compare_results_and_write_vertically(int(current_excel_data.get('questionUsage')),
                                                                question_usage, self.row, 27)
        write_excel_object.compare_results_and_write_vertically(int(current_excel_data.get('questionPapers')),
                                                                question_papers, self.row, 29)
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('tenant'),
                                                                None, self.row, 31)
        write_excel_object.compare_results_and_write_vertically(write_excel_object.current_status, None,
                                                                self.row, 1)


assessment_obj = QuestionStatistics()
excel_read_obj.excel_read(input_question_statistics, 1)
excel_data = excel_read_obj.details
hirepro_token = crpo_common_obj.login_to_crpo(cred_crpo_admin_hirepro.get('user'),
                                              cred_crpo_admin_hirepro.get('password'),
                                              cred_crpo_admin_hirepro.get('tenant'))
assessment_obj.calculate_qn_stats(excel_data, hirepro_token)
for current_excel_row in excel_data:
    assessment_obj.question_statistics(current_excel_row, hirepro_token)

write_excel_object.write_overall_status(11)
