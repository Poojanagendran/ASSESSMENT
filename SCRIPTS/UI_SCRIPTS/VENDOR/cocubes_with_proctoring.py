import time

from SCRIPTS.COMMON.io_path import *
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.UI_COMMON.assessment_ui_common_v2 import *
from SCRIPTS.CRPO_COMMON.credentials import *
from SCRIPTS.UI_SCRIPTS.assessment_data_verification import *


class CocubesAutomation:

    def __init__(self):
        self.url = "https://qaassesscocubes.hirepro.in/hprotest/#/assess/login/eyJhbGlhcyI6ImF0In0="
        self.path = '/Users/senthil/Desktop/ASSESSMENT'
        write_excel_object.save_result(output_path_ui_cocubes)
        # 0th Row Header
        header = ['Cocubes']
        # 1 Row Header
        write_excel_object.write_headers_for_scripts(0, 0, header, write_excel_object.black_color_bold)
        header = ['Testcases', 'Status', 'Test ID', 'Candidate ID', 'Testuser ID',
                  'Cocubes Disclaimer', 'Cocubes Startest', 'Group1 Name', 'Next Group Status', 'Group2 Name',
                  'Next Group Status', 'Group3 Name', 'Next Group Status', 'Group4 Name', 'Submit test',
                  'Submission Confirmation', 'Group1 mark', 'Group2 mark', 'Group3 mark', 'Group4 mark',
                  'Report link', 'Third party status', 'Candidate proctoring status', 'golden image count',
                  'snapshots count', 'Recorded audio file size', 'Audio Duration', 'Recorded video file size',
                  'Video Duration', 'Expected audio file type', 'Actual audio file type',
                  'Expected video file type', 'Actual video file type', 'Audio S3 file', 'Video s3 file']
        write_excel_object.write_headers_for_scripts(1, 0, header, write_excel_object.black_color_bold)
        self.row_size = 2

    def cocubes_technical(self, login_id, password, tkn, tu_request):
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
                cc_disclaimer = assess_ui_common_obj.cocubes_disclaimer()
                cc_startest = assess_ui_common_obj.cocubes_start_test()
                group1 = assess_ui_common_obj.cocubes_group_names('click to attempt section 01')
                print(group1)
                question1 = assess_ui_common_obj.cocubes_answer_question('n_0')
                question2 = assess_ui_common_obj.cocubes_answer_question('n_1')
                question3 = assess_ui_common_obj.cocubes_answer_question('n_2')
                question4 = assess_ui_common_obj.cocubes_answer_question('n_3')
                question5 = assess_ui_common_obj.cocubes_answer_question('n_4')
                question6 = assess_ui_common_obj.cocubes_answer_question('n_5')
                question7 = assess_ui_common_obj.cocubes_answer_question('n_6')
                question8 = assess_ui_common_obj.cocubes_answer_question('n_7')
                question9 = assess_ui_common_obj.cocubes_answer_question('n_8')
                question10 = assess_ui_common_obj.cocubes_answer_question('n_9')
                question11 = assess_ui_common_obj.cocubes_answer_question('n_10')
                question12 = assess_ui_common_obj.cocubes_answer_question('n_11')
                question13 = assess_ui_common_obj.cocubes_answer_question('n_12')
                question14 = assess_ui_common_obj.cocubes_answer_question('n_13')
                question15 = assess_ui_common_obj.cocubes_answer_question('n_14')
                question16 = assess_ui_common_obj.cocubes_answer_question('n_15')
                question17 = assess_ui_common_obj.cocubes_answer_question('n_16')
                question18 = assess_ui_common_obj.cocubes_answer_question('n_17')
                question19 = assess_ui_common_obj.cocubes_answer_question('n_18')
                question20 = assess_ui_common_obj.cocubes_answer_question('n_19')
                next_group1 = assess_ui_common_obj.cocubes_next_group()
                group2 = assess_ui_common_obj.cocubes_group_names('click to attempt section 02')
                question21 = assess_ui_common_obj.cocubes_answer_question('n_20')
                question22 = assess_ui_common_obj.cocubes_answer_question('n_21')
                question23 = assess_ui_common_obj.cocubes_answer_question('n_22')
                question24 = assess_ui_common_obj.cocubes_answer_question('n_23')
                question25 = assess_ui_common_obj.cocubes_answer_question('n_24')
                question26 = assess_ui_common_obj.cocubes_answer_question('n_25')
                question27 = assess_ui_common_obj.cocubes_answer_question('n_26')
                question28 = assess_ui_common_obj.cocubes_answer_question('n_27')
                question29 = assess_ui_common_obj.cocubes_answer_question('n_28')
                question30 = assess_ui_common_obj.cocubes_answer_question('n_29')
                question31 = assess_ui_common_obj.cocubes_answer_question('n_30')
                question32 = assess_ui_common_obj.cocubes_answer_question('n_31')
                question33 = assess_ui_common_obj.cocubes_answer_question('n_32')
                question34 = assess_ui_common_obj.cocubes_answer_question('n_33')
                question35 = assess_ui_common_obj.cocubes_answer_question('n_34')
                question36 = assess_ui_common_obj.cocubes_answer_question('n_35')
                question37 = assess_ui_common_obj.cocubes_answer_question('n_36')
                question38 = assess_ui_common_obj.cocubes_answer_question('n_37')
                question39 = assess_ui_common_obj.cocubes_answer_question('n_38')
                question40 = assess_ui_common_obj.cocubes_answer_question('n_39')

                next_group2 = assess_ui_common_obj.cocubes_next_group()
                group3 = assess_ui_common_obj.cocubes_group_names('click to attempt section 03')
                question41 = assess_ui_common_obj.cocubes_answer_question('n_40')
                question42 = assess_ui_common_obj.cocubes_answer_question('n_41')
                question43 = assess_ui_common_obj.cocubes_answer_question('n_42')
                question44 = assess_ui_common_obj.cocubes_answer_question('n_43')
                question45 = assess_ui_common_obj.cocubes_answer_question('n_44')
                question46 = assess_ui_common_obj.cocubes_answer_question('n_45')
                question47 = assess_ui_common_obj.cocubes_answer_question('n_46')
                question48 = assess_ui_common_obj.cocubes_answer_question('n_47')
                question49 = assess_ui_common_obj.cocubes_answer_question('n_48')
                question50 = assess_ui_common_obj.cocubes_answer_question('n_49')
                question51 = assess_ui_common_obj.cocubes_answer_question('n_50')
                question52 = assess_ui_common_obj.cocubes_answer_question('n_51')
                question53 = assess_ui_common_obj.cocubes_answer_question('n_52')
                question54 = assess_ui_common_obj.cocubes_answer_question('n_53')
                question55 = assess_ui_common_obj.cocubes_answer_question('n_54')
                question56 = assess_ui_common_obj.cocubes_answer_question('n_55')
                question57 = assess_ui_common_obj.cocubes_answer_question('n_56')
                question58 = assess_ui_common_obj.cocubes_answer_question('n_57')
                question59 = assess_ui_common_obj.cocubes_answer_question('n_58')
                question60 = assess_ui_common_obj.cocubes_answer_question('n_59')
                next_group3 = assess_ui_common_obj.cocubes_next_group()
                group4 = assess_ui_common_obj.cocubes_group_names('click to attempt section 04')
                question61 = assess_ui_common_obj.cocubes_answer_question('n_60')
                question62 = assess_ui_common_obj.cocubes_answer_question('n_61')
                question63 = assess_ui_common_obj.cocubes_answer_question('n_62')
                question64 = assess_ui_common_obj.cocubes_answer_question('n_63')
                question65 = assess_ui_common_obj.cocubes_answer_question('n_64')
                question66 = assess_ui_common_obj.cocubes_answer_question('n_65')
                question67 = assess_ui_common_obj.cocubes_answer_question('n_66')
                question68 = assess_ui_common_obj.cocubes_answer_question('n_67')
                question69 = assess_ui_common_obj.cocubes_answer_question('n_68')
                question70 = assess_ui_common_obj.cocubes_answer_question('n_69')
                question71 = assess_ui_common_obj.cocubes_answer_question('n_70')
                question72 = assess_ui_common_obj.cocubes_answer_question('n_71')
                question73 = assess_ui_common_obj.cocubes_answer_question('n_72')
                question74 = assess_ui_common_obj.cocubes_answer_question('n_73')
                question75 = assess_ui_common_obj.cocubes_answer_question('n_74')
                question76 = assess_ui_common_obj.cocubes_answer_question('n_75')
                question77 = assess_ui_common_obj.cocubes_answer_question('n_76')
                question78 = assess_ui_common_obj.cocubes_answer_question('n_77')
                question79 = assess_ui_common_obj.cocubes_answer_question('n_78')
                question80 = assess_ui_common_obj.cocubes_answer_question('n_79')
                question81 = assess_ui_common_obj.cocubes_answer_question('n_80')
                question82 = assess_ui_common_obj.cocubes_answer_question('n_81')
                question83 = assess_ui_common_obj.cocubes_answer_question('n_82')
                question84 = assess_ui_common_obj.cocubes_answer_question('n_83')
                question85 = assess_ui_common_obj.cocubes_answer_question('n_84')
                question86 = assess_ui_common_obj.cocubes_answer_question('n_85')
                question87 = assess_ui_common_obj.cocubes_answer_question('n_86')
                question88 = assess_ui_common_obj.cocubes_answer_question('n_87')
                question89 = assess_ui_common_obj.cocubes_answer_question('n_88')
                question90 = assess_ui_common_obj.cocubes_answer_question('n_89')
                submit_test = assess_ui_common_obj.cocubes_submit_test()
                submit_test_confirmation = assess_ui_common_obj.cocubes_comfirm_submit_test()
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

                write_excel_object.compare_results_and_write_vertically('Cocubes Check', None, self.row_size, 0)
                write_excel_object.compare_results_and_write_vertically(test_id, None, self.row_size, 2)
                write_excel_object.compare_results_and_write_vertically(candidate_id, None, self.row_size, 3)
                write_excel_object.compare_results_and_write_vertically(test_userid, None, self.row_size, 4)
                write_excel_object.compare_results_and_write_vertically('Disclaimer Success', cc_disclaimer[0],
                                                                        self.row_size, 5, True)
                write_excel_object.compare_results_and_write_vertically('Start test Success', cc_startest[0],
                                                                        self.row_size, 6, True)
                vendor_g1 = '01. English Ability\n00 / 20 attempted'
                vendor_g2 = '02. Logical Reasoning\n00 / 20 attempted'
                vendor_g3 = '03. Numerical Ability\n00 / 20 attempted'
                vendor_g4 = '04. Technical\n00 / 30 attempted'
                write_excel_object.compare_results_and_write_vertically(vendor_g1, group1[0], self.row_size, 7,
                                                                        True)
                write_excel_object.compare_results_and_write_vertically('Next group success', next_group1[0],
                                                                        self.row_size, 8, True)
                write_excel_object.compare_results_and_write_vertically(vendor_g2, group2[0],
                                                                        self.row_size, 9, True)
                write_excel_object.compare_results_and_write_vertically('Next group success', next_group2[0],
                                                                        self.row_size, 10, True)
                write_excel_object.compare_results_and_write_vertically(vendor_g3, group3[0],
                                                                        self.row_size, 11, True)
                write_excel_object.compare_results_and_write_vertically('Next group success', next_group3[0],
                                                                        self.row_size, 12, True)
                write_excel_object.compare_results_and_write_vertically(vendor_g4, group4[0],
                                                                        self.row_size, 13, True)
                write_excel_object.compare_results_and_write_vertically('Submission Successful', submit_test[0],
                                                                        self.row_size, 14, True)
                write_excel_object.compare_results_and_write_vertically('Submission Confirmed',
                                                                        submit_test_confirmation[0],
                                                                        self.row_size, 15, True)
                write_excel_object.compare_results_and_write_vertically(None, group1_mark, self.row_size, 16)
                write_excel_object.compare_results_and_write_vertically(None, group2_mark, self.row_size, 17)
                write_excel_object.compare_results_and_write_vertically(None, group3_mark, self.row_size, 18)
                write_excel_object.compare_results_and_write_vertically(None, group4_mark, self.row_size, 19)

                write_excel_object.compare_results_and_write_vertically(None, report_link, self.row_size, 20)
                write_excel_object.compare_results_and_write_vertically(None, third_party_status, self.row_size, 21)
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
                                                                        self.row_size, 22, True)

                write_excel_object.compare_results_and_write_vertically(1, golden_image, self.row_size, 23, True)

                if snapshot_image >= 4:
                    write_excel_object.compare_results_and_write_vertically(None, snapshot_image, self.row_size, 24,
                                                                            True)
                else:
                    write_excel_object.compare_results_and_write_vertically(4, snapshot_image, self.row_size, 24,
                                                                            True)

                write_excel_object.compare_results_and_write_vertically(None, audio_file_size, self.row_size, 25, True)

                write_excel_object.compare_results_and_write_vertically(None, audio_duration, self.row_size, 26, True)

                write_excel_object.compare_results_and_write_vertically(None, video_file_size, self.row_size, 27, True)

                write_excel_object.compare_results_and_write_vertically(None, video_duration, self.row_size, 28, True)

                public_audio_url = audio_s3_file.split('?AWS')[0]
                audio_filetype = public_audio_url[-4:]
                public_video_url = video_s3_file.split('?AWS')[0]
                video_filetype = public_video_url[-4:]
                write_excel_object.compare_results_and_write_vertically('opus', audio_filetype, self.row_size, 29)
                write_excel_object.compare_results_and_write_vertically('webm', video_filetype, self.row_size, 31)
                write_excel_object.compare_results_and_write_vertically(None, audio_s3_file, self.row_size, 33, True)
                write_excel_object.compare_results_and_write_vertically(None, video_s3_file, self.row_size, 34, True)

        write_excel_object.compare_results_and_write_vertically(
            write_excel_object.current_status, None, self.row_size, 1)
        self.row_size = self.row_size + 1


qs = CocubesAutomation()
token = crpo_common_obj.login_to_crpo(cred_crpo_admin_at.get('user'), cred_crpo_admin_at.get('password'),
                                      cred_crpo_admin_at.get('tenant'))

#sprint_id = input('Enter Sprint ID')
sprint_id = str(datetime.datetime.now())
candidate_id = crpo_common_obj.create_candidate(token, sprint_id)
print(candidate_id)
test_id = 13965
event_id = 10639
jobrole_id = 30251
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
print(login_id)
print(password)

qs.cocubes_technical(login_id, password, token, tu_req_payload)
write_excel_object.write_overall_status(testcases_count=1)

