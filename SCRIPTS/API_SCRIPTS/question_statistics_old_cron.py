from SCRIPTS.CRPO_COMMON.credentials import *
from SCRIPTS.DB_DELETE.question_statistics_delete import qs_old_cron_del
from SCRIPTS.UI_SCRIPTS.assessment_data_verification import *
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.COMMON.io_path import *


class OnlineAssessment:

    def __init__(self):
        self.row = 1
        qs_old_cron_del.delete_question_statistics()
        write_excel_object.save_result(output_question_statistics)
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

    def calculate_qn_stats(self, excel_datas, crpodemo_token, at_token):
        automation_question_ids = []
        hirepro_question_ids = []

        for i in excel_datas:
            if i.get('tenant') == 'automation':
                automation_question_ids.append(int(i.get('questionId')))
            elif i.get('tenant') == 'hirepro':
                hirepro_question_ids.append(int(i.get('questionId')))
        print(automation_question_ids)
        print(hirepro_question_ids)
        if automation_question_ids:
            calculate_question_stats_context_id = CrpoCommon.calculate_question_statistics(at_token, automation_question_ids)
            task_status = CrpoCommon.job_status(at_token, calculate_question_stats_context_id)
            current_task_status = task_status['data']['JobState']
            # print(current_task_status)
            while current_task_status != 'SUCCESS':
                # print("This is while")
                task_status = CrpoCommon.job_status(at_token, calculate_question_stats_context_id)
                current_task_status = task_status['data']['JobState']
                # print(current_task_status)
        if hirepro_question_ids:
            calculate_question_stats_context_id = CrpoCommon.calculate_question_statistics(crpodemo_token,
                                                                                           hirepro_question_ids)
            task_status = CrpoCommon.job_status(crpodemo_token, calculate_question_stats_context_id)
            current_task_status = task_status['data']['JobState']
            # print(current_task_status)
            while current_task_status != 'SUCCESS':
                # print("This is while")
                task_status = CrpoCommon.job_status(crpodemo_token, calculate_question_stats_context_id)
                current_task_status = task_status['data']['JobState']
                # print(current_task_status)

    def question_statistics(self, current_excel_data, at_token, hirepro_token):
        write_excel_object.current_status_color = write_excel_object.green_color
        write_excel_object.current_status = 'pass'
        excel_question_id = int(current_excel_data.get('questionId'))
        print(current_excel_data.get('tenant'))
        if current_excel_data.get('tenant') == "automation":
            qn_infos = CrpoCommon.get_question_for_id(at_token, excel_question_id)
        elif current_excel_data.get('tenant') == "hirepro":
            qn_infos = CrpoCommon.get_question_for_id(hirepro_token, excel_question_id)
        else:
            pass
        qn_statistics = qn_infos['data']['questionAttributes']['statistics']
        question_usage = qn_infos['data']['questionReuse']
        question_papers = len(qn_infos['data']['questionAttributes']['questionPaperInfos'])
        total_attempts = qn_statistics.get('totalAttempt')
        avg_res_time = qn_statistics.get('avgResponseTime')
        item_difficulty_level = qn_statistics.get('itemDifficulty')
        correct = qn_statistics.get('correct')
        partial_correct = qn_statistics.get('partialCorrect')
        facility_value = qn_statistics.get('facilityValue')
        in_correct = qn_statistics.get('inCorrect')
        un_attempted = qn_statistics.get('unAttempted')
        dist_index_a = qn_statistics.get('distractorIndexOfA')
        dist_index_b = qn_statistics.get('distractorIndexOfB')
        dist_index_c = qn_statistics.get('distractorIndexOfC')
        dist_index_d = qn_statistics.get('distractorIndexOfD')

        self.row = self.row + 1
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('testCases'), None, self.row, 0)
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('questionId'), None, self.row, 2)
        write_excel_object.compare_results_and_write_vertically(int(current_excel_data.get('totalAttempts')),
                                                                total_attempts, self.row, 3)
        write_excel_object.compare_results_and_write_vertically(round(current_excel_data.get('avgResponseTime'), 5),
                                                                round(avg_res_time, 5), self.row, 5)
        write_excel_object.compare_results_and_write_vertically(round(current_excel_data.get('itemDifficultyLevel'), 4)
                                                                , round(item_difficulty_level, 4), self.row, 7)
        write_excel_object.compare_results_and_write_vertically(int(current_excel_data.get('correct')),
                                                                correct, self.row, 9)
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('partialCorrect'),
                                                                partial_correct, self.row, 11)
        write_excel_object.compare_results_and_write_vertically(round(current_excel_data.get('facilityValue'), 5),
                                                                round(facility_value, 5), self.row, 13)
        write_excel_object.compare_results_and_write_vertically(int(current_excel_data.get('inCorrect')),
                                                                in_correct, self.row, 15)
        write_excel_object.compare_results_and_write_vertically(int(current_excel_data.get('unAttempted')),
                                                                un_attempted, self.row, 17)
        write_excel_object.compare_results_and_write_vertically(round(current_excel_data.get('distractorIndexA'), 5),
                                                                round(dist_index_a, 5), self.row, 19)
        write_excel_object.compare_results_and_write_vertically(round(current_excel_data.get('distractorIndexB'), 5),
                                                                round(dist_index_b, 5), self.row, 21)
        write_excel_object.compare_results_and_write_vertically(round(current_excel_data.get('distractorIndexC'), 5),
                                                                round(dist_index_c, 5), self.row, 23)
        write_excel_object.compare_results_and_write_vertically(round(current_excel_data.get('distracotrIndexD'), 5),
                                                                round(dist_index_d, 5), self.row, 25)
        write_excel_object.compare_results_and_write_vertically(int(current_excel_data.get('questionUsage')),
                                                                question_usage, self.row, 27)
        write_excel_object.compare_results_and_write_vertically(int(current_excel_data.get('questionPapers')),
                                                                question_papers, self.row, 29)
        write_excel_object.compare_results_and_write_vertically(current_excel_data.get('tenant'),
                                                                None, self.row, 31)
        write_excel_object.compare_results_and_write_vertically(write_excel_object.current_status, None,
                                                                self.row, 1)


assessment_obj = OnlineAssessment()
excel_read_obj.excel_read(input_question_statistics, 0)
excel_data = excel_read_obj.details
hirepro_token = crpo_common_obj.login_to_crpo(cred_crpo_admin_hirepro.get('user'),
                                               cred_crpo_admin_hirepro.get('password'),
                                               cred_crpo_admin_hirepro.get('tenant'))

automation_token = crpo_common_obj.login_to_crpo(cred_crpo_admin.get('user'),
                                         cred_crpo_admin.get('password'),
                                         cred_crpo_admin.get('tenant'))
print(hirepro_token, automation_token)
assessment_obj.calculate_qn_stats(excel_data, hirepro_token, automation_token)
for current_excel_row in excel_data:
    assessment_obj.question_statistics(current_excel_row, automation_token, hirepro_token)

write_excel_object.write_overall_status(1)
