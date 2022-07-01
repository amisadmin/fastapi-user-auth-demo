from datetime import date

from fastapi_amis_admin import admin
from fastapi_amis_admin.amis import PageSchema
from fastapi_amis_admin.models.fields import Field
from fastapi_user_auth.app import UserAuthApp
from fastapi_user_auth.auth.models import BaseUser, BaseRBAC, Group
from fastapi_user_auth.site import AuthAdminSite


class MyUser(BaseUser, table=True):
    birthday: date = Field(None, title="出生日期")
    location: str = Field(None, title="位置")


class MyGroup(BaseRBAC, table=True):
    __tablename__ = 'auth_group'  # 数据库表名,必须是这个才能覆盖默认模型
    icon: str = Field(None, title='图标')
    is_active: bool = Field(default=True, title="是否激活")


class MyGroupAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = PageSchema(label='用户组管理', icon='fa fa-group')
    model = MyGroup
    link_model_fields = [Group.roles]
    readonly_fields = ['key']


class MyUserAuthApp(UserAuthApp):
    GroupAdmin = MyGroupAdmin


class MyAuthAdminSite(AuthAdminSite):
    UserAuthApp = MyUserAuthApp
