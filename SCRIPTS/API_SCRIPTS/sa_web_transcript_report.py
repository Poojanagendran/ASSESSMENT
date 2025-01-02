from datetime import datetime, timedelta
from urllib.parse import urlparse, urlunparse
from SCRIPTS.COMMON.read_excel import excel_read_obj
from SCRIPTS.COMMON.write_excel_new import write_excel_object
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.CRPO_COMMON.credentials import cred_crpo_suparya_crpodemo
from SCRIPTS.CRPO_COMMON.crpo_common import crpo_common_obj
import xlrd
import re

class WebTranscriptReport2:
    def __init__(self):
        self.row_size = 3
        self.details = []
        excel_read_obj.excel_read(input_path_sa_web_report, 0)
        write_excel_object.save_result(output_path_sa_web_report)
        header = ["Self Assessment Web transcript report"]
        write_excel_object.write_headers_for_scripts(0, 0, header,
                                                     write_excel_object.black_color_bold)
        third_row_headers = [
            'TestCase','OverallStatus',
            'ExpectedCandidateName', 'ActualCandidateName',
            'ExpectedCandidateID', 'ActualCandidateID',
            'ExpectedTestID', 'ActualTestID',
            'ExpectedEmail', 'ActualEmail',
            'ExpectedMobile', 'ActualMobile',
            'ExpectedLocation', 'ActualLocation',
            'ExpectedPhotoURL', 'ActualPhotoURL',
            'ExpectedAttendedDate', 'ActualAttendedDate',
            'ExpectedTimeTaken', 'ActualTimeTaken',
            'ExpectedIPAddress', 'ActualIPAddress',
            'ExpectedCandidateRank', 'ActualCandidateRank',
            'ExpectedPercentile', 'ActualPercentile',
            'ExpectedTotalMarks', 'ActualTotalMarks',
            'ExpectedMarksObtained', 'ActualMarksObtained',
            'ExpectedPercentage', 'ActualPercentage',
            'ExpectedAverageScore', 'ActualAverageScore',
            'ExpectedHighestScore', 'ActualHighestScore',
            'ExpectedMcqRank', 'ActualMcqRank',
            'ExpectedMcqMarks', 'ActualMcqMarks',
            'ExpectedMcqAverageMarks', 'ActualMcqAverageMarks',
            'ExpectedMcqHighestMarks', 'ActualMcqHighestMarks',
            'ExpectedMcqLowestMarks', 'ActualMcqLowestMarks',
            'ExpectedMcqTotalMarks', 'ActualMcqTotalMarks',
            'ExpectedMcqPercentage', 'ActualMcqPercentage',
            'ExpectedCodingRank', 'ActualCodingRank',
            'ExpectedCodingMarks', 'ActualCodingMarks',
            'ExpectedCodingAverageMarks', 'ActualCodingAverageMarks',
            'ExpectedCodingHighestMarks', 'ActualCodingHighestMarks',
            'ExpectedCodingLowestMarks', 'ActualCodingLowestMarks',
            'ExpectedCodingTotalMarks', 'ActualCodingTotalMarks',
            'ExpectedCodingPercentage', 'ActualCodingPercentage',
            'ExpectedMcqwwRank', 'ActualMcqwwRank',
            'ExpectedMcqwwMarks', 'ActualMcqwwMarks',
            'ExpectedMcqwwAverageMarks', 'ActualMcqwwAverageMarks',
            'ExpectedMcqwwHighestMarks', 'ActualMcqwwHighestMarks',
            'ExpectedMcqwwLowestMarks', 'ActualMcqwwLowestMarks',
            'ExpectedMcqwwTotalMarks', 'ActualMcqwwTotalMarks',
            'ExpectedMcqwwPercentage', 'ActualMcqwwPercentage',
            'ExpectedMcaRank', 'ActualMcaRank',
            'ExpectedMcaMarks', 'ActualMcaMarks',
            'ExpectedMcaAverageMarks', 'ActualMcaAverageMarks',
            'ExpectedMcaHighestMarks', 'ActualMcaHighestMarks',
            'ExpectedMcaLowestMarks', 'ActualMcaLowestMarks',
            'ExpectedMcaTotalMarks', 'ActualMcaTotalMarks',
            'ExpectedMcaPercentage', 'ActualMcaPercentage',
            'ExpectedFibRank', 'ActualFibRank',
            'ExpectedFibMarks', 'ActualFibMarks',
            'ExpectedFibAverageMarks', 'ActualFibAverageMarks',
            'ExpectedFibHighestMarks', 'ActualFibHighestMarks',
            'ExpectedFibLowestMarks', 'ActualFibLowestMarks',
            'ExpectedFibTotalMarks', 'ActualFibTotalMarks',
            'ExpectedFibPercentage', 'ActualFibPercentage'
        ]

        write_excel_object.write_headers_for_scripts(2, 0, third_row_headers, write_excel_object.black_color_bold)

        self.merge_columns(1,0,1, 1,"Overall")
        self.merge_columns(1,2,1,15,"CandidateDetails")
        self.merge_columns(1,16,1,35,"Test Details")
        self.merge_columns(1,36,1,49,"MCQ+RTC overall")
        self.merge_columns(1,50,1,63,"Coding overall")
        self.merge_columns(1,64,1,77,"MCQWW Overall")
        self.merge_columns(1,78,1,91,"MCA Overall")
        self.merge_columns(1,92,1,105,"FIB Overall")

        # merged_cells = sheet.merged_cells
        # for (start_row, end_row, start_col, end_col) in merged_cells:
        #     write_excel_object.ws.merge_range(start_row, start_col, end_row - 1, end_col - 1,
        #                                       excel_read_obj.excel_sheet_index.cell_value(start_row, start_col))

    @staticmethod
    def merge_columns(start_row, start_col, end_row, end_col, value):
        write_excel_object.ws.merge_range(start_row, start_col, end_row, end_col, value)

    def excel_read_2(self, excel_file_path, sheet_index):
        # Open workbook and access sheet
        workbook = xlrd.open_workbook(excel_file_path)
        sheet = workbook.sheet_by_index(sheet_index)

        # Use row 3 as headers (index 2 because rows are 0-indexed)
        headers = sheet.row_values(2)

        # Use rows starting from row 4 (index 3 for values)
        for row_index in range(3, sheet.nrows):
            row_data = sheet.row_values(row_index)
            row_dict = dict(zip(headers, row_data))
            self.details.append(row_dict)

    @staticmethod
    def excel_float_to_datetime(excel_float):
        base_date = datetime.datetime(1899, 12, 30)
        converted_date = base_date + timedelta(days=excel_float)
        return converted_date.strftime("%d-%m-%Y")

    def excel_write(self, actualdata, expecteddata):
        candidate_details = actualdata['data']['candidate']
        data = expecteddata[0]
        assessment_details = actualdata['data']['assessment']
        clientinfo = actualdata['data']['loginInfo'][0]['clientSystemInfo']
        match = re.search(r"publicIp:([\d\.]+)", clientinfo)
        ipaddress = match.group(1)
        mcq = actualdata['data']['questionTypeWiseOverall']['mcq']
        coding = actualdata['data']['questionTypeWiseOverall']['coding']
        mca = actualdata['data']['questionTypeWiseOverall']['multipleCorrectAnswer']
        mcqww = actualdata['data']['questionTypeWiseOverall']['mcqWithWeightage']
        fib = actualdata['data']['questionTypeWiseOverall']['fillInTheBlank']
        photo_url = urlparse(candidate_details['photoUrl'])
        edate = data.get('AttendedDate')
        adate = assessment_details['attendedOn']
        datetime_obj = datetime.datetime.strptime(adate, "%Y-%m-%dT%H:%M:%S").date()
        actual_date = datetime_obj.strftime("%d-%m-%Y")
        expected_date = web_transcript_report_obj2.excel_float_to_datetime(edate)
        clean_url = urlunparse(photo_url._replace(query=""))

        write_excel_object.current_status_color = write_excel_object.green_color
        write_excel_object.current_status = "Pass"
        write_excel_object.compare_results_and_write_vertically(data.get('TestCase'), None, self.row_size, 0)
        write_excel_object.compare_results_and_write_vertically(candidate_details['candidateName'], data.get('CandidateName'), self.row_size, 2)
        write_excel_object.compare_results_and_write_vertically(data.get('CandidateID'), candidate_details['id'], self.row_size, 4)
        write_excel_object.compare_results_and_write_vertically(data.get('TestID'), assessment_details['testId'], self.row_size, 6)
        write_excel_object.compare_results_and_write_vertically(data.get('Email'), candidate_details['email1'], self.row_size, 8)
        write_excel_object.compare_results_and_write_vertically(str(int(data.get('Mobile'))).strip(), candidate_details['mobile1'].strip(), self.row_size, 10)
        if candidate_details['currentLocationText'] is None:
            loc = 'None'
            write_excel_object.compare_results_and_write_vertically(data.get('Location'), loc, self.row_size, 12)
        else :
            write_excel_object.compare_results_and_write_vertically(data.get('Location'), candidate_details['currentLocationText'] , self.row_size, 12)

        write_excel_object.compare_results_and_write_vertically(data.get('PhotoURL'), clean_url, self.row_size, 14)
        write_excel_object.compare_results_and_write_vertically(expected_date, actual_date, self.row_size, 16)
        write_excel_object.compare_results_and_write_vertically(data.get('TimeTaken'), assessment_details['timeSpent'], self.row_size, 18)
        write_excel_object.compare_results_and_write_vertically(data.get('IPAddress'), ipaddress, self.row_size, 20)
        write_excel_object.compare_results_and_write_vertically(data.get('CandidateRank'), assessment_details['candidateRank'], self.row_size, 22)
        write_excel_object.compare_results_and_write_vertically(data.get('Percentile'), assessment_details['percentile'], self.row_size, 24)
        write_excel_object.compare_results_and_write_vertically(int(data.get('TotalMarks')), assessment_details['totalMarks'], self.row_size, 26)
        write_excel_object.compare_results_and_write_vertically(int(data.get('MarksObtained')), assessment_details['marksObtained'], self.row_size, 28)
        write_excel_object.compare_results_and_write_vertically(data.get('Percentage'), assessment_details['percentage'], self.row_size, 30)
        write_excel_object.compare_results_and_write_vertically(data.get('AverageScore'), assessment_details['averageScore'], self.row_size, 32)
        write_excel_object.compare_results_and_write_vertically(data.get('HighestScore'), assessment_details['highestScore'], self.row_size, 34)

        write_excel_object.compare_results_and_write_vertically(int(data.get('McqRank')), mcq['rank'], self.row_size, 36)
        write_excel_object.compare_results_and_write_vertically(data.get('McqMarks'), mcq['marks'], self.row_size, 38)
        write_excel_object.compare_results_and_write_vertically(data.get('McqAverageMarks'), mcq['averageMarks'], self.row_size, 40)
        write_excel_object.compare_results_and_write_vertically(data.get('McqHighestMarks'), mcq['highestMarks'], self.row_size, 42)
        write_excel_object.compare_results_and_write_vertically(data.get('McqLowestMarks'), mcq['lowestMarks'], self.row_size, 44)
        write_excel_object.compare_results_and_write_vertically(data.get('McqTotalMarks'), mcq['totalMarks'], self.row_size, 46)
        write_excel_object.compare_results_and_write_vertically(data.get('McqPercentage'), mcq['percentage'], self.row_size, 48)

        write_excel_object.compare_results_and_write_vertically(int(data.get('CodingRank')), coding['rank'], self.row_size, 50)
        write_excel_object.compare_results_and_write_vertically(data.get('CodingMarks'), coding['marks'], self.row_size, 52)
        write_excel_object.compare_results_and_write_vertically(data.get('CodingAverageMarks'), coding['averageMarks'], self.row_size, 54)
        write_excel_object.compare_results_and_write_vertically(data.get('CodingHighestMarks'), coding['highestMarks'], self.row_size, 56)
        write_excel_object.compare_results_and_write_vertically(data.get('CodingLowestMarks'), coding['lowestMarks'], self.row_size, 58)
        write_excel_object.compare_results_and_write_vertically(data.get('CodingTotalMarks'), coding['totalMarks'], self.row_size, 60)
        write_excel_object.compare_results_and_write_vertically(data.get('CodingPercentage'), coding['percentage'], self.row_size, 62)

        write_excel_object.compare_results_and_write_vertically(int(data.get('McqwwRank')), mcqww['rank'], self.row_size, 64)
        write_excel_object.compare_results_and_write_vertically(data.get('McqwwMarks'), mcqww['marks'], self.row_size, 66)
        write_excel_object.compare_results_and_write_vertically(data.get('McqwwAverageMarks'), mcqww['averageMarks'], self.row_size, 68)
        write_excel_object.compare_results_and_write_vertically(data.get('McqwwHighestMarks'), mcqww['highestMarks'], self.row_size, 70)
        write_excel_object.compare_results_and_write_vertically(data.get('McqwwLowestMarks'), mcqww['lowestMarks'], self.row_size, 72)
        write_excel_object.compare_results_and_write_vertically(data.get('McqwwTotalMarks'), mcqww['totalMarks'], self.row_size, 74)
        write_excel_object.compare_results_and_write_vertically(data.get('McqwwPercentage'), mcqww['percentage'], self.row_size, 76)

        write_excel_object.compare_results_and_write_vertically(int(data.get('McaRank')), mca['rank'], self.row_size, 78)
        write_excel_object.compare_results_and_write_vertically(int(data.get('McaMarks')), mca['marks'], self.row_size, 80)
        write_excel_object.compare_results_and_write_vertically(data.get('McaAverageMarks'), mca['averageMarks'], self.row_size, 82)
        write_excel_object.compare_results_and_write_vertically(data.get('McaHighestMarks'), mca['highestMarks'], self.row_size, 84)
        write_excel_object.compare_results_and_write_vertically(data.get('McaLowestMarks'), mca['lowestMarks'], self.row_size, 86)
        write_excel_object.compare_results_and_write_vertically(data.get('McaTotalMarks'), mca['totalMarks'], self.row_size, 88)
        write_excel_object.compare_results_and_write_vertically(data.get('McaPercentage'), mca['percentage'], self.row_size, 90)

        write_excel_object.compare_results_and_write_vertically(int(data.get('FibRank')), fib['rank'], self.row_size, 92)
        write_excel_object.compare_results_and_write_vertically(int(data.get('FibMarks')), fib['marks'], self.row_size, 94)
        write_excel_object.compare_results_and_write_vertically(data.get('FibAverageMarks'), fib['averageMarks'], self.row_size, 96)
        write_excel_object.compare_results_and_write_vertically(data.get('FibHighestMarks'), fib['highestMarks'], self.row_size, 98)
        write_excel_object.compare_results_and_write_vertically(data.get('FibLowestMarks'), fib['lowestMarks'], self.row_size, 100)
        write_excel_object.compare_results_and_write_vertically(int(data.get('FibTotalMarks')), fib['totalMarks'], self.row_size, 102)
        write_excel_object.compare_results_and_write_vertically(data.get('FibPercentage'), fib['percentage'], self.row_size, 104)

        write_excel_object.compare_results_and_write_vertically(write_excel_object.current_status, None, self.row_size,                                                              1)
        self.row_size = self.row_size + 1


web_transcript_report_obj2 = WebTranscriptReport2()
crpo_headers = crpo_common_obj.login_to_crpo(cred_crpo_suparya_crpodemo.get('user'), cred_crpo_suparya_crpodemo.get('password'),
                                                 cred_crpo_suparya_crpodemo.get('tenant'))
web_transcript_report_obj2.excel_read_2(input_path_sa_web_report, 0)

excel_data_2 = web_transcript_report_obj2.details
print(excel_data_2)
candidate_transcript_payload = {"testId": 20880, "testUserId": 3769232}
transcript_data = crpo_common_obj.candidate_transcript_report(crpo_headers,candidate_transcript_payload)
web_transcript_report_obj2.excel_write(transcript_data,excel_data_2)

# for data in excel_data_2:
#     if candidate_details['candidateName'] == data.get('CandidateName')

# print(candidate_name)


write_excel_object.write_overall_status(testcases_count=1)
