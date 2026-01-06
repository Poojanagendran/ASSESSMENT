import time
import json
import urllib3

from SCRIPTS.COMMON.read_excel import excel_read_obj
from SCRIPTS.COMMON.write_excel_new import write_excel_object
from SCRIPTS.CRPO_COMMON.credentials import cred_crpo_admin
from SCRIPTS.CRPO_COMMON.crpo_common import crpo_common_obj, CrpoCommon
from SCRIPTS.ASSESSMENT_COMMON.assessment_common import *
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.DB_DELETE.sanitizeapi_resetuser_2_new import reset_test_user_obj

urllib3.disable_warnings()


class SanitizeAutomation:

    def __init__(self):
        reset_test_user_obj.reset_test_users()
        self.row_size = 2

        write_excel_object.save_result(output_path_sanitize_test_automation)

        write_excel_object.write_headers_for_scripts(
            0, 0,
            ["Sanitize relogin automation"],
            write_excel_object.black_color_bold
        )

        headers = [
            "Testcases", "Status",
            "Test ID", "Candidate ID", "Test User ID", "Case Number",
            "ExpectedUsecase", "ActualUsecase",
            "ExpectedMessage", "ActualMessage",
            "ExpectedTestUserStatus", "ActualTestUserStatus",
            "ExpectedApplicantStatus", "ActualApplicantStatus",
            "ExpectedScoreStatus", "ActualScoreStatus",
            "IsCandidateTaggedToT2(Expected)", "IsCandidateTaggedToT2(actual)",
            "isVendorTest", "IsSLCEnabled",
            "ExpectedDryRun", "ActualDryRun"
        ]

        write_excel_object.write_headers_for_scripts(
            1, 0,
            headers,
            write_excel_object.black_color_bold
        )

    # --------------------------------------------------
    def excel_write(self, data):
        write_excel_object.current_status = "Pass"
        write_excel_object.current_status_color = write_excel_object.green_color

        write_excel_object.compare_results_and_write_vertically(
            data.get('testCaseInfo'), None, self.row_size, 0
        )
        write_excel_object.compare_results_and_write_vertically(
            data.get('primaryTestId'), None, self.row_size, 2
        )
        write_excel_object.compare_results_and_write_vertically(
            data.get('candidateId'), None, self.row_size, 3
        )
        write_excel_object.compare_results_and_write_vertically(
            data.get('testUserID'), None, self.row_size, 4
        )
        write_excel_object.compare_results_and_write_vertically(
            data.get('caseNumber'), None, self.row_size, 5
        )
        write_excel_object.compare_results_and_write_vertically(
            data.get('useCase'),
            data.get('ActualUsecase'),
            self.row_size, 6
        )
        write_excel_object.compare_results_and_write_vertically(
            data.get('message'),
            data.get('ActualMessage'),
            self.row_size, 8
        )
        write_excel_object.compare_results_and_write_vertically(
            data.get('testUserStatus'),
            data.get('ActualTestUserStatus'),
            self.row_size, 10
        )
        write_excel_object.compare_results_and_write_vertically(
            data.get('ApplicantStatus'),
            data.get('ActualApplicantStatus'),
            self.row_size, 12
        )
        write_excel_object.compare_results_and_write_vertically(
            data.get('scoreStatus'),
            data.get('ActualScoreStatus'),
            self.row_size, 14
        )
        write_excel_object.compare_results_and_write_vertically(
            data.get('IsCandidateTaggedToT2'),
            data.get('IsCandidateTaggedToT2(actual)'),
            self.row_size, 16
        )
        write_excel_object.compare_results_and_write_vertically(
            data.get('isVendorTest'), None, self.row_size, 18
        )
        write_excel_object.compare_results_and_write_vertically(
            data.get('IsSLCEnabled'), None, self.row_size, 19
        )
        write_excel_object.compare_results_and_write_vertically(
            data.get('dryRun'),
            data.get('ActualDryRun'),
            self.row_size, 20
        )
        write_excel_object.compare_results_and_write_vertically(
            write_excel_object.current_status, None, self.row_size, 1
        )

        self.row_size += 1

    # --------------------------------------------------
    @staticmethod
    def find_excel_row(test_user_id, excel_data):
        for row in excel_data:
            if int(row.get('testUserID')) == int(test_user_id):
                return row
        return None

    # --------------------------------------------------
    @staticmethod
    def latest_applicant_status(token, candidate_id, applicant_id):
        resp = crpo_common_obj.get_applicant_infos(token, candidate_id)
        for a in resp['data'][0]['ApplicantDetails']:
            if a.get('Id') == applicant_id:
                return a['ApplicantHistory'][-1]['Status']
        return "Unknown"

    # --------------------------------------------------
    @staticmethod
    def check_task_status(token, context_id):
        job = CrpoCommon.job_status_v2(token, context_id)
        return job['data']['JobState']

    # --------------------------------------------------
    def poll_sanitize_job(self, token, context_id):
        time.sleep(10)
        for _ in range(10):
            if self.check_task_status(token, context_id) == "PENDING":
                time.sleep(30)
            else:
                return

    # --------------------------------------------------
    @staticmethod
    def untag_candidate(token, test_id, candidate_id):
        if not test_id:
            return "NotExist"

        tu = crpo_common_obj.search_test_user_by_cid_and_testid(
            token, candidate_id, test_id
        )

        tu_id = tu.get('testUserId')
        if tu_id and tu_id != 'NotExist':
            crpo_common_obj.untag_candidate(
                token, [{"testUserIds": [tu_id]}]
            )
            return "Found"

        return "NotExist"

    # --------------------------------------------------
    def process_dryrun_result(self, dryrun_response, excel_data):
        if not isinstance(dryrun_response, list):
            return

        for item in dryrun_response:
            test_user_id = item.get('testUserId')
            response = item.get('response', {})
            data = response.get('data', {})

            if not test_user_id:
                continue

            excel_row = self.find_excel_row(test_user_id, excel_data)
            if not excel_row:
                continue

            excel_row['ActualDryRun'] = json.dumps(data, indent=2)

    # --------------------------------------------------
    def process_test_user(self, sanitised, excel_data, token):
        test_user_id = sanitised.get('testUserId')
        response = sanitised.get('response', {})

        excel_row = self.find_excel_row(test_user_id, excel_data)
        if not excel_row:
            return

        candidate_id = int(excel_row['candidateId'])
        applicant_id = int(excel_row['applicantId'])
        test2_id = int(excel_row.get('untagUserFromT2', 0))

        excel_row['ActualUsecase'] = 'NULL'
        excel_row['ActualMessage'] = 'NULL'
        context_id = None

        if isinstance(response, dict):
            if isinstance(response.get('data'), dict):
                excel_row['ActualUsecase'] = response['data'].get('UseCasePassed', 'NULL')
                excel_row['ActualMessage'] = response['data'].get('Message', 'NULL')
                context_id = response['data'].get('ContextId')
            elif 'message' in response:
                excel_row['ActualMessage'] = response.get('message', 'NULL')

        if context_id:
            self.poll_sanitize_job(token, context_id)

        try:
            tc = crpo_common_obj.tests_against_candidate(token, candidate_id)
            info = tc['data']['TestsAgainstCandidate'][0]

            excel_row['ActualTestUserStatus'] = info.get('StatusText', 'NA')
            excel_row['ActualScoreStatus'] = (
                "Available"
                if info.get('TotalScore') not in [None, "null"]
                else "Not Available"
            )
        except Exception as e:
            print(f"[WARN] tests_against_candidate failed for {candidate_id}: {e}")
            excel_row['ActualTestUserStatus'] = 'NA'
            excel_row['ActualScoreStatus'] = 'NA'

        excel_row['ActualApplicantStatus'] = self.latest_applicant_status(
            token, candidate_id, applicant_id
        )

        excel_row['IsCandidateTaggedToT2(actual)'] = self.untag_candidate(
            token, test2_id, candidate_id
        )

        self.excel_write(excel_row)


# ==================================================
# MAIN EXECUTION
# ==================================================

re_initiate_obj = SanitizeAutomation()

excel_read_obj.excel_read(input_path_sanitize_automation, 1)
excel_data = excel_read_obj.details

crpo_headers = crpo_common_obj.login_to_crpo(
    cred_crpo_admin['user'],
    cred_crpo_admin['password'],
    cred_crpo_admin['tenant']
)

unique_test_ids = {
    int(row['primaryTestId'])
    for row in excel_data
    if row.get('primaryTestId')
}

for test_id in unique_test_ids:
    print(f"\n===== Dry-run Sanitizing Test ID: {test_id} =====")

    dryrun_response = crpo_common_obj.sanitise_test_automation_test_level_dryrun(
        crpo_headers, test_id
    )
    print(dryrun_response)

    re_initiate_obj.process_dryrun_result(dryrun_response, excel_data)

    print(f"\n===== Executing Sanitization for Test ID: {test_id} =====")
    result = crpo_common_obj.sanitise_test_automation_test_level_execute(
        crpo_headers, test_id
    )

    for sanitised in result:
        re_initiate_obj.process_test_user(
            sanitised, excel_data, crpo_headers
        )

write_excel_object.write_overall_status(
    testcases_count=len(excel_data)
)
