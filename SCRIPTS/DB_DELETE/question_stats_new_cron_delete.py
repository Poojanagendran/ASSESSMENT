# This  script is for hirepro cron data clean up
import datetime
from SCRIPTS.COMMON.dbconnection import *


class HireproCronQuestionStats:

    def __init__(self):
        print(datetime.datetime.now())

    def delete_question_statistics(self):
        db_connection = ams_db_connection()
        cursor = db_connection.cursor()
        question_statistics = "delete from question_statisticss where id in " \
                              "(select questionstatistics_id from questions " \
                              "where id in (132829,132837,132839,132833,132835,132843,132845,132841,132847,132849,132851,132853,132861,132863,132857,132859,132865,132867,132869,132871,132873) and tenant_id in (1,248, 1787));"
        cursor.execute(question_statistics)
        db_connection.commit()

        tuser_results = "update test_results set is_statistics_completed = 0 " \
                        "where question_id in (132829,132837,132839,132833,132835,132843,132845,132841,132847,132849,132851,132853,132861,132863,132857,132859,132865,132867,132869,132871,132873) and question_tenant_id in (1,248, 1787);"
        cursor.execute(tuser_results)
        db_connection.commit()

        questions = "update questions set questionstatistics_id=NULL " \
                    "where id in (132829,132837,132839,132833,132835,132843,132845,132841,132847,132849,132851,132853,132861,132863,132857,132859,132865,132867,132869,132871,132873) and tenant_id in (1,248, 1787);"

        cursor.execute(questions)
        db_connection.commit()
        db_connection.close()


qs_new_cron_del = HireproCronQuestionStats()
# del_data.delete_question_statistics()
print(datetime.datetime.now())
