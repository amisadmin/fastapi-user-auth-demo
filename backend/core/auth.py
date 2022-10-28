from datetime import date

from fastapi_amis_admin import admin
from fastapi_amis_admin.amis import PageSchema
from fastapi_amis_admin.models.fields import Field
from fastapi_user_auth.app import UserAuthApp
from fastapi_user_auth.auth.models import (
    CreateTimeMixin,
    Group,
    User,
    UserRoleLink,
)
from fastapi_user_auth.site import AuthAdminSite
from sqlalchemy import String, cast
from sqlalchemy.orm import column_property


class MyUser(User, table=True):
    point: float = Field(default=0, title="积分", description="用户积分")
    phone: str = Field(None, title="手机号", max_length=15)
    parent_id: int = Field(None, title="上级", foreign_key="auth_user.id")
    birthday: date = Field(None, title="出生日期")
    location: str = Field(None, title="位置")


class MyGroup(Group, table=True):
    __tablename__ = "auth_group"  # 数据库表名,必须是这个才能覆盖默认模型
    icon: str = Field(None, title="图标")
    is_active: bool = Field(default=True, title="是否激活")


class MyGroupAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = PageSchema(label="用户组管理", icon="fa fa-group")
    model = MyGroup
    link_model_fields = [Group.roles]
    readonly_fields = ["key"]


class MyUserRoleLink(UserRoleLink, CreateTimeMixin, table=True):
    # 重写UserRoleLink模型, 并且创建id虚拟主键字段
    id: str = Field(
        None, title="虚拟主键",
        sa_column=column_property(f"{cast(UserRoleLink.user_id, String)}-{cast(UserRoleLink.role_id, String)}")
    )

    description: str = Field(None, title="描述")


class MyUserRoleLinkAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = PageSchema(label="用户角色关系", icon="fa fa-group")
    model = MyUserRoleLink
    readonly_fields = ["id"]


class MyUserAuthApp(UserAuthApp):
    GroupAdmin = MyGroupAdmin

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register_admin(MyUserRoleLinkAdmin)


class MyAuthAdminSite(AuthAdminSite):
    UserAuthApp = MyUserAuthApp
