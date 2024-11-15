from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.CRPO_COMMON.crpo_common import *
from SCRIPTS.CRPO_COMMON.credentials import *
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.ASSESSMENT_COMMON.assessment_common import *
from SCRIPTS.COMMON.parallel_execution import *
# from concurrent.futures import ThreadPoolExecutor, as_completed


class AllowedFileExtensions:

    def __init__(self):
        requests.packages.urllib3.disable_warnings()
        self.row_size = 2
        write_excel_object.save_result(output_path_brightness_sharpness_check)
        header = ["Brightness and sharpness check"]
        write_excel_object.write_headers_for_scripts(0, 0, header, write_excel_object.black_color_bold)
        header = ["testcase details", "Status", "File Name", "Expected Brightness", "Actual Brightness",
                  "Expected Sharpness", "Actual Sharpness", "Expected Confidence", "Actual Confidence",
                  "Expected Face count", "Actual Face count"]
        write_excel_object.write_headers_for_scripts(1, 0, header, write_excel_object.black_color_bold)

    def brightness_sharpness_check(self, token, excel_input):
        face_count = None
        sharpness = None
        brightness = None
        confidence = None
        write_excel_object.current_status = "Pass"
        write_excel_object.current_status_color = write_excel_object.green_color
        print('Two')

        try:
            file_path = input_path_brightness_check_files % (excel_input.get('filePathName'))
            file_name = excel_input.get('fileName')
            print(file_name)
            print(file_path)
            resp = assessment_common_obj.analyze_image(token, file_name, file_path)
            if resp.get("Status") == 'OK':
                context_id = resp.get("ContextId")
                brightness_sharpness_data = assessment_common_obj.get_job_status(token, context_id)
                bright_sharp_values_json = brightness_sharpness_data['data']['Result']
                bright_sharp_values = json.loads(bright_sharp_values_json)
                face_count = bright_sharp_values['data']['faceObjects']['face_count']
                if face_count == 0:
                    sharpness = "EMPTY"
                    brightness = "EMPTY"
                    confidence = "EMPTY"
                elif face_count == 1:
                    # libra office is not supporing float digts morethan 13 so rounding off original value
                    sharpness = round(bright_sharp_values['data']['faceObjects']['faces'][0]['sharpness'], 13)
                    brightness = round(bright_sharp_values['data']['faceObjects']['faces'][0]['brightness'], 13)
                    confidence = round(bright_sharp_values['data']['faceObjects']['faces'][0]['confidence'], 13)
                else:
                    sharpness = "Multifaces Found"
                    brightness = "Multifaces Found"
                    confidence = "Multifaces Found"
                    print("Morethan 1 faces found in the image")
            else:
                print("Context id is not genetated")
                sharpness = "Context id is not genetated"
                brightness = "Context id is not genetated"
                confidence = "Context id is not genetated"

        except Exception as e:
            print(e)
            sharpness = "EXCEPTION OCCURED"
            brightness = "EXCEPTION OCCURED"
            confidence = "EXCEPTION OCCURED"
        write_excel_object.compare_results_and_write_vertically(excel_input.get('testCase'), None, self.row_size, 0)
        write_excel_object.compare_results_and_write_vertically(excel_input.get('fileName'), None, self.row_size, 2)
        write_excel_object.compare_results_and_write_vertically(excel_input.get('expectedBrightness'), brightness,
                                                                self.row_size, 3)
        write_excel_object.ws.write(self.row_size, 5, excel_input.get('expectedSharpness'),
                                    write_excel_object.black_color)
        write_excel_object.compare_results_and_write_vertically(excel_input.get('expectedSharpness'), sharpness,
                                                                self.row_size, 5)
        write_excel_object.compare_results_and_write_vertically(excel_input.get('expectedConfidence'), confidence,
                                                                self.row_size, 7)
        write_excel_object.compare_results_and_write_vertically(int(excel_input.get('expectedFaceCount')), face_count,
                                                                self.row_size, 9)
        write_excel_object.compare_results_and_write_vertically(write_excel_object.current_status, None, self.row_size,
                                                                1)
        self.row_size += 1


brightness_check = AllowedFileExtensions()
login_token = crpo_common_obj.login_to_crpo(cred_crpo_admin.get('user'), cred_crpo_admin.get('password'),
                                            cred_crpo_admin.get('tenant'))
excel_read_obj.excel_read(input_path_brightness_check, 0)
excel_data = excel_read_obj.details

thread_context(brightness_check.brightness_sharpness_check, login_token, excel_data)

write_excel_object.write_overall_status(testcases_count=40)
