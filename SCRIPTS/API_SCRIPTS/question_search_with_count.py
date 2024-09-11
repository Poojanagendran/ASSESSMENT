from SCRIPTS.COMMON.read_excel import *
import datetime
import xlsxwriter
import mysql
import mysql.connector
from SCRIPTS.CRPO_COMMON.crpo_common import *
from SCRIPTS.CRPO_COMMON.credentials import *
from SCRIPTS.COMMON.io_path import *

class QuestionSearch:

    def __init__(self):
        self.api_count = None
        self.db_count = None
        requests.packages.urllib3.disable_warnings()
        self.started = datetime.datetime.now()
        self.started = self.started.strftime("%Y-%M-%d-%H-%M-%S")
        excel_read_obj.excel_read(input_path_question_search_count, 0)
        self.excel_requests = excel_read_obj.details

        # self.write_excel = xlsxwriter.Workbook(
        #     'F:\\automation\\PythonWorkingScripts_Output\\Assessment\\search\\question_search_'
        #     + self.started + '.xls')
        self.write_excel = xlsxwriter.Workbook(output_path_question_search_count + self.started + '.xls')
        self.ws = self.write_excel.add_worksheet()
        self.black_color = self.write_excel.add_format({'font_color': 'black', 'font_size': 9})
        self.red_color = self.write_excel.add_format({'font_color': 'red', 'font_size': 9})
        self.green_color = self.write_excel.add_format({'font_color': 'green', 'font_size': 9})
        self.orange_color = self.write_excel.add_format({'font_color': 'orange', 'font_size': 9})
        self.black_color_bold = self.write_excel.add_format({'font_color': 'black', 'bold': True, 'font_size': 9})
        self.overall_status_color = self.green_color
        self.overall_status = 'Pass'

    def write_headers(self):
        self.ws.write(0, 0, "Question Search", self.black_color_bold)
        self.ws.write(1, 0, "Testcases", self.black_color)
        self.ws.write(1, 1, "Status", self.black_color)
        self.ws.write(1, 2, "Requests", self.black_color)
        self.ws.write(1, 3, "API Count", self.black_color)
        self.ws.write(1, 4, "DB Count", self.black_color)

    def amsdbconnection(self):
        # 35.154.213.175
        # 35.154.36.218
        self.conn = mysql.connector.connect(host='35.154.213.175',
                                            database='appserver_core',
                                            user='muthu',
                                            password='Muthu@123')
        self.cursor = self.conn.cursor()

    def api_total_count(self, token, request_data):
        resp_dict = CrpoCommon.get_all_questions(token, request_data)
        status = resp_dict['status']
        if status == 'OK':
            self.api_count = resp_dict['data']['totalItemCount']
        else:
            print("Please Check your Request")

    def db_total_count(self, req):

        select_str = "select count(distinct(q.id)) from questions q " \
                     "left join question_statisticss qs on q.questionstatistics_id = qs.id"
        where_str = " question_id is null and is_archived=0 and is_deleted=0 and is_alive=1 and is_active=1 " \
                    "and tenant_id=1787"

        if req.get('search').get("questionIds"):
            where_str += " and q.id in ({}) ".format(','.join(map(str, req.get('search').get("questionIds"))))

        if req.get('search').get('questionStrs'):
            where_str += " and q.question_str like '%{}%' ".format(
                ','.join(map(str, req.get('search').get("questionStrs"))))

        if req.get('search').get("questionType"):
            where_str += " and q.question_type ={} ".format(req.get('search').get("questionType"))

        if req.get('search').get("codingQuestionSubTypeIds"):
            where_str += " and q.coding_question_sub_type in ({}) " \
                .format(','.join(map(str, req.get('search').get("codingQuestionSubTypeIds"))))

        if req.get('search').get("categoryIds"):
            where_str += " and q.category_id in ({}) ".format(','.join(map(str, req.get('search').get("categoryIds"))))

        if req.get('search').get("subCategoryIds"):
            where_str += " and q.sub_categories_id in ({}) ".format(
                ','.join(map(str, req.get('search').get("subCategoryIds"))))

        if req.get('search').get("subTopicIds"):
            where_str += " and q.sub_topic_id in ({}) ".format(','.join(map(str, req.get('search').get("subTopicIds"))))

        if req.get('search').get("subTopicUnitIds"):
            where_str += " and q.sub_topic_unit_id in ({}) ".format(
                ','.join(map(str, req.get('search').get("subTopicUnitIds"))))

        if req.get('search').get("statusIds"):
            where_str += " and q.status_id in ({}) ".format(','.join(map(str, req.get('search').get("statusIds"))))

        if req.get('search').get("difficultyLevels"):
            where_str += " and q.difficulty_level in ({}) ".format(
                ','.join(map(str, req.get('search').get("difficultyLevels"))))

        if req.get('search').get("flagIds"):
            where_str += " and q.question_flag in ({}) ".format(','.join(map(str, req.get('search').get("flagIds"))))

        if req.get('search').get("labelIds"):
            where_str += " and q.question_label in ({}) ".format(','.join(map(str, req.get('search').get("labelIds"))))

        if req.get('search').get("createdByIds"):
            where_str += " and q.created_by in ({}) ".format(','.join(map(str, req.get('search').get("createdByIds"))))

        if req.get('search').get("authorIds"):
            where_str += " and q.author in ({}) ".format(','.join(map(str, req.get('search').get("authorIds"))))

        if req.get('search').get("modifiedByIds"):
            where_str += " and q.modified_by in ({}) ".format(
                ','.join(map(str, req.get('search').get("modifiedByIds"))))

        if req.get('search').get("createdOnFrom"):
            from_date = req.get('search').get("createdOnFrom")
            to_date = req.get('search').get("createdOnTo")
            where_str += " and q.created_on between '%s' and '%s' " % (from_date, to_date)

        if req.get('search').get("modifiedOnFrom"):
            from_date = req.get('search').get("modifiedOnFrom")
            to_date = req.get('search').get("modifiedOnTo")
            where_str += " and q.modified_on  between '%s' and '%s' " % (from_date, to_date)

        if req.get('search').get('questionReuseFrom'):
            if req.get('search').get('questionReuseFrom') >= 0:
                from_date = req.get('search').get('questionReuseFrom')
                to_date = req.get('search').get('questionReuseTo')
                where_str += " and q.question_reuse between '%s' and '%s' " % (from_date, to_date)

        if req.get('search').get('questionStatistics').get('avgResponseTimeFrom'):
            if req.get('search').get('questionStatistics').get('avgResponseTimeFrom') >= 0:
                from_date = req.get('search').get('questionStatistics').get("avgResponseTimeFrom")
                to_date = req.get('search').get('questionStatistics').get("avgResponseTimeTo")
                where_str += " and qs.avg_response_time between '%s' and '%s' " % (from_date, to_date)

        if req.get('search').get('questionStatistics').get('exposureRateFrom'):
            if req.get('search').get('questionStatistics').get('exposureRateFrom') >= 0:
                from_date = req.get('search').get('questionStatistics').get("exposureRateFrom")
                to_date = req.get('search').get('questionStatistics').get("exposureRateTo")
                where_str += " and qs.exposure_rate between '%s' and '%s' " % (from_date, to_date)

        if req.get('search').get('questionStatistics').get('itemDifficultyFrom'):
            if req.get('search').get('questionStatistics').get('itemDifficultyFrom') >= 0:
                from_date = req.get('search').get('questionStatistics').get("itemDifficultyFrom")
                to_date = req.get('search').get('questionStatistics').get("itemDifficultyTo")
                where_str += " and qs.item_difficulty between '%s' and '%s' " % (from_date, to_date)

        if req.get('search').get("includeQuestionPaperIds"):
            where_str += " and exists(select qpq.question_id from  question_paper_" \
                         "questions qpq where q.id = qpq.question_id and qpq.questionpaperinfo_id in ({})) "\
                .format(','.join(map(str, req.get('search').get("includeQuestionPaperIds"))))

        if req.get('search').get("excludeQuestionPaperIds"):
            where_str += " and not exists(select qpq.question_id from  question_paper_" \
                         "questions qpq where q.id = qpq.question_id and qpq.questionpaperinfo_id in ({})) " \
                .format(','.join(map(str, req.get('search').get("excludeQuestionPaperIds"))))

        if req.get('search').get('isUtilized') == True:
            where_str += " and q.question_reuse > 0 "

        elif req.get('search').get('isUtilized') == False:
            where_str += " and q.question_reuse = 0 "

        if req.get('search').get('isNotesAvailable') == True:
            where_str += " and q.notes is not null "

        elif req.get('search').get('isNotesAvailable') == False:
            where_str += " and q.notes is null "
        else:
            where_str += " "
        self.final_qur = ""
        if where_str:
            self.final_qur = select_str + " where " + where_str + ";"
        if self.final_qur:
            try:
                self.amsdbconnection()
                self.cursor.execute(self.final_qur)
                query_result = self.cursor.fetchone()
                self.db_count = query_result[0]
                self.conn.close()
            except Exception as e:
                print (e)

    def data_comparision(self, requ, row):
        self.ws.write(row, 0, 'Testcases', self.green_color)
        # self.ws.write(row, 5, self.final_qur, self.green_color)
        if self.api_count == self.db_count:
            self.ws.write(row, 1, 'Pass', self.green_color)
            self.ws.write(row, 2, requ, self.black_color)
            self.ws.write(row, 3, self.api_count, self.green_color)
            self.ws.write(row, 4, self.db_count, self.green_color)
        else:
            self.ws.write(row, 1, 'Fail', self.red_color)
            self.ws.write(row, 2, requ, self.black_color)
            self.ws.write(row, 3, self.api_count, self.red_color)
            self.ws.write(row, 4, self.db_count, self.red_color)
            self.overall_status_color = self.red_color
            self.overall_status = 'Fail'


crpo_token = crpo_common_obj.login_to_crpo(cred_crpo_admin.get('user'), cred_crpo_admin.get('password'),
                                           cred_crpo_admin.get('tenant'))
qs = QuestionSearch()
row_size = 1
qs.write_headers()
for req in qs.excel_requests:
    row_size += 1
    qs.api_total_count(crpo_token, req)
    qs.db_total_count(json.loads(req.get('request')))
    qs.data_comparision(req.get('request'), row_size)

qs.ws.write(0, 1, qs.overall_status, qs.overall_status_color)
qs.ws.write(0, 2, "Total Test Cases :- 73 ", qs.green_color)
qs.write_excel.close()
