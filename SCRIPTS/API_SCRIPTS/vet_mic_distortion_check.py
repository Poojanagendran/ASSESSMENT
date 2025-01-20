from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.CRPO_COMMON.crpo_common import *
from SCRIPTS.CRPO_COMMON.credentials import *
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.COMMON.parallel_execution import *


class MicDistortionCheck:

    def __init__(self):
        self.allowed_extensions = [".ogg"]
        requests.packages.urllib3.disable_warnings()
        self.row_size = 2
        write_excel_object.save_result(output_path_mic_check)
        header = ["Mic Distortion Check"]
        write_excel_object.write_headers_for_scripts(0, 0, header, write_excel_object.green_color_bold)
        header = ["Test Case", "Status", "File Name", "Expected Status", "Actual Status", "Exp-DistortionRatio",
                  "Act-DistortionRatio", "Exp - TotalSegments", "Act - TotalSegments", "Exp - VoiceSegments",
                  "Act - VoiceSegments", "Exp - NoiseSegments", "Act - NoiseSegments", "Exp - DistortedSegments",
                  "Act - DistortedSegments", "Exp - ClearSegments", "Act - ClearSegments", "Exp - LoudSegments",
                  "Act - LoudSegments", "Exp - NormalSegments", "Act - NormalSegments", "Exp - LowSegments",
                  "Act - LowSegments", "Exp - PeakChangedSegments", "Act - PeakChangedSegments", "Exp - Rms",
                  "Act - Rms", "Exp - CasesCode", "Act - CasesCode", "Exp - CasesDetected", "Act - CasesDetected",
                  "Exp - Message", "Act - Message"]
        write_excel_object.write_headers_for_scripts(1, 0, header, write_excel_object.green_color_bold)

    def upload_audio_file(self, token, excel_input):
        write_excel_object.current_status_color = write_excel_object.green_color
        write_excel_object.current_status = "Pass"
        file_path = input_path_mic_distortion_files % (excel_input.get('filePathName'))
        file_name = excel_input.get('fileName')
        print(file_name)
        resp = crpo_common_obj.upload_files(token, file_name, file_path)
        http_file_url = resp['data']['fileUrl']
        persistent_save_resp = crpo_common_obj.persistent_save(token, http_file_url)
        persistent_s3_url = persistent_save_resp['data']['SuccessList'][0]['s3_url']
        audio_distortion_response = crpo_common_obj.check_audio_distortion(token, persistent_s3_url)
        print(audio_distortion_response)
        write_excel_object.compare_results_and_write_vertically(excel_input.get('testCases'), None, self.row_size, 0)
        write_excel_object.compare_results_and_write_vertically(excel_input.get('fileName'), None, self.row_size, 2)
        if audio_distortion_response.get('Message') is None:
            write_excel_object.compare_results_and_write_vertically(excel_input.get('result'),
                                                                    audio_distortion_response['Result'], self.row_size,
                                                                    3)
            write_excel_object.compare_results_and_write_vertically(round(excel_input.get('distortionRatio'),4),
                                                                    round(audio_distortion_response['DistortionRatio'],4),
                                                                    self.row_size, 5)
            write_excel_object.compare_results_and_write_vertically(int(excel_input.get('totalSegments')),
                                                                    audio_distortion_response['TotalSegments'],
                                                                    self.row_size, 7)
            write_excel_object.compare_results_and_write_vertically(int(excel_input.get('voiceSegments')),
                                                                    audio_distortion_response['VoiceSegments'],
                                                                    self.row_size, 9)
            write_excel_object.compare_results_and_write_vertically(int(excel_input.get('noiseSegments')),
                                                                    audio_distortion_response['NoiseSegments'],
                                                                    self.row_size, 11)
            write_excel_object.compare_results_and_write_vertically(int(excel_input.get('distortedSegments')),
                                                                    audio_distortion_response['DistortedSegments'],
                                                                    self.row_size, 13)
            write_excel_object.compare_results_and_write_vertically(int(excel_input.get('clearSegments')),
                                                                    audio_distortion_response['ClearSegments'],
                                                                    self.row_size, 15)
            write_excel_object.compare_results_and_write_vertically(int(excel_input.get('loudSegments')),
                                                                    audio_distortion_response['LoudSegments'],
                                                                    self.row_size, 17)
            write_excel_object.compare_results_and_write_vertically(int(excel_input.get('normalSegments')),
                                                                    audio_distortion_response['NormalSegments'],
                                                                    self.row_size, 19)
            write_excel_object.compare_results_and_write_vertically(int(excel_input.get('lowSegments')),
                                                                    audio_distortion_response['LowSegments'],
                                                                    self.row_size, 21)
            write_excel_object.compare_results_and_write_vertically(int(excel_input.get('peakChangedSegments')),
                                                                    audio_distortion_response['PeakChangedSegments'],
                                                                    self.row_size, 23)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('rms'),
                                                                    audio_distortion_response['Rms'], self.row_size, 25)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('caseCode'),
                                                                    str(audio_distortion_response['CasesCode']),
                                                                    self.row_size, 27)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('caseDetected'),
                                                                    str(audio_distortion_response['CasesDetected']),
                                                                    self.row_size, 29)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('message'), "EMPTY", self.row_size,
                                                                    31)
        else:

            write_excel_object.compare_results_and_write_vertically(excel_input.get('result'),
                                                                    audio_distortion_response['Result'], self.row_size,
                                                                    3)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('distortionRatio'), "EMPTY",
                                                                    self.row_size, 5)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('totalSegments'), "EMPTY",
                                                                    self.row_size, 7)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('voiceSegments'), "EMPTY",
                                                                    self.row_size, 9)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('noiseSegments'), "EMPTY",
                                                                    self.row_size, 11)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('distortedSegments'), "EMPTY",
                                                                    self.row_size, 13)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('clearSegments'), "EMPTY",
                                                                    self.row_size, 15)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('loudSegments'), "EMPTY",
                                                                    self.row_size, 17)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('normalSegments'), "EMPTY",
                                                                    self.row_size, 19)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('lowSegments'), "EMPTY",
                                                                    self.row_size, 21)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('peakChangedSegments'), "EMPTY",
                                                                    self.row_size, 23)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('rms'), "EMPTY", self.row_size, 25)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('caseCode'), "EMPTY", self.row_size,
                                                                    27)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('caseDetected'), "EMPTY",
                                                                    self.row_size, 29)
            write_excel_object.compare_results_and_write_vertically(excel_input.get('message'),
                                                                    audio_distortion_response.get('Message'),
                                                                    self.row_size, 31)
        write_excel_object.compare_results_and_write_vertically(write_excel_object.current_status, None, self.row_size,
                                                                1)
        self.row_size += 1


mic_check = MicDistortionCheck()
login_token = crpo_common_obj.login_to_crpo(cred_crpo_admin.get('user'), cred_crpo_admin.get('password'),
                                            cred_crpo_admin.get('tenant'))
# login_token = crpo_common_obj.login_to_crpo('admin', 'At@2023$$', 'at')

excel_read_obj.excel_read(input_path_mic_distortion_check, 0)
excel_data = excel_read_obj.details
thread_context(mic_check.upload_audio_file, login_token, excel_data)
# for data in excel_data:
    # mic_check.upload_audio_file(login_token, data)
write_excel_object.write_overall_status(testcases_count=18)
