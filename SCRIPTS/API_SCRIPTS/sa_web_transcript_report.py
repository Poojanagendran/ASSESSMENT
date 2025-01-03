from datetime import datetime, timedelta
from urllib.parse import urlparse, urlunparse
from SCRIPTS.COMMON.read_excel import excel_read_obj
from SCRIPTS.COMMON.write_excel_new import write_excel_object
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.CRPO_COMMON.credentials import cred_crpo_suparya_crpodemo
from SCRIPTS.CRPO_COMMON.crpo_common import crpo_common_obj
import xlrd
import re
import json

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
            'ExpectedFibPercentage', 'ActualFibPercentage',
            'ExpectedQ1McqQuestionID', 'ActualQ1McqQuestionID',
            'ExpectedQ1McqQuestionString', 'ActualQ1McqQuestionString',
            'ExpectedQ1McqDifficultyLevel', 'ActualQ1McqDifficultyLevel',
            'ExpectedQ1McqQuestionType', 'ActualQ1McqQuestionType',
            'ExpectedQ1McqCorrectAns', 'ActualQ1McqCorrectAns',
            'ExpectedQ1McqCandidateAns', 'ActualQ1McqCandidateAns',
            'ExpectedQ1McqObtainedMarks', 'ActualQ1McqObtainedMarks',
            'ExpectedQ1McqMarks', 'ActualQ1McqMarks',
            'ExpectedQ1McqTimeSpent', 'ActualQ1McqTimeSpent',
            'ExpectedQ2McqQuestionID', 'ActualQ2McqQuestionID',
            'ExpectedQ2McqQuestionString', 'ActualQ2McqQuestionString',
            'ExpectedQ2McqDifficultyLevel', 'ActualQ2McqDifficultyLevel',
            'ExpectedQ2McqQuestionType', 'ActualQ2McqQuestionType',
            'ExpectedQ2McqCorrectAns', 'ActualQ2McqCorrectAns',
            'ExpectedQ2McqCandidateAns', 'ActualQ2McqCandidateAns',
            'ExpectedQ2McqObtainedMarks', 'ActualQ2McqObtainedMarks',
            'ExpectedQ2McqMarks', 'ActualQ2McqMarks',
            'ExpectedQ2McqTimeSpent', 'ActualQ2McqTimeSpent',
            'ExpectedQ3McqQuestionID', 'ActualQ3McqQuestionID',
            'ExpectedQ3McqQuestionString', 'ActualQ3McqQuestionString',
            'ExpectedQ3McqDifficultyLevel', 'ActualQ3McqDifficultyLevel',
            'ExpectedQ3McqQuestionType', 'ActualQ3McqQuestionType',
            'ExpectedQ3McqCorrectAns', 'ActualQ3McqCorrectAns',
            'ExpectedQ3McqCandidateAns', 'ActualQ3McqCandidateAns',
            'ExpectedQ3McqObtainedMarks', 'ActualQ3McqObtainedMarks',
            'ExpectedQ3McqMarks', 'ActualQ3McqMarks',
            'ExpectedQ3McqTimeSpent', 'ActualQ3McqTimeSpent',
            'ExpectedQ1RtcQuestionID', 'ActualQ1RtcQuestionID',
            'ExpectedQ1RtcQuestionString', 'ActualQ1RtcQuestionString',
            'ExpectedQ1RtcDifficultyLevel', 'ActualQ1RtcDifficultyLevel',
            'ExpectedQ1RtcQuestionType', 'ActualQ1RtcQuestionType',
            'ExpectedQ1RtcCorrectAns', 'ActualQ1RtcCorrectAns',
            'ExpectedQ1RtcCandidateAns', 'ActualQ1RtcCandidateAns',
            'ExpectedQ1RtcObtainedMarks', 'ActualQ1RtcObtainedMarks',
            'ExpectedQ1RtcMarks', 'ActualQ1RtcMarks',
            'ExpectedQ1RtcTimeSpent', 'ActualQ1RtcTimeSpent',
            'ExpectedQ2RtcQuestionID', 'ActualQ2RtcQuestionID',
            'ExpectedQ2RtcQuestionString', 'ActualQ2RtcQuestionString',
            'ExpectedQ2RtcDifficultyLevel', 'ActualQ2RtcDifficultyLevel',
            'ExpectedQ2RtcQuestionType', 'ActualQ2RtcQuestionType',
            'ExpectedQ2RtcCorrectAns', 'ActualQ2RtcCorrectAns',
            'ExpectedQ2RtcCandidateAns', 'ActualQ2RtcCandidateAns',
            'ExpectedQ2RtcObtainedMarks', 'ActualQ2RtcObtainedMarks',
            'ExpectedQ2RtcMarks', 'ActualQ2RtcMarks',
            'ExpectedQ2RtcTimeSpent', 'ActualQ2RtcTimeSpent',
            'ExpectedQ3RtcQuestionID', 'ActualQ3RtcQuestionID',
            'ExpectedQ3RtcQuestionString', 'ActualQ3RtcQuestionString',
            'ExpectedQ3RtcDifficultyLevel', 'ActualQ3RtcDifficultyLevel',
            'ExpectedQ3RtcQuestionType', 'ActualQ3RtcQuestionType',
            'ExpectedQ3RtcCorrectAns', 'ActualQ3RtcCorrectAns',
            'ExpectedQ3RtcCandidateAns', 'ActualQ3RtcCandidateAns',
            'ExpectedQ3RtcObtainedMarks', 'ActualQ3RtcObtainedMarks',
            'ExpectedQ3RtcMarks', 'ActualQ3RtcMarks',
            'ExpectedQ3RtcTimeSpent', 'ActualQ3RtcTimeSpent',
            'ExpectedQ4RtcQuestionID', 'ActualQ4RtcQuestionID',
            'ExpectedQ4RtcQuestionString', 'ActualQ4RtcQuestionString',
            'ExpectedQ4RtcDifficultyLevel', 'ActualQ4RtcDifficultyLevel',
            'ExpectedQ4RtcQuestionType', 'ActualQ4RtcQuestionType',
            'ExpectedQ4RtcCorrectAns', 'ActualQ4RtcCorrectAns',
            'ExpectedQ4RtcCandidateAns', 'ActualQ4RtcCandidateAns',
            'ExpectedQ4RtcObtainedMarks', 'ActualQ4RtcObtainedMarks',
            'ExpectedQ4RtcMarks', 'ActualQ4RtcMarks',
            'ExpectedQ4RtcTimeSpent', 'ActualQ4RtcTimeSpent',
            'ExpectedQ5RtcQuestionID', 'ActualQ5RtcQuestionID',
            'ExpectedQ5RtcQuestionString', 'ActualQ5RtcQuestionString',
            'ExpectedQ5RtcDifficultyLevel', 'ActualQ5RtcDifficultyLevel',
            'ExpectedQ5RtcQuestionType', 'ActualQ5RtcQuestionType',
            'ExpectedQ5RtcCorrectAns', 'ActualQ5RtcCorrectAns',
            'ExpectedQ5RtcCandidateAns', 'ActualQ5RtcCandidateAns',
            'ExpectedQ5RtcObtainedMarks', 'ActualQ5RtcObtainedMarks',
            'ExpectedQ5RtcMarks', 'ActualQ5RtcMarks',
            'ExpectedQ5RtcTimeSpent', 'ActualQ5RtcTimeSpent',
            'ExpectedQ6RtcQuestionID', 'ActualQ6RtcQuestionID',
            'ExpectedQ6RtcQuestionString', 'ActualQ6RtcQuestionString',
            'ExpectedQ6RtcDifficultyLevel', 'ActualQ6RtcDifficultyLevel',
            'ExpectedQ6RtcQuestionType', 'ActualQ6RtcQuestionType',
            'ExpectedQ6RtcCorrectAns', 'ActualQ6RtcCorrectAns',
            'ExpectedQ6RtcCandidateAns', 'ActualQ6RtcCandidateAns',
            'ExpectedQ6RtcObtainedMarks', 'ActualQ6RtcObtainedMarks',
            'ExpectedQ6RtcMarks', 'ActualQ6RtcMarks',
            'ExpectedQ6RtcTimeSpent', 'ActualQ6RtcTimeSpent',
            'ExpectedQ1QAQuestionID', 'ActualQ1QAQuestionID',
            'ExpectedQ1QAQuestionString', 'ActualQ1QAQuestionString',
            'ExpectedQ1QADifficultyLevel', 'ActualQ1QADifficultyLevel',
            'ExpectedQ1QAQuestionType', 'ActualQ1QAQuestionType',
            'ExpectedQ1QACorrectAns', 'ActualQ1QACorrectAns',
            'ExpectedQ1QACandidateAns', 'ActualQ1QACandidateAns',
            'ExpectedQ1QAObtainedMarks', 'ActualQ1QAObtainedMarks',
            'ExpectedQ1QAMarks', 'ActualQ1QAMarks',
            'ExpectedQ1QATimeSpent', 'ActualQ1QATimeSpent',
            'ExpectedQ2QAQuestionID', 'ActualQ2QAQuestionID',
            'ExpectedQ2QAQuestionString', 'ActualQ2QAQuestionString',
            'ExpectedQ2QADifficultyLevel', 'ActualQ2QADifficultyLevel',
            'ExpectedQ2QAQuestionType', 'ActualQ2QAQuestionType',
            'ExpectedQ2QACorrectAns', 'ActualQ2QACorrectAns',
            'ExpectedQ2QACandidateAns', 'ActualQ2QACandidateAns',
            'ExpectedQ2QAObtainedMarks', 'ActualQ2QAObtainedMarks',
            'ExpectedQ2QAMarks', 'ActualQ2QAMarks',
            'ExpectedQ2QATimeSpent', 'ActualQ2QATimeSpent',
            'ExpectedQ3QAQuestionID', 'ActualQ3QAQuestionID',
            'ExpectedQ3QAQuestionString', 'ActualQ3QAQuestionString',
            'ExpectedQ3QADifficultyLevel', 'ActualQ3QADifficultyLevel',
            'ExpectedQ3QAQuestionType', 'ActualQ3QAQuestionType',
            'ExpectedQ3QACorrectAns', 'ActualQ3QACorrectAns',
            'ExpectedQ3QACandidateAns', 'ActualQ3QACandidateAns',
            'ExpectedQ3QAObtainedMarks', 'ActualQ3QAObtainedMarks',
            'ExpectedQ3QAMarks', 'ActualQ3QAMarks',
            'ExpectedQ3QATimeSpent', 'ActualQ3QATimeSpent',
            'ExpectedQ1FibQuestionID', 'ActualQ1FibQuestionID',
            'ExpectedQ1FibQuestionString', 'ActualQ1FibQuestionString',
            'ExpectedQ1FibDifficultyLevel', 'ActualQ1FibDifficultyLevel',
            'ExpectedQ1FibQuestionType', 'ActualQ1FibQuestionType',
            'ExpectedQ1FibCorrectAns', 'ActualQ1FibCorrectAns',
            'ExpectedQ1FibCandidateAns', 'ActualQ1FibCandidateAns',
            'ExpectedQ1FibObtainedMarks', 'ActualQ1FibObtainedMarks',
            'ExpectedQ1FibMarks', 'ActualQ1FibMarks',
            'ExpectedQ1FibTimeSpent', 'ActualQ1FibTimeSpent',
            'ExpectedQ2FibQuestionID', 'ActualQ2FibQuestionID',
            'ExpectedQ2FibQuestionString', 'ActualQ2FibQuestionString',
            'ExpectedQ2FibDifficultyLevel', 'ActualQ2FibDifficultyLevel',
            'ExpectedQ2FibQuestionType', 'ActualQ2FibQuestionType',
            'ExpectedQ2FibCorrectAns', 'ActualQ2FibCorrectAns',
            'ExpectedQ2FibCandidateAns', 'ActualQ2FibCandidateAns',
            'ExpectedQ2FibObtainedMarks', 'ActualQ2FibObtainedMarks',
            'ExpectedQ2FibMarks', 'ActualQ2FibMarks',
            'ExpectedQ2FibTimeSpent', 'ActualQ2FibTimeSpent',
            'ExpectedQ3FibQuestionID', 'ActualQ3FibQuestionID',
            'ExpectedQ3FibQuestionString', 'ActualQ3FibQuestionString',
            'ExpectedQ3FibDifficultyLevel', 'ActualQ3FibDifficultyLevel',
            'ExpectedQ3FibQuestionType', 'ActualQ3FibQuestionType',
            'ExpectedQ3FibCorrectAns', 'ActualQ3FibCorrectAns',
            'ExpectedQ3FibCandidateAns', 'ActualQ3FibCandidateAns',
            'ExpectedQ3FibObtainedMarks', 'ActualQ3FibObtainedMarks',
            'ExpectedQ3FibMarks', 'ActualQ3FibMarks',
            'ExpectedQ3FibTimeSpent', 'ActualQ3FibTimeSpent',
            'ExpectedQ1McaQuestionID', 'ActualQ1McaQuestionID',
            'ExpectedQ1McaQuestionString', 'ActualQ1McaQuestionString',
            'ExpectedQ1McaDifficultyLevel', 'ActualQ1McaDifficultyLevel',
            'ExpectedQ1McaQuestionType', 'ActualQ1McaQuestionType',
            'ExpectedQ1McaCorrectAns', 'ActualQ1McaCorrectAns',
            'ExpectedQ1McaCandidateAns', 'ActualQ1McaCandidateAns',
            'ExpectedQ1McaObtainedMarks', 'ActualQ1McaObtainedMarks',
            'ExpectedQ1McaMarks', 'ActualQ1McaMarks',
            'ExpectedQ1McaTimeSpent', 'ActualQ1McaTimeSpent',
            'ExpectedQ2McaQuestionID', 'ActualQ2McaQuestionID',
            'ExpectedQ2McaQuestionString', 'ActualQ2McaQuestionString',
            'ExpectedQ2McaDifficultyLevel', 'ActualQ2McaDifficultyLevel',
            'ExpectedQ2McaQuestionType', 'ActualQ2McaQuestionType',
            'ExpectedQ2McaCorrectAns', 'ActualQ2McaCorrectAns',
            'ExpectedQ2McaCandidateAns', 'ActualQ2McaCandidateAns',
            'ExpectedQ2McaObtainedMarks', 'ActualQ2McaObtainedMarks',
            'ExpectedQ2McaMarks', 'ActualQ2McaMarks',
            'ExpectedQ2McaTimeSpent', 'ActualQ2McaTimeSpent',
            'ExpectedQ3McaQuestionID', 'ActualQ3McaQuestionID',
            'ExpectedQ3McaQuestionString', 'ActualQ3McaQuestionString',
            'ExpectedQ3McaDifficultyLevel', 'ActualQ3McaDifficultyLevel',
            'ExpectedQ3McaQuestionType', 'ActualQ3McaQuestionType',
            'ExpectedQ3McaCorrectAns', 'ActualQ3McaCorrectAns',
            'ExpectedQ3McaCandidateAns', 'ActualQ3McaCandidateAns',
            'ExpectedQ3McaObtainedMarks', 'ActualQ3McaObtainedMarks',
            'ExpectedQ3McaMarks', 'ActualQ3McaMarks',
            'ExpectedQ3McaTimeSpent', 'ActualQ3McaTimeSpent',
            'ExpectedQ1McqwwQuestionID', 'ActualQ1McqwwQuestionID',
            'ExpectedQ1McqwwQuestionString', 'ActualQ1McqwwQuestionString',
            'ExpectedQ1McqwwDifficultyLevel', 'ActualQ1McqwwDifficultyLevel',
            'ExpectedQ1McqwwQuestionType', 'ActualQ1McqwwQuestionType',
            'ExpectedQ1McqwwCorrectAns', 'ActualQ1McqwwCorrectAns',
            'ExpectedQ1McqwwCandidateAns', 'ActualQ1McqwwCandidateAns',
            'ExpectedQ1McqwwObtainedMarks', 'ActualQ1McqwwObtainedMarks',
            'ExpectedQ1McqwwMarks', 'ActualQ1McqwwMarks',
            'ExpectedQ1McqwwTimeSpent', 'ActualQ1McqwwTimeSpent',
            'ExpectedQ2McqwwQuestionID', 'ActualQ2McqwwQuestionID',
            'ExpectedQ2McqwwQuestionString', 'ActualQ2McqwwQuestionString',
            'ExpectedQ2McqwwDifficultyLevel', 'ActualQ2McqwwDifficultyLevel',
            'ExpectedQ2McqwwQuestionType', 'ActualQ2McqwwQuestionType',
            'ExpectedQ2McqwwCorrectAns', 'ActualQ2McqwwCorrectAns',
            'ExpectedQ2McqwwCandidateAns', 'ActualQ2McqwwCandidateAns',
            'ExpectedQ2McqwwObtainedMarks', 'ActualQ2McqwwObtainedMarks',
            'ExpectedQ2McqwwMarks', 'ActualQ2McqwwMarks',
            'ExpectedQ2McqwwTimeSpent', 'ActualQ2McqwwTimeSpent',
            'ExpectedQ3McqwwQuestionID', 'ActualQ3McqwwQuestionID',
            'ExpectedQ3McqwwQuestionString', 'ActualQ3McqwwQuestionString',
            'ExpectedQ3McqwwDifficultyLevel', 'ActualQ3McqwwDifficultyLevel',
            'ExpectedQ3McqwwQuestionType', 'ActualQ3McqwwQuestionType',
            'ExpectedQ3McqwwCorrectAns', 'ActualQ3McqwwCorrectAns',
            'ExpectedQ3McqwwCandidateAns', 'ActualQ3McqwwCandidateAns',
            'ExpectedQ3McqwwObtainedMarks', 'ActualQ3McqwwObtainedMarks',
            'ExpectedQ3McqwwMarks', 'ActualQ3McqwwMarks',
            'ExpectedQ3McqwwTimeSpent', 'ActualQ3McqwwTimeSpent',
            'ExpectedQ1CodingQuestionID', 'ActualQ1CodingQuestionID',
            'ExpectedQ1CodingQuestionString', 'ActualQ1CodingQuestionString',
            'ExpectedQ1CodingDifficultyLevel', 'ActualQ1CodingDifficultyLevel',
            'ExpectedQ1CodingQuestionType', 'ActualQ1CodingQuestionType',
            'ExpectedQ1CodingCorrectAns', 'ActualQ1CodingCorrectAns',
            'ExpectedQ1CodingCandidateAns', 'ActualQ1CodingCandidateAns',
            'ExpectedQ1CodingObtainedMarks', 'ActualQ1CodingObtainedMarks',
            'ExpectedQ1CodingMarks', 'ActualQ1CodingMarks',
            'ExpectedQ1CodingTimeSpent', 'ActualQ1CodingTimeSpent',
            'ExpectedQ1CodingLOC', 'ActualQ1CodingLOC',
            'ExpectedQ1CodingCC', 'ActualQ1CodingCC',
            'ExpectedQ1CodingNoOfCompilations', 'ActualQ1CodingNoOfCompilations',
            'ExpectedQ1CodingStatus', 'ActualQ1CodingStatus',
            'ExpectedQ1CodingAvgTCExecutionTime', 'ActualQ1CodingAvgTCExecutionTime',
            'ExpectedQ1CodingAvgMemoryUsage', 'ActualQ1CodingAvgMemoryUsage',
            'ExpectedQ1CodingTCPassed', 'ActualQ1CodingTCPassed',
            'ExpectedQ1CodingTCFailed', 'ActualQ1CodingTCFailed',
            'ExpectedQ2CodingQuestionID', 'ActualQ2CodingQuestionID',
            'ExpectedQ2CodingQuestionString', 'ActualQ2CodingQuestionString',
            'ExpectedQ2CodingDifficultyLevel', 'ActualQ2CodingDifficultyLevel',
            'ExpectedQ2CodingQuestionType', 'ActualQ2CodingQuestionType',
            'ExpectedQ2CodingCorrectAns', 'ActualQ2CodingCorrectAns',
            'ExpectedQ2CodingCandidateAns', 'ActualQ2CodingCandidateAns',
            'ExpectedQ2CodingObtainedMarks', 'ActualQ2CodingObtainedMarks',
            'ExpectedQ2CodingMarks', 'ActualQ2CodingMarks',
            'ExpectedQ2CodingTimeSpent', 'ActualQ2CodingTimeSpent',
            'ExpectedQ2CodingLOC', 'ActualQ2CodingLOC',
            'ExpectedQ2CodingCC', 'ActualQ2CodingCC',
            'ExpectedQ2CodingNoOfCompilations', 'ActualQ2CodingNoOfCompilations',
            'ExpectedQ2CodingStatus', 'ActualQ2CodingStatus',
            'ExpectedQ2CodingAvgTCExecutionTime', 'ActualQ2CodingAvgTCExecutionTime',
            'ExpectedQ2CodingAvgMemoryUsage', 'ActualQ2CodingAvgMemoryUsage',
            'ExpectedQ2CodingTCPassed', 'ActualQ2CodingTCPassed',
            'ExpectedQ2CodingTCFailed', 'ActualQ2CodingTCFailed',
            'ExpectedQ3CodingQuestionID', 'ActualQ3CodingQuestionID',
            'ExpectedQ3CodingQuestionString', 'ActualQ3CodingQuestionString',
            'ExpectedQ3CodingDifficultyLevel', 'ActualQ3CodingDifficultyLevel',
            'ExpectedQ3CodingQuestionType', 'ActualQ3CodingQuestionType',
            'ExpectedQ3CodingCorrectAns', 'ActualQ3CodingCorrectAns',
            'ExpectedQ3CodingCandidateAns', 'ActualQ3CodingCandidateAns',
            'ExpectedQ3CodingObtainedMarks', 'ActualQ3CodingObtainedMarks',
            'ExpectedQ3CodingMarks', 'ActualQ3CodingMarks',
            'ExpectedQ3CodingTimeSpent', 'ActualQ3CodingTimeSpent',
            'ExpectedQ3CodingLOC', 'ActualQ3CodingLOC',
            'ExpectedQ3CodingCC', 'ActualQ3CodingCC',
            'ExpectedQ3CodingNoOfCompilations', 'ActualQ3CodingNoOfCompilations',
            'ExpectedQ3CodingStatus', 'ActualQ3CodingStatus',
            'ExpectedQ3CodingAvgTCExecutionTime', 'ActualQ3CodingAvgTCExecutionTime',
            'ExpectedQ3CodingAvgMemoryUsage', 'ActualQ3CodingAvgMemoryUsage',
            'ExpectedQ3CodingTCPassed', 'ActualQ3CodingTCPassed',
            'ExpectedQ3CodingTCFailed', 'ActualQ3CodingTCFailed'
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
        self.merge_columns(1, 106, 1, 123, "Q1 MCQ Questionwise data")
        self.merge_columns(1, 124, 1, 141, "Q2 MCQ Questionwise data")
        self.merge_columns(1, 142, 1, 159, "Q3 MCQ Questionwise data")
        self.merge_columns(1, 160, 1, 177, "Q1 RTC Questionwise data")
        self.merge_columns(1, 178, 1, 195, "Q2 RTC Questionwise data")
        self.merge_columns(1, 196, 1, 213, "Q3 RTC Questionwise data")
        self.merge_columns(1, 214, 1, 231, "Q4 RTC Questionwise data")
        self.merge_columns(1, 232, 1, 249, "Q5 RTC Questionwise data")
        self.merge_columns(1, 250, 1, 267, "Q6 RTC Questionwise data")
        self.merge_columns(1, 268, 1, 285, "Q1 QA Questionwise data")
        self.merge_columns(1, 286, 1, 303, "Q2 QA Questionwise data")
        self.merge_columns(1, 304, 1, 321, "Q3 QA Questionwise data")
        self.merge_columns(1, 322, 1, 339, "Q1 FIB Questionwise data")
        self.merge_columns(1, 340, 1, 357, "Q2 FIB Questionwise data")
        self.merge_columns(1, 358, 1, 375, "Q3 FIB Questionwise data")
        self.merge_columns(1, 376, 1, 393, "Q1 MCA Questionwise data")
        self.merge_columns(1, 394, 1, 411, "Q2 MCA Questionwise data")
        self.merge_columns(1, 412, 1, 429, "Q3 MCA Questionwise data")
        self.merge_columns(1, 430, 1, 447, "Q1 MCQWW Questionwise data")
        self.merge_columns(1, 448, 1, 465, "Q2 MCQWW Questionwise data")
        self.merge_columns(1, 466, 1, 483, "Q3 MCQWW Questionwise data")
        self.merge_columns(1, 484, 1, 517, "Q1 Coding Questionwise data")
        self.merge_columns(1, 518, 1, 551, "Q2 Coding Questionwise data")
        self.merge_columns(1, 552, 1, 584, "Q3 Coding Questionwise data")

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

    def clean_urls1(self, data2):
        # Regex to match the AWS security parameters in the URLs
        url_pattern = re.compile(r"(\?AWSAccessKeyId=[^&]+&Signature=[^&]+&Expires=[^&]+)")

        if isinstance(data2, dict):
            for key in data2:
                data2[key] = self.clean_urls1(data2[key])
        elif isinstance(data2, list):
            for i in range(len(data2)):
                data2[i] = url_pattern.sub("", data2[i])
        elif isinstance(data2, str):
            data2 = url_pattern.sub("", data2)

        return data2

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

        #question wise data

        mcqq1 = actualdata['data']['mcq'][0]
        mcqq2 = actualdata['data']['mcq'][1]
        mcqq3 = actualdata['data']['mcq'][2]

        rtcq1 = actualdata['data']['referenceToContext'][0]
        rtcq2 = actualdata['data']['referenceToContext'][1]
        rtcq3 = actualdata['data']['referenceToContext'][2]
        rtcq4 = actualdata['data']['referenceToContext'][3]
        rtcq5 = actualdata['data']['referenceToContext'][4]
        rtcq6 = actualdata['data']['referenceToContext'][5]

        fibq1 = actualdata['data']['fillInTheBlank'][0]
        fibq2 = actualdata['data']['fillInTheBlank'][1]
        fibq3 = actualdata['data']['fillInTheBlank'][2]

        mcaq1 = actualdata['data']['multipleCorrectAnswer'][0]
        mcaq2 = actualdata['data']['multipleCorrectAnswer'][1]
        mcaq3 = actualdata['data']['multipleCorrectAnswer'][2]

        mcqwwq1 = actualdata['data']['mcqWithWeightage'][0]
        mcqwwq2 = actualdata['data']['mcqWithWeightage'][1]
        mcqwwq3 = actualdata['data']['mcqWithWeightage'][2]

        codingq1 = actualdata['data']['coding'][0]
        # print(codingq1)
        codingsummaryq1 = codingq1['codingSummary']
        codingq2 = actualdata['data']['coding'][1]
        codingsummaryq2 = codingq2['codingSummary']

        codingq3 = actualdata['data']['coding'][2]
        codingsummaryq3 = codingq2['codingSummary']

        qaq1 = actualdata['data']['qa'][0]
        qaq2 = actualdata['data']['qa'][1]
        qaq3 = actualdata['data']['qa'][2]

        cleaned_data = web_transcript_report_obj2.clean_urls1(qaq1['jsonCandidateAnswer'])
        # Print the cleaned data in JSON format
        qaq1candidateans = json.dumps(cleaned_data, indent=2)
        cleaned_data = web_transcript_report_obj2.clean_urls1(qaq2['jsonCandidateAnswer'])
        # Print the cleaned data in JSON format
        qaq2candidateans = json.dumps(cleaned_data, indent=2)

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
        write_excel_object.compare_results_and_write_vertically(data.get('CandidateName'), candidate_details['candidateName'], self.row_size, 2)
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

        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1McqQuestionID')), mcqq1['id'], self.row_size, 106)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1McqQuestionString'), mcqq1['questionString'], self.row_size, 108)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1McqDifficultyLevel')), mcqq1['difficultyLevel'], self.row_size, 110)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1McqQuestionType'), mcqq1['typeOfQuestionText'], self.row_size, 112)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1McqCorrectAns'), mcqq1['correctAnswer'], self.row_size, 114)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1McqCandidateAns'), mcqq1['candidateAnswer'], self.row_size, 116)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1McqObtainedMarks')), mcqq1['obtainedMark'], self.row_size, 118)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1McqMarks')), mcqq1['mark'], self.row_size, 120)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1McqTimeSpent'), mcqq1['timeSpent'], self.row_size, 122)

        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2McqQuestionID')), mcqq2['id'], self.row_size, 124)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2McqQuestionString'), mcqq2['questionString'], self.row_size, 126)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2McqDifficultyLevel')), mcqq2['difficultyLevel'], self.row_size, 128)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2McqQuestionType'), mcqq2['typeOfQuestionText'], self.row_size, 130)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2McqCorrectAns'), mcqq2['correctAnswer'], self.row_size, 132)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2McqCandidateAns'), mcqq2['candidateAnswer'], self.row_size, 134)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2McqObtainedMarks')), mcqq2['obtainedMark'], self.row_size, 136)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2McqMarks')), mcqq2['mark'], self.row_size, 138)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2McqTimeSpent'), mcqq2['timeSpent'], self.row_size, 140)

        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3McqQuestionID')), mcqq3['id'], self.row_size, 142)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3McqQuestionString'), mcqq3['questionString'], self.row_size, 144)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3McqDifficultyLevel')), mcqq3['difficultyLevel'], self.row_size, 146)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3McqQuestionType'), mcqq3['typeOfQuestionText'], self.row_size, 148)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3McqCorrectAns'), mcqq3['correctAnswer'], self.row_size, 150)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3McqCandidateAns'), mcqq3['candidateAnswer'], self.row_size, 152)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3McqObtainedMarks')), mcqq3['obtainedMark'], self.row_size, 154)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3McqMarks')), mcqq3['mark'], self.row_size, 156)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3McqTimeSpent'), mcqq3['timeSpent'], self.row_size, 158)

        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1RtcQuestionID')), rtcq1['id'],
                                                                self.row_size, 160)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1RtcQuestionString'),
                                                                rtcq1['questionString'], self.row_size, 162)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1RtcDifficultyLevel')),
                                                                rtcq1['difficultyLevel'], self.row_size, 164)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1RtcQuestionType'),
                                                                rtcq1['typeOfQuestionText'], self.row_size, 166)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1RtcCorrectAns'), rtcq1['correctAnswer'],
                                                                self.row_size, 168)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1RtcCandidateAns'), rtcq1['candidateAnswer'],
                                                                self.row_size, 170)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1RtcObtainedMarks')),
                                                                rtcq1['obtainedMark'], self.row_size, 172)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1RtcMarks')), rtcq1['mark'],
                                                                self.row_size, 174)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1RtcTimeSpent'), rtcq1['timeSpent'],
                                                                self.row_size, 176)

        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2RtcQuestionID')), rtcq2['id'],
                                                                self.row_size, 178)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2RtcQuestionString'),
                                                                rtcq2['questionString'], self.row_size, 180)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2RtcDifficultyLevel')),
                                                                rtcq2['difficultyLevel'], self.row_size, 182)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2RtcQuestionType'),
                                                                rtcq2['typeOfQuestionText'], self.row_size, 184)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2RtcCorrectAns'), rtcq2['correctAnswer'],
                                                                self.row_size, 186)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2RtcCandidateAns'), rtcq2['candidateAnswer'],
                                                                self.row_size, 188)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2RtcObtainedMarks')),
                                                                rtcq2['obtainedMark'], self.row_size, 190)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2RtcMarks')), rtcq2['mark'],
                                                                self.row_size, 192)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2RtcTimeSpent'), rtcq2['timeSpent'],
                                                                self.row_size, 194)

        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3RtcQuestionID')), rtcq3['id'],
                                                                self.row_size, 196)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3RtcQuestionString'),
                                                                rtcq3['questionString'], self.row_size, 198)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3RtcDifficultyLevel')),
                                                                rtcq3['difficultyLevel'], self.row_size, 200)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3RtcQuestionType'),
                                                                rtcq3['typeOfQuestionText'], self.row_size, 202)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3RtcCorrectAns'), rtcq3['correctAnswer'],
                                                                self.row_size, 204)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3RtcCandidateAns'), rtcq3['candidateAnswer'],
                                                                self.row_size, 206)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3RtcObtainedMarks')),
                                                                rtcq3['obtainedMark'], self.row_size, 208)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3RtcMarks')), rtcq3['mark'],
                                                                self.row_size, 210)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3RtcTimeSpent'), rtcq3['timeSpent'],
                                                                self.row_size, 212)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q4RtcQuestionID')), rtcq4['id'],
                                                                self.row_size, 214)
        write_excel_object.compare_results_and_write_vertically(data.get('Q4RtcQuestionString'),
                                                                rtcq4['questionString'], self.row_size, 216)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q4RtcDifficultyLevel')),
                                                                rtcq4['difficultyLevel'], self.row_size, 218)
        write_excel_object.compare_results_and_write_vertically(data.get('Q4RtcQuestionType'),
                                                                rtcq4['typeOfQuestionText'], self.row_size, 220)
        write_excel_object.compare_results_and_write_vertically(data.get('Q4RtcCorrectAns'), rtcq4['correctAnswer'],
                                                                self.row_size, 222)
        write_excel_object.compare_results_and_write_vertically(data.get('Q4RtcCandidateAns'), rtcq4['candidateAnswer'],
                                                                self.row_size, 224)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q4RtcObtainedMarks')),
                                                                rtcq4['obtainedMark'], self.row_size, 226)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q4RtcMarks')), rtcq4['mark'],
                                                                self.row_size, 228)
        write_excel_object.compare_results_and_write_vertically(data.get('Q4RtcTimeSpent'), rtcq4['timeSpent'],
                                                                self.row_size, 230)

        write_excel_object.compare_results_and_write_vertically(int(data.get('Q5RtcQuestionID')), rtcq5['id'],
                                                                self.row_size, 232)
        write_excel_object.compare_results_and_write_vertically(data.get('Q5RtcQuestionString'),
                                                                rtcq5['questionString'], self.row_size, 234)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q5RtcDifficultyLevel')),
                                                                rtcq5['difficultyLevel'], self.row_size, 236)
        write_excel_object.compare_results_and_write_vertically(data.get('Q5RtcQuestionType'),
                                                                rtcq5['typeOfQuestionText'], self.row_size, 238)
        write_excel_object.compare_results_and_write_vertically(data.get('Q5RtcCorrectAns'), rtcq5['correctAnswer'],
                                                                self.row_size, 240)
        write_excel_object.compare_results_and_write_vertically(data.get('Q5RtcCandidateAns'), rtcq5['candidateAnswer'],
                                                                self.row_size, 242)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q5RtcObtainedMarks')),
                                                                rtcq5['obtainedMark'], self.row_size, 244)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q5RtcMarks')), rtcq5['mark'],
                                                                self.row_size, 246)
        write_excel_object.compare_results_and_write_vertically(data.get('Q5RtcTimeSpent'), rtcq5['timeSpent'],
                                                                self.row_size, 248)

        write_excel_object.compare_results_and_write_vertically(int(data.get('Q6RtcQuestionID')), rtcq6['id'],
                                                                self.row_size, 250)
        write_excel_object.compare_results_and_write_vertically(data.get('Q6RtcQuestionString'),
                                                                rtcq6['questionString'], self.row_size, 252)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q6RtcDifficultyLevel')),
                                                                rtcq6['difficultyLevel'], self.row_size, 254)
        write_excel_object.compare_results_and_write_vertically(data.get('Q6RtcQuestionType'),
                                                                rtcq6['typeOfQuestionText'], self.row_size, 256)
        write_excel_object.compare_results_and_write_vertically(data.get('Q6RtcCorrectAns'), rtcq6['correctAnswer'],
                                                                self.row_size, 258)
        write_excel_object.compare_results_and_write_vertically(data.get('Q6RtcCandidateAns'), rtcq6['candidateAnswer'],
                                                                self.row_size, 260)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q6RtcObtainedMarks')),
                                                                rtcq6['obtainedMark'], self.row_size, 262)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q6RtcMarks')), rtcq6['mark'],
                                                                self.row_size, 264)
        write_excel_object.compare_results_and_write_vertically(data.get('Q6RtcTimeSpent'), rtcq6['timeSpent'],
                                                                self.row_size, 266)

        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1QAQuestionID')), qaq1['id'],
                                                                self.row_size, 268)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1QAQuestionString'), qaq1['questionString'],
                                                                self.row_size, 270)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1QADifficultyLevel')),
                                                                qaq1['difficultyLevel'], self.row_size, 272)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1QAQuestionType'),
                                                                qaq1['typeOfQuestionText'], self.row_size, 274)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1QACorrectAns'), qaq1['correctAnswer'],
                                                                self.row_size, 276)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1QACandidateAns'), qaq1candidateans,
                                                                self.row_size, 278)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1QAObtainedMarks')),
                                                                qaq1['obtainedMark'], self.row_size, 280)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1QAMarks')), qaq1['mark'], self.row_size,
                                                                282)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1QATimeSpent'), qaq1['timeSpent'],
                                                                self.row_size, 284)

        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2QAQuestionID')), qaq2['id'],
                                                                self.row_size, 286)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2QAQuestionString'), qaq2['questionString'],
                                                                self.row_size, 288)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2QADifficultyLevel')),
                                                                qaq2['difficultyLevel'], self.row_size, 290)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2QAQuestionType'),
                                                                qaq2['typeOfQuestionText'], self.row_size, 292)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2QACorrectAns'), qaq2['correctAnswer'],
                                                                self.row_size, 294)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2QACandidateAns'), qaq2candidateans,
                                                                self.row_size, 296)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2QAObtainedMarks')),
                                                                qaq2['obtainedMark'], self.row_size, 298)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2QAMarks')), qaq2['mark'], self.row_size,
                                                                300)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2QATimeSpent'), qaq2['timeSpent'],
                                                                self.row_size, 302)

        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3QAQuestionID')), qaq3['id'],
                                                                self.row_size, 304)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3QAQuestionString'), qaq3['questionString'],
                                                                self.row_size, 306)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3QADifficultyLevel')),
                                                                qaq3['difficultyLevel'], self.row_size, 308)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3QAQuestionType'),
                                                                qaq3['typeOfQuestionText'], self.row_size, 310)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3QACorrectAns'), qaq3['correctAnswer'],
                                                                self.row_size, 312)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3QACandidateAns'), qaq3['candidateAnswer'],
                                                                self.row_size, 314)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3QAObtainedMarks')),
                                                                qaq3['obtainedMark'], self.row_size, 316)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3QAMarks')), qaq3['mark'], self.row_size,
                                                                318)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3QATimeSpent'), qaq3['timeSpent'],
                                                                self.row_size, 320)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1FibQuestionID')), fibq1['id'],
                                                                self.row_size, 322)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1FibQuestionString'),
                                                                fibq1['questionString'], self.row_size, 324)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1FibDifficultyLevel')),
                                                                fibq1['difficultyLevel'], self.row_size, 326)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1FibQuestionType'),
                                                                fibq1['typeOfQuestionText'], self.row_size, 328)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1FibCorrectAns'), fibq1['jsonCorrectAnswerStr'],
                                                                self.row_size, 330)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1FibCandidateAns'), fibq1['candidateAnswer'],
                                                                self.row_size, 332)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1FibObtainedMarks')),
                                                                fibq1['obtainedMark'], self.row_size, 334)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1FibMarks')), fibq1['mark'],
                                                                self.row_size, 336)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1FibTimeSpent'), fibq1['timeSpent'],
                                                                self.row_size, 338)

        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2FibQuestionID')), fibq2['id'],
                                                                self.row_size, 340)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2FibQuestionString'),
                                                                fibq2['questionString'], self.row_size, 342)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2FibDifficultyLevel')),
                                                                fibq2['difficultyLevel'], self.row_size, 344)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2FibQuestionType'),
                                                                fibq2['typeOfQuestionText'], self.row_size, 346)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2FibCorrectAns'), fibq2['jsonCorrectAnswerStr'],
                                                                self.row_size, 348)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2FibCandidateAns'), fibq2['candidateAnswer'],
                                                                self.row_size, 350)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2FibObtainedMarks')),
                                                                fibq2['obtainedMark'], self.row_size, 352)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2FibMarks')), fibq2['mark'],
                                                                self.row_size, 354)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2FibTimeSpent'), fibq2['timeSpent'],
                                                                self.row_size, 356)

        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3FibQuestionID')), fibq3['id'],
                                                                self.row_size, 358)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3FibQuestionString'),
                                                                fibq3['questionString'], self.row_size, 360)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3FibDifficultyLevel')),
                                                                fibq3['difficultyLevel'], self.row_size, 362)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3FibQuestionType'),
                                                                fibq3['typeOfQuestionText'], self.row_size, 364)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3FibCorrectAns'), fibq3['jsonCorrectAnswerStr'],
                                                                self.row_size, 366)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3FibCandidateAns'), fibq3['candidateAnswer'],
                                                                self.row_size, 368)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3FibObtainedMarks')),
                                                                fibq3['obtainedMark'], self.row_size, 370)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3FibMarks')), fibq3['mark'],
                                                                self.row_size, 372)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3FibTimeSpent'), fibq3['timeSpent'],
                                                                self.row_size, 374)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1McaQuestionID')), mcaq1['id'],
                                                                self.row_size, 376)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1McaQuestionString'),
                                                                mcaq1['questionString'], self.row_size, 378)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1McaDifficultyLevel')),
                                                                mcaq1['difficultyLevel'], self.row_size, 380)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1McaQuestionType'),
                                                                mcaq1['typeOfQuestionText'], self.row_size, 382)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1McaCorrectAns'), mcaq1['jsonCorrectAnswerStr'],
                                                                self.row_size, 384)
        # print("mca answer1 : ",data.get('Q1McaCorrectAns'))
        # print("mca answer2 : ", mcaq1['correctAnswer'])
        write_excel_object.compare_results_and_write_vertically(data.get('Q1McaCandidateAns'), mcaq1['candidateAnswer'],
                                                                self.row_size, 386)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1McaObtainedMarks')),
                                                                mcaq1['obtainedMark'], self.row_size, 388)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1McaMarks')), mcaq1['mark'],
                                                                self.row_size, 390)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1McaTimeSpent'), mcaq1['timeSpent'],
                                                                self.row_size, 392)

        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2McaQuestionID')), mcaq2['id'],
                                                                self.row_size, 394)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2McaQuestionString'),
                                                                mcaq2['questionString'], self.row_size, 396)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2McaDifficultyLevel')),
                                                                mcaq2['difficultyLevel'], self.row_size, 398)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2McaQuestionType'),
                                                                mcaq2['typeOfQuestionText'], self.row_size, 400)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2McaCorrectAns'), mcaq2['jsonCorrectAnswerStr'],
                                                                self.row_size, 402)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2McaCandidateAns'), mcaq2['candidateAnswer'],
                                                                self.row_size, 404)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2McaObtainedMarks')),
                                                                mcaq2['obtainedMark'], self.row_size, 406)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2McaMarks')), mcaq2['mark'],
                                                                self.row_size, 408)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2McaTimeSpent'), mcaq2['timeSpent'],
                                                                self.row_size, 410)

        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3McaQuestionID')), mcaq3['id'],
                                                                self.row_size, 412)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3McaQuestionString'),
                                                                mcaq3['questionString'], self.row_size, 414)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3McaDifficultyLevel')),
                                                                mcaq3['difficultyLevel'], self.row_size, 416)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3McaQuestionType'),
                                                                mcaq3['typeOfQuestionText'], self.row_size, 418)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3McaCorrectAns'), mcaq3['jsonCorrectAnswerStr'],
                                                                self.row_size, 420)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3McaCandidateAns'), mcaq3['candidateAnswer'],
                                                                self.row_size, 422)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3McaObtainedMarks')),
                                                                mcaq3['obtainedMark'], self.row_size, 424)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3McaMarks')), mcaq3['mark'],
                                                                self.row_size, 426)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3McaTimeSpent'), mcaq3['timeSpent'],
                                                                self.row_size, 428)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1McqwwQuestionID')), mcqwwq1['id'],
                                                                self.row_size, 430)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1McqwwQuestionString'),
                                                                mcqwwq1['questionString'], self.row_size, 432)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1McqwwDifficultyLevel')),
                                                                mcqwwq1['difficultyLevel'], self.row_size, 434)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1McqwwQuestionType'),
                                                                mcqwwq1['typeOfQuestionText'], self.row_size, 436)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1McqwwCorrectAns'), mcqwwq1['jsonCorrectAnswerStr'],
                                                                self.row_size, 438)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1McqwwCandidateAns'),
                                                                mcqwwq1['candidateAnswer'], self.row_size, 440)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1McqwwObtainedMarks'),
                                                                mcqwwq1['obtainedMark'], self.row_size, 442)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1McqwwMarks')), mcqwwq1['mark'],
                                                                self.row_size, 444)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1McqwwTimeSpent'), mcqwwq1['timeSpent'],
                                                                self.row_size, 446)

        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2McqwwQuestionID')), mcqwwq2['id'],
                                                                self.row_size, 448)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2McqwwQuestionString'),
                                                                mcqwwq2['questionString'], self.row_size, 450)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2McqwwDifficultyLevel')),
                                                                mcqwwq2['difficultyLevel'], self.row_size, 452)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2McqwwQuestionType'),
                                                                mcqwwq2['typeOfQuestionText'], self.row_size, 454)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2McqwwCorrectAns'), mcqwwq2['jsonCorrectAnswerStr'],
                                                                self.row_size, 456)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2McqwwCandidateAns'),
                                                                mcqwwq2['candidateAnswer'], self.row_size, 458)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2McqwwObtainedMarks'),
                                                                mcqwwq2['obtainedMark'], self.row_size, 460)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2McqwwMarks')), mcqwwq2['mark'],
                                                                self.row_size, 462)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2McqwwTimeSpent'), mcqwwq2['timeSpent'],
                                                                self.row_size, 464)

        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3McqwwQuestionID')), mcqwwq3['id'],
                                                                self.row_size, 466)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3McqwwQuestionString'),
                                                                mcqwwq3['questionString'], self.row_size, 468)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3McqwwDifficultyLevel')),
                                                                mcqwwq3['difficultyLevel'], self.row_size, 470)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3McqwwQuestionType'),
                                                                mcqwwq3['typeOfQuestionText'], self.row_size, 472)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3McqwwCorrectAns'), mcqwwq3['jsonCorrectAnswerStr'],
                                                                self.row_size, 474)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3McqwwCandidateAns'),
                                                                mcqwwq3['candidateAnswer'], self.row_size, 476)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3McqwwObtainedMarks'),
                                                                mcqwwq3['obtainedMark'], self.row_size, 478)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3McqwwMarks')), mcqwwq3['mark'],
                                                                self.row_size, 480)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3McqwwTimeSpent'), mcqwwq3['timeSpent'],
                                                                self.row_size, 482)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1CodingQuestionID')), codingq1['id'],
                                                                self.row_size, 484)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1CodingQuestionString'),
                                                                codingq1['questionString'], self.row_size, 486)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1CodingDifficultyLevel')),
                                                                codingq1['difficultyLevel'], self.row_size, 488)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1CodingQuestionType'),
                                                                codingq1['typeOfQuestionText'], self.row_size, 490)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1CodingCorrectAns'),
                                                                codingq1['correctAnswer'], self.row_size, 492)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1CodingCandidateAns'),
                                                                codingq1['candidateAnswer'], self.row_size, 494)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1CodingObtainedMarks'),
                                                                codingq1['obtainedMark'], self.row_size, 496)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1CodingMarks')), codingq1['mark'],
                                                                self.row_size, 498)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1CodingTimeSpent'), codingq1['timeSpent'],
                                                                self.row_size, 500)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1CodingLOC'), codingsummaryq1['linesOfCode'], self.row_size,
                                                                502)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1CodingCC'),
                                                                codingsummaryq1['codeComplexity'], self.row_size, 504)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1CodingNoOfCompilations')),
                                                                codingsummaryq1['noOfCompilations'], self.row_size, 506)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1CodingStatus'), codingsummaryq1['statusOfCode'],
                                                                self.row_size, 508)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1CodingAvgTCExecutionTime'),
                                                                codingsummaryq1['avgTestCaseExecutionTime'], self.row_size,
                                                                510)
        write_excel_object.compare_results_and_write_vertically(data.get('Q1CodingAvgMemoryUsage'),
                                                                codingsummaryq1['avgMemoryUsage'], self.row_size, 512)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1CodingTCPassed')),
                                                                codingsummaryq1['testCasePassed'], self.row_size, 514)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q1CodingTCFailed')),
                                                                codingsummaryq1['testCaseFailed'], self.row_size, 516)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2CodingQuestionID')), codingq2['id'],
                                                                self.row_size, 518)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2CodingQuestionString'),
                                                                codingq2['questionString'], self.row_size, 520)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2CodingDifficultyLevel')),
                                                                codingq2['difficultyLevel'], self.row_size, 522)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2CodingQuestionType'),
                                                                codingq2['typeOfQuestionText'], self.row_size, 524)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2CodingCorrectAns'),
                                                                codingq2['correctAnswer'], self.row_size, 526)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2CodingCandidateAns'),
                                                                codingq2['candidateAnswer'], self.row_size, 528)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2CodingObtainedMarks'),
                                                                codingq2['obtainedMark'], self.row_size, 530)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2CodingMarks')), codingq2['mark'],
                                                                self.row_size, 532)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2CodingTimeSpent'), codingq2['timeSpent'],
                                                                self.row_size, 534)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2CodingLOC'), codingsummaryq2['linesOfCode'],
                                                                self.row_size, 536)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2CodingCC'),
                                                                codingsummaryq2['codeComplexity'], self.row_size, 538)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2CodingNoOfCompilations')),
                                                                codingsummaryq2['noOfCompilations'], self.row_size, 540)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2CodingStatus'),
                                                                codingsummaryq2['statusOfCode'], self.row_size, 542)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2CodingAvgTCExecutionTime'),
                                                                codingsummaryq2['avgTestCaseExecutionTime'],
                                                                self.row_size, 544)
        write_excel_object.compare_results_and_write_vertically(data.get('Q2CodingAvgMemoryUsage'),
                                                                codingsummaryq2['avgMemoryUsage'], self.row_size, 546)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2CodingTCPassed')),
                                                                codingsummaryq2['testCasePassed'], self.row_size, 548)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q2CodingTCFailed')),
                                                                codingsummaryq2['testCaseFailed'], self.row_size, 550)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3CodingQuestionID')), codingq3['id'],
                                                                self.row_size, 552)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3CodingQuestionString'),
                                                                codingq3['questionString'], self.row_size, 554)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3CodingDifficultyLevel')),
                                                                codingq3['difficultyLevel'], self.row_size, 556)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3CodingQuestionType'),
                                                                codingq3['typeOfQuestionText'], self.row_size, 558)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3CodingCorrectAns'),
                                                                codingq3['correctAnswer'], self.row_size, 560)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3CodingCandidateAns'),
                                                                codingq3['candidateAnswer'], self.row_size, 562)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3CodingObtainedMarks'),
                                                                codingq3['obtainedMark'], self.row_size, 564)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3CodingMarks')), codingq3['mark'],
                                                                self.row_size, 566)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3CodingTimeSpent'), codingq3['timeSpent'],
                                                                self.row_size, 568)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3CodingLOC'), codingsummaryq3['linesOfCode'],
                                                                self.row_size, 570)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3CodingCC'),
                                                                codingsummaryq3['codeComplexity'], self.row_size, 572)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3CodingNoOfCompilations')),
                                                                codingsummaryq3['noOfCompilations'], self.row_size, 574)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3CodingStatus'),
                                                                codingsummaryq3['statusOfCode'], self.row_size, 576)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3CodingAvgTCExecutionTime'),
                                                                codingsummaryq3['avgTestCaseExecutionTime'],
                                                                self.row_size, 578)
        write_excel_object.compare_results_and_write_vertically(data.get('Q3CodingAvgMemoryUsage'),
                                                                codingsummaryq3['avgMemoryUsage'], self.row_size, 580)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3CodingTCPassed')),
                                                                codingsummaryq3['testCasePassed'], self.row_size, 582)
        write_excel_object.compare_results_and_write_vertically(int(data.get('Q3CodingTCFailed')),
                                                                codingsummaryq3['testCaseFailed'], self.row_size, 584)

        write_excel_object.compare_results_and_write_vertically(write_excel_object.current_status, None, self.row_size,
                                                                1)
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
