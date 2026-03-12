"""
Plagiarism report: generates and compares plagiarism reports.

Run directly: from project root, python -m SCRIPTS.API_SCRIPTS.plagiarism_report
Safe to import: main logic runs only when executed as __main__ (pytest-friendly).
"""
from SCRIPTS.COMMON.report import *
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.CRPO_COMMON.crpo_common import *
from SCRIPTS.CRPO_COMMON.credentials import *
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.COMMON.api_requests_for_reports import *

if __name__ == "__main__":
    crpo_headers = crpo_common_obj.login_to_crpo(cred_crpo_admin.get('user'), cred_crpo_admin.get('password'),
                                                 cred_crpo_admin.get('tenant'))
    for report_items in range(0, 1):
        try:
            report_obj.writeExcelConfigurations(output_path_plagiarism_report)
            download_api_response = crpo_common_obj.generate_plagiarism_report(crpo_headers,
                                                                               getall_plagarism_request_payload)
            report_obj.downloadReport(crpo_headers, input_path_plagiarism_report_downloaded, download_api_response)
            write_excel_object.save_result(output_path_plagiarism_report)
            write_excel_object.excelReadExpectedSheet(input_path_plagiarism_report)
            write_excel_object.excelReadActualSheet(input_path_plagiarism_report_downloaded)
            write_excel_object.excelWriteHeaders(hierarchy_headers_count=1)
            write_excel_object.excelMatchValues(usecase_name='Plagiarism Report', comparision_required_from_index=1,
                                                total_testcase_count=18)
        except Exception as e:
            print("Please Verify it manually...")
            print(e)
