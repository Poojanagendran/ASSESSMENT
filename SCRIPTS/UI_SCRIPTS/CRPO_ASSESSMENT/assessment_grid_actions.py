import xlrd
from SCRIPTS.COMMON.read_excel import excel_read_obj
from SCRIPTS.COMMON.write_excel_new import write_excel_object
from SCRIPTS.CRPO_COMMON.credentials import cred_crpo_admin
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.UI_COMMON.crpo_ui_common import *
import datetime
from SCRIPTS.UI_SCRIPTS.CRPO_ASSESSMENT.enable_all_actions import enable_actions_obj


class GridActions:
    def __init__(self):
        print("Started at : ", datetime.datetime.now())
        enable_actions_obj.enable_all_actions()
        self.row_size = 2
        self.details = []
        write_excel_object.save_result(output_path_ui_assessment_grid_actions)
        header = ["Grid Actions"]
        write_excel_object.write_headers_for_scripts(0, 0, header,
                                                     write_excel_object.black_color_bold)
        header1 = ["Testcases", "Status", "Test ID", "Event ID", "Test User ID", "Candidate ID", "Expected Grid Action Status", "Actual Grid Action Status", "Expected Grid Actions", "Actual Grid Actions"]
        write_excel_object.write_headers_for_scripts(1, 0, header1,
                                                     write_excel_object.black_color_bold)

    @staticmethod
    def compare_arrays(array1, array2):

        # Find missing values in array2 that are in array1
        missing_in_array2 = {item for item in array1 if item not in array2}

        # Find missing values in array1 that are in array2
        missing_in_array1 = {item for item in array2 if item not in array1}

        # Combine the results and return as a sorted list
        unique_mismatches = missing_in_array2.union(missing_in_array1)
        if unique_mismatches:
            # print("Mismatched values:", unique_mismatches)
            return unique_mismatches
        else:
            # print("Grid actions Matched")
            return "Arrays match"

    def excel_write(self, data):
        write_excel_object.current_status_color = write_excel_object.green_color
        write_excel_object.current_status = "Pass"
        write_excel_object.compare_results_and_write_vertically(data.get('TestCases'), None, self.row_size, 0)
        write_excel_object.compare_results_and_write_vertically(data.get('TestID'), None, self.row_size, 2)
        write_excel_object.compare_results_and_write_vertically(data.get('EventId'), None, self.row_size, 3)
        write_excel_object.compare_results_and_write_vertically(data.get('TestUserId'), None, self.row_size, 4)
        write_excel_object.compare_results_and_write_vertically(data.get('CandidateID'), None, self.row_size, 5)
        write_excel_object.compare_results_and_write_vertically(write_excel_object.current_status, None, self.row_size,
                                                                1)
        self.row_size = self.row_size + 1

    def excel_read_2(self, excel_file_path, sheet_index):
        # Open workbook and access sheet
        workbook = xlrd.open_workbook(excel_file_path)
        sheet = workbook.sheet_by_index(sheet_index)

        # Use rows starting from row 3 (index 2) and get data from column 6 (index 5)
        for row_index in range(1, sheet.nrows):
            # Extract data from column 5 (index 4) to the last column
            row_data = sheet.row_values(row_index)[6:]  # Starting from column 5 (index 4)

            # Filter out empty values from row_data
            row_data_filtered = [value for value in row_data if value != '']

            # Only append to details if there's any data
            if row_data_filtered:
                self.details.append(row_data_filtered)

    @staticmethod
    def grid_actions(expected):
        try:
            event_id = 18603
            event_candidate_id = [1564087,1565333,1564089,1564093,1564095]
            test_id = 21193
            test_user_id = [3774865,3778101, 3774867, 3774869, 3774871]
            vendor_test_id = 21381
            vendor_test_user_id = [3778097,3778099]

            if not isinstance(expected, list):
                raise ValueError("Expected actions must be a list.")

            # Initialize the browser and login
            browser = crpo_ui_obj.initiate_browser(amsin_automation_crpo_login, chrome_driver_path)
            crpo_ui_obj.ui_login_to_crpo(cred_crpo_admin.get('user'), cred_crpo_admin.get('password'))

            def process_actions(expected_actions_l, actual_actions_l, row, testcases_l):
                """Compare expected vs actual grid actions and log results."""
                action_status = grid_action_obj.compare_arrays(expected_actions, actual_actions)

                write_excel_object.compare_results_and_write_vertically(
                    'Arrays match',
                    "\n".join(action_status) if isinstance(action_status, list) else str(action_status), row, 6
                )
                write_excel_object.compare_results_and_write_vertically(
                    "\n".join(expected_actions) if isinstance(expected_actions, list) else str(expected_actions),
                    "\n".join(actual_actions) if isinstance(actual_actions, list) else str(actual_actions),
                    row, 8
                )
                print(f"Test Case : {testcases_l}")
                print(f"Expected: {expected_actions_l}")
                print(f"Actual: {actual_actions_l}")
                print(f"Action Status: {action_status}")

            # Fetch grid actions
            assessment_grid_actions = crpo_ui_obj.get_assessment_grid_actions(test_user_id,'Assessments', test_id) or []
            vendor_grid_actions = crpo_ui_obj.get_assessment_grid_actions(vendor_test_user_id, 'Assessments', vendor_test_id) or []
            event_grid_actions = crpo_ui_obj.get_event_grid_actions(event_candidate_id, 'Events', event_id) or []
            assessment_candidate_grid_actions = crpo_ui_obj.get_assessment_grid_actions(test_user_id, 'Assessment Candidates') or []

            # Combine grid actions into a list
            grid_actions = [*assessment_grid_actions, *vendor_grid_actions, *event_grid_actions,*assessment_candidate_grid_actions]

            # Validate list lengths before processing
            if not (len(expected) == len(grid_actions) == len(testcase)):
                raise ValueError("Mismatch in list lengths for processing grid actions.")

            # Process each action
            for i, (expected_actions, actual_actions, testcases) in enumerate(
                    zip(expected, grid_actions, testcase), start=2
            ):
                process_actions(expected_actions, actual_actions, i, testcases)

        except Exception as e:
            print(f"Error occurred in grid_actions: {e}")

        finally:
            # Ensure browser quits
            if 'browser' in locals() and browser:
                browser.quit()


grid_action_obj = GridActions()

excel_read_obj.excel_read(input_path_ui_grid_actions, 0)
grid_action_obj.excel_read_2(input_path_ui_grid_actions, 0)
grid_actions_list = grid_action_obj.details
excel_data_2 = excel_read_obj.details
testcase = [data.get('TestCases') for data in excel_data_2]
grid_action_obj.grid_actions(grid_actions_list)
for data in excel_data_2:
    grid_action_obj.excel_write(data)
write_excel_object.write_overall_status(testcases_count=20)

print("Ended at : ", datetime.datetime.now())
