import datetime
# import os
from SCRIPTS.COMMON.environment import *
from SCRIPTS.COMMON.io_user_directory import *

# path = os.getcwd()
# print(path)
# Assessment URLS

domain = env_obj.domain
pearson_domain = env_obj.pearson_domain
eu_domain = env_obj.eu_domain
amsin_at_assessment_url = domain + "/assessment/#/assess/login/eyJhbGlhcyI6ImF0In0="
amsin_at_vet_url = pearson_domain + "/assessment/#/assess/login/eyJhbGlhcyI6ImF0In0="
amsin_automation_assessment_url = domain + "/assessment/#/assess/login/eyJhbGlhcyI6ImF1dG9tYXRpb24ifQ=="
amsin_crpodemo_assessment_url = domain + "/assessment/#/assess/login/eyJhbGlhcyI6ImNycG9kZW1vIn0="

# CRPO Login
amsin_at_crpo_login = domain + "/crpo/#/login/AT"
amsin_crpodemo_crpo_login = domain + "/crpo/#/login/crpodemo"

# Chromedriver Related
chrome_driver_path = chrome_driver_dir + '\chromedriver.exe'
started = datetime.datetime.now()
started = started.strftime("%d-%m-%Y")

# input paths
input_path_allowed_extension = input_common_dir + r'\allowed_extensions\allowed_extensions_inputfile.xls'
print(input_path_allowed_extension)
input_path_suspicious_list = input_common_dir + '\MURALITEAM\sep8.xls'
input_path_allowed_extension_files = input_common_dir + r'\allowed_extensions\%s'
input_path_applicant_report = input_common_dir + r'\Assessment\applicant_report\applicantreport.xlsx'
input_path_applicant_report_downloaded = input_common_dir + r'\Assessment\applicant_report\downloaded\downloadedfile.xlsx'
input_path_2tests_chaining = input_common_dir + r'\Assessment\chaining\2ndlogincase.xls'
input_path_3tests_chaining = input_common_dir + r'\Assessment\chaining\3_tests_login_automation.xls'
input_path_plagiarism_report = input_common_dir + r'\Assessment\plagiarism_report\plagiarism_report.xlsx'
input_path_plagiarism_report_downloaded = input_common_dir + r'\Assessment\plagiarism_report\downloaded\plagiarism_report' + started + '.xlsx'
input_path_proctor_evaluation = input_common_dir + r'\Assessment\proc_eval\proc_eval3.xls'
input_path_question_search_count = input_common_dir + r'\Assessment\Search\question_search_Automation.xls'
input_path_question_search_boundary = input_common_dir + r'\Assessment\Search\question_search_boundary_automation.xls'
input_path_reinitiate_automation = input_common_dir + r'\Assessment\reinitiateautomation1.xls'
input_path_mic_distortion_check = input_common_dir + r'\Assessment\mic_distortion_check\1input.xls'
input_path_mic_distortion_files = input_common_dir + r'\Assessment\mic_distortion_check\%s'
input_path_brightness_check = input_common_dir + r'\Assessment\brightnesscheck\brightnesscheck.xls'
input_path_brightness_check_files = input_common_dir + r'\Assessment\brightnesscheck\%s'
input_coding_compiler = input_common_dir + r'\Assessment\coding\codingcompiler.xls'
input_question_statistics = input_common_dir + r'\Assessment\question_statistics_for_questions.xls'
input_question_statistics_tests = input_common_dir + r'\Assessment\question_statistics_for_tests.xls'
# input_question_statistics_hirepro_cron = input_common_dir + 'Assessment\\question_statistics_new_cron_1.xls'
input_path_sanitize_automation = input_common_dir + r'\Assessment\sanitizeautomation.xls'


input_path_microsite_create_case = input_common_dir + r'\Microsite\GenericExcelTest.xls'
input_path_microsite_update_case = input_common_dir + r'\Microsite\GenericExcelTest.xls'
input_path_microsite_generic_case = input_common_dir + r'\Microsite\GenericExcelTest.xls'

# interview
input_interview_proctoring_evaluation = input_common_dir + r'\Interview\proctoring\proctoring.xls'

# security
input_path_ssrf_check = input_common_dir + r'\SSRF\SSRF_Final1.xls'
input_path_encryption_check = input_common_dir + r'\Security\encryption.xls'

# UI Automation Input Path
input_path_ui_mcq_randomization = input_common_dir + r'\UI\Assessment\qprandomization_automation.xls'
input_path_ui_video_randomization = input_common_dir + r'\UI\Assessment\qprandomization_crpodemo.xls'
input_path_ui_assessment_verification = input_common_dir + r'\UI\Assessment\ui_relogin.xls'
input_path_ui_qp_verification = input_common_dir + r"\UI\Assessment\qp_verification.xls"
input_path_ui_hirepro_chaining = input_common_dir + r'\UI\Assessment\hirepro_chaining_at.xls'
input_path_ui_vet_vet_chaining = input_common_dir + r'\UI\Assessment\vet_chaining.xls'
input_path_ui_test_security = input_common_dir + r'\UI\Assessment\test_security.xls'
input_path_ui_reuse_score = input_common_dir + r'\Assessment\reuse_score.xls'
input_path_ui_mcq_client_section_random = input_common_dir + r'\UI\Assessment\clientside_randomization.xls'
input_path_ui_rtc_static = input_common_dir + r'\UI\Assessment\rtc_static.xls'
input_path_ui_marking_schema = input_common_dir + r'\UI\Assessment\test_marking.xls'
input_path_ui_self_assessment = input_common_dir + r'\UI\Assessment\self_assessment.xls'
# input_path_ui_fib_marking_schema = input_common_dir + 'UI\\Assessment\\test_marking_fib.xls'

# INFRA
input_infra_strict_domain_validations = input_common_dir + r"\INFRA\strict_domain.xls"
input_adhoc_profile_validations = input_common_dir + r"\INFRA\adhoc_profile.xls"

# output paths
output_path_allowed_extension = output_common_dir + r'\allowed_extensions\API_allowed_extensions'
output_path_suspicious_candidates = output_common_dir + r'\allowed_extensions\suspicious(' + started + ').xlsx'
output_path_applicant_report = output_common_dir + r'\Assessment\report\API_applicantreport'
output_path_2tests_chaining = output_common_dir + r'\Assessment\API_2tests_Chaining_Automation -'
output_path_3tests_chaining = output_common_dir + r'\Assessment\API_3tests_Chaining_Automation - '
output_path_plagiarism_report = output_common_dir + r'\Assessment\plagiarism_report\API_plagiarism_report'
output_path_proctor_evaluation = output_common_dir + r'\Assessment\proctoring\API_proctoring_eval100'
output_path_dev_proctor_evaluation = output_common_dir + r'\Assessment\proctoring\API_device_proctoring_eval'
output_path_behaviour_proctor_evaluation_new = output_common_dir + r'\Assessment\proctoring\API_behaviour_proctoring_eval_new'
output_path_behaviour_proctor_evaluation = output_common_dir + r'\Assessment\proctoring\API_behaviour_proctoring_eval'
output_path_question_search_count = output_common_dir + r'\Assessment\search\API_question_search_'
output_path_question_search_boundary = output_common_dir + r'\Assessment\search\API_question_boundary_search_'
output_path_reinitiate_automation = output_common_dir + r'\Assessment\reinitiate\API_reinitiate - '
output_path_ssrf_check = output_common_dir + r'\SSRF\API_security_check -'
output_path_microsite_create_case = output_common_dir + r'\Microsite\UI_Microsite_CreateCase(' + started + ').xlsx'
output_path_microsite_update_case = output_common_dir + r'\Microsite\UI_Microsite_UpdateCase(' + started + ').xlsx'
output_path_microsite_generic_case = output_common_dir + r'\Microsite\UI_Functionality_VandV(' + started + ').xlsx'
output_path_encryption_check = output_common_dir + r'\SSRF\API_encryption_check -'
output_path_reuse_score = output_common_dir + r'\Assessment\reuse_score - '
output_path_mic_check = output_common_dir + r'\Assessment\mic_distortion_check'
output_path_brightness_sharpness_check = output_common_dir + r'\Assessment\API_brightness_sharpnesscheck- '
output_coding_compiler = output_common_dir + r'\Assessment\codingcompiler'
output_question_statistics = output_common_dir + r'\Assessment\API_qn_statisctis'
output_question_statistics_tests = output_common_dir + r'\Assessment\API_qn_statisctis_tests'
output_question_statistics_new_cron = output_common_dir + r'\Assessment\API_qn_statisctis_new_cron'
output_question_statistics_tests_hp_cron = output_common_dir + r'\Assessment\API_hp_qn_statisctis_tests'
output_path_sanitize_automation = output_common_dir + r'\Assessment\reinitiate\API_sanitize - '

# Interview
output_interview_proctor_evaluation = output_common_dir + r'\interview\interview_proctoring_eval'

# UI Automation Output Path
output_path_ui_vet_qs = output_common_dir + r'\Assessment\UI\VET\UI_qs(' + started + ').xlsx'
output_path_ui_cocubes = output_common_dir + r'\UI\UI_cocubes'
output_path_ui_mettl = output_common_dir + r'\UI\UI_Mettl'
output_path_ui_wheebox = output_common_dir + r'\UI\UI_Wheebox'
output_path_ui_mcq_randomization = output_common_dir + r'\UI\UI_mcq_qprandomization_'
output_path_ui_rtc_server_random = output_common_dir + r'\UI\UI_rtc_server_qprandomization_'
output_path_ui_coding_randomization = output_common_dir + r'\UI\UI_coding_qprandomization_'
output_path_ui_subjective_randomization = output_common_dir + r'\UI\UI_subjective_qprandomization_'
output_path_ui_mcqww_randomization = output_common_dir + r'\UI\UI_mcqww_qprandomization_'
output_path_ui_mca_randomization = output_common_dir + r'\UI\UI_mca_qprandomization_'
output_path_ui_fib_randomization = output_common_dir + r'\UI\UI_fib_qprandomization_'
output_path_ui_video_randomization = output_common_dir + r'\UI\UI_video_qprandomization_'
output_path_ui_draw_randomization = output_common_dir + r'\UI\UI_draw_qprandomization_'
output_path_ui_assessment_verification = output_common_dir + r'\UI\UI_ui_assessment_relogin.xls'
output_path_ui_qp_verification = output_common_dir + r"\UI\UI_QP_verification"
output_path_ui_test_security = output_common_dir + r"\UI\UI_Test_Security"
output_path_ui_hirepro_chaining = output_common_dir + r'\UI\UI_hirepro_chaining - ' + started + '.xls'
output_path_ui_vet_vet_chaining = output_common_dir + r'\UI\UI_vet_vet_chaining_plus_retest_consent - ' + started + '.xls'
output_path_ui_mcq_client_section_random = output_common_dir + r'\UI\UI_client_mcq_random_sectionwise_qprandomization_'
output_path_ui_mcq_client_group_random = output_common_dir + r'\UI\UI_client_mcq_random_groupwise_qprandomization_'
output_path_ui_mcq_client_test_random = output_common_dir + r'\UI\UI_client_mcq_random_testlevel_qprandomization_'

output_path_ui_mcqww_client_test_random = output_common_dir + r'\UI\UI_client_mcqww_test_randomization_'
output_path_ui_mcqww_client_group_random = output_common_dir + r'\UI\UI_client_mcqww_group_randomization_'
output_path_ui_mcqww_client_section_random = output_common_dir + r'\UI\UI_client_mcqww_section_randomization_'

output_path_ui_coding_client_test_random = output_common_dir + r'\UI\UI_client_coding_test_randomization_'
output_path_ui_coding_client_group_random = output_common_dir + r'\UI\UI_client_coding_group_randomization_'
output_path_ui_coding_client_section_random = output_common_dir + r'\UI\UI_client_coding_section_randomization_'

output_path_ui_mca_client_test_random = output_common_dir + r'\UI\UI_client_mca_test_randomization_'
output_path_ui_mca_client_group_random = output_common_dir + r'\UI\UI_client_mca_group_randomization_'
output_path_ui_mca_client_section_random = output_common_dir + r'\UI\UI_client_mca_section_randomization_'

output_path_ui_rtc_static = output_common_dir + r'\UI\rtc_static.xls'
output_path_ui_subjective_client_test_random = output_common_dir + r'\UI\UI_client_subjective_random_testlevel_'
output_path_ui_subjective_client_group_random = output_common_dir + r'\UI\UI_client_subjective_random_grouplevel_'
output_path_ui_subjective_client_section_random = output_common_dir + r'\UI\UI_client_subjective_random_sectionlevel_'
output_path_ui_marking_schema = output_common_dir + r'\UI\UI_Static_MCQ_Marking'
output_path_ui_rtc_marking_schema = output_common_dir + r'\UI\UI_Static_rtc_Marking'
output_path_ui_mcqww_marking_schema = output_common_dir + r'\UI\UI_Static_mcqww_Marking'
output_path_ui_psych_marking_schema = output_common_dir + r'\UI\UI_Static_psych_Marking'
output_path_ui_mca_marking_schema = output_common_dir + r'\UI\UI_Static_mca_Marking'
output_path_ui_fib_marking_schema = output_common_dir + r'\UI\UI_Static_fib_Marking'
output_path_ui_self_assessment = output_common_dir + r'\UI\UI_self_assessment'

# INFRA
output_path_infra_strict_domain = output_common_dir + r'\INFRA\API_infra_strict_domain'
output_path_adhoc_profile_api_validation = output_common_dir + r'\INFRA\API_adhoc_profile_api_validation'
