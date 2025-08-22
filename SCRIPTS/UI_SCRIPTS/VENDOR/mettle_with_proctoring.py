import datetime

from SCRIPTS.COMMON.io_path import *
# from SCRIPTS.COMMON.writeExcel import write_excel_object
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.UI_COMMON.assessment_ui_common_v2 import *
from SCRIPTS.CRPO_COMMON.credentials import *
import time
from SCRIPTS.UI_SCRIPTS.assessment_data_verification import *


class MettleAutomation:

    def __init__(self):
        self.url = "https://amsin.hirepro.in/assessment/#/assess/login/eyJhbGlhcyI6ImF1dG9tYXRpb24ifQ=="
        self.path = chrome_driver_path
        write_excel_object.save_result(output_path_ui_mettl)
        # 0th Row Header
        header = ['Mettl']
        # 1 Row Header
        write_excel_object.write_headers_for_scripts(0, 0, header, write_excel_object.black_color_bold)
        header = ['Testcases', 'Status', 'Test ID', 'Candidate ID', 'Testuser ID',
                  'start test button1 ', 'start test button2', 'Group1 Name', 'Next Group Status', 'Group2 Name',
                  'Next Group Status', 'Group3 Name', 'Next Group Status', 'Group4 Name', 'Next Group Status',
                  'Group5 Name', 'Next Group Status', 'Group6 Name', 'Submit test',
                  'Submission Confirmation', 'Group1 mark', 'Group2 mark', 'Group3 mark', 'Group4 mark', 'Group5 mark',
                  'Group6 mark', 'Report link', 'Candidate proctoring status', 'golden image count',
                  'snapshots count', 'Recorded audio file size', 'Audio Duration', 'Recorded video file size',
                  'Video Duration', 'Expected audio file type', 'Actual audio file type',
                  'Expected video file type', 'Actual video file type', 'Audio S3 file', 'Video s3 file']
        write_excel_object.write_headers_for_scripts(1, 0, header, write_excel_object.black_color_bold)
        self.row_size = 2

    def mettl_technical(self, login_id, password, tkn, tu_request):
        testuser_id = tu_request['testUserId']
        overall_color = write_excel_object.green_color
        browser = assess_ui_common_obj.initiate_browser(self.url, self.path)
        login_details = assess_ui_common_obj.ui_login_to_test(login_id, password)
        about_online_proctoring = assess_ui_common_obj.about_online_proctoring()
        assessment_terms_and_conditions = assess_ui_common_obj.assessment_terms_and_conditions()
        selfie = assess_ui_common_obj.selfie()
        time.sleep(3)
        overall_status = 'pass'
        if login_details == 'SUCCESS':
            i_agreed = assess_ui_common_obj.select_i_agree()
            if i_agreed:
                start_test_status = assess_ui_common_obj.start_test_button_status()
                hirepro_start_test = assess_ui_common_obj.start_test()
                mettl_start_test1 = assess_ui_common_obj.mettl_start_test()
                mettl_start_test2 = assess_ui_common_obj.mettl_start_test2()
                mettl_terms_and_conditions = assess_ui_common_obj.mettl_terms_and_conditions()
                mettl_start_test3 = assess_ui_common_obj.mettl_start_test3()
                mettl_group1_name = assess_ui_common_obj.mettl_group_names()
                answer1 = assess_ui_common_obj.mettl_answer_question()
                next_group1 = assess_ui_common_obj.mettl_next_section()
                mettl_group2_name = assess_ui_common_obj.mettl_group_names()
                answer2 = assess_ui_common_obj.mettl_answer_question()
                next_group2 = assess_ui_common_obj.mettl_next_section()
                mettl_group3_name = assess_ui_common_obj.mettl_group_names()
                answer3 = assess_ui_common_obj.mettl_answer_question()
                next_group3 = assess_ui_common_obj.mettl_next_section()
                mettl_group4_name = assess_ui_common_obj.mettl_group_names()
                answer4 = assess_ui_common_obj.mettl_answer_question()
                next_group4 = assess_ui_common_obj.mettl_next_section()
                mettl_group5_name = assess_ui_common_obj.mettl_group_names()
                answer5 = assess_ui_common_obj.mettl_answer_question()
                next_group5 = assess_ui_common_obj.mettl_next_section()
                mettl_group6_name = assess_ui_common_obj.mettl_group_names()
                answer6 = assess_ui_common_obj.mettl_answer_question()
                final_submit = assess_ui_common_obj.mettl_finish_test()
                final_submit_confirmation = assess_ui_common_obj.mettl_finish_test_confirmation()
                time.sleep(180)
                tu_infos = crpo_common_obj.get_test_user_infos(tkn, tu_request)
                report_link = tu_infos['data']['vendorDetails']['reportLink']
                third_party_status = tu_infos['data']['vendorDetails']['thirdPartyStatus']
                data = tu_infos['data']['groupAndSectionWiseMarks']
                # group1_name = data[0]['name']
                group1_mark = int(data[0]['obtainedMarks'])
                # group2_name = data[1]['name']
                group2_mark = int(data[1]['obtainedMarks'])
                # group3_name = data[2]['name']
                group3_mark = int(data[2]['obtainedMarks'])
                # group4_name = data[3]['name']
                group4_mark = int(data[3]['obtainedMarks'])
                # group5_name = data[4]['name']
                group5_mark = int(data[4]['obtainedMarks'])
                # group6_name = data[5]['name']
                group6_mark = int(data[5]['obtainedMarks'])
                print(group1_mark)
                print(group2_mark)
                print(group3_mark)
                print(group4_mark)
                print(group5_mark)
                print(group6_mark)
                write_excel_object.compare_results_and_write_vertically('Mettl Check', None, self.row_size, 0)
                # write_excel_object.compare_results_and_write_vertically('stand alone case', None,self.row_size, 2)
                write_excel_object.compare_results_and_write_vertically(test_id, None, self.row_size, 2)
                write_excel_object.compare_results_and_write_vertically(candidate_id, None, self.row_size, 3)
                write_excel_object.compare_results_and_write_vertically(test_userid, None, self.row_size, 4)
                write_excel_object.compare_results_and_write_vertically('Start test1 Success', mettl_start_test1[0],
                                                                        self.row_size, 5, True)
                write_excel_object.compare_results_and_write_vertically('Start test2 Success', mettl_start_test2[0],
                                                                        self.row_size, 6, True)
                vendor_g1 = '1. English Ability'
                vendor_g2 = '2. Analytical Reasoning'
                vendor_g3 = '3. Numerical Ability'
                vendor_g4 = '4. Common Applications and MS office'
                vendor_g5 = '5. Pseudo Code'
                vendor_g6 = '6. Networking Security and Cloud'
                write_excel_object.compare_results_and_write_vertically(vendor_g1, mettl_group1_name[0], self.row_size,
                                                                        7, True)
                write_excel_object.compare_results_and_write_vertically('Next group success', next_group1[0],
                                                                        self.row_size, 8, True)
                write_excel_object.compare_results_and_write_vertically(vendor_g2, mettl_group2_name[0],
                                                                        self.row_size, 9, True)
                write_excel_object.compare_results_and_write_vertically('Next group success', next_group2[0],
                                                                        self.row_size, 10, True)
                write_excel_object.compare_results_and_write_vertically(vendor_g3, mettl_group3_name[0],
                                                                        self.row_size, 11, True)
                write_excel_object.compare_results_and_write_vertically('Next group success', next_group3[0],
                                                                        self.row_size, 12, True)
                write_excel_object.compare_results_and_write_vertically(vendor_g4, mettl_group4_name[0],
                                                                        self.row_size, 13, True)
                write_excel_object.compare_results_and_write_vertically('Next group success', next_group4[0],
                                                                        self.row_size, 14, True)
                write_excel_object.compare_results_and_write_vertically(vendor_g5, mettl_group5_name[0],
                                                                        self.row_size, 15, True)
                write_excel_object.compare_results_and_write_vertically('Next group success', next_group5[0],
                                                                        self.row_size, 16, True)
                write_excel_object.compare_results_and_write_vertically(vendor_g6, mettl_group6_name[0],
                                                                        self.row_size, 17, True)
                write_excel_object.compare_results_and_write_vertically('Mettl Final Submit success', final_submit[0],
                                                                        self.row_size, 18, True)
                write_excel_object.compare_results_and_write_vertically('Mettl Final Submit Confirmation success',
                                                                        final_submit_confirmation[0],
                                                                        self.row_size, 19, True)

                write_excel_object.compare_results_and_write_vertically(None, group1_mark, self.row_size, 20,
                                                                        is_act_zero_considered=True)
                write_excel_object.compare_results_and_write_vertically(None, group2_mark, self.row_size, 21,
                                                                        is_act_zero_considered=True)
                write_excel_object.compare_results_and_write_vertically(None, group3_mark, self.row_size, 22,
                                                                        is_act_zero_considered=True)
                write_excel_object.compare_results_and_write_vertically(None, group4_mark, self.row_size, 23,
                                                                        is_act_zero_considered=True)
                write_excel_object.compare_results_and_write_vertically(None, group5_mark, self.row_size, 24,
                                                                        is_act_zero_considered=True)
                write_excel_object.compare_results_and_write_vertically(None, group6_mark, self.row_size, 25,
                                                                        is_act_zero_considered=True)
                write_excel_object.compare_results_and_write_vertically(None, report_link, self.row_size, 26)
                # write_excel_object.compare_results_and_write_vertically(None, third_party_status, self.row_size, 27)
                get_tu_proc_screen_data_payload = {"tuId": testuser_id}
                proctor_results = crpo_common_obj.get_tu_proc_screen_data(tkn, get_tu_proc_screen_data_payload)
                candidate_proctoring_status = proctor_results['data']['testUserDetails']['proctorStatus']
                recorded_urls = proctor_results['data']['getRecordedUrls']
                proctored_images = proctor_results['data']['getTestUserProcImg']
                golden_image = 0
                snapshot_image = 0
                for images in proctored_images:
                    if images.get('GoldenImage'):
                        golden_image = golden_image + 1
                    else:
                        snapshot_image = snapshot_image + 1
                audio_json = recorded_urls[0]['recordedVideo'][0]['recordedMedia']['audio']
                audio_file_size = audio_json.get('size')
                audio_s3_file = audio_json.get('s3Url')
                audio_duration = audio_json.get('duration')
                video_json = recorded_urls[0]['recordedVideo'][0]['recordedMedia']['video']
                video_file_size = video_json.get('size')
                video_s3_file = video_json.get('s3Url')
                video_duration = video_json.get('duration')
                write_excel_object.compare_results_and_write_vertically('Proctored', candidate_proctoring_status,
                                                                        self.row_size, 27, True)

                write_excel_object.compare_results_and_write_vertically(1, golden_image, self.row_size, 28, True)

                if snapshot_image >= 4:
                    write_excel_object.compare_results_and_write_vertically(None, snapshot_image, self.row_size, 29,
                                                                            True)
                else:
                    write_excel_object.compare_results_and_write_vertically(4, snapshot_image, self.row_size, 29, True)
                write_excel_object.compare_results_and_write_vertically(None, audio_file_size, self.row_size, 30, True)
                write_excel_object.compare_results_and_write_vertically(None, audio_duration, self.row_size, 31, True)
                write_excel_object.compare_results_and_write_vertically(None, video_file_size, self.row_size, 32, True)
                write_excel_object.compare_results_and_write_vertically(None, video_duration, self.row_size, 33, True)
                public_audio_url = audio_s3_file.split('?AWS')[0]
                audio_filetype = public_audio_url[-4:]
                public_video_url = video_s3_file.split('?AWS')[0]
                video_filetype = public_video_url[-4:]
                write_excel_object.compare_results_and_write_vertically('opus', audio_filetype, self.row_size, 34)
                write_excel_object.compare_results_and_write_vertically('webm', video_filetype, self.row_size, 36)
                write_excel_object.compare_results_and_write_vertically(None, audio_s3_file, self.row_size, 38,
                                                                        True)
                write_excel_object.compare_results_and_write_vertically(None, video_s3_file, self.row_size, 39,
                                                                        True)

        write_excel_object.compare_results_and_write_vertically(
            write_excel_object.current_status, None, self.row_size, 1)
        self.row_size = self.row_size + 1
        browser.quit()


qs = MettleAutomation()
token = crpo_common_obj.login_to_crpo(cred_crpo_admin.get('user'), cred_crpo_admin.get('password'),
                                      cred_crpo_admin.get('tenant'))
sprint_id = str(datetime.datetime.now())
candidate_id = crpo_common_obj.create_candidate(token, sprint_id)
print(candidate_id)
test_id = 20882
event_id = 11105
jobrole_id = 30337
tag_candidate = crpo_common_obj.tag_candidate_to_test(token, candidate_id, test_id, event_id, jobrole_id)
time.sleep(20)
test_userid = crpo_common_obj.get_all_test_user(token, candidate_id)
print(test_userid)
tu_req_payload = {"testUserId": test_userid,
                  "requiredFlags": {"fileContentRequired": False, "isQuestionWise": True, "questionTypes": [16, 8],
                                    "isGroupSectionWiseMarks": True, "isVendorDetails": True, "isCodingSummary": False}}
tu_cred = crpo_common_obj.test_user_credentials(token, test_userid)
login_id = tu_cred['data']['testUserCredential']['loginId']
password = tu_cred['data']['testUserCredential']['password']
# print(login_id)
# print(password)
qs.mettl_technical(login_id, password, token, tu_req_payload)
write_excel_object.write_overall_status(testcases_count=1)
