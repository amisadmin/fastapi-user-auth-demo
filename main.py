from fastapi import FastAPI
from starlette.responses import RedirectResponse

from core.adminsite import site, auth, scheduler
from apps import blog

app = FastAPI(debug=True)
# 导入已注册的后台管理类
blog.setup(app)
# 挂载后台管理系统
site.mount_app(app)


@app.get('/')
async def index():
    return RedirectResponse(url=site.router_path)


@app.on_event("startup")
async def startup():
    scheduler.start()
    await site.create_db_and_tables()
    await auth.create_role_user(role_key='admin')
    await auth.create_role_user(role_key='vip')
    await auth.create_role_user(role_key='test')
