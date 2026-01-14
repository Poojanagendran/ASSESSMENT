from SCRIPTS.UI_COMMON.assessment_ui_common_v2 import *
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.COMMON.io_path import *


class TestSecurity:
    def __init__(self):
        self.row = 1
        write_excel_object.save_result(output_path_ui_test_security)
        header = ['QP_Verification']
        write_excel_object.write_headers_for_scripts(0, 0, header, write_excel_object.black_color_bold)
        header = ['Test Cases', 'Status', 'Test Id', 'Candidate Id', 'Testuser ID', 'User Name', 'Password',
                  'Expected Status', 'Actual Status']
        write_excel_object.write_headers_for_scripts(1, 0, header, write_excel_object.black_color_bold)

    def test_security(self, candidate_details):
        self.row = self.row + 1
        write_excel_object.current_status = 'Pass'
        write_excel_object.current_status_color = write_excel_object.green_color
        self.browser = assess_ui_common_obj.initiate_browser(amsin_automation_assessment_url)
        login_details = assess_ui_common_obj.ui_login_to_test(candidate_details.get('userName'),
                                                              candidate_details.get('password'))
        if login_details == 'SUCCESS':
            i_agreed = assess_ui_common_obj.select_i_agree()
            if i_agreed:
                assess_ui_common_obj.start_test_button_status()
                assess_ui_common_obj.start_test()
                time.sleep(2)
                secure_password_model_window = assess_ui_common_obj.check_security_key_model_window_availability()
                if secure_password_model_window == 'Success':
                    assess_ui_common_obj.validate_security_key(candidate_details.get('securityKey'))
                secure_password_model_window1 = assess_ui_common_obj.check_security_key_model_window_availability()
                if secure_password_model_window1 == 'Success':
                    print("Invalid Password")
                    actual_status = 'Invalid Password'
                else:
                    print("Valid Psssword")
                    actual_status = 'Valid Password'

                write_excel_object.compare_results_and_write_vertically(candidate_details.get('testCases'), None,
                                                                        self.row, 0)
                write_excel_object.compare_results_and_write_vertically(candidate_details.get('testID'), None,
                                                                        self.row, 2)
                write_excel_object.compare_results_and_write_vertically(candidate_details.get('candidateID'), None,
                                                                        self.row, 3)
                write_excel_object.compare_results_and_write_vertically(candidate_details.get('testUserId'), None,
                                                                        self.row, 4)
                write_excel_object.compare_results_and_write_vertically(candidate_details.get('userName'), None,
                                                                        self.row, 5)
                write_excel_object.compare_results_and_write_vertically(candidate_details.get('password'), None,
                                                                        self.row, 6)
                write_excel_object.compare_results_and_write_vertically(candidate_details.get('expectedStatus'),
                                                                        actual_status, self.row, 7)
                write_excel_object.compare_results_and_write_vertically(write_excel_object.current_status, None,
                                                                        self.row, 1)
        self.browser.quit()


print(datetime.datetime.now())
test_security_obj = TestSecurity()
excel_read_obj.excel_read(input_path_ui_test_security, 0)
excel_data = excel_read_obj.details
for current_excel_row in excel_data:
    print(current_excel_row)
    test_security_obj.test_security(current_excel_row)
write_excel_object.write_overall_status(1)
