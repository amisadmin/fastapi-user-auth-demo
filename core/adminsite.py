from fastapi_amis_admin.utils.db import SqlalchemyAsyncClient
from fastapi_user_auth.auth import Auth
from fastapi_user_auth.auth.backends.jwt import JwtTokenStore
from fastapi_user_auth.site import AuthAdminSite
from sqlalchemy.ext.asyncio import create_async_engine

from core.settings import settings

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
