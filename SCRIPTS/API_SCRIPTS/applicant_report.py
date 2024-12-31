from SCRIPTS.COMMON.report import *
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.CRPO_COMMON.crpo_common import *
from SCRIPTS.CRPO_COMMON.credentials import *
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.COMMON.api_requests_for_reports import *

reports = {
    'job_report': {'output_path': output_path_applicant_report, 'expected_input_path': input_path_applicant_report,
                   'actual_input_path': input_path_applicant_report_downloaded,
                   'request_payload': getall_applicant_request_payload, 'test_case_count': 48}}
crpo_headers = crpo_common_obj.login_to_crpo(cred_crpo_admin.get('user'), cred_crpo_admin.get('password'),
                                             cred_crpo_admin.get('tenant'))
for report_type, request in reports.items():
    try:
        report_obj.writeExcelConfigurations(request.get('output_path'))
        download_api_response = crpo_common_obj.generate_applicant_report(crpo_headers, request.get('request_payload'))
        report_obj.downloadReport(crpo_headers, request.get('actual_input_path'), download_api_response)
        write_excel_object.save_result(request.get('output_path'))
        write_excel_object.excelReadExpectedSheet(request.get('expected_input_path'))
        write_excel_object.excelReadActualSheet(request.get('actual_input_path'))
        write_excel_object.excelWriteHeaders(hierarchy_headers_count=3)
        write_excel_object.excelMatchValues(usecase_name=report_type, comparision_required_from_index=1,
                                            total_testcase_count=request.get('test_case_count'))
    except Exception as e:
        print("Please Verify it manually...")
        print(e)
