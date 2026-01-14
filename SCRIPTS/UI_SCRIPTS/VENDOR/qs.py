from SCRIPTS.COMMON.io_path import *
from SCRIPTS.COMMON.writeExcel import write_excel_object
from SCRIPTS.UI_COMMON.assessment_ui_common_v2 import *
from SCRIPTS.CRPO_COMMON.credentials import *
import time
from SCRIPTS.UI_SCRIPTS.assessment_data_verification import *
from SCRIPTS.COMMON.io_path import *


class VersantQuickScreener:

    def __init__(self):
        self.url = "https://pearsonstg.hirepro.in/assessment/#/assess/login/eyJhbGlhcyI6ImF1dG9tYXRpb24ifQ%3D%3D"
        self.path = chrome_driver_path
        write_excel_object.save_result(output_path_ui_vet_qs)
        # 0th Row Header
        header = ['VET Quick Screener']
        # 1 Row Header
        write_excel_object.write_headers_for_scripts(0, 0, header, write_excel_object.black_color_bold)
        header = ['Testcases', 'Status', 'Test ID', 'Candidate ID', 'Testuser ID', 'vet test started',
                  'vet welcome page', 'quiet please page', 'ready check page', 'ready start page', 'proceed test page',
                  'speaking tips page', 'overview page', 'instruction page', 'survey page']
        write_excel_object.write_headers_for_scripts(1, 0, header, write_excel_object.black_color_bold)

    def quick_screener(self, login_id, password):
        overall_color = write_excel_object.green_color
        browser = assess_ui_common_obj.initiate_browser(self.url)
        login_details = assess_ui_common_obj.ui_login_to_test(login_id, password)
        # self.browser.get_screenshot_as_file(self.common_path + "\\1_t1_afterlogin.png")
        overall_status = 'pass'
        if login_details == 'SUCCESS':
            i_agreed = assess_ui_common_obj.select_i_agree()
            if i_agreed:
                start_test_status = assess_ui_common_obj.start_test_button_status()
                assess_ui_common_obj.start_test()
                vet_start = assess_ui_common_obj.vet_start_test()
                vet_welcome = assess_ui_common_obj.vet_welcome_page()
                vet_quiet = assess_ui_common_obj.vet_quiet_please()
                ready_check = assess_ui_common_obj.vet_ready_check_box()
                ready_start = assess_ui_common_obj.vet_ready_start_link()
                proceed_test = assess_ui_common_obj.vet_proceed_test()
                speaking_tips = assess_ui_common_obj.vet_speaking_tips()
                overview = assess_ui_common_obj.vet_overview()
                instruction = assess_ui_common_obj.vet_instruction()
                for i in range(0, 9):
                    # assess_ui_common_obj.play_audio()
                    print("Current_iteration is :  ", i)
                    time.sleep(60)
                survey = assess_ui_common_obj.survey_submit()
                time.sleep(60)
                print("Test is Successfully Submitted")


        write_excel_object.ws.write(2, 0, 'Check VET', write_excel_object.green_color)

        # write_excel_object.ws.write(2, 2, '111', write_excel_object.green_color)
        write_excel_object.ws.write(2, 2, test_id, write_excel_object.green_color)
        write_excel_object.ws.write(2, 3, candidate_id, write_excel_object.green_color)
        write_excel_object.ws.write(2, 4, test_userid, write_excel_object.green_color)

        if vet_start[0] == 'Successful':
            color = write_excel_object.green_color

        else:
            color = write_excel_object.red_color
            overall_color = write_excel_object.red_color
            overall_status = 'Fail'
        write_excel_object.ws.write(2, 5, vet_start[0], color)
        if vet_welcome[0] == 'Successful':
            color = write_excel_object.green_color

        else:
            color = write_excel_object.red_color
            overall_color = write_excel_object.red_color
            overall_status = 'Fail'
        write_excel_object.ws.write(2, 6, vet_welcome[0], color)

        if vet_quiet[0] == 'Successful':
            color = write_excel_object.green_color

        else:
            color = write_excel_object.red_color
            overall_color = write_excel_object.red_color
            overall_status = 'Fail'
        write_excel_object.ws.write(2, 7, vet_quiet[0], color)

        if ready_check[0] == 'Successful':
            color = write_excel_object.green_color

        else:
            color = write_excel_object.red_color
            overall_color = write_excel_object.red_color
            overall_status = 'Fail'
        write_excel_object.ws.write(2, 8, ready_check[0], color)

        if ready_start[0] == 'Successful':
            color = write_excel_object.green_color

        else:
            color = write_excel_object.red_color
            overall_color = write_excel_object.red_color
            overall_status = 'Fail'
        write_excel_object.ws.write(2, 9, ready_start[0], color)

        if proceed_test[0] == 'Successful':
            color = write_excel_object.green_color

        else:
            color = write_excel_object.red_color
            overall_color = write_excel_object.red_color
            overall_status = 'Fail'
        write_excel_object.ws.write(2, 10, proceed_test[0], color)

        if speaking_tips[0] == 'Successful':
            color = write_excel_object.green_color

        else:
            color = write_excel_object.red_color
            overall_color = write_excel_object.red_color
            overall_status = 'Fail'
        write_excel_object.ws.write(2, 11, speaking_tips[0], color)

        if overview[0] == 'Successful':
            color = write_excel_object.green_color

        else:
            color = write_excel_object.red_color
            overall_color = write_excel_object.red_color
            overall_status = 'Fail'
        write_excel_object.ws.write(2, 12, overview[0], color)

        if instruction[0] == 'Successful':
            color = write_excel_object.green_color

        else:
            color = write_excel_object.red_color
            overall_color = write_excel_object.red_color
            overall_status = 'Fail'
        write_excel_object.ws.write(2, 13, instruction[0], color)

        if survey[0] == 'Successful':
            color = write_excel_object.green_color

        else:
            color = write_excel_object.red_color
            overall_color = write_excel_object.red_color
            overall_status = 'Fail'
        write_excel_object.ws.write(2, 14, survey[0], color)
        write_excel_object.ws.write(2, 1, overall_status, overall_color)
        write_excel_object.write_excel.close()

qs = VersantQuickScreener()
token = crpo_common_obj.login_to_crpo(cred_crpo_admin.get('user'), cred_crpo_admin.get('password'),
                                      cred_crpo_admin.get('tenant'))
sprint_id = input('Enter Sprint ID')
candidate_id = crpo_common_obj.create_candidate(token, sprint_id)
print(candidate_id)
test_id = 14677
event_id = 11105
jobrole_id = 30337
tag_candidate = crpo_common_obj.tag_candidate_to_test(token, candidate_id, test_id, event_id, jobrole_id)
test_userid = crpo_common_obj.get_all_test_user(token, candidate_id)
print(test_userid)
tu_cred = crpo_common_obj.test_user_credentials(token, test_userid)
login_id = tu_cred['data']['testUserCredential']['loginId']
password = tu_cred['data']['testUserCredential']['password']
print(login_id)
print(password)
qs.quick_screener(login_id, password)
