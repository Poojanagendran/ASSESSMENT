import subprocess
import time
import threading
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
                time.sleep(5)
            else:
                print(f"{script_name} failed after {max_retries} attempts.")
    return success


# Thread wrapper for non-blocking job execution
def threaded_job(script_name, relative_path):
    def job():
        script_path = str(path) + relative_path
        print(script_path)
        if run_script(script_name, script_path):
            time.sleep(2)
    threading.Thread(target=job).start()


# Scheduler setup
scheduler = BlockingScheduler()

# Job mappings
jobs = [
    ("coding_group_level", "/SCRIPTS/UI_SCRIPTS/CLIENT_RANDOMIZATION/coding_group_level.py"),
    ("coding_section_level", "/SCRIPTS/UI_SCRIPTS/CLIENT_RANDOMIZATION/coding_section_level.py"),
    ("coding_test_level", "/SCRIPTS/UI_SCRIPTS/CLIENT_RANDOMIZATION/coding_test_level.py"),
    ("mca_group_level", "/SCRIPTS/UI_SCRIPTS/CLIENT_RANDOMIZATION/mca_group_level.py"),
    ("mca_section_level", "/SCRIPTS/UI_SCRIPTS/CLIENT_RANDOMIZATION/mca_section_level.py"),
    ("mca_test_level", "/SCRIPTS/UI_SCRIPTS/CLIENT_RANDOMIZATION/mca_test_level.py"),
    ("mcq_group_level", "/SCRIPTS/UI_SCRIPTS/CLIENT_RANDOMIZATION/mcq_group_level.py"),
    ("mcq_section_level", "/SCRIPTS/UI_SCRIPTS/CLIENT_RANDOMIZATION/mcq_section_level.py"),
    ("mcq_test_level", "/SCRIPTS/UI_SCRIPTS/CLIENT_RANDOMIZATION/mcq_test_level.py"),
    ("mcq_weightage_group_level", "/SCRIPTS/UI_SCRIPTS/CLIENT_RANDOMIZATION/mcq_weightage_group_level.py"),
    ("mcq_weightage_section_level", "/SCRIPTS/UI_SCRIPTS/CLIENT_RANDOMIZATION/mcq_weightage_section_level.py"),
    ("mcq_weightage_test_level", "/SCRIPTS/UI_SCRIPTS/CLIENT_RANDOMIZATION/mcq_weightage_test_level.py"),
    ("subjective_group_level", "/SCRIPTS/UI_SCRIPTS/CLIENT_RANDOMIZATION/subjective_group_level.py"),
    ("subjective_section_level", "/SCRIPTS/UI_SCRIPTS/CLIENT_RANDOMIZATION/subjective_section_level.py"),
    ("subjective_test_level", "/SCRIPTS/UI_SCRIPTS/CLIENT_RANDOMIZATION/subjective_test_level.py"),
]

# Start time
custom_hour = 18
custom_minute = 45

# Register jobs with scheduler
for job_name, relative_path in jobs:
    scheduler.add_job(
        threaded_job,
        args=[job_name, relative_path],
        trigger='cron',
        hour=custom_hour,
        minute=custom_minute,
        max_instances=1,
        misfire_grace_time=300
    )
    # Update time for next job
    custom_hour, custom_minute = (custom_hour + (custom_minute + 4) // 60) % 24, (custom_minute + 4) % 60

# Start the scheduler
try:
    print("Starting scheduler...")
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    print("Shutting down scheduler...")
    scheduler.shutdown()
