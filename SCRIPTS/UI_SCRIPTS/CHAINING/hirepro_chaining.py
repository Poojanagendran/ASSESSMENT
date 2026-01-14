from SCRIPTS.UI_COMMON.assessment_ui_common_v2 import *
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.UI_SCRIPTS.assessment_data_verification import *
from SCRIPTS.COMMON.read_excel import *
import xlsxwriter
from SCRIPTS.DB_DELETE.db_cleanup import *
import datetime


class HireproChainingOfTwoTests:

    def __init__(self):
        # Data cleanup
        data_clean_obj.hirepro_chaining_delete()

        self.started_time = datetime.datetime.now()
        self.write_excel = xlsxwriter.Workbook(output_path_ui_hirepro_chaining)
        self.ws = self.write_excel.add_worksheet()

        # Formats
        self.formats = {
            'black': self.write_excel.add_format({'font_color': 'black', 'font_size': 9}),
            'bold': self.write_excel.add_format({'bold': True, 'font_size': 9}),
            'red': self.write_excel.add_format({'font_color': 'red', 'font_size': 9}),
            'green': self.write_excel.add_format({'font_color': 'green', 'font_size': 9})
        }

        self.over_all_status = 'Pass'
        self.over_all_status_color = self.formats['green']
        self._prepare_excel_header()

    def _prepare_excel_header(self):
        headers = [
            "Testcases", "Status", "Test ID", "Candidate ID", "Login Name", "Password",
            "T1 Expected Status", "T1 Actual Status", "Expected SLC Message", "Actual SLC Message",
            "Exp Consent Yes", "Act Consent Yes", "Exp Consent No", "Act Consent No",
            "Exp Consent Para", "Act Consent Para", "Exp Overall Msg", "Act Overall Msg", "Time Taken"
        ]
        self.ws.write(0, 0, "Hirepro Chaining Report", self.formats['bold'])
        for i, header in enumerate(headers):
            self.ws.write(1, i, header, self.formats['bold'])

    def mcq_assessment(self, data, row):
        started = datetime.datetime.now()
        self.browser = None
        status = {}
        tc_status = 'Fail'

        try:
            self.browser = assess_ui_common_obj.initiate_browser(amsin_automation_assessment_url)
            login = assess_ui_common_obj.ui_login_to_test(data.get('loginName'), data.get('password'))

            # Write static input data to Excel
            self._write_input_data(data, row)

            if login == 'SUCCESS':
                # Test 1 Flow
                if assess_ui_common_obj.select_i_agree():
                    assess_ui_common_obj.start_test()

                    # Answering questions 1 to 5
                    for q_idx in range(1, 6):
                        ans = data.get(f'ans_qid{q_idx}')
                        assess_ui_common_obj.select_answer_for_the_question(ans)
                        if q_idx < 5: assess_ui_common_obj.next_question(q_idx + 1)

                    assess_ui_common_obj.end_test()
                    assess_ui_common_obj.end_test_confirmation()

                    # Analyze Shortlisting Page
                    status = assess_ui_common_obj.shortlisting_page()

                    # Test 2 Logic (Chaining)
                    if status.get('is_next_test_available') == 'Available':
                        if data.get('consent') == "No":
                            assess_ui_common_obj.consent_no()
                        else:
                            print("Proceeding to Test 2...")
                            assess_ui_common_obj.start_next_test()
                            assess_ui_common_obj.select_i_agree()
                            assess_ui_common_obj.start_test()
                            # Quick skip for Test 2 questions
                            for i in range(2, 6): assess_ui_common_obj.next_question(i)
                            assess_ui_common_obj.end_test()
                            assess_ui_common_obj.end_test_confirmation()
                    else:
                        status = assess_ui_common_obj.rejection_page()

                # Validation Logic
                tc_status = self._validate_results(data, status, row)

        except Exception as e:
            print(f"Error in Test Case at row {row}: {e}")
            self.ws.write(row, 1, 'Error/Exception', self.formats['red'])
            self.over_all_status = 'Fail'

        finally:
            if self.browser:
                self.browser.quit()

            duration = str(datetime.datetime.now() - started).split(".")[0]
            self.ws.write(row, 18, duration, self.formats['black'])
            print(f"Row {row} completed in {duration}. Status: {tc_status}")

    def _write_input_data(self, data, row):
        # Columns 0, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16 are input expectations
        mapping = {0: 'testCases', 2: 'testId', 3: 'candidateId', 4: 'loginName',
                   5: 'password', 6: 't1ExpectedStatus', 8: 'message',
                   10: 'consentYesButtonMessage', 12: 'consentNoButtonMessage',
                   14: 'consentMessage', 16: 'overAllPageMessage'}
        for col, key in mapping.items():
            self.ws.write(row, col, data.get(key), self.formats['black'])

    def _validate_results(self, data, status, row):
        # Validation mapping: (ActualKey, ExpectedKey, ExcelCol)
        validations = [
            ('is_shortlisted', 't1ExpectedStatus', 7),
            ('message', 'message', 9),
            ('consent_yes', 'consentYesButtonMessage', 11),
            ('consent_no', 'consentNoButtonMessage', 13),
            ('consent_paragraph', 'consentMessage', 15),
            ('next_test_page_message', 'overAllPageMessage', 17)
        ]

        all_passed = True
        for act_key, exp_key, col in validations:
            actual = str(status.get(act_key))
            expected = str(data.get(exp_key))

            if actual == expected:
                self.ws.write(row, col, actual, self.formats['green'])
            else:
                self.ws.write(row, col, actual, self.formats['red'])
                all_passed = False

        final_status = 'pass' if all_passed else 'Fail'
        color = self.formats['green'] if all_passed else self.formats['red']

        if not all_passed:
            self.over_all_status = 'Fail'
            self.over_all_status_color = self.formats['red']

        self.ws.write(row, 1, final_status, color)
        return final_status


# --- Main Execution Block ---
chaining_obj = HireproChainingOfTwoTests()
excel_read_obj.excel_read(input_path_ui_hirepro_chaining, 0)
excel_data = excel_read_obj.details

current_row = 2  # Starting row in Excel
for record in excel_data:
    chaining_obj.mcq_assessment(record, current_row)
    current_row += 1  # Using +1 to keep Excel compact

# Finalize Report
chaining_obj.ws.write(0, 1, chaining_obj.over_all_status, chaining_obj.over_all_status_color)
chaining_obj.write_excel.close()
print(f"Execution Finished. Overall Status: {chaining_obj.over_all_status}")