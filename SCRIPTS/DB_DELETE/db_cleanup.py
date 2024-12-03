from SCRIPTS.COMMON.dbconnection import *
import datetime


class DataCleanUp:

    def __init__(self):
        print(datetime.datetime.now())

    @staticmethod
    def delete_assessment_test_users_for_2testschaining():
        db_connection = ams_db_connection()
        cursor = db_connection.cursor()
        tuser_scores = 'delete from candidate_scores where testuser_id in ' \
                       '(select tu.id from test_users tu inner join tests t on t.id = tu.test_id ' \
                       'where test_id in(10038,10039,10046,10047, 10081, 10082,10189,10190,10191,' \
                       '10192,10199,10200,10201,10202,10204,10205,10206, 10207,10208,10209,10210,10211,10328,10329,' \
                       '10330,10331,10338,10339,10376,10377,10378,10379,10210,10211,10402,10403)' \
                       ' and login_time is not null and t.tenant_id in (159,1787));'
        print(tuser_scores)

        cursor.execute(tuser_scores)
        # self.conn.commit()
        tuser_login_infos = 'delete from test_user_login_infos where testuser_id in ' \
                            '(select tu.id from test_users tu inner join tests t on t.id = tu.test_id ' \
                            'where test_id in(10038,10039,10046,10047, 10081, 10082,10189,10190,10191,10192,' \
                            '10199,10200,10201,10202,10204,10205,10206, 10207,10208,10209,10210,10211,10328,10329,' \
                            '10330,10331,10338,10339,10376,10377,10378,10379,10210,10211,10402,10403) ' \
                            'and login_time is not null and t.tenant_id in (159,1787));'
        print(tuser_login_infos)
        cursor.execute(tuser_login_infos)
        # self.conn.commit()

        tuser_proctoring_infos = 'delete from test_user_proctor_details where testuser_id in ' \
                                 '(select tu.id from test_users tu inner join tests t on t.id = tu.test_id ' \
                                 'where test_id in(10038,10039,10046,10047, 10081, 10082,10189,10190,10191,10192,' \
                                 '10199,10200,10201,10202,10204,10205,10206, 10207,10208,10209,10210,10211,10328,10329,' \
                                 '10330,10331,10338,10339,10376,10377,10378,10379,10210,10211,10402,10403) ' \
                                 'and login_time is not null and t.tenant_id in (159,1787));'
        print(tuser_proctoring_infos)
        cursor.execute(tuser_proctoring_infos)
        # self.conn.commit()

        update_tuser_statuss = 'update test_users set login_time = NULL, log_out_time = NULL, status = 0, ' \
                               'client_system_info = NULL, time_spent = NULL, is_password_disabled = 0,config = NULL, ' \
                               'client_system_info = NULL, total_score = NULL, percentage = NULL ' \
                               'where test_id in(10038,10039,10046,10047, 10081, 10082,10189,10190,10191,10192,' \
                               '10199,10200,10201,10202,10204,10205, 10206, 10207,10208,10209,10210,10211,10328,10329,' \
                               '10330,10331,10338,10339,10376,10377,10378,10379,10210,10211,10402,10403) and ' \
                               'login_time is not null;'
        print(update_tuser_statuss)
        cursor.execute(update_tuser_statuss)
        # self.conn.commit()
        # delete_question_approval = 'delete from question_approvals where question_id =\'113596\' and tenant_id=159;'
        # self.cursor.execute(delete_question_approval)
        # self.conn.commit()
        """# don't add tu id for cocubes, mettl, wheebox...etc  Vendors her"""
        update_test_users_partner_infos = 'update test_users_partner_info set status=3, partner_uuid = NULL, ' \
                                          'remote_candidate_json= NULL, score_status = NULL,task_id_score_fetch = NULL,' \
                                          ' report_link = NULL, tenant_id = NULL, third_party_status = NULL,' \
                                          ' third_party_login_time = NULL,third_party_test_link = NULL, ' \
                                          'third_party_overall_status = NULL, communication_history_json = NULL  ' \
                                          'where testuser_id in (880531,880555,880556,880557,880558,880559,880561,' \
                                          '880562,880563,880564,880565,880594,880596,880598,882985,882984,882983,' \
                                          '882982,882988,882989,882990,882991);'

        print(update_test_users_partner_infos)
        cursor.execute(update_test_users_partner_infos)
        # self.conn.commit()
        """ add tu id for cocubes, mettl, wheebox...etc  Vendors here."""
        update_test_users_partner_info_for_pull_score = 'update  test_users_partner_info set score_status = Null, ' \
                                                        'task_id_score_fetch = Null, communication_history_json =Null, ' \
                                                        'report_link = Null, third_party_status =Null, ' \
                                                        'third_party_overall_status = Null where ' \
                                                        'testuser_id in (882370,882393,882400,882401,882402,882484,' \
                                                        '882485,882486,882487,882505,882506,882507,882508);'
        print(update_test_users_partner_info_for_pull_score)
        cursor.execute(update_test_users_partner_info_for_pull_score)
        db_connection.commit()
        db_connection.close()

    @staticmethod
    def encryption_delete():
        db_connection = ams_db_connection()
        cursor = db_connection.cursor()
        query = "delete from candidates where  hp_dec(email1) COLLATE  utf8mb4_unicode_ci = 'testencryptionautomationtenant@gmail.com' and tenant_id=1787;"
        print(query)
        cursor.execute(query)
        db_connection.commit()
        db_connection.close()

    def delete_assessment_test_users_for_3tests_chaining(self):
        db_connection = ams_db_connection()
        cursor = db_connection.cursor()
        tuser_scores = 'delete from candidate_scores where testuser_id in ' \
                       '(select tu.id from test_users tu inner join tests t on t.id = tu.test_id ' \
                       'where test_id in(10508,10509,10510,10568,10569,10570,10581,10582,10584,10698,10699,10700,10709,10710,10711,10713,10714,10715)' \
                       ' and login_time is not null and t.tenant_id in (159,1787));'
        print(tuser_scores)

        cursor.execute(tuser_scores)
        db_connection.commit()
        tuser_login_infos = 'delete from test_user_login_infos where testuser_id in ' \
                            '(select tu.id from test_users tu inner join tests t on t.id = tu.test_id ' \
                            'where test_id in(10508,10509,10510,10568,10569,10570,10581,10582,10584,10698,10699,10700,10709,10710,10711,10713,10714,10715) ' \
                            'and login_time is not null and t.tenant_id in (159,1787));'
        print(tuser_login_infos)
        cursor.execute(tuser_login_infos)
        db_connection.commit()

        tuser_proctoring_infos = 'delete from test_user_proctor_details where testuser_id in ' \
                                 '(select tu.id from test_users tu inner join tests t on t.id = tu.test_id ' \
                                 'where test_id in(10508,10509,10510,10568,10569,10570,10581,10582,10584,10698,10699,10700,10709,10710,10711,10713,10714,10715) ' \
                                 'and login_time is not null and t.tenant_id in (159,1787));'
        print(tuser_proctoring_infos)
        cursor.execute(tuser_proctoring_infos)
        db_connection.commit()

        update_tuser_statuss = 'update test_users set login_time = NULL, is_disabled = 0, log_out_time = NULL, ' \
                               'status = 0, client_system_info = NULL, time_spent = NULL, is_password_disabled = 0,' \
                               'config = NULL, client_system_info = NULL, total_score = NULL, percentage = NULL ' \
                               'where test_id in(10508,10509,10510,10568,10569,10570,10581,10582,10584,10698,10699,10700,10709,10710,10711,10713,10714,10715) and login_time is not null;'
        print(update_tuser_statuss)
        cursor.execute(update_tuser_statuss)
        db_connection.commit()
        # # delete_question_approval = 'delete from question_approvals where question_id =\'113596\' and tenant_id=159;'
        # # self.cursor.execute(delete_question_approval)
        # # self.conn.commit()
        """# don't add tu id for cocubes, mettl, wheebox...etc  Vendors her"""
        update_test_users_partner_infos = 'update test_users_partner_info set status=3, partner_uuid = NULL, ' \
                                          'remote_candidate_json= NULL, score_status = NULL,task_id_score_fetch = NULL,' \
                                          ' report_link = NULL, tenant_id = NULL, third_party_status = NULL,' \
                                          ' third_party_login_time = NULL,third_party_test_link = NULL, ' \
                                          'third_party_overall_status = NULL, communication_history_json = NULL  ' \
                                          'where testuser_id in (885141,885142,885143,885144,885145,885165,885166,885167,885168,885169);'

        print(update_test_users_partner_infos)
        cursor.execute(update_test_users_partner_infos)
        db_connection.commit()
        # """ add tu id for cocubes, mettl, wheebox...etc  Vendors here."""
        # update_test_users_partner_info_for_pull_score = 'update  test_users_partner_info set score_status = Null, ' \
        #                                                 'task_id_score_fetch = Null, communication_history_json =Null, ' \
        #                                                 'report_link = Null, third_party_status =Null, ' \
        #                                                 'third_party_overall_status = Null where ' \
        #                                                 'testuser_id in (884052);'
        # print(update_test_users_partner_info_for_pull_score)
        # self.cursor.execute(update_test_users_partner_info_for_pull_score)
        # self.conn.commit()
        db_connection.close()

    def hirepro_chaining_delete(self):
        db_connection = ams_db_connection()
        cursor = db_connection.cursor()
        tuser_scores = 'delete from candidate_scores where testuser_id in ' \
                       '(select tu.id from test_users tu inner join tests t on t.id = tu.test_id ' \
                       'where test_id in(12397,12399,12401,12403,12405,12407)' \
                       ' and login_time is not null and t.tenant_id in (1787));'
        print(tuser_scores)

        cursor.execute(tuser_scores)
        # self.conn.commit()
        tuser_login_infos = 'delete from test_user_login_infos where testuser_id in ' \
                            '(select tu.id from test_users tu inner join tests t on t.id = tu.test_id ' \
                            'where test_id in(12397,12399,12401,12403,12405,12407) ' \
                            'and login_time is not null and t.tenant_id in (1787));'
        print(tuser_login_infos)
        cursor.execute(tuser_login_infos)
        # self.conn.commit()

        tuser_proctoring_infos = 'delete from test_user_proctor_details where testuser_id in ' \
                                 '(select tu.id from test_users tu inner join tests t on t.id = tu.test_id ' \
                                 'where test_id in(12397,12399,12401,12403,12405,12407) ' \
                                 'and login_time is not null and t.tenant_id in (1787));'
        print(tuser_proctoring_infos)
        cursor.execute(tuser_proctoring_infos)
        # self.conn.commit()

        update_tuser_statuss = 'update test_users set login_time = NULL, log_out_time = NULL, status = 0, ' \
                               'client_system_info = NULL, time_spent = NULL, is_password_disabled = 0,config = NULL, ' \
                               'client_system_info = NULL, total_score = NULL, percentage = NULL ' \
                               'where test_id in(12397,12399,12401,12403,12405,12407) and ' \
                               'login_time is not null;'
        print(update_tuser_statuss)
        cursor.execute(update_tuser_statuss)
        # self.conn.commit()
        # delete_question_approval = 'delete from question_approvals where question_id =\'113596\' and tenant_id=159;'
        # self.cursor.execute(delete_question_approval)
        # self.conn.commit()
        """# don't add tu id for cocubes, mettl, wheebox...etc  Vendors test"""
        # update_test_users_partner_infos = 'update test_users_partner_info set status=3, partner_uuid = NULL, ' \
        #                                   'remote_candidate_json= NULL, score_status = NULL,task_id_score_fetch = NULL,' \
        #                                   ' report_link = NULL, tenant_id = NULL, third_party_status = NULL,' \
        #                                   ' third_party_login_time = NULL,third_party_test_link = NULL, ' \
        #                                   'third_party_overall_status = NULL, communication_history_json = NULL  ' \
        #                                   'where testuser_id in (880531,880555,880556,880557,880558,880559,880561,' \
        #                                   '880562,880563,880564,880565,880594,880596,880598,882985,882984,882983,' \
        #                                   '882982,882988,882989,882990,882991);'

        # print(update_test_users_partner_infos)
        # self.cursor.execute(update_test_users_partner_infos)
        # self.conn.commit()
        """ add tu id for cocubes, mettl, wheebox...etc  Vendors here."""
        # update_test_users_partner_info_for_pull_score = 'update  test_users_partner_info set score_status = Null, ' \
        #                                                 'task_id_score_fetch = Null, communication_history_json =Null, ' \
        #                                                 'report_link = Null, third_party_status =Null, ' \
        #                                                 'third_party_overall_status = Null where ' \
        #                                                 'testuser_id in (882370,882393,882400,882401,882402,882484,' \
        #                                                 '882485,882486,882487,882505,882506,882507,882508);'
        # print(update_test_users_partner_info_for_pull_score)
        # self.cursor.execute(update_test_users_partner_info_for_pull_score)
        db_connection.commit()
        db_connection.close()

    def mca_static_automation_delete(self):
        db_connection = ams_db_connection()
        cursor = db_connection.cursor()
        tuser_results = "delete from test_results where testuser_id in (2551271,2551269,2551267,2551265,2551263);"
        cursor.execute(tuser_results)
        db_connection.commit()
        tuser_scores = 'delete from candidate_scores where testuser_id in ' \
                       '(select tu.id from test_users tu inner join tests t on t.id = tu.test_id ' \
                       'where test_id in(16287)' \
                       ' and login_time is not null and t.tenant_id in (159,1786));'
        print(tuser_scores)

        cursor.execute(tuser_scores)
        db_connection.commit()
        tuser_login_infos = 'delete from test_user_login_infos where testuser_id in ' \
                            '(select tu.id from test_users tu inner join tests t on t.id = tu.test_id ' \
                            'where test_id in(16287) ' \
                            'and login_time is not null and t.tenant_id in (159,1786));'
        print(tuser_login_infos)
        cursor.execute(tuser_login_infos)
        db_connection.commit()

        tuser_proctoring_infos = 'delete from test_user_proctor_details where testuser_id in ' \
                                 '(select tu.id from test_users tu inner join tests t on t.id = tu.test_id ' \
                                 'where test_id in(16287) ' \
                                 'and login_time is not null and t.tenant_id in (159,1786));'
        print(tuser_proctoring_infos)
        cursor.execute(tuser_proctoring_infos)
        db_connection.commit()

        update_tuser_statuss = 'update test_users set login_time = NULL, log_out_time = NULL, status = 0, ' \
                               'client_system_info = NULL, time_spent = NULL, is_password_disabled = 0,config = NULL, ' \
                               'client_system_info = NULL, total_score = NULL, test_start_time = NULL, percentage = NULL, ' \
                               'correct_answers = NULL, in_correct_answers = NULL, un_attended_questions=NULL,' \
                               ' is_partially_evaluated = NULL, eval_status = "NotEvaluated", eval_on = NULL' \
                               ' where test_id in(16287) and ' \
                               'login_time is not null;'
        print(update_tuser_statuss)
        cursor.execute(update_tuser_statuss)
        db_connection.commit()
        db_connection.close()

    @staticmethod
    def delete_question_statistics():
        db_connection = ams_db_connection()
        cursor = db_connection.cursor()
        question_statistics = "delete from question_statisticss where id in " \
                              "(select questionstatistics_id from questions " \
                              "where id in (132101,132097,132107,132121,132123,132133,132135,132127,132181,132157,132149, 132391,132399,132401,132395,132397,132405,132407,132403,132409,132411,132413) and tenant_id in (1,1787));"
        cursor.execute(question_statistics)
        db_connection.commit()

        tuser_results = "update test_results set is_statistics_completed = 0 " \
                        "where question_id in (132101,132097,132107,132121,132123,132133,132135,132127,132181,132157,132149,132391,132399,132401,132395,132397,132405,132407,132403,132409,132411,132413) and question_tenant_id in (1,1787);"
        cursor.execute(tuser_results)
        db_connection.commit()

        questions = "update questions set questionstatistics_id=NULL " \
                    "where id in (132101,132097,132107,132121,132123,132133,132135,132127,132181,132157,132149,132391,132399,132401,132395,132397,132405,132407,132403,132409,132411,132413) and tenant_id in (1,1787);"

        cursor.execute(questions)
        db_connection.commit()
        db_connection.close()

    def delete_question_statistics_test(self):
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

    def delete_question_statistics_test_new_cron(self):
        db_connection = ams_db_connection()
        cursor = db_connection.cursor()
        question_statistics = "delete from question_statisticss where id in " \
                              "(select questionstatistics_id from questions " \
                              "where id in (132829,132833,132835,132837,132839,132841,132843,132845,132847,132849," \
                              "132851,132853,132857,132859,132861,132863,132865,132867,132869,132871,132873) " \
                              "and tenant_id in (1,1787));"
        cursor.execute(question_statistics)
        db_connection.commit()

        tuser_results = "update test_results set is_statistics_completed = 0 " \
                        "where question_id in (132829,132833,132835,132837,132839,132841,132843,132845,132847,132849," \
                        "132851,132853,132857,132859,132861,132863,132865,132867,132869,132871,132873) " \
                        "and question_tenant_id in (1,1787);"
        cursor.execute(tuser_results)
        db_connection.commit()

        questions = "update questions set questionstatistics_id=NULL " \
                    "where id in (132829,132833,132835,132837,132839,132841,132843,132845,132847,132849,132851," \
                    "132853,132857,132859,132861,132863,132865,132867,132869,132871,132873) and tenant_id in (1,1787);"

        cursor.execute(questions)
        db_connection.commit()
        db_connection.close()

    def delete_question_statistics_new_cron(self):
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

    def test_marking_delete(self):
        db_connection = ams_db_connection()
        cursor = db_connection.cursor()
        tuser_result_infos = "delete from test_result_infos where testresult_id in " \
                             "(SELECT tr.id from test_results tr inner join test_users tu on tu.id=tr.testuser_id " \
                             "where tu.test_id in(16241,16243,16249,16267,16265,16345) and tu.status=1);"
        cursor.execute(tuser_result_infos)
        db_connection.commit()

        tuser_results = "delete from test_results where testuser_id in (2550033,2550035,2550037,2549815,2549813,2549819,2549817,2549879,2549877,2549875,2549873,2550047,2550045,2552033,2552031);"
        cursor.execute(tuser_results)
        db_connection.commit()
        tuser_scores = "delete from candidate_scores where testuser_id in(select tu.id from test_users tu " \
                       "inner join tests t on t.id = tu.test_id where test_id in(16241,16243,16249,16267,16265,16345) and login_time " \
                       "is not null and t.tenant_id in (1787));"
        cursor.execute(tuser_scores)
        db_connection.commit()
        tuser_login_infos = "delete from test_user_login_infos where testuser_id in " \
                            "(select tu.id from test_users tu inner join tests t on t.id = tu.test_id " \
                            "where test_id in(16241,16243,16249,16267,16265,16345) and login_time is not null and t.tenant_id in (1787));"
        print(tuser_login_infos)
        cursor.execute(tuser_login_infos)
        db_connection.commit()

        tuser_proctoring_infos = "delete from test_user_proctor_details where testuser_id in " \
                                 "(select tu.id from test_users tu inner join tests t on " \
                                 "t.id = tu.test_id where test_id in(16241,16243,16249,16267,16265,16345) and login_time is not null " \
                                 "and t.tenant_id in (1787));"
        print(tuser_proctoring_infos)
        cursor.execute(tuser_proctoring_infos)
        db_connection.commit()

        update_tuser_statuss = "update test_users set login_time = NULL, log_out_time = NULL, status = 0, " \
                               "client_system_info = NULL, time_spent = NULL, is_password_disabled = 0," \
                               "config = NULL,client_system_info = NULL, total_score = NULL, percentage = NULL, " \
                               "test_start_time = NULL where test_id in(16241,16243,16249,16267,16265,16345) and login_time is not null;"
        print(update_tuser_statuss)
        cursor.execute(update_tuser_statuss)
        db_connection.commit()
        db_connection.close()

    def static_ui_automation_delete(self):
        db_connection = ams_db_connection()
        cursor = db_connection.cursor()
        tuser_results = "delete from test_results where testuser_id in (2359422,2359424,2359426,2359468,2359470);"
        cursor.execute(tuser_results)
        db_connection.commit()
        tuser_scores = 'delete from candidate_scores where testuser_id in ' \
                       '(select tu.id from test_users tu inner join tests t on t.id = tu.test_id ' \
                       'where test_id in(10564,15254)' \
                       ' and login_time is not null and t.tenant_id in (159,1786));'
        print(tuser_scores)

        cursor.execute(tuser_scores)
        db_connection.commit()
        tuser_login_infos = 'delete from test_user_login_infos where testuser_id in ' \
                            '(select tu.id from test_users tu inner join tests t on t.id = tu.test_id ' \
                            'where test_id in(10564,15254) ' \
                            'and login_time is not null and t.tenant_id in (159,1786));'
        print(tuser_login_infos)
        cursor.execute(tuser_login_infos)
        db_connection.commit()

        tuser_proctoring_infos = 'delete from test_user_proctor_details where testuser_id in ' \
                                 '(select tu.id from test_users tu inner join tests t on t.id = tu.test_id ' \
                                 'where test_id in(10564,15254) ' \
                                 'and login_time is not null and t.tenant_id in (159,1786));'
        print(tuser_proctoring_infos)
        cursor.execute(tuser_proctoring_infos)
        db_connection.commit()

        update_tuser_statuss = 'update test_users set login_time = NULL, log_out_time = NULL, status = 0, ' \
                               'client_system_info = NULL, time_spent = NULL, is_password_disabled = 0,config = NULL, ' \
                               'client_system_info = NULL, total_score = NULL, test_start_time = NULL, percentage = NULL ' \
                               'where test_id in(10564,15254) and ' \
                               'login_time is not null;'
        print(update_tuser_statuss)
        cursor.execute(update_tuser_statuss)
        db_connection.commit()
        db_connection.close()

    @staticmethod
    def vendor_automation_delete():
        db_connection = ams_db_connection()
        cursor = db_connection.cursor()
        delete_candidates = 'delete from candidates where id in (select candidate_id ' \
                            'from test_users where test_id  in (14671,14673,14675,14677));'
        print(delete_candidates)
        cursor.execute(delete_candidates)
        db_connection.commit()
        delete_test_users = 'delete from test_users where test_id  in (14671,14673,14675,14677);'
        print(delete_test_users)
        cursor.execute(delete_test_users)
        db_connection.commit()
        db_connection.close()

    def vet_ui_chaining_delete(self):
        db_connection = ams_db_connection()
        cursor = db_connection.cursor()
        tuser_scores = 'delete from candidate_scores where testuser_id in ' \
                       '(select tu.id from test_users tu inner join tests t on t.id = tu.test_id ' \
                       'where test_id in(10036,10037)' \
                       ' and login_time is not null and t.tenant_id in (159,1786));'
        print(tuser_scores)
        cursor.execute(tuser_scores)
        tuser_login_infos = 'delete from test_user_login_infos where testuser_id in ' \
                            '(select tu.id from test_users tu inner join tests t on t.id = tu.test_id ' \
                            'where test_id in(10036,10037) ' \
                            'and login_time is not null and t.tenant_id in (159,1786));'
        print(tuser_login_infos)
        cursor.execute(tuser_login_infos)

        tuser_proctoring_infos = 'delete from test_user_proctor_details where testuser_id in ' \
                                 '(select tu.id from test_users tu inner join tests t on t.id = tu.test_id ' \
                                 'where test_id in(10036,10037) ' \
                                 'and login_time is not null and t.tenant_id in (159,1786));'
        print(tuser_proctoring_infos)
        cursor.execute(tuser_proctoring_infos)

        update_tuser_statuss = 'update test_users set login_time = NULL, log_out_time = NULL, status = 0, ' \
                               'client_system_info = NULL, time_spent = NULL, is_password_disabled = 0,config = NULL, ' \
                               'client_system_info = NULL, total_score = NULL, percentage = NULL ' \
                               'where test_id in(10036,10037) and ' \
                               'login_time is not null;'
        print(update_tuser_statuss)
        cursor.execute(update_tuser_statuss)

        """# don't add tu id for cocubes, mettl, wheebox...etc  Vendors her"""
        update_test_users_partner_infos = 'update test_users_partner_info set status=3, partner_uuid = NULL, ' \
                                          'remote_candidate_json= NULL, score_status = NULL,task_id_score_fetch = NULL,' \
                                          ' report_link = NULL, tenant_id = NULL, third_party_status = NULL,' \
                                          ' third_party_login_time = NULL,third_party_test_link = NULL, ' \
                                          'third_party_overall_status = NULL, communication_history_json = NULL  ' \
                                          'where testuser_id in (1330306,871187, 1017152, 885579, 885578);'

        print(update_test_users_partner_infos)
        cursor.execute(update_test_users_partner_infos)

        """ add tu id for cocubes, mettl, wheebox...etc  Vendors here."""
        update_test_users_partner_info_for_pull_score = 'update  test_users_partner_info set score_status = Null, ' \
                                                        'task_id_score_fetch = Null, communication_history_json =Null, ' \
                                                        'report_link = Null, third_party_status =Null, ' \
                                                        'third_party_overall_status = Null where ' \
                                                        'testuser_id in (1330306,871187, 1017152, 885579, 885578);'
        print(update_test_users_partner_info_for_pull_score)
        cursor.execute(update_test_users_partner_info_for_pull_score)
        db_connection.commit()
        db_connection.close()

    @staticmethod
    def delete_assessment_test_users_for_reinitateautomation():
        db_connection = ams_db_connection()
        cursor = db_connection.cursor()
        tuser_scores = 'delete from candidate_scores where testuser_id in ' \
                       '(select tu.id from test_users tu inner join tests t on t.id = tu.test_id ' \
                       'where test_id in(9214,9216,9218,9220) and login_time is not null and t.tenant_id=1787 ' \
                       'and tu.candidate_id not in(1292531,1292536));'
        print(tuser_scores)

        cursor.execute(tuser_scores)
        db_connection.commit()
        tuser_login_infos = 'delete from test_user_login_infos where testuser_id in ' \
                            '(select tu.id from test_users tu inner join tests t on t.id = tu.test_id ' \
                            'where test_id in(9214,9216,9218,9220) and login_time is not null and t.tenant_id=1787 ' \
                            'and tu.candidate_id not in(1292531,1292536));'
        print(tuser_login_infos)
        cursor.execute(tuser_login_infos)
        db_connection.commit()

        tuser_proctoring_infos = 'delete from test_user_proctor_details where testuser_id in ' \
                                 '(select tu.id from test_users tu inner join tests t on t.id = tu.test_id ' \
                                 'where test_id in(9214,9216,9218,9220) and login_time is not null and t.tenant_id=1787' \
                                 ' and tu.candidate_id not in(1292531,1292536));'
        print(tuser_proctoring_infos)
        cursor.execute(tuser_proctoring_infos)
        db_connection.commit()

        update_tuser_statuss = 'update test_users tu set login_time = NULL, log_out_time = NULL, status = 0, ' \
                               'client_system_info = NULL, time_spent = NULL, is_password_disabled = 0,config = NULL, ' \
                               'client_system_info = NULL, total_score = NULL, percentage = NULL ' \
                               'where test_id in(9214,9216,9218,9220) and login_time is not null ' \
                               'and tu.candidate_id not in(1292531,1292536);'
        print(update_tuser_statuss)
        cursor.execute(update_tuser_statuss)
        db_connection.commit()
        db_connection.close()

    @staticmethod
    def delete_ssrf_assessment_test_users():
        db_connection = ams_db_connection()
        cursor = db_connection.cursor()
        tuser_scores = 'delete from candidate_scores where testuser_id in ' \
                       '(select tu.id from test_users tu inner join tests t on t.id = tu.test_id ' \
                       'where test_id in(8916,8921) and login_time is not null and t.tenant_id=1787);'

        cursor.execute(tuser_scores)
        db_connection.commit()
        tuser_login_infos = 'delete from test_user_login_infos where testuser_id in ' \
                            '(select tu.id from test_users tu inner join tests t on t.id = tu.test_id ' \
                            'where test_id in(8916,8921) and login_time is not null and t.tenant_id=1787);'
        cursor.execute(tuser_login_infos)
        db_connection.commit()

        tuser_proctoring_infos = 'delete from test_user_proctor_details where testuser_id in ' \
                                 '(select tu.id from test_users tu inner join tests t on t.id = tu.test_id ' \
                                 'where test_id in(8916,8921) and login_time is not null and t.tenant_id=1787);'
        cursor.execute(tuser_proctoring_infos)
        db_connection.commit()

        update_tuser_statuss = 'update test_users set login_time = NULL, log_out_time = NULL, status = 0, ' \
                               'client_system_info = NULL, time_spent = NULL, is_password_disabled = 0,config = NULL, ' \
                               'client_system_info = NULL, total_score = NULL, percentage = NULL ' \
                               'where test_id in(8916,8921) and login_time is not null;'
        cursor.execute(update_tuser_statuss)
        db_connection.commit()
        delete_question_approval = 'delete from question_approvals where question_id =\'113596\' and tenant_id=1787;'
        cursor.execute(delete_question_approval)
        db_connection.commit()
        db_connection.close()

    @staticmethod
    def delete_ssrf_vendor_integration():
        db_connection = ams_db_connection()
        cursor = db_connection.cursor()
        delete_vendor_configurations = 'delete from assessment_vendor_integration where vendor_id=8830;'
        cursor.execute(delete_vendor_configurations)
        db_connection.commit()
        db_connection.close()

    @staticmethod
    def delete_ssrf_template():
        db_connection = ams_db_connection()
        cursor = db_connection.cursor()
        delete_vendor_configurations = 'delete from templates where template_name = \'SSRF_Template\' and  tenant_id=1787;'
        cursor.execute(delete_vendor_configurations)
        db_connection.commit()
        db_connection.close()

    @staticmethod
    def delete_ssrf_job():
        db_connection = ams_db_connection()
        cursor = db_connection.cursor()
        delete_vendor_configurations = 'delete from jobs where job_name=\'SSRF_Job2\' and tenant_id=1787;'
        cursor.execute(delete_vendor_configurations)
        db_connection.commit()
        db_connection.close()

    @staticmethod
    def delete_ssrf_candidate():
        try:
            db_connection = ams_db_connection()
            cursor = db_connection.cursor()
            candidate_id = "select id from candidates where email1='ssrfautomation@hirepro.in' " \
                           "and candidate_name like '%ssrf%' and usn = 'ssrfautomation' and tenant_id=1787;"

            cursor.execute(candidate_id)
            cid = cursor.fetchone()
            delete_candidate_customes = 'delete from  candidate_customs where id = ' \
                                        '(select candidatecustom_id from candidates where id=%s);' % cid[0]
            cursor.execute(delete_candidate_customes)
            db_connection.commit()
            delete_edu_profiles = 'delete from candidate_education_profiles where candidate_id =%s;' % cid[0]
            cursor.execute(delete_edu_profiles)
            db_connection.commit()
            delete_emp_profiles = 'delete from candidate_work_profiles where candidate_id =%s;' % cid[0]
            cursor.execute(delete_emp_profiles)
            db_connection.commit()
            delete_technologies = 'delete from technologys where candidate_id in (%s);' % cid[0]
            cursor.execute(delete_technologies)
            db_connection.commit()
            #
            # delete_candidate_preferences = 'delete from candidate_preferences where id in ' \
            #                                '(select candidatepreference_id from candidates where id in ' \
            #                                '(%s))' % cid[0]
            # self.cursor.execute(delete_candidate_preferences)
            # self.conn.commit()
            #
            # delete_location_preferences = 'select * from candidate_location_preferences where id in ' \
            #                               '(select candidatepreference_id from candidates where id in ' \
            #                               '(%s));' % cid[0]
            # self.cursor.execute(delete_location_preferences)
            # self.conn.commit()
            delete_candidates = 'delete from candidates where id= %s;' % cid[0]
            cursor.execute(delete_candidates)
            db_connection.commit()
            db_connection.close()
        except Exception as e:
            print(e)
            print("Check wheather the candidate is available or not")

    @staticmethod
    def delete_ssrf_questions():
        try:
            db_connection = ams_db_connection()
            cursor = db_connection.cursor()
            delete_ans_choices = 'delete from answer_choices where question_id in ' \
                                 '(select id from questions where tenant_id=1787 and  question_str = ' \
                                 '\'https%3A//s3-ap-southeast-1.amazonaws.com/test-all-hirepro-files/Automation/question/' \
                                 '8a724890-71c2-44ed-9f7f-89e0bd58cdf9Muthu_Murugan_Ramalingam.jpeg\' ' \
                                 'and modified_by is null);'
            cursor.execute(delete_ans_choices)
            db_connection.commit()
            delete_answers = 'delete from answers where question_id in (select id from questions where tenant_id=1787 ' \
                             'and  question_str = \'https%3A//s3-ap-southeast-1.amazonaws.com/test-all-hirepro-files/' \
                             'Automation/question/8a724890-71c2-44ed-9f7f-89e0bd58cdf9Muthu_Murugan_Ramalingam.jpeg\' ' \
                             'and modified_by is null);'
            cursor.execute(delete_answers)
            db_connection.commit()

            delete_child_questions = 'delete q2 from questions q2 inner join questions q1 on q2.question_id =q1.id ' \
                                     'where q1.question_str =\'https%3A//s3-ap-southeast-1.amazonaws.com/' \
                                     'test-all-hirepro-files/Automation/question/8a724890-71c2-44ed-9f7f-89e0bd58cdf9' \
                                     'Muthu_Murugan_Ramalingam.jpeg\' and q1.modified_by is null and q1.tenant_id=1787 ' \
                                     'and  q1.question_id is null;'
            cursor.execute(delete_child_questions)
            db_connection.commit()

            delete_parent_questions = 'delete from questions where tenant_id=1787 and ' \
                                      'question_str = \'https%3A//s3-ap-southeast-1.amazonaws.com/test-all-hirepro-files/' \
                                      'Automation/question/8a724890-71c2-44ed-9f7f-89e0bd58cdf9Muthu_' \
                                      'Murugan_Ramalingam.jpeg\' and modified_by is null and question_id is null;'
            cursor.execute(delete_parent_questions)
            db_connection.commit()
            db_connection.close()
        except Exception as e:
            print(e)

    @staticmethod
    def rate_control_delete():
        db_connection = ams_db_connection_for_core2517()
        cursor = db_connection.cursor()
        query = "delete from candidates where hp_dec(candidate_name) = '<script>alert(1)</script>' and tenant_id=2517;"
        print(query)
        cursor.execute(query)
        db_connection.commit()
        db_connection.close()


data_clean_obj = DataCleanUp()
# del_data.delete_assessment_test_users()
# print(datetime.datetime.now())
