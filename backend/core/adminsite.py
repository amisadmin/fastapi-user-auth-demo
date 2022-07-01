from datetime import datetime

from fastapi_user_auth.site import AuthAdminSite

from core.settings import settings

# from fastapi_amis_admin.utils.db import SqlalchemyAsyncClient
# from fastapi_user_auth.auth import Auth
# from fastapi_user_auth.auth.backends.jwt import JwtTokenStore
# from sqlalchemy.ext.asyncio import create_async_engine
#
# # 创建异步数据库引擎
# engine = create_async_engine(url=settings.database_url_async, echo=settings.debug, future=True)
#
# # 使用`JwtTokenStore`创建auth对象
# auth = Auth(db=SqlalchemyAsyncClient(engine),
#             token_store=JwtTokenStore(secret_key='09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'))
#
# # 创建后台管理系统,在导入路由之前先实例化对象
# site = AuthAdminSite(settings, auth=auth)

site = AuthAdminSite(settings)
auth = site.auth

from fastapi_scheduler import SchedulerAdmin

# # 自定义定时任务调度器
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler.jobstores.redis import RedisJobStore
# # 使用`RedisJobStore`创建任务存储
# scheduler = AsyncIOScheduler(jobstores={'default':RedisJobStore(db=2,host="127.0.0.1",port=6379,password="test")})
# scheduler = SchedulerAdmin.bind(site,scheduler=scheduler)

# 创建定时任务调度器`SchedulerAdmin`实例

scheduler = SchedulerAdmin.bind(site)


# 添加定时任务,参考官方文档: https://apscheduler.readthedocs.io/en/master/
# use when you want to run the job at fixed intervals of time
@scheduler.scheduled_job('interval', seconds=300)
def interval_task_test():
    print('interval task is run...')


# use when you want to run the job periodically at certain time(s) of day
@scheduler.scheduled_job('cron', hour=3, minute=30)
def cron_task_test():
    print('cron task is run...')


# use when you want to run the job just once at a certain point of time
@scheduler.scheduled_job('date', run_date=datetime(2022, 11, 11, 1, 2, 3))
def date_task_test():
    print('date task is run...')
