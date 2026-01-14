from SCRIPTS.UI_COMMON.assessment_ui_common_v2 import *
import time
from SCRIPTS.UI_SCRIPTS.assessment_data_verification import *
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.COMMON.io_path import *


class OnlineAssessment:

    def __init__(self):
        pass

    def mcq_assessment(self, current_excel_data):
        # code = 'using System; using System.Collections.Generic; using System.Linq; using System.Text; namespace check1 { class Program { static void Main(string[] args) { int i; Console.Write("Enter an integer"); i = int.Parse(Console.ReadLine()); if (i % 2 == 0) { Console.Write("Even"); Console.Read(); } else { Console.Write("Odd"); Console.Read(); } } } }'
        # print(code)
        code = json.loads(current_excel_data.get('code'))
        original_code1 = code.get('Source')
        self.browser = assess_ui_common_obj.initiate_browser(amsin_at_assessment_url)
        login_details = assess_ui_common_obj.ui_login_to_test(current_excel_data.get('loginName'),
                                                              (current_excel_data.get('password')))
        if login_details == 'SUCCESS':
            i_agreed = assess_ui_common_obj.select_i_agree()
            if i_agreed:
                start_test_status = assess_ui_common_obj.start_test_button_status()
                assess_ui_common_obj.start_test()
                assess_ui_common_obj.coding_editor(original_code1)
        else:
            print("login failed due to below reason")
            print(login_details)


print(datetime.datetime.now())
assessment_obj = OnlineAssessment()
# input_file_path = r"F:\automation\PythonWorkingScripts_InputData\UI\Assessment\ui_relogin.xls"
input_file_path = r"F:\qa_automation\PythonWorkingScripts_InputData\UI\Assessment\ui_coding_test.xls"
excel_read_obj.excel_read(input_file_path, 0)
excel_data = excel_read_obj.details
for current_excel_row in excel_data:
    # print(current_excel_row)
    # print(current_excel_row.get("code"))
    assessment_obj.mcq_assessment(current_excel_row)
# crpo_token = crpo_common_obj.login_to_crpo('admin', 'At@2021$$', 'AT')
# print(crpo_token)
# # time.sleep(10)
# obj_assessment_data_verification.assessment_data_report(crpo_token, excel_data)
# obj_assessment_data_verification.write_excel.close()
# print(datetime.datetime.now())
#
