import os

from SCRIPTS.COMMON.report import *
from SCRIPTS.CRPO_COMMON.crpo_common import *
from SCRIPTS.CRPO_COMMON.credentials import *
from SCRIPTS.COMMON.api_requests_for_reports import *
import zipfile
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.COMMON.environment import *
class AudioTranscript:
    def __init__(self):
        self.row_size = 2
        write_excel_object.save_result(output_path_audio_transcript)
        header = ["Audio Transcript Of Overall Best Question Summary With CEFR Score"]
        write_excel_object.write_headers_for_scripts(0, 0, header, write_excel_object.black_color_bold)
        header1 = ["Test cases", "Status", "expected vocab", "actual vocab", "expected fluency", "actual fluency",
                   "expected grammar", "actual grammar", "expected overall", "actual overall", "expected coherence",
                   "actual coherence", "expected pronunciation", "actual pronunciation", "expected vocabPercentage",
                   "actual vocabPercentage", "expected fluencyPercentage", "actual fluencyPercentage",
                   "expected grammarPercentage", "actual grammarPercentage", "expected overallPercentage",
                   "actual overallPercentage", "expected coherencePercentage", "actual coherencePercentage",
                   "expected pronunciationPercentage", "actual pronunciationPercentage", "Test ID", "Test User ID",
                   "Tenant Alias","Question1_Id","Q1_expected vocab","Q1_actual vocab","Q1_expected fluency","Q1_actual fluency",
                   "Q1_expected grammar","Q1_actual grammar","Q1_expected overall","Q1_actual overall",
                   "Q1_expected coherence","Q1_actual coherence","Q1_expected pronunciation","Q1_actual pronunciation",
                   "Q1_expected vocabPercentage","Q1_actual vocabPercentage","Q1_expected fluencyPercentage","Q1_actual fluencyPercentage",
                   "Q1_expected grammarPercentage","Q1_actual grammarPercentage","Q1_expected overallPercentage","Q1_actual overallPercentage",
                   "Q1_expected coherencePercentage","Q1_actual coherencePercentage","Q1_expected pronunciationPercentage","Q1_actual pronunciationPercentage",
                   "Question2_Id","Q2_expected vocab","Q2_actual vocab","Q2_expected fluency","Q2_actual fluency","Q2_expected grammar","Q2_actual grammar",
                   "Q2_expected overall","Q2_actual overall","Q2_expected coherence","Q2_actual coherence","Q2_expected pronunciation","Q2_actual pronunciation",
                   "Q2_expected vocabPercentage","Q2_actual vocabPercentage","Q2_expected fluencyPercentage","Q2_actual fluencyPercentage",
                   "Q2_expected grammarPercentage","Q2_actual grammarPercentage","Q2_expected overallPercentage","Q2_actual overallPercentage",
                   "Q2_expected coherencePercentage","Q2_actual coherencePercentage","Q2_expected pronunciationPercentage","Q2_actual pronunciationPercentage"]


        write_excel_object.write_headers_for_scripts(1, 0, header1, write_excel_object.black_color_bold)

    def excel_write(self, data):
        write_excel_object.current_status_color = write_excel_object.green_color
        write_excel_object.current_status = "Pass"
        write_excel_object.compare_results_and_write_vertically(data.get('Test Cases'), None, self.row_size, 0)
        write_excel_object.compare_results_and_write_vertically(data.get('expected vocab',"None"), cefr_data.get('vocab',"None"), self.row_size, 2)
        write_excel_object.compare_results_and_write_vertically(data.get('expected fluency',"None"), cefr_data.get('fluency',"None"), self.row_size, 4)
        write_excel_object.compare_results_and_write_vertically(data.get('expected grammar',"None"), cefr_data.get('grammar',"None"), self.row_size, 6)
        write_excel_object.compare_results_and_write_vertically(data.get('expected overall',"None"), cefr_data.get('overall',"None"), self.row_size, 8)
        write_excel_object.compare_results_and_write_vertically(data.get('expected coherence',"None"), cefr_data.get('coherence',"None"), self.row_size, 10)
        write_excel_object.compare_results_and_write_vertically(data.get('expected pronunciation',"None"), cefr_data.get('pronunciation',"None"), self.row_size, 12)
        write_excel_object.compare_results_and_write_vertically(data.get('expected vocabPercentage',"None"), cefr_data.get('vocabPercentage',"None"), self.row_size, 14)
        write_excel_object.compare_results_and_write_vertically(data.get('expected fluencyPercentage',"None"), cefr_data.get('fluencyPercentage',"None"), self.row_size, 16)
        write_excel_object.compare_results_and_write_vertically(data.get('expected grammarPercentage',"None"), cefr_data.get('grammarPercentage',"None"), self.row_size, 18)
        write_excel_object.compare_results_and_write_vertically(data.get('expected overallPercentage',"None"), cefr_data.get('overallPercentage',"None"), self.row_size, 20)
        write_excel_object.compare_results_and_write_vertically(data.get('expected coherencePercentage',"None"), cefr_data.get('coherencePercentage',"None"), self.row_size, 22)
        write_excel_object.compare_results_and_write_vertically(data.get('expected pronunciationPercentage',"None"), cefr_data.get('pronunciationPercentage',"None"), self.row_size,24)
        write_excel_object.compare_results_and_write_vertically(data.get('Test ID'), None,self.row_size, 26)
        write_excel_object.compare_results_and_write_vertically(data.get('Test User ID'), None,self.row_size, 27)
        write_excel_object.compare_results_and_write_vertically(cred_crpo_admin.get('tenant'), None,self.row_size, 28)
        write_excel_object.compare_results_and_write_vertically(data.get('Question1_Id'), None, self.row_size, 29)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1_expected vocab', "None"),
                                                                question_1_data.get('vocab', "None"), self.row_size, 30)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1_expected fluency', "None"),
                                                                question_1_data.get('fluency', "None"), self.row_size,
                                                                32)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1_expected grammar', "None"),
                                                                question_1_data.get('grammar', "None"), self.row_size,
                                                                34)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1_expected overall', "None"),
                                                                question_1_data.get('overall', "None"), self.row_size,
                                                                36)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1_expected coherence', "None"),
                                                                question_1_data.get('coherence', "None"), self.row_size,
                                                                38)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1_expected pronunciation', "None"),
                                                                question_1_data.get('pronunciation', "None"),
                                                                self.row_size, 40)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1_expected vocabPercentage', "None"),
                                                                question_1_data.get('vocabPercentage', "None"),
                                                                self.row_size, 42)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1_expected fluencyPercentage', "None"),
                                                                question_1_data.get('fluencyPercentage', "None"),
                                                                self.row_size, 44)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1_expected grammarPercentage', "None"),
                                                                question_1_data.get('grammarPercentage', "None"),
                                                                self.row_size, 46)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1_expected overallPercentage', "None"),
                                                                question_1_data.get('overallPercentage', "None"),
                                                                self.row_size, 48)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1_expected coherencePercentage', "None"),
                                                                question_1_data.get('coherencePercentage', "None"),
                                                                self.row_size, 50)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1_expected pronunciationPercentage', "None"),
                                                                question_1_data.get('pronunciationPercentage', "None"),
                                                                self.row_size, 52)
        write_excel_object.compare_results_and_write_vertically(data.get('Question2_Id'), None, self.row_size, 54)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2_expected vocab', "None"),
                                                                question_2_data.get('vocab', "None"), self.row_size, 55)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2_expected fluency', "None"),
                                                                question_2_data.get('fluency', "None"), self.row_size,
                                                                57)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2_expected grammar', "None"),
                                                                question_2_data.get('grammar', "None"), self.row_size,
                                                                59)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2_expected overall', "None"),
                                                                question_2_data.get('overall', "None"), self.row_size,
                                                                61)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2_expected coherence', "None"),
                                                                question_2_data.get('coherence', "None"), self.row_size,
                                                                63)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2_expected pronunciation', "None"),
                                                                question_2_data.get('pronunciation', "None"),
                                                                self.row_size, 65)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2_expected vocabPercentage', "None"),
                                                                question_2_data.get('vocabPercentage', "None"),
                                                                self.row_size, 67)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2_expected fluencyPercentage', "None"),
                                                                question_2_data.get('fluencyPercentage', "None"),
                                                                self.row_size, 69)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2_expected grammarPercentage', "None"),
                                                                question_2_data.get('grammarPercentage', "None"),
                                                                self.row_size, 71)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2_expected overallPercentage', "None"),
                                                                question_2_data.get('overallPercentage', "None"),
                                                                self.row_size, 73)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2_expected coherencePercentage', "None"),
                                                                question_2_data.get('coherencePercentage', "None"),
                                                                self.row_size, 75)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2_expected pronunciationPercentage', "None"),
                                                                question_2_data.get('pronunciationPercentage', "None"),
                                                                self.row_size, 77)
        write_excel_object.compare_results_and_write_vertically(write_excel_object.current_status, None, self.row_size,1)
        self.row_size = self.row_size + 1

audio_transcript_obj=AudioTranscript()
crpo_headers = crpo_common_obj.login_to_crpo(cred_crpo_admin.get('user'), cred_crpo_admin.get('password'),
                                                 cred_crpo_admin.get('tenant'))
#print("crpo_headers_token--", crpo_headers)
excel_read_obj.excel_read(input_audio_transcript_cefr, 0)
excel_data = excel_read_obj.details
#print(excel_data)
#req_payload={'testId':20609,'testUserId':3764377}
for data in excel_data:
    testId = int(data.get('Test ID'))
    testUserId = int(data.get('Test User ID'))
    #print(testId)
    testUserIds = int(data.get('Test User ID'))
    req_payload = {
        'testId': testId,'testUserId': testUserId
        }
    print(req_payload)
    req_payload2 = {
        'testId': testId,'testUserIds': testUserIds
    }
    clear_test_results_response = crpo_common_obj.clear_test_results(crpo_headers,req_payload2)
    re_evaluate_candidate = crpo_common_obj.evaluate_candidate(crpo_headers,req_payload2)
    time.sleep(30)
    audiotranscript_report = crpo_common_obj.audio_transcript(crpo_headers,req_payload)
    #print("audiotranscript_report--", audiotranscript_report)
    cefr_data = audiotranscript_report['data']['overAllBestQuestionSummary']['cefr_score']
    # print(cefr_data)
    # print(cefr_data.get('vocab'))
    question_1_data = audiotranscript_report['data']['assessment']['questionPaper']['questions'][0]['tpScore']['cefr_score']
    question_2_data = audiotranscript_report['data']['assessment']['questionPaper']['questions'][1]['tpScore']['cefr_score']
    #print(question_2_data.get('fluency'))

    audio_transcript_obj.excel_write(data)

write_excel_object.write_overall_status(testcases_count=4)


