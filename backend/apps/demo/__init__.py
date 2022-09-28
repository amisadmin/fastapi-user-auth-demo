from fastapi import FastAPI


def setup(app: FastAPI):
    # 1. 导入管理应用
    # 3. 注册普通路由
    # 2. 导入定时任务
    from . import admin, apis, jobs

    app.include_router(apis.router)
