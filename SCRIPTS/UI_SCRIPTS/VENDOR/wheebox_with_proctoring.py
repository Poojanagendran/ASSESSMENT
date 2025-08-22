from SCRIPTS.COMMON.io_path import *
#from SCRIPTS.COMMON.writeExcel import write_excel_object
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.UI_COMMON.assessment_ui_common_v2 import *
from SCRIPTS.CRPO_COMMON.credentials import *
import time
from SCRIPTS.UI_SCRIPTS.assessment_data_verification import *


class WheeboxAutomation:

    def __init__(self):
        self.url = "https://amsin.hirepro.in/assessment/#/assess/login/eyJhbGlhcyI6ImF1dG9tYXRpb24ifQ=="
        self.path = chrome_driver_path
        write_excel_object.save_result(output_path_ui_wheebox)
        # 0th Row Header
        header = ['Wheebox']
        # 1 Row Header
        write_excel_object.write_headers_for_scripts(0, 0, header, write_excel_object.black_color_bold)
        header = ['Testcases', 'Status', 'Test ID', 'Candidate ID', 'Testuser ID',
                  'I agree', 'Proceed to Wheebox test', 'auto question movement', 'End test', 'End test confirmation',
                  'Group1', 'Group2', 'Group3', 'Group4', 'Group1 mark', 'Group2 mark', 'Group3 mark', 'Group4 mark',
                  'Report link','Candidate proctoring status', 'golden image count',
                  'snapshots count', 'Recorded audio file size', 'Audio Duration', 'Recorded video file size',
                  'Video Duration', 'Expected audio file type', 'Actual audio file type',
                  'Expected video file type', 'Actual video file type', 'Audio S3 file', 'Video s3 file']
        write_excel_object.write_headers_for_scripts(1, 0, header, write_excel_object.black_color_bold)
        self.row_size = 2
    def wheebox_technical(self, login_id, password, tkn, tu_request):
        testuser_id = tu_request['testUserId']
        overall_color = write_excel_object.green_color
        browser = assess_ui_common_obj.initiate_browser(self.url, self.path)
        login_details = assess_ui_common_obj.ui_login_to_test(login_id, password)
        # self.browser.get_screenshot_as_file(self.common_path + "\\1_t1_afterlogin.png")
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
                wb_agreement = assess_ui_common_obj.wheebox_starttest_checkbox()
                wb_proceed_test = assess_ui_common_obj.wheebox_proceed_test()
                wb_auto_next_qn = assess_ui_common_obj.wheebox_auto_next_qn()
                wb_click_q1 = assess_ui_common_obj.wheebox_q1_ans()
                for question_count in range(0, 90):
                    answer_qn = assess_ui_common_obj.wheebox_answer_qn()
                    print(question_count)
                time.sleep(10)
                wb_submit_test = assess_ui_common_obj.wheebox_submit_test()
                wb_confirm_submit = assess_ui_common_obj.wheebox_confirm_submit()
                time.sleep(180)
                tu_infos = crpo_common_obj.get_test_user_infos(tkn, tu_request)
                report_link = tu_infos['data']['vendorDetails']['reportLink']
                #third_party_status = tu_infos['data']['vendorDetails']['thirdPartyStatus']
                data = tu_infos['data']['groupAndSectionWiseMarks']
                group1_name = data[0]['name']
                group1_mark = int(data[0]['obtainedMarks'])
                group2_name = data[1]['name']
                group2_mark = int(data[1]['obtainedMarks'])
                group3_name = data[2]['name']
                group3_mark = int(data[2]['obtainedMarks'])
                group4_name = data[3]['name']
                group4_mark = int(data[3]['obtainedMarks'])
                write_excel_object.compare_results_and_write_vertically('Wheebox Check', None, self.row_size, 0)
                write_excel_object.compare_results_and_write_vertically('single test', None,self.row_size, 2)
                write_excel_object.compare_results_and_write_vertically(test_id, None, self.row_size, 3)
                write_excel_object.compare_results_and_write_vertically(candidate_id, None, self.row_size, 4)
                write_excel_object.compare_results_and_write_vertically(test_userid, None, self.row_size, 5)
                write_excel_object.compare_results_and_write_vertically('Agreed', wb_agreement[0], self.row_size, 6,True)
                write_excel_object.compare_results_and_write_vertically('Success', wb_proceed_test[0], self.row_size, 7,True)
                write_excel_object.compare_results_and_write_vertically('Success', wb_auto_next_qn[0], self.row_size, 8,True)
                write_excel_object.compare_results_and_write_vertically('submitted', wb_submit_test[0], self.row_size, 9,
                                                                        True)
                write_excel_object.compare_results_and_write_vertically('submitted', wb_confirm_submit[0], self.row_size, 10,True)

                vendor_g1 = '1. Logical Reasoning'
                vendor_g2 = '2. Numerical Ability'
                vendor_g3 = '3. English Ability'
                vendor_g4 = '4. Technical'

                write_excel_object.compare_results_and_write_vertically(vendor_g1, group1_name, self.row_size,11, True)
                write_excel_object.compare_results_and_write_vertically(vendor_g2, group2_name, self.row_size,12, True)
                write_excel_object.compare_results_and_write_vertically(vendor_g3, group3_name, self.row_size,13, True)
                write_excel_object.compare_results_and_write_vertically(vendor_g4, group4_name, self.row_size,14, True)
                write_excel_object.compare_results_and_write_vertically(None, group1_mark, self.row_size, 15, True)
                write_excel_object.compare_results_and_write_vertically(None, group2_mark, self.row_size, 16, True)
                write_excel_object.compare_results_and_write_vertically(None, group3_mark, self.row_size, 17, True)
                write_excel_object.compare_results_and_write_vertically(None, group4_mark, self.row_size, 18, True)
                write_excel_object.compare_results_and_write_vertically(None, report_link, self.row_size, 19)
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
                                                                        self.row_size, 20, True)

                write_excel_object.compare_results_and_write_vertically(1, golden_image, self.row_size, 21, True)

                if snapshot_image >= 4:
                    write_excel_object.compare_results_and_write_vertically(None, snapshot_image, self.row_size, 22,
                                                                            True)
                else:
                    write_excel_object.compare_results_and_write_vertically(4, snapshot_image, self.row_size, 22, True)
                write_excel_object.compare_results_and_write_vertically(None, audio_file_size, self.row_size, 23, True)
                write_excel_object.compare_results_and_write_vertically(None, audio_duration, self.row_size, 24, True)
                write_excel_object.compare_results_and_write_vertically(None, video_file_size, self.row_size, 25, True)
                write_excel_object.compare_results_and_write_vertically(None, video_duration, self.row_size, 26, True)
                public_audio_url = audio_s3_file.split('?AWS')[0]
                audio_filetype = public_audio_url[-4:]
                public_video_url = video_s3_file.split('?AWS')[0]
                video_filetype = public_video_url[-4:]
                write_excel_object.compare_results_and_write_vertically('opus', audio_filetype, self.row_size, 27)
                write_excel_object.compare_results_and_write_vertically('webm', video_filetype, self.row_size, 29)
                write_excel_object.compare_results_and_write_vertically(None, audio_s3_file, self.row_size, 30,
                                                                        True)
                write_excel_object.compare_results_and_write_vertically(None, video_s3_file, self.row_size, 31,
                                                                        True)
        write_excel_object.compare_results_and_write_vertically(
            write_excel_object.current_status, None, self.row_size, 1)
        self.row_size = self.row_size + 1
        browser.quit()

qs = WheeboxAutomation()
token = crpo_common_obj.login_to_crpo(cred_crpo_admin.get('user'), cred_crpo_admin.get('password'),
                                      cred_crpo_admin.get('tenant'))
#sprint_id = input('Enter Sprint ID')
sprint_id = str(datetime.datetime.now())
candidate_id = crpo_common_obj.create_candidate(token, sprint_id)
print(candidate_id)
test_id = 21014
event_id = 11105
jobrole_id = 30337
tag_candidate = crpo_common_obj.tag_candidate_to_test(token, candidate_id, test_id, event_id, jobrole_id)
test_userid = crpo_common_obj.get_all_test_user(token, candidate_id)
# test_userid = 1329566
print(test_userid)
tu_req_payload = {"testUserId": test_userid,
                  "requiredFlags": {"fileContentRequired": False, "isQuestionWise": True, "questionTypes": [16, 8],
                                    "isGroupSectionWiseMarks": True, "isVendorDetails": True, "isCodingSummary": False}}
tu_cred = crpo_common_obj.test_user_credentials(token, test_userid)
login_id = tu_cred['data']['testUserCredential']['loginId']
password = tu_cred['data']['testUserCredential']['password']
print(login_id)
print(password)
qs.wheebox_technical(login_id, password, token, tu_req_payload)
