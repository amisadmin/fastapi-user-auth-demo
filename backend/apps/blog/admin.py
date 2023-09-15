from typing import Any, Dict, List

from core.globals import site
from fastapi_amis_admin import admin
from fastapi_amis_admin.admin import (
    AdminApp,
    FieldPermEnum,
    RecentTimeSelectPerm,
    SimpleSelectPerm,
    UserSelectPerm,
)
from fastapi_amis_admin.amis.components import PageSchema, TableColumn
from fastapi_amis_admin.crud.parser import LabelField, PropertyField
from fastapi_amis_admin.models import Field
from fastapi_user_auth.auth.models import User
from fastapi_user_auth.mixins.admin import AuthFieldModelAdmin, AuthSelectModelAdmin
from pydantic import BaseModel
from sqlmodel.sql.expression import Select
from starlette.requests import Request

from apps.blog.models import Article, ArticleStatus, Category, Tag


@site.register_admin
class BlogApp(admin.AdminApp):
    page_schema = PageSchema(label="博客应用", icon="fa fa-wordpress")
    router_prefix = "/blog"

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.register_admin(CategoryAdmin, ArticleAdmin, TagAdmin)


class CategoryAdmin(admin.ModelAdmin):
    page_schema = PageSchema(label="分类管理", icon="fa fa-folder")
    model = Category
    search_fields = [Category.name]


class TagAdmin(admin.ModelAdmin):
    page_schema = PageSchema(label="标签管理", icon="fa fa-tags")
    model = Tag
    search_fields = [Tag.name]
    link_model_fields = [Tag.articles]


class ArticleAdmin(AuthSelectModelAdmin, AuthFieldModelAdmin):
    page_schema = PageSchema(label="文章管理", icon="fa fa-file")
    model = Article
    # 配置列表展示字段
    list_display = [
        Article.id,
        Article.title,
        Article.img,
        Article.status,
        Category.name,
        User.username,
        TableColumn(type="tpl", label="自定义模板列", tpl='<a href="${source}" target="_blank">ID:${id},Title:${title}</a>'),
        Article.create_time,
        Article.description,
        User.nickname.label("nickname"),  # 重命名字段;也可以使用sqlalchemy函数, 例如:
        # func.count('*').label('article_count'), 注意在`get_select`中修改对应的sql查询语句
        LabelField(
            User.nickname.label("nickname2"),
            Field("默认用户", title="发布者"),  # 通过Field配置Amis表格列信息,Amis表单字段信息.
        ),
    ]
    # 配置模糊搜索字段
    search_fields = [Article.title, Category.name, User.username]
    # 配置关联模型
    link_model_fields = [Article.tags]
    # 读取查看表单字段
    read_fields = [
        Article,
        PropertyField(name="category", type_=Category),
        PropertyField(name="user", type_=User),
        PropertyField(name="tags", type_=List[Tag]),
    ]
    # 数据权限
    select_permissions = [
        # 最近7天创建的数据. reverse=True表示反向选择,即默认选择最近7天之内的数据
        RecentTimeSelectPerm(name="recent7_create", label="最近7天创建", td=60 * 60 * 24 * 7, reverse=True),
        # 最近30天创建的数据
        RecentTimeSelectPerm(name="recent30_create", label="最近30天创建", td=60 * 60 * 24 * 30),
        # 最近3天更新的数据
        RecentTimeSelectPerm(name="recent3_update", label="最近3天更新", td=60 * 60 * 24 * 3, time_column="update_time"),
        # 只能选择自己创建的数据, reverse=True表示反向选择,即默认选择自己创建的数据
        UserSelectPerm(name="self_create", label="自己创建", user_column="user_id", reverse=True),
        # # 只能选择自己更新的数据
        # UserSelectPerm(name="self_update", label="自己更新", user_column="update_by"),
        # 只能选择已发布的数据
        SimpleSelectPerm(name="published", label="已发布", column="status", values=[ArticleStatus.published]),
        # 只能选择状态为[1,2,3]的数据
        SimpleSelectPerm(name="status_1_2", label="状态为1_2", column="status", values=[1, 2]),
    ]
    # 字段权限
    perm_fields_exclude = {
        # 全部字段可读,无需验证权限
        FieldPermEnum.VIEW: ["__all__"],
        # 创建或更新时无需验证权限的字段
        FieldPermEnum.EDIT: ["description"],
        # 创建时无需验证权限的字段
        FieldPermEnum.CREATE: ["title", "description", "content", "img", "tags"],
    }

    # 自定义查询选择器
    async def get_select(self, request: Request) -> Select:
        sel = await super().get_select(request)
        return sel.outerjoin(Category).outerjoin(User, Article.user_id == User.id)

    async def on_create_pre(self, request: Request, obj: BaseModel, **kwargs) -> Dict[str, Any]:
        data = await super().on_create_pre(request, obj, **kwargs)
        # 创建新文章时,设置当前用户为发布者
        data["user_id"] = request.user.id
        return data
