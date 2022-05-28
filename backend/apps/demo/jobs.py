# from datetime import datetime
#
# from core.adminsite import scheduler


# # use when you want to run the job at fixed intervals of time
# @scheduler.scheduled_job('interval', seconds=300)
# def interval_task_test():
#     print('interval task is run...')
#
#
# # use when you want to run the job periodically at certain time(s) of day
# @scheduler.scheduled_job('cron', hour=3, minute=30)
# def cron_task_test():
#     print('cron task is run...')
#
#
# # use when you want to run the job just once at a certain point of time
# @scheduler.scheduled_job('date', run_date=datetime(2022, 11, 11, 1, 1, 1))
# def date_task_test():
#     print('date task is run...')
