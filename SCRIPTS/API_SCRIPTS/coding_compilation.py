from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.ASSESSMENT_COMMON.assessment_common import *
from SCRIPTS.COMMON.environment import *


class CodingCompiler:
    def __init__(self):
        self.main_domain = env_obj.domain
        requests.packages.urllib3.disable_warnings()
        self.started = datetime.datetime.now()
        self.started = self.started.strftime("%Y-%M-%d-%H-%M-%S")
        self.row_size = 2
        write_excel_object.save_result(output_coding_compiler)
        # 0th Row Header
        header = ["Coding compilation Check"]
        write_excel_object.write_headers_for_scripts(0, 0, header, write_excel_object.black_color_bold)
        # 1st Row Header
        header = ["Test cases", "status", "Login_Id", "Password", "TestID", "CandidateID",
                  "LanguageId", "QuestionId", "Code", "Expected Compilation Message", "Actual Compilation Message",
                  "Expected Testcase1 Error Message", "Actual Testcase1 Error Message",
                  "Expected Testcase1 - is System test Case?", "Actual Testcase1 - is System test Case?",
                  "Expected - Testcase1 Output", "Actual - Testcase1 Output", "Expected - Testcase1  System Input",
                  "Actual - Testcase1 System Input", "Expected - Testcase1 System Output",
                  "Actual - Testcase1 System Output", "Expected - Testcase1 Result", "Actual - Testcase1 Result",
                  "Expected - Testcase1 Reason", "Actual - Testcase1 Reason", "Testcase1 Memory", "Testcase1 Time",
                  "Expected Testcase2 Error Message", "Actual Testcase2 Error Message",
                  "Expected Testcase2 - is System test Case?", "Actual Testcase2 - is System test Case?",
                  "Expected - Testcase2 Output", "Actual - Testcase2 Output", "Expected - Testcase2 System Input",
                  "Actual - Testcase2 System Input", "Expected - Testcase2 System Output",
                  "Actual - Testcase2 System Output", "Expected - Testcase2 Result", "Actual - Testcase2 Result",
                  "Expected - Testcase2 Reason", "Actual - Testcase2 Reason", "Testcase2 Memory", "Testcase2 Time"]
        write_excel_object.write_headers_for_scripts(1, 0, header, write_excel_object.black_color_bold)

    def coding_compilation_check(self, excel_input):
        print(excel_input.get('testCases'))
        write_excel_object.current_status_color = write_excel_object.green_color
        write_excel_object.current_status = "Pass"
        # write_excel_object.current_status_color = write_excel_object.green_color
        code_compiler_request = {}
        cid = "%s:%s:%s:%s" % (int(excel_input.get('tenantId')), int(excel_input.get('questionId')),
                               int(excel_input.get('testId')), int(excel_input.get('candidateID')))

        code_data = json.loads(excel_input.get('code'))
        code_data['cid'] = cid
        code_data = json.dumps(code_data)
        code_compiler_request = {
            "action": excel_input.get('action'),
            "TenantId": int(excel_input.get('tenantId')),
            "UserId": "0",
            "cid": cid,
            "languageId": int(excel_input.get('languageId')),
            "disableBlockUI": True,
            "isForTestCaseResult": True,
            "data": code_data
        }
        token = assessment_common_obj.login_to_test_v3(data.get('loginId'), data.get('password'),
                                                       data.get('tenantName'), self.main_domain)

        code_token_result = assessment_common_obj.code_compiler(token.get('login_token'), request=code_compiler_request)
        print(code_token_result)
        code_token = code_token_result.get('codeToken')
        if code_token:
            compilation_result_request = {"codeToken": code_token, "TenantId": int(excel_input.get('tenantId')),
                                          "UserId": "0",
                                          "cid": cid,
                                          "languageId": int(excel_input.get('languageId')), "disableBlockUI": True,
                                          "isForTestCaseResult": True,
                                          "debugTimeStamp": "2022-07-07T10:27:47.298Z"}
            compilation_results = assessment_common_obj.code_compiler_get_result(token.get('login_token'),
                                                                                 compilation_result_request)
            # print(compilation_results)
            compilation_message = compilation_results['codingCompileResponse']['compilationMessage']
            testcases_results = compilation_results['testCaseResults']
            total_tcs_results = []
            for tcs in testcases_results:
                tc_result = tcs.get("testCaseResult")
                tc_memory = tcs.get("memory")
                tc_time = tcs.get("time")
                if not tcs.get("reason"):
                    tc_reason = "EMPTY"
                else:
                    tc_reason = tcs.get("reason")

                if not tcs['isSystem']:
                    is_system = "NO"
                    tc_output = tcs.get("output")
                    tc_system_input = tcs.get("sysInput")
                    tc_system_output = tcs.get("sysOutput")
                    if not tcs.get("error"):
                        tc_error = "EMPTY"
                    else:
                        tc_error = tcs.get("error")
                else:
                    is_system = "Yes"
                    tc_output = "NA-SystemTC"
                    tc_system_input = "NA-SystemTC"
                    tc_system_output = "NA-SystemTC"
                    tc_error = "NA-SystemTC"

                current_tcs_results = {"tc_result": tc_result, "tc_reason": tc_reason, "is_system": is_system,
                                       "tc_output": tc_output, "tc_system_input": tc_system_input,
                                       "tc_system_output": tc_system_output, "tc_error": tc_error, "memory": tc_memory,
                                       "time": tc_time}
                total_tcs_results.append(current_tcs_results)

            print(total_tcs_results)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('testCases'), None, self.row_size,
                                                                    0)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('loginId'), None, self.row_size, 2)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('password'), None, self.row_size, 3)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('testId'), None, self.row_size, 4)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('candidateID'), None, self.row_size,
                                                                    5)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('languageId'), None, self.row_size,
                                                                    6)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('questionId'), None, self.row_size,
                                                                    7)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('code'), None, self.row_size, 8)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('expectedCompilationMessage'),
                                                                    compilation_message, self.row_size, 9)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('tc1Error'),
                                                                    total_tcs_results[0]['tc_error'], self.row_size, 11)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('tc1IsSystem'),
                                                                    total_tcs_results[0]['is_system'], self.row_size,
                                                                    13)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('tc1Output'),
                                                                    total_tcs_results[0]['tc_output'], self.row_size,
                                                                    15)
            if type(excel_input.get('tc1SystemInput')) != str:
                excel_tc1SystemInput = str(int(excel_input.get('tc1SystemInput')))
            else:
                excel_tc1SystemInput = excel_input.get('tc1SystemInput')

            write_excel_object.compare_results_and_write_vertically(excel_tc1SystemInput,
                                                                    total_tcs_results[0]['tc_system_input'],
                                                                    self.row_size, 17)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('tc1SystemOutput').strip(),
                                                                    total_tcs_results[0]['tc_system_output'].strip(),
                                                                    self.row_size, 19)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('tc1Result'),
                                                                    total_tcs_results[0]['tc_result'], self.row_size,
                                                                    21)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('tc1Reason'),
                                                                    total_tcs_results[0]['tc_reason'], self.row_size,
                                                                    23)

            write_excel_object.compare_results_and_write_vertically(None, total_tcs_results[0]['memory'], self.row_size,
                                                                    25)
            write_excel_object.compare_results_and_write_vertically(None, total_tcs_results[0]['time'], self.row_size,
                                                                    26)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('tc2Error'),
                                                                    total_tcs_results[1]['tc_error'], self.row_size, 27)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('tc2IsSystem'),
                                                                    total_tcs_results[1]['is_system'], self.row_size,
                                                                    29)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('tc2Output'),
                                                                    total_tcs_results[1]['tc_output'], self.row_size,
                                                                    31)

            if type(excel_input.get('tc2SystemInput')) != str:
                excel_tc2SystemInput = str(int(excel_input.get('tc2SystemInput')))
            else:
                excel_tc2SystemInput = excel_input.get('tc2SystemInput')

            write_excel_object.compare_results_and_write_vertically(excel_tc2SystemInput,
                                                                    total_tcs_results[1]['tc_system_input'],
                                                                    self.row_size, 33)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('tc2SystemOutput').strip(),
                                                                    total_tcs_results[1]['tc_system_output'].strip(),
                                                                    self.row_size, 35)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('tc2Result'),
                                                                    total_tcs_results[1]['tc_result'], self.row_size,
                                                                    37)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('tc2Reason'),
                                                                    total_tcs_results[1]['tc_reason'], self.row_size,
                                                                    39)

            write_excel_object.compare_results_and_write_vertically(None, total_tcs_results[1]['memory'], self.row_size,
                                                                    41)
            write_excel_object.compare_results_and_write_vertically(None, total_tcs_results[1]['time'], self.row_size,
                                                                    42)

        write_excel_object.compare_results_and_write_vertically(write_excel_object.current_status, None, self.row_size,
                                                                1)
        self.row_size += 1


coding_compiler = CodingCompiler()
excel_read_obj.excel_read(input_coding_compiler, 0)
excel_data = excel_read_obj.details
for data in excel_data:
    coding_compiler.coding_compilation_check(data)
write_excel_object.write_overall_status(testcases_count=2)
