import datetime
from SCRIPTS.COMMON.dbconnection import *


class DeleteSSRFData:

    def __init__(self):
        print(datetime.datetime.now())

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
            print (e)
            print ("Check wheather the candidate is available or not")

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


del_data = DeleteSSRFData()
del_data.delete_ssrf_assessment_test_users()
del_data.delete_ssrf_template()
del_data.delete_ssrf_job()
del_data.delete_ssrf_vendor_integration()
del_data.delete_ssrf_candidate()
del_data.delete_ssrf_questions()
del_data.delete_assessment_test_users_for_reinitateautomation()
print (datetime.datetime.now())
