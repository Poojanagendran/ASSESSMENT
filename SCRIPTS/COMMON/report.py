import ast
import xlsxwriter
import datetime
import time
from SCRIPTS.CRPO_COMMON.crpo_common import *
import urllib.request
import certifi
import ssl

# ----------------------------------------------------------------------------------------------------------------------#
# "ast" package is used to convert Dictionary to Json (which is used in "downloadReport" method)
# subprocess is used download the file from the webserver (which is used in "downloadReport" method)
# ----------------------------------------------------------------------------------------------------------------------#
class Reports:

    def __init__(self):
        self.total_jobs = {}
        requests.packages.urllib3.disable_warnings()
        self.started = datetime.datetime.now()
        self.started = self.started.strftime("%Y-%M-%d")

    #---------------------------------------------------------------------------------------------------------------#
    # 1.  xlsxwriter.Workbook is used to create Excel Workbook in the specified path
    # 2. "add_worksheet" is used to create work sheet in the created workbook
    # -----------------------------------------------------------------------------------------------------------------#
    def writeExcelConfigurations(self, output_path):
        self.write_excel = xlsxwriter.Workbook(output_path)
        self.ws = self.write_excel.add_worksheet()
        self.black_color = self.write_excel.add_format({'font_color': 'black', 'font_size': 9})
        self.red_color = self.write_excel.add_format({'font_color': 'red', 'font_size': 9})
        self.green_color = self.write_excel.add_format({'font_color': 'green', 'font_size': 9})
        self.black_color_bold = self.write_excel.add_format({'font_color': 'black', 'bold': True, 'font_size': 9})

    # -----------------------------------------------------------------------------------------------------------------#
    # This method downloads the Excel sheet and keeps in the user specified path
    # subprocess is a builtin method is used to download the file from the website
    # ast.literal_eval is converts dictionary type value into json type
    # -----------------------------------------------------------------------------------------------------------------#
    def downloadReport(self, token, download_path, download_api_response):
        print(token)


        resp_dict = download_api_response
        print(resp_dict)
        getall_applicant_status = resp_dict['status']
        context_guid = resp_dict['data']['ContextId']
        print("Context GUID is:- %s" % context_guid)
        if getall_applicant_status == 'OK':
            get_api_job_status = 'PROGRESS'
            while get_api_job_status == 'PROGRESS' or get_api_job_status == 'PENDING':
                resp_dict = crpo_common_obj.job_status(token, context_guid)
                get_api_job_status = resp_dict['data']['JobState']
                time.sleep(5)
                print("--------------------------------")
                print('job Status is in %s' % get_api_job_status)
                print(time.time())
                print("--------------------------------")
            else:
                print("Job status changed to Success")
                # urllib.request.urlretrieve(downloadurl.get('downloadLink'), download_path, context=ssl_context)

                downloadurl = ast.literal_eval(resp_dict['data']['Result'])
                print(downloadurl)
                ssl_context = ssl.create_default_context(cafile=certifi.where())
                download_link = downloadurl.get('downloadLink')

                with urllib.request.urlopen(download_link, context=ssl_context) as response:
                    with open(download_path, 'wb') as out_file:
                        out_file.write(response.read())
                # urllib.request.urlretrieve(downloadurl.get('downloadLink'), download_path)
                # urllib.request.urlretrieve(downloadurl, config_obj.download_path)

                # subprocess.check_output(['wget', '-O', config_obj.download_path, downloadurl['downloadLink']])
                # print config_obj.download_path
        else:
            print("Getall Applicant Api Failed")


report_obj = Reports()
