import time
import schedule

class TaskScheduler:

    def schedule_daily_job(self, at, method, *args, **kwargs):
        schedule.every().day.at(at).do(method, *args, **kwargs)


    def run_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def run_all(self):
        schedule.run_all()
