import os
from SCRIPTS.COMMON.report import *
from SCRIPTS.CRPO_COMMON.crpo_common import *
from SCRIPTS.CRPO_COMMON.credentials import *
import zipfile
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.COMMON.io_path import *


class AssessmentDocket:
    def __init__(self):
        self.row_size = 2
        write_excel_object.save_result(output_path_assessmentdocket)
        header = ["Typing test assessment docket data"]
        write_excel_object.write_headers_for_scripts(0, 0, header, write_excel_object.black_color_bold)
        header1 = ["Test cases", "Status", "Expected No. of files in zip file", "Actual No. of files in zip file",
                   "Expected Q1_answer", "Actual Q1_answer ", "Expected Q2_answer", "Actual Q2_answer", "Test User Id",
                   "Tenant Alias"]
        write_excel_object.write_headers_for_scripts(1, 0, header1, write_excel_object.black_color_bold)

    def excel_write(self, data):

        write_excel_object.current_status_color = write_excel_object.green_color
        write_excel_object.current_status = "Pass"
        write_excel_object.compare_results_and_write_vertically(data.get('Test cases'), None, self.row_size, 0)
        write_excel_object.compare_results_and_write_vertically(data.get('Expected No. of files in zip file'),
                                                                len(candidate_data),
                                                                self.row_size, 2)
        write_excel_object.compare_results_and_write_vertically(data.get('Expected Q1_answer'), candidate_data[0],
                                                                self.row_size, 4)
        write_excel_object.compare_results_and_write_vertically(data.get('Expected Q2_answer'), candidate_data[1],
                                                                self.row_size, 6)
        write_excel_object.compare_results_and_write_vertically(data.get('Test User Id'), None, self.row_size, 8)
        write_excel_object.compare_results_and_write_vertically(cred_crpo_admin.get('tenant'), None,
                                                                self.row_size, 9)
        write_excel_object.compare_results_and_write_vertically(write_excel_object.current_status, None, self.row_size,
                                                                1)
        self.row_size = self.row_size + 1

    def downlaod_docket(self, token_header, tu_id):
        req_payload = {"testId": 19697, "testUserIds": [tu_id]}
        zip_file_path_downloaded = input_path_assessmentdocket_downloaded + str(tu_id) + ".zip"
        download_api_response = crpo_common_obj.download_assessment_docket(token_header, req_payload)
        report_obj.downloadReport(token_header, zip_file_path_downloaded, download_api_response)
        # Path to the download ZIP file

        print(zip_file_path_downloaded)
        # Path to extract the zip file
        extract_dir = input_common_dir + r'/Assessment/assessment_docket'
        # Extract the contents of the ZIP file
        with zipfile.ZipFile(zip_file_path_downloaded, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            # Get a list of all files and folders in the zip
            file_list = zip_ref.namelist()
            print(file_list)
        # Iterate over each file in the directory
        print(os.listdir(extract_dir))
        for filename in os.listdir(extract_dir):
            if filename.endswith('.txt'):
                file_path = os.path.join(extract_dir, filename)
                # Read text file content
                with open(file_path, 'r', encoding='utf-8') as file:
                    text_content = file.read()
                    candidate_data.append(text_content)


assessment_dock_obj = AssessmentDocket()
crpo_headers_token = crpo_common_obj.login_to_crpo(cred_crpo_admin.get('user'),
                                                   cred_crpo_admin.get('password'),
                                                   cred_crpo_admin.get('tenant'))
# Reading data from Excel file
excel_read_obj.excel_read(input_path_assessmentdocket, 0)
excel_data = excel_read_obj.details

for excel_test_case_data in excel_data:
    testuser_id = int(excel_test_case_data.get("Test User Id"))
    candidate_data = []
    assessment_dock_obj.downlaod_docket(crpo_headers_token, testuser_id)
    assessment_dock_obj.excel_write(excel_test_case_data)
write_excel_object.write_overall_status(testcases_count=3)
