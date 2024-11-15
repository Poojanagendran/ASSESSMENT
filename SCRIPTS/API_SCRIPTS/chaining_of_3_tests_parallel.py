import xlsxwriter
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.CRPO_COMMON.crpo_common import *
from SCRIPTS.ASSESSMENT_COMMON.assessment_common import *
from SCRIPTS.COMMON.io_path import *
import time
from SCRIPTS.DB_DELETE.db_cleanup import *
from SCRIPTS.COMMON.parallel_execution import *


class ChainingOfTests:

    def __init__(self):
        self.row_size = 1
        data_clean_obj.delete_assessment_test_users_for_3tests_chaining()
        self.test_login_informations = {}
        self.started = datetime.datetime.now()
        self.started = self.started.strftime("%Y-%m-%d-%H-%M-%S")
        self.write_excel = xlsxwriter.Workbook(output_path_3tests_chaining + self.started + '.xls')

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
        self.ws.write(1, 0, "Test cases", self.black_color_bold)
        self.ws.write(1, 1, "Test case Status", self.black_color_bold)
        self.ws.write(1, 2, "Use case", self.black_color_bold)
        self.ws.write(1, 3, "Primary Login Name", self.black_color_bold)
        self.ws.write(1, 4, "Primary Password", self.black_color_bold)
        self.ws.write(1, 5, "Expected T1 Test id ", self.black_color_bold)
        self.ws.write(1, 6, "Actual T1 Test id", self.black_color_bold)
        self.ws.write(1, 7, "Expected T2 Test id", self.black_color_bold)
        self.ws.write(1, 8, "Actual T2 Test id", self.black_color_bold)
        self.ws.write(1, 9, "Actual T3 Test id", self.black_color_bold)
        self.ws.write(1, 10, "Expected T3 Test id", self.black_color_bold)

        self.ws.write(1, 11, "Expected T1 Candidate Id", self.black_color_bold)
        self.ws.write(1, 12, "Actual T1 Candidate Id", self.black_color_bold)
        self.ws.write(1, 13, "Expected T2 Candidate Id", self.black_color_bold)
        self.ws.write(1, 14, "Actual T2 Candidate Id", self.black_color_bold)
        self.ws.write(1, 15, "Expected T3 Candidate Id", self.black_color_bold)
        self.ws.write(1, 16, "Actual T3 Candidate Id", self.black_color_bold)

        self.ws.write(1, 17, "Expected T1 test type", self.black_color_bold)
        self.ws.write(1, 18, "Actual T1 test type", self.black_color_bold)
        self.ws.write(1, 19, "Expected T2 test type", self.black_color_bold)
        self.ws.write(1, 20, "Actual T2 test type", self.black_color_bold)
        self.ws.write(1, 21, "Expected T3 test type", self.black_color_bold)
        self.ws.write(1, 22, "Actual T3 test type", self.black_color_bold)

        self.ws.write(1, 23, "Expected T1 Status", self.black_color_bold)
        self.ws.write(1, 24, "Actual T1 Status", self.black_color_bold)
        self.ws.write(1, 25, "Expected T2 Status", self.black_color_bold)
        self.ws.write(1, 26, "Actual T2 Status", self.black_color_bold)

        self.ws.write(1, 27, "Expected - next test info for T1", self.black_color_bold)
        self.ws.write(1, 28, "Actual - next test info for T1", self.black_color_bold)
        self.ws.write(1, 29, "Expected - next test info for T2", self.black_color_bold)
        self.ws.write(1, 30, "Actual - next test info for T2", self.black_color_bold)

        self.ws.write(1, 31, "Expected - T1 - T2 Auto or SLC", self.black_color_bold)
        self.ws.write(1, 32, "Actual - T1 - T2 Auto or SLC", self.black_color_bold)
        self.ws.write(1, 33, "Expected - T2 - T3 Auto or SLC", self.black_color_bold)
        self.ws.write(1, 34, "Actual - T2 - T3 Auto or SLC", self.black_color_bold)

        self.ws.write(1, 35, "Expected - Domain for t2", self.black_color_bold)
        self.ws.write(1, 36, "Actual - Domain for t2", self.black_color_bold)
        self.ws.write(1, 37, "Expected - Domain for t3", self.black_color_bold)
        self.ws.write(1, 38, "Actual - Domain for t3", self.black_color_bold)

    def compare_data(self, expected_data, actual_data):
        if expected_data == actual_data:
            self.color = self.green_color
        else:
            self.color = self.red_color_with_bg
            self.actual_status = 'Fail'
            self.over_all_status_color = self.red_color
            self.actual_status_color = self.red_color
            self.over_all_status = 'OVERALL STATUS :- Fail'

    def final_report(self, row_value, data, login_infos):

        primary_test_actual_data = login_infos.get('test1')
        secondtest_actual_data = login_infos.get('test2')
        thirdtest_actual_data = login_infos.get('test3')

        self.actual_status = 'Pass'
        self.actual_status_color = self.green_color
        self.ws.write(row_value, 0, data.get('testCaseInfo'), self.black_color)
        self.ws.write(row_value, 2, data.get('useCase'), self.black_color)
        self.ws.write(row_value, 3, data.get('loginName'), self.black_color)
        self.ws.write(row_value, 4, data.get('password'), self.black_color)

        self.compare_data(data.get('primaryTestId'), primary_test_actual_data.get('test_id'))
        self.ws.write(row_value, 5, data.get('primaryTestId'), self.black_color)
        self.ws.write(row_value, 6, primary_test_actual_data.get('test_id'), self.color)

        self.compare_data(data.get('secondTestId'), secondtest_actual_data.get('test_id'))
        self.ws.write(row_value, 7, data.get('secondTestId'), self.black_color)
        self.ws.write(row_value, 8, secondtest_actual_data.get('test_id'), self.color)

        self.compare_data(data.get('thirdTestId'), thirdtest_actual_data.get('test_id'))
        self.ws.write(row_value, 9, data.get('thirdTestId'), self.black_color)
        self.ws.write(row_value, 10, thirdtest_actual_data.get('test_id'), self.color)

        self.compare_data(data.get('candidateId'), primary_test_actual_data.get('cid'))
        self.ws.write(row_value, 11, data.get('candidateId'), self.black_color)
        self.ws.write(row_value, 12, primary_test_actual_data.get('cid'), self.color)

        self.compare_data(data.get('candidateId2'), secondtest_actual_data.get('cid'))
        self.ws.write(row_value, 13, data.get('candidateId2'), self.black_color)
        self.ws.write(row_value, 14, secondtest_actual_data.get('cid'), self.color)

        self.compare_data(data.get('candidateId3'), thirdtest_actual_data.get('cid'))
        self.ws.write(row_value, 15, data.get('candidateId3'), self.black_color)
        self.ws.write(row_value, 16, thirdtest_actual_data.get('cid'), self.color)

        self.compare_data(data.get('firstTestIsTypeOf'), primary_test_actual_data.get('test_type_for_test'))
        self.ws.write(row_value, 17, data.get('firstTestIsTypeOf'), self.black_color)
        self.ws.write(row_value, 18, primary_test_actual_data.get('test_type_for_test'), self.color)

        self.compare_data(data.get('secondTestIsTypeOf'), secondtest_actual_data.get('test_type_for_test'))
        self.ws.write(row_value, 19, data.get('secondTestIsTypeOf'), self.black_color)
        self.ws.write(row_value, 20, secondtest_actual_data.get('test_type_for_test'), self.color)

        self.compare_data(data.get('thirdTestIsTypeOf'), thirdtest_actual_data.get('test_type_for_test'))
        self.ws.write(row_value, 21, data.get('thirdTestIsTypeOf'), self.black_color)
        self.ws.write(row_value, 22, thirdtest_actual_data.get('test_type_for_test'), self.color)

        self.compare_data(data.get('expectedStatusofT1'), secondtest_actual_data.get('next_test_status'))
        self.ws.write(row_value, 23, data.get('expectedStatusofT1'), self.black_color)
        self.ws.write(row_value, 24, secondtest_actual_data.get('next_test_status'), self.color)

        self.compare_data(data.get('expectedStatusofT2'), thirdtest_actual_data.get('next_test_status'))
        self.ws.write(row_value, 25, data.get('expectedStatusofT2'), self.black_color)
        self.ws.write(row_value, 26, thirdtest_actual_data.get('next_test_status'), self.color)
        #
        self.compare_data(data.get('expectingNextTestForT1'), secondtest_actual_data.get('nextTestAvailability'))
        self.ws.write(row_value, 27, data.get('expectingNextTestForT1'), self.black_color)
        self.ws.write(row_value, 28, secondtest_actual_data.get('nextTestAvailability'), self.color)

        self.compare_data(data.get('expectingNextTestForT2'), thirdtest_actual_data.get('nextTestAvailability'))
        self.ws.write(row_value, 29, data.get('expectingNextTestForT2'), self.black_color)
        self.ws.write(row_value, 30, thirdtest_actual_data.get('nextTestAvailability'), self.color)
        #
        self.compare_data(data.get('IsT1SlcOrAutoTest '), secondtest_actual_data.get('is_slc_or_auto'))
        self.ws.write(row_value, 31, data.get('IsT1SlcOrAutoTest '), self.black_color)
        self.ws.write(row_value, 32, secondtest_actual_data.get('is_slc_or_auto'), self.color)

        self.compare_data(data.get('IsT2SlcOrAutoTest '), thirdtest_actual_data.get('is_slc_or_auto'))
        self.ws.write(row_value, 33, data.get('IsT2SlcOrAutoTest '), self.black_color)
        self.ws.write(row_value, 34, thirdtest_actual_data.get('is_slc_or_auto'), self.color)

        self.compare_data(data.get('secondTestDomain'), secondtest_actual_data.get('domain'))
        self.ws.write(row_value, 35, data.get('secondTestDomain'), self.black_color)
        self.ws.write(row_value, 36, secondtest_actual_data.get('domain'), self.color)

        self.compare_data(data.get('thirdTestDomain'), thirdtest_actual_data.get('domain'))
        self.ws.write(row_value, 37, data.get('thirdTestDomain'), self.black_color)
        self.ws.write(row_value, 38, thirdtest_actual_data.get('domain'), self.color)

        self.ws.write(row_value, 1, self.actual_status, self.actual_status_color)

    def recursive_login(self, login_info, test_id_count, current_row_of_excel_data):
        global do_you_want_to_login_with_first_test
        test_id_data = login_info.get('test' + str(test_id_count))
        if do_you_want_to_login_with_first_test == 'Yes':
            print("Need to Login with T1 Credentials")
            test_id_data = login_info.get('test1')
        print(test_id_data)

        login_details = assessment_common_obj.login_to_test_v2(login_name=test_id_data.get('login_id'),
                                                               password=test_id_data.get('password'),
                                                               tenant='automation',
                                                               domain=test_id_data.get('domain'))
        login_response_data = login_details.get('login_response')
        if login_response_data.get('status') == 'OK':
            print(test_id_data.get('submit_test_var_name'))
            # print(test_id_data.get('submitTestVariableName' + str(test_id_count)))
            submit_test_results = assessment_common_obj.submit_test_result(
                assessment_token=login_details.get('login_token'),
                domain=test_id_data.get('domain'),
                submit_test_request=test_id_data.get('submit_test_var_name'))
            if submit_test_results:

                # print(test_id_data.get('test_type_for_test'))
                if test_id_data.get('test_type_for_test') == 'versant' and test_id_data.get(
                        'is_callback_req_for_test') == 'Yes':
                    assessment_common_obj.pearson_call_backs(int(test_id_data.get('tu_id')),
                                                             test_id_data.get('score_callback'), 'AUTOMATION')

                # Below condition is to fetch score for non Hirepro and Non VET tests Currently Talentlens is not in use
                elif test_id_data.get('test_type_for_test') != 'VET' and test_id_data.get('test_type_for_test') != 'HP':
                    crpo_common_obj.initiate_vendor_score(crpo_headers, test_id_data.get('cid'),
                                                          int(test_id_data.get('test_id')))
                    if test_id_data.get('test_type_for_test') == 'TALENTLENS':
                        time.sleep(60)
                    else:
                        time.sleep(10)

                next_test_details = {}
                next_tu_infos1 = {}
                actual_status = "None"
                initiate_automation_resp = assessment_common_obj.initiate_automation(submit_test_results,
                                                                                     test_id_data.get('cid'),
                                                                                     int(test_id_data.get('test_id')),
                                                                                     domain=test_id_data.get('domain'))
                initiate_automation_data = initiate_automation_resp.get('data')
                # Context ID would be returned from the initiate automation API for Chaining tests
                if initiate_automation_data.get('contextId'):
                    do_you_want_to_login_with_first_test = 'No'
                    print("this is chaining test")
                    polling_api_response = assessment_common_obj.get_job_status(submit_test_results,
                                                                                initiate_automation_data.get(
                                                                                    'contextId'))
                    if polling_api_response['data']['JobState'] == "SUCCESS":
                        # once Job status is success, we are processing the response below
                        next_test_details = assessment_common_obj.process_next_test_links_for_chaining(
                            polling_api_response,
                            previous_domain=test_id_data.get('domain'))
                        if next_test_details.get('actualStatus') == 'Shortlisted' or next_test_details.get(
                                'actualStatus') == 'EMPTY':
                            login_details = assessment_common_obj.login_to_test_v2(
                                login_name=next_test_details.get('next_test_login_id'),
                                password=next_test_details.get('next_test_pwd'), tenant='automation',
                                domain=next_test_details.get('nextTestDomainHost'))
                            login_det = login_details.get('login_response')
                            test_id_count = test_id_count + 1
                            login_config = json.loads(login_det.get('Config'))
                            test_type = login_config.get('thirdPartyTestType')
                            if not test_type:
                                test_type = 'HP'
                            self.login_infos.update({
                                'test' + str(test_id_count): {'login_id': next_test_details.get('next_test_login_id'),
                                                              'password': next_test_details.get('next_test_pwd'),
                                                              'cid': login_det.get('CandidateId'),
                                                              'test_id': login_det.get('TestId'),
                                                              'test_type_for_test': test_type,
                                                              'is_callback_req_for_test': current_row_of_excel_data.get(
                                                                  'IsCallbackRequired' + str(test_id_count)),
                                                              'domain': next_test_details.get('nextTestDomainHost'),
                                                              'submit_test_var_name': current_row_of_excel_data.get(
                                                                  'submitTestVariableName' + str(test_id_count)),
                                                              'tu_id': int(current_row_of_excel_data.get(
                                                                  'testUserId' + str(test_id_count))),
                                                              'score_callback': current_row_of_excel_data.get(
                                                                  'scoreCallBack' + str(test_id_count)),
                                                              'next_test_status': next_test_details.get(
                                                                  'actualStatus'),
                                                              'is_slc_or_auto': next_test_details.get(
                                                                  'is_slc_or_auto'),
                                                              'nextTestAvailability': next_test_details.get(
                                                                  'nextTestAvailability')}})

                        else:
                            test_id_count = test_id_count + 1
                            do_you_want_to_login_with_first_test = 'Yes'
                            self.login_infos.update({
                                'test' + str(test_id_count): {'login_id': 'EMPTY', 'password': 'EMPTY',
                                                              'cid': 'EMPTY', 'test_id': 'EMPTY',
                                                              'test_type_for_test': 'EMPTY',
                                                              'is_callback_req_for_test': 'EMPTY',
                                                              'domain': 'EMPTY',
                                                              'submit_test_var_name': 'EMPTY',
                                                              'tu_id': 'EMPTY', 'score_callback': 'EMPTY',
                                                              'next_test_status': 'Rejected',
                                                              'is_slc_or_auto': 'EMPTY',
                                                              'nextTestAvailability': 'No'}})


                else:
                    test_id_count = test_id_count + 1
                    do_you_want_to_login_with_first_test = 'Yes'
                    self.login_infos.update({
                        'test' + str(test_id_count): {'login_id': 'EMPTY', 'password': 'EMPTY',
                                                      'cid': 'EMPTY', 'test_id': 'EMPTY',
                                                      'test_type_for_test': 'EMPTY',
                                                      'is_callback_req_for_test': 'EMPTY',
                                                      'domain': 'EMPTY',
                                                      'submit_test_var_name': 'EMPTY',
                                                      'tu_id': 'EMPTY', 'score_callback': 'EMPTY',
                                                      'next_test_status': 'EMPTY', 'is_slc_or_auto': 'EMPTY',
                                                      'nextTestAvailability': 'No'}})

        else:
            test_id_count = test_id_count + 1
            do_you_want_to_login_with_first_test = 'Yes'
            self.login_infos.update({
                'test' + str(test_id_count): {'login_id': 'EMPTY', 'password': 'EMPTY',
                                              'cid': 'EMPTY', 'test_id': 'EMPTY',
                                              'test_type_for_test': 'EMPTY',
                                              'is_callback_req_for_test': 'EMPTY',
                                              'domain': 'EMPTY',
                                              'submit_test_var_name': 'EMPTY',
                                              'tu_id': 'EMPTY', 'score_callback': 'EMPTY',
                                              'next_test_status': 'EMPTY', 'is_slc_or_auto': 'EMPTY',
                                              'nextTestAvailability': 'No'}})

    def process_test_case(self, data):
        print('_________________________________________________________________________')
        self.row_size = self.row_size + 1
        self.login_infos = {}
        # test_count = current_test_case + 1
        # data = excel_data[testcases]
        # data = testcases
        domain = assessment_common_obj.decide_domain(type_of_test=data.get('firstTestIsTypeOf'))
        self.login_infos.update({'test1': {'login_id': data.get('loginName'), 'password': data.get('password'),
                                      'cid': int(data.get('candidateId')),
                                      'test_id': int(data.get('primaryTestId')),
                                      'test_type_for_test': data.get('firstTestIsTypeOf'),
                                      'is_callback_req_for_test': data.get('IsCallbackRequired'),
                                      'domain': domain,
                                      'submit_test_var_name': data.get('submitTestVariableName1'),
                                      'tu_id': int(data.get('testUserId')),
                                      'score_callback': data.get('scoreCallBack'),
                                      'next_test_status': 'ThisISFirstTest_NA'}})
        for test_iter_count in range(0, int(data.get('chainingOfHowManyTests'))):
            test_count = test_iter_count + 1
            chaining_obj.recursive_login(self.login_infos, test_count, data)

        print(self.login_infos)
        chaining_obj.final_report(self.row_size, data, self.login_infos)


chaining_obj = ChainingOfTests()
# input_file_path = 'F:\\automation\\PythonWorkingScripts_InputData\\Assessment\\chaining\\3_tests_login_automation.xls'
crpo_headers = crpo_common_obj.login_to_crpo(cred_crpo_admin.get('user'), cred_crpo_admin.get('password'),
                                             cred_crpo_admin.get('tenant'))
excel_read_obj.excel_read(input_path_3tests_chaining, 1)
excel_data = excel_read_obj.details
total_tcs = len(excel_data)
do_you_want_to_login_with_first_test = 'Yes'
thread_context_for_chaining(chaining_obj.process_test_case, excel_data)
# for current_test_case in range(0, total_tcs):


ended = datetime.datetime.now()
ended = "Ended:- %s" % ended.strftime("%Y-%m-%d-%H-%M-%S")
chaining_obj.ws.write(0, 1, chaining_obj.over_all_status, chaining_obj.over_all_status_color)
chaining_obj.ws.write(0, 2, 'Started:- ' + chaining_obj.started, chaining_obj.black_color_bold)
chaining_obj.ws.write(0, 3, ended, chaining_obj.black_color_bold)
chaining_obj.ws.write(0, 4, "Total_Testcase_Count:- %s" % len(excel_data), chaining_obj.black_color_bold)
chaining_obj.write_excel.close()
