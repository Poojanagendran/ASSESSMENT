import datetime
import time
started = datetime.datetime.now()
time.sleep(5)
ended = datetime.datetime.now()
time_taken = str(ended - started)
print(time_taken)