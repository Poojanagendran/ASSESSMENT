import xlrd
from SCRIPTS.COMMON.read_excel import excel_read_obj
from SCRIPTS.COMMON.write_excel_new import write_excel_object
from SCRIPTS.CRPO_COMMON.credentials import cred_crpo_admin
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.UI_COMMON.crpo_ui_common import *
import datetime

class AuthoringGridActions:
    def __init__(self):
        print("Started at : ", datetime.datetime.now())
        self.row_size = 2
        self.details = []
        write_excel_object.save_result(output_path_ui_authoring_grid_actions)
        header = ["Grid Actions"]
        write_excel_object.write_headers_for_scripts(0, 0, header,
                                                     write_excel_object.black_color_bold)
        header1 = ["Testcases", "Status", "Question/ QP ID", "Expected Action Status", "Actual Action Status", "Expected Grid Actions", "Actual Grid Actions"]
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
        write_excel_object.compare_results_and_write_vertically(data.get('ID'), None, self.row_size, 2)
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
            row_data = sheet.row_values(row_index)[2:]  # Starting from column 5 (index 4)

            # Filter out empty values from row_data
            row_data_filtered = [value for value in row_data if value != '']

            # Only append to details if there's any data
            if row_data_filtered:
                self.details.append(row_data_filtered)

    @staticmethod
    def grid_actions(expected):
        try:
            bp_ids = [int(qid[0]), int(qid[1])]
            qp_ids = [qid[2], qid[3]]
            q_ids = qid[4:24]
            q_dump_ids = qid[24:]

            def process_actions(expected_actions_l, actual_actions_l, row, testcases_l):
                """Compare expected vs actual grid actions and log results."""
                action_status = authoring_grid_action_obj.compare_arrays(expected_actions, actual_actions)

                write_excel_object.compare_results_and_write_vertically(
                    "Arrays match", "\n".join(action_status) if isinstance(action_status, list) else str(action_status), row, 3
                )
                write_excel_object.compare_results_and_write_vertically(
                    "\n".join(expected_actions) if isinstance(expected_actions, list) else str(expected_actions),
                    "\n".join(actual_actions) if isinstance(actual_actions, list) else str(actual_actions),
                    row, 5
                )
                print(f"Test Case : {testcases_l}")
                print(f"Expected: {expected_actions_l}")
                print(f"Actual: {actual_actions_l}")
                print(f"Action Status: {action_status}")


            # Initialize the browser and login
            browser = crpo_ui_obj.initiate_browser(amsin_automation_crpo_login)
            crpo_ui_obj.ui_login_to_crpo(cred_crpo_admin.get('user'), cred_crpo_admin.get('password'))


            # Fetch grid actions
            bp_grid_actions = crpo_ui_obj.get_blueprint_grid_actions(bp_ids, 'Authoring', "Blueprints") or []
            qp_grid_actions = crpo_ui_obj.get_authoring_grid_actions(qp_ids,'Authoring',"Question Papers") or []
            question_grid_actions = crpo_ui_obj.get_authoring_grid_actions(q_ids,'Authoring',"Questions") or []
            question_dump_grid_actions = crpo_ui_obj.get_authoring_grid_actions(q_dump_ids,'Authoring',"Questions") or []

            # Combine grid actions into a list
            grid_actions = [*bp_grid_actions, *qp_grid_actions, *question_grid_actions,*question_dump_grid_actions]
            # print(grid_actions)

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


authoring_grid_action_obj = AuthoringGridActions()
excel_read_obj.excel_read(input_path_ui_grid_actions, 1)
authoring_grid_action_obj.excel_read_2(input_path_ui_grid_actions, 1)
grid_actions_list = authoring_grid_action_obj.details
excel_data_2 = excel_read_obj.details
testcase = [data.get('TestCases') for data in excel_data_2]
qid = [data.get('ID') for data in excel_data_2]
authoring_grid_action_obj.grid_actions(grid_actions_list)
for data in excel_data_2:
    authoring_grid_action_obj.excel_write(data)
write_excel_object.write_overall_status(testcases_count=24)

print("Ended at : ", datetime.datetime.now())
