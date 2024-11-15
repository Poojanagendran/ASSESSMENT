from SCRIPTS.UI_COMMON.self_assessment_1 import *
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.CRPO_COMMON.credentials import cred_crpo_suparya_crpodemo
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.COMMON.read_excel import *


class SaTest:
    def __init__(self):
        self.browser = None
        self.row_size = 2
        write_excel_object.save_result(output_path_ui_self_assessment)
        header = ["Self Assessment test creation"]
        write_excel_object.write_headers_for_scripts(0, 0, header, write_excel_object.black_color_bold)
        header1 = ["Test cases", "Overall Status", "Expected status ", "Actual status"]
        write_excel_object.write_headers_for_scripts(1, 0, header1, write_excel_object.black_color_bold)

    def excel_write(self, data):

        write_excel_object.current_status_color = write_excel_object.green_color
        write_excel_object.current_status = "Pass"
        write_excel_object.compare_results_and_write_vertically(data.get('testCases'), None, self.row_size, 0)
        # write_excel_object.compare_results_and_write_vertically(data.get('expectedStatus'), actual_status,
        #                                                         self.row_size, 2)
        write_excel_object.compare_results_and_write_vertically(write_excel_object.current_status, None, self.row_size,
                                                                1)
        self.row_size = self.row_size + 1

    def self_assessment(self, username, password):
        print("inside tenant_login")
        self.browser = self_assessment_obj.initiate_browser(amsin_crpodemo_crpo_login, chrome_driver_path)
        print("Initiate browser SUCCESS")
        login_details = self_assessment_obj.ui_login_to_tenant(username, password)
        if login_details == 'SUCCESS':
            print("Login to tenant : ", login_details)
            time.sleep(5)
            # self_assessment_obj.select_plus(4)
            # create_subjective_q = self_assessment_obj.add_mcq_local("141573")
            create_fib_q = self_assessment_obj.create_fib_q()
            print("Creating q ", create_fib_q)
            self.browser.quit()
            # time.sleep(5)
        else:
            print("Login to tenant :", login_details)
            self.browser.quit()


print(datetime.datetime.now())
assessment_obj = SaTest()
actual_status = "failed"
excel_read_obj.excel_read(input_path_ui_self_assessment, 0)
excel_data = excel_read_obj.details
assessment_obj.self_assessment(cred_crpo_suparya_crpodemo.get('user'), cred_crpo_suparya_crpodemo.get('password'))
for current_excel_row in excel_data:
    assessment_obj.excel_write(excel_data)

write_excel_object.write_overall_status(testcases_count=1)
print(datetime.datetime.now())
