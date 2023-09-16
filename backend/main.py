from core.globals import auth, scheduler, site
from core.settings import settings
from fastapi import FastAPI
from fastapi_amis_admin_nav.admin import NavPageAdmin
from sqlmodel import SQLModel
from starlette.responses import RedirectResponse

# 创建FastAPI实例
app = FastAPI(debug=settings.debug)

# 安装应用demo
from apps import demo

demo.setup(app)
# 安装应用blog
from apps import blog

blog.setup(app)

site.register_admin(NavPageAdmin)

# 挂载后台管理系统
site.mount_app(app)


# 注意1: site.mount_app会默认添加site.db的session会话上下文中间件,如果你使用了其他的数据库连接,请自行添加.例如:
# from core.globals import sync_db
# app.add_middleware(sync_db.asgi_middleware) # 注意中间件的注册顺序.

# 注意2: 非请求上下文中,请自行创建session会话,例如:定时任务,测试脚本等.
# from core.globals import async_db
# async with async_db():
#     async_db.async_get(...)
#     async_db.session.get(...)
#     # do something


# 添加启动运行事件
@app.on_event("startup")
async def startup():
    await site.db.async_run_sync(SQLModel.metadata.create_all, is_session=False)
    # 创建默认管理员,用户名: admin,密码: admin, 请及时修改密码!!!
    await auth.create_role_user("admin")
    # 创建默认超级管理员,用户名: root,密码: root, 请及时修改密码!!!
    await auth.create_role_user("root")
    # 运行site的startup方法,加载casbin策略等
    await site.router.startup()
    if not auth.enforcer.enforce("u:admin", site.unique_id, "page", "page"):
        await auth.enforcer.add_policy("u:admin", site.unique_id, "page", "page", "allow")
    # 启动定时任务
    scheduler.start()


# 注册首页路由
@app.get("/")
async def index():
    return RedirectResponse(url=site.router_path)
