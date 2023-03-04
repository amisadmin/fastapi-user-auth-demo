from datetime import datetime, timedelta
from typing import Any, Dict, List

from apps.blog.models import Article, Category, Tag
from core.adminsite import site
from fastapi_amis_admin import admin
from fastapi_amis_admin.admin import AdminApp, PageSchemaAdmin
from fastapi_amis_admin.amis.components import PageSchema, TableColumn
from fastapi_amis_admin.crud.parser import LabelField, PropertyField
from fastapi_amis_admin.crud.schema import Paginator
from fastapi_amis_admin.models import Field
from fastapi_user_auth.auth.models import User
from pydantic import BaseModel
from sqlmodel.sql.expression import Select
from starlette.requests import Request


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


class ArticleAdmin(admin.ModelAdmin):
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

    # 自定义查询选择器
    async def get_select(self, request: Request) -> Select:
        sel = await super().get_select(request)
        return sel.join(Category, isouter=True).join(User, isouter=True)

    # 权限验证
    async def has_page_permission(self, request: Request, obj: PageSchemaAdmin = None, action: str = None) -> bool:
        return True

    async def has_list_permission(self, request: Request, paginator: Paginator, filters: BaseModel = None, **kwargs) -> bool:
        # 用户未登录,不可按标题过滤文章,并且最多每页最多只能查看10条数据.
        return bool(await self.site.auth.requires(response=False)(request) or (paginator.perPage <= 10 and filters.title == ""))

    async def has_create_permission(self, request: Request, data: BaseModel, **kwargs) -> bool:
        # 用户已登录,并且注册时间大于3天,才可以发布文章
        return bool(
            await self.site.auth.requires(response=False)(request)
            and request.user.create_time < datetime.now() - timedelta(days=3)
        ) or await self.site.auth.requires(roles="admin", response=False)(request)

    async def has_delete_permission(self, request: Request, item_id: List[str], **kwargs) -> bool:
        # 必须管理员才可以删除文章.
        return await self.site.auth.requires(roles="admin", response=False)(request)

    async def has_update_permission(self, request: Request, item_id: List[str], data: BaseModel, **kwargs) -> bool:
        if not await self.site.auth.requires(response=False)(request):
            return False
        if item_id is None:
            return True
        return await self.site.db.async_run_sync(Article.check_update_permission, request.user, item_id)

    async def on_create_pre(self, request: Request, obj: BaseModel, **kwargs) -> Dict[str, Any]:
        data = await super().on_create_pre(request, obj, **kwargs)
        # 创建新文章时,设置当前用户为发布者
        data["user_id"] = request.user.id
        return data
