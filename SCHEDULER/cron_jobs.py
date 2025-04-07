import subprocess
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from SCRIPTS.COMMON.io_user_directory import *


# Function to run scripts with retries
def run_script(script_name, script_path):
    print(f"Running {script_name}...")
    attempt = 0
    success = False
    max_retries = 3
    while attempt < max_retries and not success:
        result = subprocess.run(["python", script_path], capture_output=True, text=True)

        if result.returncode == 0:
            print(f"{script_name} ran successfully!")
            success = True
        else:
            attempt += 1
            print(f"{script_name} failed with error: {result.stderr}")
            if attempt < max_retries:
                print(f"Retrying... (Attempt {attempt}/{max_retries})")
                time.sleep(5)  # Wait for 5 seconds before retrying
            else:
                print(f"{script_name} failed after {max_retries} attempts.")
    return success


# Create a scheduler
scheduler = BlockingScheduler()


# Define the script execution functions with retries
def task_allowed_extensions():
    script_path = str(path) + r"\SCRIPTS\API_SCRIPTS\allowed_extensions.py"
    print(script_path)
    if run_script("allowed_extensions", script_path):
        time.sleep(2)


def task_analyze_brightness_shapness():
    script_path = str(path) + r"\SCRIPTS\API_SCRIPTS\analyze_brightness_shapness.py"
    if run_script("analyze_brightness_shapness", script_path):
        time.sleep(2)


def task_applicant_report():
    script_path = str(path) + r"\SCRIPTS\API_SCRIPTS\applicant_report.py"
    if run_script("applicant_report", script_path):
        time.sleep(2)


def task_chaining_of_2_tests():
    script_path = str(path) + r"/SCRIPTS/API_SCRIPTS/chaining_2nd_login_generic.py"
    if run_script("chaining of 2 tests", script_path):
        time.sleep(2)


def task_chaining_of_3_tests():
    script_path = str(path) + r"/SCRIPTS/API_SCRIPTS/chaining_of_3_tests.py"
    if run_script("chaining of 3 tests", script_path):
        time.sleep(2)


def task_code_compilation():
    script_path = str(path) + r"/SCRIPTS/API_SCRIPTS/coding_compilation.py"
    if run_script("Code Compilation", script_path):
        time.sleep(2)


def task_email_verification():
    script_path = str(path) + r"/SCRIPTS/API_SCRIPTS/email_verification.py"
    if run_script("Email Verification", script_path):
        time.sleep(2)


def task_encryption_check():
    script_path = str(path) + r"/SCRIPTS/API_SCRIPTS/encryption_check.py"
    if run_script("Encryption Check", script_path):
        time.sleep(2)


def task_plagiarism_report():
    script_path = str(path) + r"/SCRIPTS/API_SCRIPTS/plagiarism_report.py"
    if run_script("Encryption Check", script_path):
        time.sleep(2)


def task_question_search_with_boundary():
    script_path = str(path) + r"/SCRIPTS/API_SCRIPTS/question_search_with_boundary.py"
    if run_script("Question Search with Boundary", script_path):
        time.sleep(2)


def task_question_search_with_count():
    script_path = str(path) + r"/SCRIPTS/API_SCRIPTS/question_search_with_count.py"
    if run_script("Question Search with Count", script_path):
        time.sleep(2)


def task_reinitiate_automation():
    script_path = str(path) + r"/SCRIPTS/API_SCRIPTS/reinitiate_automation.py"
    if run_script("Reinitiate automation", script_path):
        time.sleep(2)


def task_reuse_test_score():
    script_path = str(path) + r"/SCRIPTS/API_SCRIPTS/reuse_test_score.py"
    if run_script("Reuse test score", script_path):
        time.sleep(2)


def task_ssrf_check():
    script_path = str(path) + r"/SCRIPTS/API_SCRIPTS/ssrfCheck.py"
    if run_script("SSRF check", script_path):
        time.sleep(2)


def task_mic_distortion():
    script_path = str(path) + r"/SCRIPTS/API_SCRIPTS/vet_mic_distortion_check.py"
    if run_script("Mic Distortion check", script_path):
        time.sleep(2)


def task_audio_transcript_report_cefr():
    script_path = str(path) + r"/SCRIPTS/API_SCRIPTS/audio_transcript_report_cefr.py"
    if run_script("Task Audio Transcript CEFR", script_path):
        time.sleep(2)


def task_behaviour_proctoring_evaluation_new():
    script_path = str(path) + r"/SCRIPTS/API_SCRIPTS/behaviour_proctoring_evaluation_new.py"
    if run_script("behaviour_proctoring_evaluation_new", script_path):
        time.sleep(2)


def task_device_proctoring_evaluation():
    script_path = str(path) + r"/SCRIPTS/API_SCRIPTS/device_proctoring_evaluation.py"
    if run_script("device_proctoring_evaluation", script_path):
        time.sleep(2)


def task_proctor_evaluation():
    script_path = str(path) + r"/SCRIPTS/API_SCRIPTS/proctor_evaluation.py"
    if run_script("proctor_evaluation", script_path):
        time.sleep(2)


def task_question_statistics_tests_old_cron():
    script_path = str(path) + r"/SCRIPTS/API_SCRIPTS/question_statistics_tests_old_cron.py"
    if run_script("question_statistics_tests_old_cron", script_path):
        time.sleep(2)


def task_question_statistics_with_hirepro_cron():
    script_path = str(path) + r"/SCRIPTS/API_SCRIPTS/question_statistics_with_hirepro_cron.py"
    if run_script("question_statistics_tests_old_cron", script_path):
        time.sleep(2)


def task_question_statistics_old_cron():
    script_path = str(path) + r"/SCRIPTS/API_SCRIPTS/question_statistics_old_cron.py"
    if run_script("question_statistics_tests_old_cron", script_path):
        time.sleep(2)


def task_question_statistics_tests_hirepro_cron():
    script_path = str(path) + r"/SCRIPTS/API_SCRIPTS/question_statistics_tests_hirepro_cron.py"
    if run_script("question_statistics_tests_old_cron", script_path):
        time.sleep(2)


def task_sa_web_transcript_report():
    script_path = str(path) + r"/SCRIPTS/API_SCRIPTS/sa_web_transcript_report.py"
    if run_script("sa_web_transcript_report", script_path):
        time.sleep(2)


def task_sanitizeapi():
    script_path = str(path) + r"/SCRIPTS/API_SCRIPTS/sanitizeapi.py"
    if run_script("sanitizeapi", script_path):
        time.sleep(2)


def task_typing_assessment_docket():
    script_path = str(path) + r"/SCRIPTS/API_SCRIPTS/typing_assessment_docket.py"
    if run_script("typing_assessment_docket", script_path):
        time.sleep(2)


def task_rate_controller():
    script_path = str(path) + r"/SCRIPTS/SECURITY/rate_control.py"
    if run_script("rate_control", script_path):
        time.sleep(2)


def task_xss():
    script_path = str(path) + r"/SCRIPTS/SECURITY/xss.py"
    if run_script("xss", script_path):
        time.sleep(2)


def task_response_encryption():
    script_path = str(path) + r"/SCRIPTS/SECURITY/response_encryption.py"
    if run_script("response_encryption", script_path):
        time.sleep(2)


custom_hour = 19
custom_minute = 1
scheduler.add_job(task_question_statistics_tests_old_cron, 'cron', hour=custom_hour, minute=custom_minute,
                  max_instances=1)
scheduler.add_job(task_question_statistics_tests_hirepro_cron, 'cron', hour=custom_hour, minute=custom_minute,
                  max_instances=1)
scheduler.add_job(task_question_statistics_old_cron, 'cron', hour=custom_hour, minute=custom_minute, max_instances=1)
scheduler.add_job(task_question_statistics_with_hirepro_cron, 'cron', hour=custom_hour, minute=custom_minute,
                  max_instances=1)
custom_minute = 4

scheduler.add_job(task_xss, 'cron', hour=custom_hour, minute=custom_minute, max_instances=1)
scheduler.add_job(task_allowed_extensions, 'cron', hour=custom_hour, minute=custom_minute, max_instances=1)
scheduler.add_job(task_analyze_brightness_shapness, 'cron', hour=custom_hour, minute=custom_minute,
                  max_instances=1)

# custom_hour = 11
custom_minute = 7
scheduler.add_job(task_applicant_report, 'cron', hour=custom_hour, minute=custom_minute, max_instances=1)

scheduler.add_job(task_encryption_check, 'cron', hour=custom_hour, minute=custom_minute, max_instances=1)

scheduler.add_job(task_plagiarism_report, 'cron', hour=custom_hour, minute=custom_minute, max_instances=1)
scheduler.add_job(task_proctor_evaluation, 'cron', hour=custom_hour, minute=custom_minute, max_instances=1)

# custom_hour = 11
custom_minute = 10
scheduler.add_job(task_question_search_with_boundary, 'cron', hour=custom_hour, minute=custom_minute, max_instances=1)
scheduler.add_job(task_question_search_with_count, 'cron', hour=custom_hour, minute=custom_minute, max_instances=1)
scheduler.add_job(task_reuse_test_score, 'cron', hour=custom_hour, minute=custom_minute, max_instances=1)

# custom_hour = 11
custom_minute = 13
scheduler.add_job(task_reinitiate_automation, 'cron', hour=custom_hour, minute=custom_minute, max_instances=1)
scheduler.add_job(task_ssrf_check, 'cron', hour=custom_hour, minute=custom_minute, max_instances=1)
scheduler.add_job(task_mic_distortion, 'cron', hour=custom_hour, minute=custom_minute, max_instances=1)

custom_minute = 16
scheduler.add_job(task_sa_web_transcript_report, 'cron', hour=custom_hour, minute=custom_minute, max_instances=1)
scheduler.add_job(task_response_encryption, 'cron', hour=custom_hour, minute=custom_minute, max_instances=1)
# scheduler.add_job(task_audio_transcript_report_cefr, 'cron', hour=custom_hour, minute=custom_minute, max_instances=1)

custom_minute = 19
scheduler.add_job(task_behaviour_proctoring_evaluation_new, 'cron', hour=custom_hour, minute=custom_minute,
                  max_instances=1)

scheduler.add_job(task_sanitizeapi, 'cron', hour=custom_hour, minute=custom_minute, max_instances=1)
scheduler.add_job(task_typing_assessment_docket, 'cron', hour=custom_hour, minute=custom_minute, max_instances=1)
scheduler.add_job(task_code_compilation, 'cron', hour=custom_hour, minute=custom_minute, max_instances=1)

# custom_hour = 17
custom_minute = 21
scheduler.add_job(task_chaining_of_2_tests, 'cron', hour=custom_hour, minute=custom_minute, max_instances=1)
scheduler.add_job(task_chaining_of_3_tests, 'cron', hour=custom_hour, minute=custom_minute, max_instances=1)
scheduler.add_job(task_email_verification, 'cron', hour=custom_hour, minute=custom_minute, max_instances=1)

custom_minute = 25
scheduler.add_job(task_rate_controller, 'cron', hour=custom_hour, minute=custom_minute, max_instances=1)
scheduler.add_job(task_device_proctoring_evaluation, 'cron', hour=custom_hour, minute=custom_minute, max_instances=1)

# Start the scheduler
scheduler.start()
scheduler.shutdown()
print("Check the report.")
