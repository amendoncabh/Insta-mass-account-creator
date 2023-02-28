"""
Use the background scheduler to schedule a job that executes on timing second intervals.
"""

import os
import time

from apscheduler.schedulers.background import BackgroundScheduler

__scheduler = BackgroundScheduler()

def schedule(task, interval=1):
    __scheduler.add_job(task, 'interval', seconds = (interval  * 60))
    __scheduler.start()

    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        __scheduler.shutdown()
