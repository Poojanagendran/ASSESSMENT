from SCRIPTS.UI_COMMON.self_assessment_1 import *
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.CRPO_COMMON.credentials import cred_crpo_suparya_crpodemo
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.COMMON.read_excel import *
import logging
import time

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("sa_test.log", mode='w')])


class SaTest:
    def __init__(self):
        self.browser = None
        self.row_size = 2
        write_excel_object.save_result(output_path_ui_self_assessment)
        header = ["Self Assessment test creation"]
        write_excel_object.write_headers_for_scripts(0, 0, header, write_excel_object.black_color_bold)
        header1 = ["Test cases", "Status", "Expected status", "Actual status"]
        write_excel_object.write_headers_for_scripts(1, 0, header1, write_excel_object.black_color_bold)

    def excel_write(self, test_case, expected_status, actual_status):
        try:
            current_status = "Pass" if expected_status == actual_status else "Fail"
            write_excel_object.compare_results_and_write_vertically(test_case, None, self.row_size, 0)
            write_excel_object.compare_results_and_write_vertically(expected_status, actual_status, self.row_size, 2)
            write_excel_object.compare_results_and_write_vertically(current_status, None, self.row_size, 1)
            self.row_size += 1
        except Exception as e:
            logging.error(f"Error writing to Excel: {e}")

    def self_assessment(self, username, password, test_cases):
        try:
            sprint_id = ''
            while sprint_id == '':
                sprint_id = input('Please enter sprint no : ')
                print(" ")
            self.browser = self_assessment_obj.initiate_browser(amsin_crpodemo_crpo_login, chrome_driver_path)
            logging.info("Initiate browser SUCCESSFUL")
            login_details = self_assessment_obj.ui_login_to_tenant(username, password)
            if login_details == 'SUCCESS':
                logging.info(f"Login to tenant : {login_details}")
                time.sleep(5)
                
                create_test = self_assessment_obj.create_test_sa(sprint_id)
                if create_test == 'SUCCESS':
                    for test_case in test_cases:
                        actual_status = "none"
                        if test_case['testCases'] == 'Test Creation':
                            actual_status = 'Test created successfully' if create_test == 'SUCCESS' else create_test
                        elif test_case['testCases'] == 'MCQ Question Creation':
                            create_mcq_q = self_assessment_obj.create_mcq_q()
                            actual_status = "MCQ question created successfully" if create_mcq_q == 'SUCCESS' else create_mcq_q
                        elif test_case['testCases'] == 'MCQ Addition (Local)':
                            time.sleep(5)
                            self_assessment_obj.select_plus(2)
                            add_mcq_q = self_assessment_obj.add_q_local("136095")
                            actual_status = "MCQ question added from local tenant" if add_mcq_q == 'SUCCESS' else add_mcq_q
                        elif test_case['testCases'] == 'MCQ Addition (HirePro)':
                            time.sleep(5)
                            self_assessment_obj.select_plus(2)
                            add_mcq_hp_q = self_assessment_obj.add_q_hirepro("136097")
                            # add_mcq_hp_q = self_assessment_obj.add_mcq_hirepro()
                            actual_status = "MCQ question added from hirepro tenant" if add_mcq_hp_q == 'SUCCESS' else add_mcq_hp_q
                        elif test_case['testCases'] == 'RTC Question Creation':
                            create_rtc_q = self_assessment_obj.create_rtc_q()
                            actual_status = "RTC question created successfully" if create_rtc_q == 'SUCCESS' else create_rtc_q
                        elif test_case['testCases'] == 'RTC Addition (Local)':
                            # time.sleep(5)
                            # self_assessment_obj.select_plus(3)
                            add_rtc_q = self_assessment_obj.add_rtc_local()
                            actual_status = "RTC question added from local tenant" if add_rtc_q == 'SUCCESS' else add_rtc_q
                        elif test_case['testCases'] == 'RTC Addition (HirePro)':
                            add_rtc_hp_q = self_assessment_obj.add_rtc_hirepro()
                            actual_status = "RTC question added from hirepro tenant" if add_rtc_hp_q == 'SUCCESS' else add_rtc_hp_q
                        elif test_case['testCases'] == 'Subjective Question Creation':
                            create_subjective_q = self_assessment_obj.create_subjective_q()
                            actual_status = "Subjective question created successfully" if create_subjective_q == 'SUCCESS' else create_subjective_q
                        elif test_case['testCases'] == 'Subjective Addition (Local)':
                            time.sleep(5)
                            self_assessment_obj.select_plus(4)
                            add_subjective_q = self_assessment_obj.add_q_local("141573")
                            actual_status = "Subjective question added from local tenant" if add_subjective_q == 'SUCCESS' else add_subjective_q
                        elif test_case['testCases'] == 'Subjective Addition (HirePro)':
                            time.sleep(5)
                            self_assessment_obj.select_plus(4)
                            add_subjective_hp_q = self_assessment_obj.add_q_hirepro("141575")
                            actual_status = "Subjective question added from hirepro tenant" if add_subjective_hp_q == 'SUCCESS' else add_subjective_hp_q
                        elif test_case['testCases'] == 'FIB Question Creation':
                            create_fib_q = self_assessment_obj.create_fib_q()
                            actual_status = "FIB question created successfully" if create_fib_q == 'SUCCESS' else create_fib_q
                        elif test_case['testCases'] == 'FIB Addition (Local)':
                            time.sleep(5)
                            self_assessment_obj.select_plus(5)
                            add_fib_q = self_assessment_obj.add_q_local("141667")
                            actual_status = "FIB question added from local tenant" if add_fib_q == 'SUCCESS' else add_fib_q
                        elif test_case['testCases'] == 'FIB Addition (HirePro)':
                            time.sleep(5)
                            self_assessment_obj.select_plus(5)
                            add_fib_hp_q = self_assessment_obj.add_q_hirepro("141693")
                            actual_status = "FIB question added from hirepro tenant" if add_fib_hp_q == 'SUCCESS' else add_fib_hp_q

                        self.excel_write(test_case['testCases'], test_case['expectedStatus'], actual_status)
                else:
                    for test_case in test_cases:
                        actual_status = create_test
                        self.excel_write(test_case['testCases'], test_case['expectedStatus'], actual_status)
                    print("Test Creation Failed")
                self.browser.quit()
            else:
                logging.error(f"Login to tenant failed: {login_details}")
                self.browser.quit()
        except Exception as e:
            logging.error(f"An error occurred during the self assessment process: {e}")
            if self.browser:
                self.browser.quit()


if __name__ == "__main__":
    try:
        logging.info("Script started")
        print(datetime.datetime.now())
        assessment_obj = SaTest()
        excel_read_obj.excel_read(input_path_ui_self_assessment, 0)
        excel_data = excel_read_obj.details
        assessment_obj.self_assessment(cred_crpo_suparya_crpodemo.get('user'),
                                       cred_crpo_suparya_crpodemo.get('password'),
                                       excel_data)
        write_excel_object.write_overall_status(testcases_count=len(excel_data))
        print(datetime.datetime.now())
        logging.info("Script completed successfully")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
