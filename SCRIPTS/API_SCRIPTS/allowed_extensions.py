# from concurrent.futures import ThreadPoolExecutor, as_completed
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.CRPO_COMMON.crpo_common import *
from SCRIPTS.CRPO_COMMON.credentials import *
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.COMMON.parallel_execution import *


class AllowedFileExtensions:
    def __init__(self):
        self.allowed_extensions = [".doc", ".rtf", ".dot", ".docx", ".docm", ".dotx", ".dotm", ".docb", ".pdf", ".xls",
                                   ".xlt", ".xlm", ".xlsx", ".xlsm", ".xltx", ".xltm", ".xlsb", ".xla", ".xlam", ".xll",
                                   ".xlw", ".ppt", ".pot", ".pps", ".pptx", ".pptm", ".potx", ".potm", ".ppam", ".ppsx",
                                   ".ppsm", ".sldx", ".sldm", ".zip", ".rar", ".7z", ".gz", ".jpeg", ".jpg", ".gif",
                                   ".png", ".msg", ".txt", ".mp4", ".mvw", ".3gp", ".sql", ".webm", ".csv", ".odt",
                                   ".json", ".ods", ".ogg", ".p12"]
        requests.packages.urllib3.disable_warnings()
        self.row_size = 2
        write_excel_object.save_result(output_path_allowed_extension)
        self.write_headers()

    def write_headers(self):
        # Writing headers in the Excel file
        headers = ["Allowed Extensions"]
        write_excel_object.write_headers_for_scripts(0, 0, headers, write_excel_object.black_color_bold)
        headers1 = ["Extension Type", "Status", "File Name", "Expected Status", "Actual Status", "API Response"]
        write_excel_object.write_headers_for_scripts(1, 0, headers1, write_excel_object.black_color_bold)

    def validate_files(self, token, excel_input):
        # Validating files and writing results
        file_path = Path(input_path_allowed_extension_files % (excel_input.get('filePathName')))
        file_name = excel_input.get('fileName')
        resp = crpo_common_obj.upload_files(token, file_name, file_path)
        actual_status = self.get_actual_status(resp)
        self.write_results(excel_input, actual_status)

    def get_actual_status(self, resp):
        # (Same as your original method)
        # Determining actual status based on API response
        error_desc = resp['error']['errorDescription'] if 'error' in resp else ''
        if resp.get('status') == 'OK' and resp['data']:
            return 'allowed'
        elif "DisAllowed fileExtension" in error_desc:
            return 'disallowed - fileExtension for the control'
        elif 'File extension does not match file format' in error_desc:
            return "disallowed - File extension does not match file format"
        elif 'UnAcceptable file format' in error_desc:
            return "UnAcceptable file format"
        elif 'DisAllowedFileExtFiles' in error_desc or 'ExtNFileFormatMismatchedFiles' in error_desc:
            return error_desc
        else:
            return "status unknown"

    def write_results(self, excel_input, actual_status):
        # (Same as your original method)
        write_excel_object.compare_results_and_write_vertically(excel_input.get('extensionType'), None, self.row_size,
                                                                0)
        write_excel_object.compare_results_and_write_vertically(excel_input.get('fileName'), None, self.row_size, 2)
        write_excel_object.compare_results_and_write_vertically(excel_input.get('expectedStatus'), actual_status,
                                                                self.row_size, 3)
        write_excel_object.compare_results_and_write_vertically(write_excel_object.current_status, None, self.row_size,
                                                                1)
        self.row_size += 1


# Initializing AllowedFileExtensions object
allowed_ext_obj = AllowedFileExtensions()

# Logging in to CRPO
login_token = crpo_common_obj.login_to_crpo(cred_crpo_admin.get('user'), cred_crpo_admin.get('password'),
                                            cred_crpo_admin.get('tenant'))

# Reading data from Excel file
excel_read_obj.excel_read(input_path_allowed_extension, 0)
excel_data = excel_read_obj.details
thread_context(allowed_ext_obj.validate_files, login_token, excel_data)
write_excel_object.write_overall_status(testcases_count=len(excel_data))
