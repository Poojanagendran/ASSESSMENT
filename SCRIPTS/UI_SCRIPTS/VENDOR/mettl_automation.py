from SCRIPTS.COMMON.io_path import *
from SCRIPTS.COMMON.writeExcel import write_excel_object
from SCRIPTS.UI_COMMON.assessment_ui_common_v2 import *
from SCRIPTS.CRPO_COMMON.credentials import *
import time
from SCRIPTS.UI_SCRIPTS.assessment_data_verification import *


class MettlAutomation:

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
                  'Group6 mark', 'Report link']
        write_excel_object.write_headers_for_scripts(1, 0, header, write_excel_object.black_color_bold)

    def mettl_technical(self, login_id, password, tkn, tu_request):
        overall_color = write_excel_object.green_color
        browser = assess_ui_common_obj.initiate_browser(self.url, self.path)
        login_details = assess_ui_common_obj.ui_login_to_test(login_id, password)
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
                # third_party_status = tu_infos['data']['vendorDetails']['thirdPartyStatus']
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

                write_excel_object.ws.write(2, 0, 'Mettl Check', write_excel_object.green_color)

                write_excel_object.ws.write(2, 2, 'stand alone case', write_excel_object.green_color)
                write_excel_object.ws.write(2, 2, test_id, write_excel_object.green_color)
                write_excel_object.ws.write(2, 3, candidate_id, write_excel_object.green_color)
                write_excel_object.ws.write(2, 4, test_userid, write_excel_object.green_color)

                if mettl_start_test1[0] == 'Start test1 Success':
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 5, mettl_start_test1[0], color)

                if mettl_start_test2[0] == 'Start test2 Success':
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 6, mettl_start_test2[0], color)

                print(mettl_group1_name)
                if "1. English Ability" == mettl_group1_name[0]:
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 7, mettl_group1_name[0], color)

                if next_group1[0] == 'Next group success':
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 8, next_group1[0], color)

                if '2. Analytical Reasoning' == mettl_group2_name[0]:
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 9, mettl_group2_name[0], color)

                if next_group2[0] == 'Next group success':
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 10, next_group2[0], color)

                if '3. Numerical Ability' == mettl_group3_name[0]:
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 11, mettl_group3_name[0], color)

                if next_group3[0] == 'Next group success':
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 12, next_group3[0], color)

                if '4. Common Applications and MS office' == mettl_group4_name[0]:
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 13, mettl_group4_name[0], color)

                if next_group4[0] == 'Next group success':
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 14, next_group4[0], color)

                if '5. Pseudo Code' == mettl_group5_name[0]:
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 15, mettl_group5_name[0], color)

                if next_group5[0] == 'Next group success':
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 16, next_group5[0], color)

                if '6. Networking Security and Cloud' == mettl_group6_name[0]:
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 17, mettl_group6_name[0], color)

                if final_submit[0] == 'Mettl Final Submit success':
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 18, final_submit[0], color)

                if final_submit_confirmation[0] == 'Mettl Final Submit Confirmation success':
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 19, final_submit_confirmation[0], color)

                if group1_mark is not None:
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 20, group1_mark, color)

                if group2_mark is not None:
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 21, group2_mark, color)

                if group3_mark is not None:
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 22, group3_mark, color)

                if group4_mark is not None:
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 23, group4_mark, color)

                if group5_mark is not None:
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 24, group5_mark, color)

                if group6_mark is not None:
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 25, group6_mark, color)

                if report_link:
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 26, report_link, color)

        write_excel_object.ws.write(2, 1, overall_status, overall_color)
        write_excel_object.write_excel.close()
        browser.quit()

qs = MettlAutomation()
token = crpo_common_obj.login_to_crpo(cred_crpo_admin.get('user'), cred_crpo_admin.get('password'),
                                      cred_crpo_admin.get('tenant'))

sprint_id = input('Enter Sprint ID')
candidate_id = crpo_common_obj.create_candidate(token, sprint_id)
print(candidate_id)
test_id = 14675
event_id = 11105
jobrole_id = 30337
tag_candidate = crpo_common_obj.tag_candidate_to_test(token, candidate_id, test_id, event_id, jobrole_id)
time.sleep(10)
test_userid = crpo_common_obj.get_all_test_user(token, candidate_id)
print(test_userid)
# test_userid = 2548311
tu_req_payload = {"testUserId": test_userid,
                  "requiredFlags": {"fileContentRequired": False, "isQuestionWise": True, "questionTypes": [16, 8],
                                    "isGroupSectionWiseMarks": True, "isVendorDetails": True, "isCodingSummary": False}}
tu_cred = crpo_common_obj.test_user_credentials(token, test_userid)
login_id = tu_cred['data']['testUserCredential']['loginId']
password = tu_cred['data']['testUserCredential']['password']
# login_id = "Automation146751461805"
# password = "2PYU~~"
print(login_id)
print(password)
qs.mettl_technical(login_id, password, token, tu_req_payload)
