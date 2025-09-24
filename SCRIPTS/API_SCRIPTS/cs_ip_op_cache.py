import hashlib
import json

from SCRIPTS.CRPO_COMMON.crpo_common import *
from SCRIPTS.CRPO_COMMON.credentials import *
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.ASSESSMENT_COMMON.assessment_common import *
from SCRIPTS.COMMON.environment import *
from SCRIPTS.COMMON.parallel_execution import *
import threading
from SCRIPTS.COMMON.redis_connection import *


class CodingCompiler:
    def __init__(self):
        self.write_lock = threading.Lock()
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
        header = ["Test cases", "status", "Question ID","question_type","is_language_wise_schema","is_default_caching",
                  "expected_input_Cache_format", "actual_input_Cache_format", "input ttl duration remaining",
                  "exp_ttl_status","actual_ttl_status", "expected_output_caching_format","actual_output_caching_format",
                  "output ttl duration remaining","exp_ttl_status","actual_ttl_statis"]
        write_excel_object.write_headers_for_scripts(1, 0, header, write_excel_object.black_color_bold)


    def coding_compilation_check(self, token, excel_input):
        app_pref_proc_eval_id = 5903
        crpo_token = crpo_common_obj.login_to_crpo(cred_crpo_admin.get('user'), cred_crpo_admin.get('password'),
                                                   cred_crpo_admin.get('tenant'))
        content = json.dumps({"cacheTestCases": {"isCachingEnabled": True, "cachingDurationInSeconds": 600,
                                                 "taskWaitTimeInQueueInSeconds": 60,
                                                 "maxTaskWaitTimeInQueueInSeconds": 60}})
        if excel_input.get('defaultCaching') =='Yes':
            app_pref_proc_eval_type = 'crpo.launchCsSlaveNode.config_del'
            update_app_preference = CrpoCommon.save_apppreferences(crpo_token, content, app_pref_proc_eval_id,
                                                                   app_pref_proc_eval_type)
        else:
            app_pref_proc_eval_type = 'crpo.launchCsSlaveNode.config'
            update_app_preference = CrpoCommon.save_apppreferences(crpo_token, content, app_pref_proc_eval_id,
                                                                   app_pref_proc_eval_type)
        request = json.dumps({"Type":"crpo.launchCsSlaveNode.config","IsTenantGlobal":True})
        #calling get app preferecne is required to remove the cache.
        CrpoCommon.get_app_preference_generic(crpo_token, request)
        print("____________________________________Started \n \n")
        print(excel_input.get('testCases'))
        print("____________________________________Completed \n \n")
        with self.write_lock:
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
                question_id = int(excel_input.get('questionId'))
                tenant_id = int(excel_input.get('tenantId'))
                language_id = int(excel_input.get('languageId'))
                compilation_message = compilation_results['codingCompileResponse']['compilationMessage']
                if excel_input.get('qnType') == 'generic':
                    hash_value = hash((question_id, tenant_id))
                    cs_hash_id = 'TestCaseInfoCaching' + ":" + str(hash_value)
                    print(cs_hash_id)
                    is_only_input_files = False
                    is_only_sample = None
                    str_to_be_hashed = '%s.%s.%s.%s' % (tenant_id, question_id, is_only_input_files, is_only_sample)
                    hash_key = hashlib.md5(str_to_be_hashed.encode('utf-8')).hexdigest()
                    python_hash = 'CodingQuestionAttachmentContent' + ':' + hash_key
                    print(python_hash)

                elif excel_input.get('qnType') == 'sql':
                    hash_value = hash((question_id, tenant_id,language_id))
                    cs_hash_id = 'TestCaseInfoCaching' + ":" + str(hash_value)
                    print(cs_hash_id)
                    is_only_input_files = False
                    is_only_sample = None
                    str_to_be_hashed = '%s.%s.%s.%s.%s' % (tenant_id, question_id, is_only_input_files, is_only_sample,
                                                           language_id)
                    hash_key = hashlib.md5(str_to_be_hashed.encode('utf-8')).hexdigest()
                    python_hash = 'CodingQuestionAttachmentContent' + ':' + hash_key
                    print(python_hash)
                py_private_key_path = amsin_python_server.get('password')
                py_ssh_user = amsin_python_server.get('user_name')
                py_ssh_port = amsin_python_server.get('port')
                py_ssh_host = amsin_python_server.get('server_ip')
                py_redis_host = py_redis_server.get('redis_host')
                py_redis_port = py_redis_server.get('port')
                cs_ssh_host = amsin_coding_master_server.get('server_ip')
                cs_ssh_port = amsin_coding_master_server.get('port')
                cs_ssh_user = amsin_coding_master_server.get('user_name')
                cs_redis_host = cs_redis_server.get('redis_host')
                cs_redis_port = cs_redis_server.get('port')
                cs_private_key_path = cs_redis_server.get('password')
                redis_connection = create_ssh_client()
                connect_to_py_server = connect_to_server(redis_connection, py_ssh_host, py_ssh_port, py_ssh_user,
                                                         py_private_key_path)
                python_hash_details = run_redis_command(redis_connection, py_redis_host, python_hash, 'GET', redis_port=None)
                python_ttl = run_redis_command(redis_connection, py_redis_host, python_hash, 'TTL', redis_port=None)
                print("this is python get")
                print(python_ttl)

                connect_to_cs_master = connect_to_server(redis_connection, cs_ssh_host, cs_ssh_port, cs_ssh_user,
                                                         cs_private_key_path)
                cs_hash_details = run_redis_command(redis_connection, cs_redis_host, cs_hash_id, 'GET', redis_port=cs_redis_port)
                cs_ttl = run_redis_command(redis_connection, cs_redis_host, cs_hash_id, 'TTL', redis_port=cs_redis_port)
                print("this is CS get")
                print(cs_ttl)
                close_ssh_connection(redis_connection)
                write_excel_object.compare_results_and_write_vertically(excel_input.get('testCases'), None, self.row_size, 0)
                write_excel_object.compare_results_and_write_vertically(excel_input.get('questionId'), None, self.row_size, 2)
                write_excel_object.compare_results_and_write_vertically(excel_input.get('qnType'), None, self.row_size, 3)
                write_excel_object.compare_results_and_write_vertically(excel_input.get('languageSchema'), None, self.row_size, 4)
                write_excel_object.compare_results_and_write_vertically(excel_input.get('defaultCaching'), None, self.row_size,
                                                                        5)

                write_excel_object.compare_results_and_write_vertically(excel_input.get('expectedInputCache'),
                                                                        str(python_hash_details[0]), self.row_size, 6)

                if int(python_ttl[0])>= int(excel_input.get('expectedInputTTL')):
                    py_ttl_status = 'pass'
                else:
                    py_ttl_status = 'fail'
                write_excel_object.compare_results_and_write_vertically(int(python_ttl[0]),
                                                                        None, self.row_size, 8)
                write_excel_object.compare_results_and_write_vertically(excel_input.get('expectedInputTtlStatus'),
                                                                        py_ttl_status, self.row_size, 9)


                write_excel_object.compare_results_and_write_vertically(excel_input.get('expectedOutputCache'),
                                                                        str(cs_hash_details[0]), self.row_size, 11)
                if int(cs_ttl[0])>= int(excel_input.get('expectedOutputTTL')):
                    cs_ttl_status = 'pass'
                else:
                    cs_ttl_status = 'fail'

                write_excel_object.compare_results_and_write_vertically(int(python_ttl[0]),
                                                                        None, self.row_size, 13)

                write_excel_object.compare_results_and_write_vertically(excel_input.get('expectedOutputTtlStatus'),
                                                                        cs_ttl_status, self.row_size, 14)


                write_excel_object.compare_results_and_write_vertically(write_excel_object.current_status, None, self.row_size,
                                                                    1)
            self.row_size += 1


coding_compiler = CodingCompiler()
excel_read_obj.excel_read(input_coding_cache, 0)
excel_data = excel_read_obj.details
print(excel_data)

login_token = assessment_common_obj.login_to_test_v3('Automation152371400389', 'passpass', 'Automation',
                                                     coding_compiler.main_domain)
thread_context(coding_compiler.coding_compilation_check, login_token, excel_data)

# for data in excel_data:
#     coding_compiler.coding_compilation_check(data)
write_excel_object.write_overall_status(testcases_count=10)
