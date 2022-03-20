from fastapi import FastAPI


def setup(app: FastAPI):
    # 1. 导入博客管理应用
    from . import app as blog
    # 2. 注册普通路由
    from .apis import router
    app.include_router(router)
