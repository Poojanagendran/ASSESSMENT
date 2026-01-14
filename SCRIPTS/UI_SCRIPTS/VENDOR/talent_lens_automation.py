from SCRIPTS.COMMON.io_path import *
from SCRIPTS.COMMON.writeExcel import write_excel_object
from SCRIPTS.UI_COMMON.assessment_ui_common_v2 import *
from SCRIPTS.CRPO_COMMON.credentials import *
import time
from SCRIPTS.UI_SCRIPTS.assessment_data_verification import *


class TalentLensAutomation:

    def __init__(self):
        self.url = "https://talentlensstg.hirepro.in/assessment/#/assess/login/eyJhbGlhcyI6ImF0In0="
        self.path = r"/chromedriver.exe"
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
        browser = assess_ui_common_obj.initiate_browser(self.url)
        login_details = assess_ui_common_obj.ui_login_to_test(login_id, password)
        # self.browser.get_screenshot_as_file(self.common_path + "\\1_t1_afterlogin.png")
        overall_status = 'pass'
        if login_details == 'SUCCESS':
            i_agreed = assess_ui_common_obj.select_i_agree()
            if i_agreed:
                start_test_status = assess_ui_common_obj.start_test_button_status()
                hirepro_start_test = assess_ui_common_obj.start_test()
                tl_fill_start_page_details = assess_ui_common_obj.tl_start_test()
                # tl_fill_copyright = assess_ui_common_obj.tl_copyright_page()
                tl_fill_copyright = assess_ui_common_obj.tl_copyright_page()
                tl_instruction1 = assess_ui_common_obj.tl_instructions_page1()
                tl_instruction1 = assess_ui_common_obj.tl_instructions_page2()
                tl_direction = assess_ui_common_obj.tl_test_directions1()
                # mettl_start_test1 = assess_ui_common_obj.mettl_start_test()
                # mettl_start_test2 = assess_ui_common_obj.mettl_start_test2()
                # mettl_group_names = assess_ui_common_obj.mettl_group_names()
                # answer1 = assess_ui_common_obj.mettl_answer_question()
                # next_group1 = assess_ui_common_obj.mettl_next_section()
                # answer2 = assess_ui_common_obj.mettl_answer_question()
                # next_group2 = assess_ui_common_obj.mettl_next_section()
                # answer3 = assess_ui_common_obj.mettl_answer_question()
                # next_group3 = assess_ui_common_obj.mettl_next_section()
                # answer4 = assess_ui_common_obj.mettl_answer_question()
                # next_group4 = assess_ui_common_obj.mettl_next_section()
                # answer5 = assess_ui_common_obj.mettl_answer_question()
                # next_group5 = assess_ui_common_obj.mettl_next_section()
                # answer6 = assess_ui_common_obj.mettl_answer_question()
                # final_submit = assess_ui_common_obj.mettl_finish_test()
                # final_submit_confirmation = assess_ui_common_obj.mettl_finish_test_confirmation()
                # print(mettl_group_names)
                # group_names = mettl_group_names[0].split('\n')
                # mettl_group1_name = group_names[0]
                # mettl_group2_name = group_names[1]
                # mettl_group3_name = group_names[2]
                # mettl_group4_name = group_names[3]
                # mettl_group5_name = group_names[4]
                # mettl_group6_name = group_names[5]
                #
                # time.sleep(180)
                # tu_infos = crpo_common_obj.get_test_user_infos(tkn, tu_request)
                # report_link = tu_infos['data']['vendorDetails']['reportLink']
                # # third_party_status = tu_infos['data']['vendorDetails']['thirdPartyStatus']
                # data = tu_infos['data']['groupAndSectionWiseMarks']
                # # group1_name = data[0]['name']
                # group1_mark = int(data[0]['obtainedMarks'])
                # # group2_name = data[1]['name']
                # group2_mark = int(data[1]['obtainedMarks'])
                # # group3_name = data[2]['name']
                # group3_mark = int(data[2]['obtainedMarks'])
                # # group4_name = data[3]['name']
                # group4_mark = int(data[3]['obtainedMarks'])
                # # group5_name = data[4]['name']
                # group5_mark = int(data[4]['obtainedMarks'])
                # # group6_name = data[5]['name']
                # group6_mark = int(data[5]['obtainedMarks'])
                # print(group1_mark)
                # print(group2_mark)
                # print(group3_mark)
                # print(group4_mark)
                # print(group5_mark)
                # print(group6_mark)

        #         write_excel_object.ws.write(2, 0, 'Mettl Check', write_excel_object.green_color)
        #
        #         write_excel_object.ws.write(2, 2, 'stand alone case', write_excel_object.green_color)
        #         write_excel_object.ws.write(2, 2, test_id, write_excel_object.green_color)
        #         write_excel_object.ws.write(2, 3, candidate_id, write_excel_object.green_color)
        #         write_excel_object.ws.write(2, 4, test_userid, write_excel_object.green_color)
        #
        #         if mettl_start_test1[0] == 'Start test1 Success':
        #             color = write_excel_object.green_color
        #
        #         else:
        #             color = write_excel_object.red_color
        #             overall_color = write_excel_object.red_color
        #             overall_status = 'Fail'
        #         write_excel_object.ws.write(2, 5, mettl_start_test1[0], color)
        #
        #         if mettl_start_test2[0] == 'Start test2 Success':
        #             color = write_excel_object.green_color
        #
        #         else:
        #             color = write_excel_object.red_color
        #             overall_color = write_excel_object.red_color
        #             overall_status = 'Fail'
        #         write_excel_object.ws.write(2, 6, mettl_start_test2[0], color)
        #
        #         if "English Ability" in mettl_group1_name:
        #             color = write_excel_object.green_color
        #
        #         else:
        #             color = write_excel_object.red_color
        #             overall_color = write_excel_object.red_color
        #             overall_status = 'Fail'
        #         write_excel_object.ws.write(2, 7, mettl_group1_name, color)
        #
        #         if next_group1[0] == 'Next group success':
        #             color = write_excel_object.green_color
        #
        #         else:
        #             color = write_excel_object.red_color
        #             overall_color = write_excel_object.red_color
        #             overall_status = 'Fail'
        #         write_excel_object.ws.write(2, 8, next_group1[0], color)
        #
        #         if 'Analytical Reasoning' in mettl_group2_name:
        #             color = write_excel_object.green_color
        #
        #         else:
        #             color = write_excel_object.red_color
        #             overall_color = write_excel_object.red_color
        #             overall_status = 'Fail'
        #         write_excel_object.ws.write(2, 9, mettl_group2_name, color)
        #
        #         if next_group2[0] == 'Next group success':
        #             color = write_excel_object.green_color
        #
        #         else:
        #             color = write_excel_object.red_color
        #             overall_color = write_excel_object.red_color
        #             overall_status = 'Fail'
        #         write_excel_object.ws.write(2, 10, next_group2[0], color)
        #
        #         if 'Numerical Ability' in mettl_group3_name:
        #             color = write_excel_object.green_color
        #
        #         else:
        #             color = write_excel_object.red_color
        #             overall_color = write_excel_object.red_color
        #             overall_status = 'Fail'
        #         write_excel_object.ws.write(2, 11, mettl_group3_name, color)
        #
        #         if next_group3[0] == 'Next group success':
        #             color = write_excel_object.green_color
        #
        #         else:
        #             color = write_excel_object.red_color
        #             overall_color = write_excel_object.red_color
        #             overall_status = 'Fail'
        #         write_excel_object.ws.write(2, 12, next_group3[0], color)
        #
        #         if 'Common Applications and MS office' in mettl_group4_name:
        #             color = write_excel_object.green_color
        #
        #         else:
        #             color = write_excel_object.red_color
        #             overall_color = write_excel_object.red_color
        #             overall_status = 'Fail'
        #         write_excel_object.ws.write(2, 13, mettl_group4_name, color)
        #
        #         if next_group4[0] == 'Next group success':
        #             color = write_excel_object.green_color
        #
        #         else:
        #             color = write_excel_object.red_color
        #             overall_color = write_excel_object.red_color
        #             overall_status = 'Fail'
        #         write_excel_object.ws.write(2, 14, next_group4[0], color)
        #
        #         if 'Pseudo Code' in mettl_group5_name:
        #             color = write_excel_object.green_color
        #
        #         else:
        #             color = write_excel_object.red_color
        #             overall_color = write_excel_object.red_color
        #             overall_status = 'Fail'
        #         write_excel_object.ws.write(2, 15, mettl_group5_name, color)
        #
        #         if next_group5[0] == 'Next group success':
        #             color = write_excel_object.green_color
        #
        #         else:
        #             color = write_excel_object.red_color
        #             overall_color = write_excel_object.red_color
        #             overall_status = 'Fail'
        #         write_excel_object.ws.write(2, 16, next_group5[0], color)
        #
        #         if 'Networking Security and Cloud' in mettl_group6_name:
        #             color = write_excel_object.green_color
        #
        #         else:
        #             color = write_excel_object.red_color
        #             overall_color = write_excel_object.red_color
        #             overall_status = 'Fail'
        #         write_excel_object.ws.write(2, 17, mettl_group6_name, color)
        #
        #         if final_submit[0] == 'Mettl Final Submit success':
        #             color = write_excel_object.green_color
        #
        #         else:
        #             color = write_excel_object.red_color
        #             overall_color = write_excel_object.red_color
        #             overall_status = 'Fail'
        #         write_excel_object.ws.write(2, 18, final_submit[0], color)
        #
        #         if final_submit_confirmation[0] == 'Mettl Final Submit Confirmation success':
        #             color = write_excel_object.green_color
        #
        #         else:
        #             color = write_excel_object.red_color
        #             overall_color = write_excel_object.red_color
        #             overall_status = 'Fail'
        #         write_excel_object.ws.write(2, 19, final_submit_confirmation[0], color)
        #
        #         if group1_mark is not None:
        #             color = write_excel_object.green_color
        #
        #         else:
        #             color = write_excel_object.red_color
        #             overall_color = write_excel_object.red_color
        #             overall_status = 'Fail'
        #         write_excel_object.ws.write(2, 20, group1_mark, color)
        #
        #         if group2_mark is not None:
        #             color = write_excel_object.green_color
        #
        #         else:
        #             color = write_excel_object.red_color
        #             overall_color = write_excel_object.red_color
        #             overall_status = 'Fail'
        #         write_excel_object.ws.write(2, 21, group2_mark, color)
        #
        #         if group3_mark is not None:
        #             color = write_excel_object.green_color
        #
        #         else:
        #             color = write_excel_object.red_color
        #             overall_color = write_excel_object.red_color
        #             overall_status = 'Fail'
        #         write_excel_object.ws.write(2, 22, group3_mark, color)
        #
        #         if group4_mark is not None:
        #             color = write_excel_object.green_color
        #
        #         else:
        #             color = write_excel_object.red_color
        #             overall_color = write_excel_object.red_color
        #             overall_status = 'Fail'
        #         write_excel_object.ws.write(2, 23, group4_mark, color)
        #
        #         if group5_mark is not None:
        #             color = write_excel_object.green_color
        #
        #         else:
        #             color = write_excel_object.red_color
        #             overall_color = write_excel_object.red_color
        #             overall_status = 'Fail'
        #         write_excel_object.ws.write(2, 24, group5_mark, color)
        #
        #         if group6_mark is not None:
        #             color = write_excel_object.green_color
        #
        #         else:
        #             color = write_excel_object.red_color
        #             overall_color = write_excel_object.red_color
        #             overall_status = 'Fail'
        #         write_excel_object.ws.write(2, 25, group6_mark, color)
        #
        #         if report_link:
        #             color = write_excel_object.green_color
        #
        #         else:
        #             color = write_excel_object.red_color
        #             overall_color = write_excel_object.red_color
        #             overall_status = 'Fail'
        #         write_excel_object.ws.write(2, 26, report_link, color)
        #
        # write_excel_object.ws.write(2, 1, overall_status, overall_color)
        # write_excel_object.write_excel.close()
        #

qs = TalentLensAutomation()
token = crpo_common_obj.login_to_crpo(cred_crpo_admin_at.get('user'), cred_crpo_admin_at.get('password'),
                                      cred_crpo_admin_at.get('tenant'))

# sprint_id = input('Enter Sprint ID')
# candidate_id = crpo_common_obj.create_candidate(token, sprint_id)
# print(candidate_id)
# test_id = 14070
# event_id = 10660
# jobrole_id = 30258
# tag_candidate = crpo_common_obj.tag_candidate_to_test(token, candidate_id, test_id, event_id, jobrole_id)
# test_userid = crpo_common_obj.get_all_test_user(token, candidate_id)
test_userid = 1329546
print(test_userid)
tu_req_payload = {"testUserId": test_userid,
                  "requiredFlags": {"fileContentRequired": False, "isQuestionWise": True, "questionTypes": [16, 8],
                                    "isGroupSectionWiseMarks": True, "isVendorDetails": True, "isCodingSummary": False}}
tu_cred = crpo_common_obj.test_user_credentials(token, test_userid)
login_id = tu_cred['data']['testUserCredential']['loginId']
password = tu_cred['data']['testUserCredential']['password']
print(login_id)
print(password)
qs.mettl_technical(login_id, password, token, tu_req_payload)
