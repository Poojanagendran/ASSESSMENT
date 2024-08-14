from SCRIPTS.COMMON.dbconnection import *
import datetime


class delete_ssrf_data:

    def __init__(self):
        print(datetime.datetime.now())
        # connection = ams_db_connection()
        # cursor = connection.cursor()
        # cursor.execute(candidate_personal_details_query)

    def delete_assessment_test_users(self):
        db_connection = ams_db_connection()
        cursor = db_connection.cursor()
        tuser_scores = 'delete from candidate_scores where testuser_id in ' \
                       '(select tu.id from test_users tu inner join tests t on t.id = tu.test_id ' \
                       'where test_id in(10036,10037)' \
                       ' and login_time is not null and t.tenant_id in (159,1787));'
        print(tuser_scores)
        cursor.execute(tuser_scores)
        tuser_login_infos = 'delete from test_user_login_infos where testuser_id in ' \
                            '(select tu.id from test_users tu inner join tests t on t.id = tu.test_id ' \
                            'where test_id in(10036,10037) ' \
                            'and login_time is not null and t.tenant_id in (159,1787));'
        print(tuser_login_infos)
        cursor.execute(tuser_login_infos)

        tuser_proctoring_infos = 'delete from test_user_proctor_details where testuser_id in ' \
                                 '(select tu.id from test_users tu inner join tests t on t.id = tu.test_id ' \
                                 'where test_id in(10036,10037) ' \
                                 'and login_time is not null and t.tenant_id in (159,1787));'
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


del_data = delete_ssrf_data()
del_data.delete_assessment_test_users()
print(datetime.datetime.now())
