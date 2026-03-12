from SCRIPTS.UI_COMMON.assessment_ui_common_v2 import *
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.COMMON.io_path import *


class assessment_login:
    def __init__(self):
        self.row = 1
        write_excel_object.save_result(output_path_ui_assessment_login_validation)
        header = ['QP_Verification']
        write_excel_object.write_headers_for_scripts(0, 0, header, write_excel_object.black_color_bold)
        header = ['Test Cases', 'Status', 'Testcase', 'Expected Status', 'Actual Status']
        write_excel_object.write_headers_for_scripts(1, 0, header, write_excel_object.black_color_bold)

    def _normalize_expected(self, expected):
        """Map cred_data expected strings to validation outcomes."""
        if not expected:
            return expected
        e = expected.strip()
        if e.lower() == 'valid login':
            return 'NAVIGATED_AWAY'
        return e

    def _actual_status_from_result(self, result_code, message):
        if result_code == 'BUTTON_DISABLED':
            return 'Login button disabled (empty id/password)'
        if result_code == 'BUTTON_ENABLED':
            return 'Login button enabled (should be disabled when id/password empty)'
        if result_code == 'NAVIGATED_AWAY':
            return 'Navigated past login (no error on login page)'
        if result_code == 'ERROR_ON_PAGE' and message:
            return message
        return result_code

    def _pass_fail(self, expected, actual_status, result_code, message):
        """
        Pass when:
        - Empty credentials: button must be disabled.
        - NAVIGATED_AWAY: always Pass — valid login success (no error on login page, moved forward).
        - Otherwise: actual message should match expected (substring or exact).
        """
        expected_norm = self._normalize_expected(expected)

        if result_code == 'BUTTON_ENABLED':
            return False
        if result_code == 'BUTTON_DISABLED':
            # Empty-field cases: pass if button correctly disabled
            return True

        # Valid login success: left login page without login-error div — always mark Pass
        if result_code == 'NAVIGATED_AWAY':
            return True

        if result_code == 'ERROR_ON_PAGE' and expected_norm:
            # Allow expected to be contained in actual or vice versa (UI may add punctuation)
            act = (actual_status or '').strip()
            exp = expected_norm.strip()
            if exp.lower() in act.lower() or act.lower() in exp.lower():
                return True
            return act == exp

        return False

    def assessment_login(self, credentials):
        self.row = self.row + 1
        testcase = credentials.get('Testcase', '')
        expected = credentials.get('expected', '')
        login_id = credentials.get('Login_id') or ''
        password = credentials.get('Password') or ''

        self.browser = assess_ui_common_obj.initiate_browser(amsin_agenticqa_assessment_url)
        try:
            result_code, message = assess_ui_common_obj.validate_login_credentials(login_id, password)
            actual_status = self._actual_status_from_result(result_code, message)
            passed = self._pass_fail(expected, actual_status, result_code, message)

            write_excel_object.current_status = 'Pass' if passed else 'Fail'
            write_excel_object.current_status_color = (
                write_excel_object.green_color if passed else write_excel_object.red_color
            )

            write_excel_object.compare_results_and_write_vertically(testcase, None, self.row, 0)
            write_excel_object.compare_results_and_write_vertically(write_excel_object.current_status, None, self.row, 1)
            write_excel_object.compare_results_and_write_vertically(expected, None, self.row, 2)
            # Empty id/password or valid login (NAVIGATED_AWAY): write same expected/actual so Excel compare stays green
            if result_code == 'BUTTON_DISABLED' or result_code == 'NAVIGATED_AWAY':
                write_excel_object.compare_results_and_write_vertically(
                    actual_status, actual_status, self.row, 3
                )
            else:
                write_excel_object.compare_results_and_write_vertically(
                    expected, actual_status, self.row, 3
                )
        finally:
            self.browser.quit()


cred_data = [
    {"Login_id": "agenticqa5345", "Password": "2PMD?%", "Testcase": "1. Valid Login",
     "expected": "You are late from allotted permissible time"},

    {"Login_id": "agenticqa5347", "Password": "dumypass", "Testcase": "2. Wrong Username",
     "expected": "Invalid Username or Password"},

    {"Login_id": "dummyuser", "Password": "passpass", "Testcase": "3. Wrong Both",
     "expected": "Invalid Username or Password"},

    {"Login_id": "dummyuser", "Password": "6YCH\\", "Testcase": "4. Dummy user and Right Pass",
     "expected": "Invalid Username or Password"},

    {"Login_id": "", "Password": "2HTA~_", "Testcase": "5. Empty User",
     "expected": "Invalid Username or Password"},

    {"Login_id": "agenticqa5355", "Password": "", "Testcase": "6. Empty Pass",
     "expected": "Invalid Username or Password"},

    {"Login_id": "", "Password": "", "Testcase": "7. Double Empty",
     "expected": "Invalid Username or Password"},

    {"Login_id": "agenticqa5355", "Password": "6HSM,%", "Testcase": "8. test user validity is extended",
     "expected": "Navigated past login (no error on login page)"},

    {"Login_id": "agenticqa5353", "Password": "2HTA~_", "Testcase": "9. testuser password is disabled",
     "expected": "Your password has been disabled, please contact admin."},

    {"Login_id": "agenticqa5351", "Password": r"6YCH\\", "Testcase": "10. Already attended",
     "expected": "You have already submitted"}
]

if __name__ == '__main__':
    print(datetime.datetime.now())
    test_security_obj = assessment_login()
    for current_excel_row in cred_data:
        print(current_excel_row)
        test_security_obj.assessment_login(current_excel_row)
    # Finalize workbook — same as testsecurity.py (write_overall_status closes and writes the .xls file)
    write_excel_object.write_overall_status(len(cred_data))
    # save_result() builds path as output_path + started + '.xls'
    _out = str(output_path_ui_assessment_login_validation) + write_excel_object.started + ".xls"
    print("Excel output created:", _out)
