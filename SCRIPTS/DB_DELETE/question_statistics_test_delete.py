import datetime
from SCRIPTS.COMMON.dbconnection import *


class DeleteQuestionStatistics:

    def __init__(self):
        print(datetime.datetime.now())

    def delete_question_statistics(self):
        db_connection = ams_db_connection()
        cursor = db_connection.cursor()
        question_statistics = "delete from question_statisticss where id in " \
                              "(select questionstatistics_id from questions " \
                              "where id in (132101,132097,132107,132121,132123,132127,132135,132149,132157,132133," \
                              "132181,132391,132395,132397,132399,132401,132403,132407,132409,132411,132413,132405) " \
                              "and tenant_id in ( 1, 1787));"
        cursor.execute(question_statistics)
        db_connection.commit()

        tuser_results = "update test_results set is_statistics_completed = 0 " \
                        "where question_id in (132101,132097,132107,132121,132123,132127,132135,132149,132157,132133," \
                        "132181,132391,132395,132397,132399,132401,132403,132407,132409,132411,132413,132405) " \
                        "and question_tenant_id=1787;"
        cursor.execute(tuser_results)
        db_connection.commit()

        questions = "update questions set questionstatistics_id=NULL " \
                    "where id in (132101,132097,132107,132121,132123,132127,132135,132149,132157,132133,132181," \
                    "132391,132395,132397,132399,132401,132403,132407,132409,132411,132413,132405) and tenant_id=1787;"

        cursor.execute(questions)
        db_connection.commit()
        db_connection.close()


qs_test_del = DeleteQuestionStatistics()

# del_data.delete_question_statistics()
print(datetime.datetime.now())
