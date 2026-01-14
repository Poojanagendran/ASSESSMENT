from SCRIPTS.COMMON.io_path import *
from SCRIPTS.COMMON.writeExcel import write_excel_object
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
                  'Report link']
        write_excel_object.write_headers_for_scripts(1, 0, header, write_excel_object.black_color_bold)

    def wheebox_technical(self, login_id, password, tkn, tu_request):
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
                wb_agreement = assess_ui_common_obj.wheebox_starttest_checkbox()
                wb_proceed_test = assess_ui_common_obj.wheebox_proceed_test()
                wb_auto_next_qn = assess_ui_common_obj.wheebox_auto_next_qn()
                browser.close()
        browser1 = assess_ui_common_obj.initiate_browser(self.url, self.path)
        login_details = assess_ui_common_obj.ui_login_to_test(login_id, password)
        if login_details == 'SUCCESS':
            time.sleep(60)
            i_agreed = assess_ui_common_obj.select_i_agree()
            if i_agreed:
                start_test_status = assess_ui_common_obj.start_test_button_status()
                hirepro_start_test = assess_ui_common_obj.start_test()
                wb_agreement = assess_ui_common_obj.wheebox_starttest_checkbox()
                wb_proceed_test = assess_ui_common_obj.wheebox_proceed_test()
                wb_auto_next_qn = assess_ui_common_obj.wheebox_auto_next_qn()
                for question_count in range(0, 90):
                    time.sleep(5)
                    answer_qn = assess_ui_common_obj.wheebox_answer_qn()
                    print(question_count)
                wb_submit_test = assess_ui_common_obj.wheebox_submit_test()
                wb_confirm_submit = assess_ui_common_obj.wheebox_confirm_submit()
                time.sleep(180)
                tu_infos = crpo_common_obj.get_test_user_infos(tkn, tu_request)
                report_link = tu_infos['data']['vendorDetails']['reportLink']
                # third_party_status = tu_infos['data']['vendorDetails']['thirdPartyStatus']
                data = tu_infos['data']['groupAndSectionWiseMarks']
                group1_name = data[0]['name']
                group1_mark = int(data[0]['obtainedMarks'])
                group2_name = data[1]['name']
                group2_mark = int(data[1]['obtainedMarks'])
                group3_name = data[2]['name']
                group3_mark = int(data[2]['obtainedMarks'])
                group4_name = data[3]['name']
                group4_mark = int(data[3]['obtainedMarks'])

                write_excel_object.ws.write(2, 0, 'Wheebox Check', write_excel_object.green_color)

                write_excel_object.ws.write(2, 2, 'single test', write_excel_object.green_color)
                write_excel_object.ws.write(2, 2, test_id, write_excel_object.green_color)
                write_excel_object.ws.write(2, 3, candidate_id, write_excel_object.green_color)
                write_excel_object.ws.write(2, 4, test_userid, write_excel_object.green_color)

                if wb_agreement[0] == 'Agreed':
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 5, wb_agreement[0], color)

                if wb_proceed_test[0] == 'Success':
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 6, wb_proceed_test[0], color)

                if wb_auto_next_qn[0] == 'Success':
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 7, wb_auto_next_qn[0], color)

                if wb_submit_test[0] == 'submitted':
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 8, wb_submit_test[0], color)

                if wb_confirm_submit[0] == 'submitted':
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 9, wb_confirm_submit[0], color)

                if "Logical Reasoning" in group1_name:
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 10, group1_name, color)

                if 'Numerical Ability' in group2_name:
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 11, group2_name, color)

                if 'English Ability' in group3_name:
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 12, group3_name, color)

                if 'Technical' in group4_name:
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 13, group4_name, color)

                if group1_mark is not None:
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 14, group1_mark, color)

                if group2_mark is not None:
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 15, group2_mark, color)

                if group3_mark is not None:
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 16, group3_mark, color)

                if group4_mark is not None:
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 17, group4_mark, color)

                if report_link:
                    color = write_excel_object.green_color

                else:
                    color = write_excel_object.red_color
                    overall_color = write_excel_object.red_color
                    overall_status = 'Fail'
                write_excel_object.ws.write(2, 18, report_link, color)

        write_excel_object.ws.write(2, 1, overall_status, overall_color)
        write_excel_object.write_excel.close()
        browser.quit()

qs = WheeboxAutomation()
token = crpo_common_obj.login_to_crpo(cred_crpo_admin.get('user'), cred_crpo_admin.get('password'),
                                      cred_crpo_admin.get('tenant'))
#sprint_id = input('Enter Sprint ID')
sprint_id = str(datetime.datetime.now())
candidate_id = crpo_common_obj.create_candidate(token, sprint_id)
print(candidate_id)
test_id = 14673
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
