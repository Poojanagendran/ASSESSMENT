import xlsxwriter
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.ASSESSMENT_COMMON.assessment_common import *
from SCRIPTS.CRPO_COMMON.crpo_common import *
from SCRIPTS.COMMON.io_path import *
import time
from SCRIPTS.DB_DELETE.db_cleanup import *


class ChainingOfTwoTests:

    def __init__(self):
        # data clean up is important, b'coz we need to create a candidate everytime to check the create is working fine.
        data_clean_obj.delete_assessment_test_users_for_2testschaining()
        self.started = datetime.datetime.now()
        self.started = self.started.strftime("%Y-%m-%d-%H-%M-%S")
        # self.write_excel = xlsxwriter.Workbook(
        #     'F:\\automation\\PythonWorkingScripts_Output'
        #     '\\Assessment\\Chaining_Automation - ' + self.started + '.xls')
        self.write_excel = xlsxwriter.Workbook(output_path_2tests_chaining + self.started + '.xls')
        self.ws = self.write_excel.add_worksheet()
        self.black_color = self.write_excel.add_format({'font_color': 'black', 'font_size': 9})
        self.red_color = self.write_excel.add_format({'font_color': 'red', 'font_size': 9})
        self.red_color_with_bg = self.write_excel.add_format({'bg_color': 'red', 'font_color': 'black', 'font_size': 9})
        self.green_color = self.write_excel.add_format({'font_color': 'green', 'font_size': 9})
        self.orange_color = self.write_excel.add_format({'font_color': 'orange', 'font_size': 9})
        self.black_color_bold = self.write_excel.add_format({'font_color': 'black', 'bold': True, 'font_size': 9})
        self.over_all_status_pass = self.write_excel.add_format({'font_color': 'green', 'bold': True, 'font_size': 9})
        self.over_all_status_failed = self.write_excel.add_format({'font_color': 'red', 'bold': True, 'font_size': 9})
        self.over_all_status_color = self.over_all_status_pass
        self.over_all_status = 'OVERALL STATUS :- Pass'
        self.ws.write(0, 0, "Chaining Of Two Tests", self.black_color_bold)
        self.ws.write(1, 0, "Testcases", self.black_color_bold)
        self.ws.write(1, 1, "Testcase Status", self.black_color_bold)
        self.ws.write(1, 2, "Test ID", self.black_color_bold)
        self.ws.write(1, 3, "Candidate ID", self.black_color_bold)
        self.ws.write(1, 4, "Login Name", self.black_color_bold)
        self.ws.write(1, 5, "Password", self.black_color_bold)
        self.ws.write(1, 6, "First test is type of ", self.black_color_bold)
        self.ws.write(1, 7, "Is auto test", self.black_color_bold)
        self.ws.write(1, 8, "Is SLC Enabled", self.black_color_bold)
        self.ws.write(1, 9, "T1 Expected Status", self.black_color_bold)
        self.ws.write(1, 10, "T1 Actual Status", self.black_color_bold)

        self.ws.write(1, 11, "Expected - are you expecting next test info?", self.black_color_bold)
        self.ws.write(1, 12, "Actual - Is next test info available in response?", self.black_color_bold)
        self.ws.write(1, 13, "if next test is available, Are you able to login to next test?", self.black_color_bold)
        self.ws.write(1, 14, "Expected domain URL for next test", self.black_color_bold)
        self.ws.write(1, 15, "Actual domain URL for next test", self.black_color_bold)
        self.ws.write(1, 16, "Expected candidate id in second test ", self.black_color_bold)
        self.ws.write(1, 17, "Actual candidate id in second test ", self.black_color_bold)
        self.ws.write(1, 18, "Expected second test id", self.black_color_bold)
        self.ws.write(1, 19, "Actual second test id", self.black_color_bold)
        self.ws.write(1, 20, "Expected second test type", self.black_color_bold)
        self.ws.write(1, 21, "Actual second test type", self.black_color_bold)

        self.ws.write(1, 22, "Expected - Are you able to login via T1 Cretentials", self.black_color_bold)
        self.ws.write(1, 23, "Actual - Are you able to login via T1 Cretentials", self.black_color_bold)
        self.ws.write(1, 24, "2nd Login Expected Cid", self.black_color_bold)
        self.ws.write(1, 25, "2nd Login Acual Cid", self.black_color_bold)
        self.ws.write(1, 26, "2nd Login Expected Testid of T2", self.black_color_bold)
        self.ws.write(1, 27, "2nd Login Acual Testid of T2", self.black_color_bold)

        self.ws.write(1, 28, "2nd Login Expected T2 test type", self.black_color_bold)
        self.ws.write(1, 29, "2nd Login Expected T2 test type", self.black_color_bold)
        self.ws.write(1, 30, "Do you Expect SLC or Auto Test?", self.black_color_bold)
        self.ws.write(1, 31, "IS Actual SLC or AutoTest?", self.black_color_bold)
        self.ws.write(1, 32, "Expected - Are you able to login to T2 via T1 credentials", self.black_color_bold)
        self.ws.write(1, 33, "Actual - Are you able to login to T2 via T1 credentials?", self.black_color_bold)
        self.ws.write(1, 34, "2nd Login Expected URL for T2", self.black_color_bold)
        self.ws.write(1, 35, "2nd Login Acual URL for T2", self.black_color_bold)

    def compare_data(self, expected_data, actual_data):
        if expected_data == actual_data:
            self.color = self.green_color
        else:
            self.color = self.red_color_with_bg
            self.actual_status = 'Fail'
            self.over_all_status_color = self.red_color
            self.actual_status_color = self.red_color
            self.over_all_status = 'OVERALL STATUS :- Fail'

    def final_report(self, row_value, next_test_info, excel_data, next_tu_infos, second_login_nexttest_infos):
        self.actual_status = 'Pass'
        self.actual_status_color = self.green_color

        self.compare_data(next_test_info.get('actualStatus'), excel_data.get('expectedStatus'))
        self.ws.write(row_value, 9, excel_data.get('expectedStatus'), self.black_color)
        self.ws.write(row_value, 10, next_test_info.get('actualStatus'), self.color)

        self.compare_data(excel_data.get('expectingNextTest'), next_test_info.get('nextTestAvailability'))
        self.ws.write(row_value, 11, excel_data.get('expectingNextTest'), self.black_color)
        self.ws.write(row_value, 12, next_test_info.get('nextTestAvailability'), self.color)

        self.compare_data(excel_data.get('expectedDomainUrlForSecondTest'), next_test_info.get('nextTestDomainHost'))
        self.ws.write(row_value, 14, excel_data.get('expectedDomainUrlForSecondTest'), self.black_color)
        self.ws.write(row_value, 15, next_test_info.get('nextTestDomainHost'), self.color)

        if excel_data.get('expectedCandidateId') != 'EMPTY':
            expected_candidate_id_in_next_test = int(excel_data.get('expectedCandidateId'))
        else:
            expected_candidate_id_in_next_test = excel_data.get('expectedCandidateId')

        self.compare_data(expected_candidate_id_in_next_test, next_tu_infos.get('nextTestCandidateId'))
        self.ws.write(row_value, 16, expected_candidate_id_in_next_test, self.black_color)
        self.ws.write(row_value, 17, next_tu_infos.get('nextTestCandidateId'), self.color)

        if excel_data.get('expectedSecondTestId') != 'EMPTY':
            expected_test_id_in_next_test = int(excel_data.get('expectedSecondTestId'))
        else:
            expected_test_id_in_next_test = excel_data.get('expectedSecondTestId')

        self.compare_data(expected_test_id_in_next_test, next_tu_infos.get('nextTestID'))
        self.ws.write(row_value, 18, expected_test_id_in_next_test, self.black_color)
        self.ws.write(row_value, 19, next_tu_infos.get('nextTestID'), self.color)

        self.compare_data(excel_data.get('expectedSecondTestType'), next_tu_infos.get('next_test_type'))
        self.ws.write(row_value, 20, excel_data.get('expectedSecondTestType'), self.black_color)
        self.ws.write(row_value, 21, next_tu_infos.get('next_test_type'), self.color)

        self.compare_data(excel_data.get('secondTimeLoginExpectedStatusofT1'),
                          second_login_nexttest_infos.get('test_user_infos').get('login_staus'))
        self.ws.write(row_value, 22, excel_data.get('secondTimeLoginExpectedStatusofT1'), self.black_color)
        self.ws.write(row_value, 23, second_login_nexttest_infos.get('test_user_infos').get('login_staus'), self.color)

        self.compare_data(excel_data.get('secondTimeLoginExpectedCid'),
                          second_login_nexttest_infos.get('second_login_cid'))
        self.ws.write(row_value, 24, excel_data.get('secondTimeLoginExpectedCid'), self.black_color)
        self.ws.write(row_value, 25, second_login_nexttest_infos.get('second_login_cid'), self.color)

        self.compare_data(excel_data.get('expectedSecondTestId'),
                          second_login_nexttest_infos.get('second_login_test_id'))
        self.ws.write(row_value, 26, excel_data.get('expectedSecondTestId'), self.black_color)
        self.ws.write(row_value, 27, second_login_nexttest_infos.get('second_login_test_id'), self.color)

        self.compare_data(excel_data.get('expectedSecondTestType'),
                          second_login_nexttest_infos.get('second_time_login_t2_test_type'))
        self.ws.write(row_value, 28, excel_data.get('expectedSecondTestType'), self.black_color)
        self.ws.write(row_value, 29, second_login_nexttest_infos.get('second_time_login_t2_test_type'), self.color)

        self.compare_data(excel_data.get('isSlcOrAutoTest'),
                          second_login_nexttest_infos.get('second_login_is_shortlisted'))
        self.ws.write(row_value, 30, excel_data.get('isSlcOrAutoTest'), self.black_color)
        self.ws.write(row_value, 31, second_login_nexttest_infos.get('second_login_is_shortlisted'), self.color)

        self.compare_data(excel_data.get('secondTimeLoginExpectedStatusofT2'),
                          second_login_nexttest_infos.get('second_time_able_to_login_to_t2'))
        self.ws.write(row_value, 32, excel_data.get('secondTimeLoginExpectedStatusofT2'), self.black_color)
        self.ws.write(row_value, 33, second_login_nexttest_infos.get('second_time_able_to_login_to_t2'), self.color)

        self.compare_data(excel_data.get('expectedDomainUrlForSecondTest'),
                          second_login_nexttest_infos.get('login_url'))
        self.ws.write(row_value, 34, excel_data.get('expectedDomainUrlForSecondTest'), self.black_color)
        self.ws.write(row_value, 35, second_login_nexttest_infos.get('login_url'), self.color)

        self.ws.write(row_value, 0, excel_data.get('testCaseInfo'), self.black_color)
        self.ws.write(row_value, 1, self.actual_status, self.actual_status_color)
        self.ws.write(row_value, 2, excel_data.get('primaryTestId'), self.black_color)
        self.ws.write(row_value, 3, excel_data.get('candidateId'), self.black_color)
        self.ws.write(row_value, 4, excel_data.get('loginName'), self.black_color)
        self.ws.write(row_value, 5, excel_data.get('password'), self.black_color)
        self.ws.write(row_value, 6, excel_data.get('firstTestIsTypeOf'), self.black_color)
        self.ws.write(row_value, 7, excel_data.get('isAutoTest'), self.black_color)
        self.ws.write(row_value, 8, excel_data.get('IsSLCEnabled'), self.black_color)
        self.ws.write(row_value, 13, next_tu_infos.get('login_staus'), self.black_color)


chaining_obj = ChainingOfTwoTests()
excel_read_obj.excel_read(input_path_2tests_chaining, 0)
excel_data = excel_read_obj.details
crpo_headers = crpo_common_obj.login_to_crpo(cred_crpo_admin.get('user'), cred_crpo_admin.get('password'),
                                             cred_crpo_admin.get('tenant'))
test_id = 10190
candidate_ids = [1301162, 1301164, 1301163, 1301165]
crpo_common_obj.untag_candidate_by_cid(crpo_headers, test_id, candidate_ids)

test_id = 10192
candidate_ids = [1301162, 1301164, 1301163, 1301165]
crpo_common_obj.untag_candidate_by_cid(crpo_headers, test_id, candidate_ids)

test_id = 10199
candidate_ids = [1301162]
crpo_common_obj.untag_candidate_by_cid(crpo_headers, test_id, candidate_ids)

test_id = 10201
candidate_ids = [1301166]
crpo_common_obj.untag_candidate_by_cid(crpo_headers, test_id, candidate_ids)

test_id = 10209
candidate_ids = [1301162]
crpo_common_obj.untag_candidate_by_cid(crpo_headers, test_id, candidate_ids)

test_id = 10206
candidate_ids = [1301162]
crpo_common_obj.untag_candidate_by_cid(crpo_headers, test_id, candidate_ids)

# test_id = 10211
# candidate_ids = [1301162, 1301164, 1301166]
# crpo_common_obj.untag_candidate(crpo_headers, test_id, candidate_ids)

test_id = 10377
candidate_ids = [1302717]
crpo_common_obj.untag_candidate_by_cid(crpo_headers, test_id, candidate_ids)

test_id = 10379
candidate_ids = [1302717]
crpo_common_obj.untag_candidate_by_cid(crpo_headers, test_id, candidate_ids)

test_id = 10210
candidate_ids = [1301162, 1301163, 1301164, 1301165]
crpo_common_obj.untag_candidate_by_cid(crpo_headers, test_id, candidate_ids)

test_id = 10403
candidate_ids = [1301162]
crpo_common_obj.untag_candidate_by_cid(crpo_headers, test_id, candidate_ids)

# test_id = 10329
# candidate_ids = [1301162]
# crpo_common_obj.untag_candidate(crpo_headers, test_id, candidate_ids)

rowsize = 1
for data in excel_data:
    # domain = data.get('firstTestDomain')
    rowsize = rowsize + 1

    domain = assessment_common_obj.decide_domain(type_of_test=data.get('firstTestIsTypeOf'))
    login_details = assessment_common_obj.login_to_test_v3(login_name=data.get('loginName'),
                                                           password=data.get('password'),
                                                           tenant='automation', domain=domain)
    # print(login_details)

    submit_token = assessment_common_obj.submit_test_result(assessment_token=login_details.get('login_token'),
                                                            domain=domain,
                                                            submit_test_request=data.get('submitTestVariableName'))
    if submit_token:
        # Below condition is required to add scores to the test users only for VET
        if data.get('firstTestIsTypeOf') == 'VET' and data.get('IsCallbackRequired') == 'Yes':
            # print(data.get('scoreCallBack'))
            # print(type(data.get('scoreCallBack')))
            assessment_common_obj.pearson_call_backs(int(data.get('testUserId')), data.get('scoreCallBack'),
                                                     'AUTOMATION')

        # Below condition is to fetch score for non Hirepro and Non VET tests Currently Talentlens is not in use
        elif data.get('firstTestIsTypeOf') != 'VET' or data.get('firstTestIsTypeOf') != 'HP':
            crpo_common_obj.initiate_vendor_score(crpo_headers, data.get('candidateId'),
                                                  int(data.get('primaryTestId')))
            if data.get('firstTestIsTypeOf') == 'TALENTLENS':
                time.sleep(60)
            else:
                time.sleep(10)

        next_test_details = {}
        next_tu_infos1 = {}
        actual_status = "None"
        print(submit_token)
        initiate_automation_resp = assessment_common_obj.initiate_automation(submit_token, data.get('candidateId'),
                                                                             int(data.get('primaryTestId')),
                                                                             domain=domain)
        initiate_automation_data = initiate_automation_resp.get('data')

        # Context ID would be returned from the initiate automation API for Chaining tests
        if initiate_automation_data.get('contextId'):
            print("this is chaining test")
            polling_api_response = assessment_common_obj.get_job_status(submit_token,
                                                                        initiate_automation_data.get('contextId'))
            if polling_api_response['data']['JobState'] == "SUCCESS":
                # once Job status is success, we are processing the response below
                print(polling_api_response)
                next_test_details = assessment_common_obj.process_next_test_links_for_chaining(polling_api_response,
                                                                                               previous_domain=domain)

                # print(next_test_details)
                # Actual Status Shortlisted means - SLC tests and EMPTY means AutoTest
                if next_test_details.get('actualStatus') == 'Shortlisted' or next_test_details.get(
                        'actualStatus') == 'EMPTY':
                    # below loign to test is needed only for T2 login
                    next_tu_infos1 = assessment_common_obj.login_to_test_v3(
                        login_name=next_test_details.get('next_test_login_id'),
                        password=next_test_details.get('next_test_pwd'),
                        tenant='automation',
                        domain=next_test_details.get('nextTestDomainHost'))
                    next_tu_infos1 = next_tu_infos1.get('test_user_infos')

                # Below line is for Rejected case
                else:
                    next_tu_infos1 = {'nextTestID': 'EMPTY',
                                      'nextTestName': 'EMPTY',
                                      'nextTestCandidateId': 'EMPTY', 'login_staus': 'EMPTY', 'next_test_type': 'EMPTY'}

        # Below line handles Non chaining test, currently for our test its not needed but for handling purpose condition is  added
        else:
            print("this is not a chaining test")
            next_tu_infos1 = {'nextTestID': 'EMPTY', 'nextTestName': 'EMPTY', 'nextTestCandidateId': 'EMPTY',
                              'login_staus': 'EMPTY', 'next_test_type': 'EMPTY'}

        print('T2 Login via T1 Credentials')
        second_login_stat = assessment_common_obj.login_to_test_v3(login_name=data.get('loginName'),
                                                                   password=data.get('password'), tenant='automation',
                                                                   domain=domain)

        second_login_infos = second_login_stat
        if second_login_stat.get('login_response').get('status') == 'KO':
            if second_login_stat.get('login_response').get('error').get('isAutoTest'):
                nextTestFlags = second_login_stat.get('login_response').get('error').get('nextTestFlags')
                if nextTestFlags.get('isShortlisted') == False:
                    second_login_nexttest_infos = {'second_login_cid': 'EMPTY',
                                                   'second_login_test_id': 'EMPTY',
                                                   'second_test_login_id': 'EMPTY',
                                                   'second_test_password': 'EMPTY',
                                                   'login_url': 'EMPTY',
                                                   'second_login_is_shortlisted': 'EMPTY'}

                    t2_status = {'second_time_able_to_login_to_t2': 'No',
                                 'second_time_login_t2_test_type': 'EMPTY'}
                    second_login_nexttest_infos.update(t2_status)
                else:
                    print("Second Login Block Entred")
                    second_login_nexttest_infos = assessment_common_obj.next_test_info_for_2nd_login(
                        login_name=data.get('loginName'),
                        password=data.get('password'),
                        tenant='automation', domain=second_login_stat.get('domain'))

                    t2_login_second_time = assessment_common_obj.login_to_test_v3(
                        login_name=second_login_nexttest_infos.get('second_test_login_id'),
                        password=second_login_nexttest_infos.get('second_test_password'),
                        tenant='automation',
                        domain=domain)

                    second_time_able_to_login_to_t2 = t2_login_second_time.get('test_user_infos').get('login_staus')

                    second_time_login_t2_test_type = t2_login_second_time.get('test_user_infos').get('next_test_type')
                    t2_status = {'second_time_able_to_login_to_t2': second_time_able_to_login_to_t2,
                                 'second_time_login_t2_test_type': second_time_login_t2_test_type}
                    second_login_nexttest_infos.update(t2_status)
            else:
                second_login_nexttest_infos = {'second_login_cid': 'EMPTY',
                                               'second_login_test_id': 'EMPTY',
                                               'second_test_login_id': 'EMPTY',
                                               'second_test_password': 'EMPTY',
                                               'login_url': 'EMPTY',
                                               'second_login_is_shortlisted': 'EMPTY'}

                t2_status = {'second_time_able_to_login_to_t2': 'No',
                             'second_time_login_t2_test_type': 'EMPTY'}
                second_login_nexttest_infos.update(t2_status)
        second_login_infos.update(second_login_nexttest_infos)
        # print(second_login_nexttest_infos)
        # print(second_login_infos)
        chaining_obj.final_report(rowsize, next_test_details, data, next_tu_infos1, second_login_infos)
    else:
        print("Either unable to submit the test or Submit token is not available")

ended = datetime.datetime.now()
ended = "Ended:- %s" % ended.strftime("%Y-%m-%d-%H-%M-%S")
chaining_obj.ws.write(0, 1, chaining_obj.over_all_status, chaining_obj.over_all_status_color)
chaining_obj.ws.write(0, 2, 'Started:- ' + chaining_obj.started, chaining_obj.black_color_bold)
chaining_obj.ws.write(0, 3, ended, chaining_obj.black_color_bold)
chaining_obj.ws.write(0, 4, "Total_Testcase_Count:- %s" % len(excel_data), chaining_obj.black_color_bold)
chaining_obj.write_excel.close()
