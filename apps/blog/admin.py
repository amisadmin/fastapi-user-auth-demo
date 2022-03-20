from datetime import datetime, timedelta
from typing import List, Dict, Any
from fastapi_amis_admin.amis.components import PageSchema, TableColumn
from fastapi_amis_admin.amis_admin import admin
from fastapi_amis_admin.crud.schema import Paginator
from fastapi_user_auth.auth.models import User
from pydantic import BaseModel
from sqlmodel.sql.expression import Select, select
from starlette.requests import Request
from apps.blog.models import Category, Article, Tag


class CategoryAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = PageSchema(label='分类管理', icon='fa fa-folder')
    model = Category
    search_fields = [Category.name]


class TagAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = PageSchema(label='标签管理', icon='fa fa-tags')
    model = Tag
    search_fields = [Tag.name]
    link_model_fields = [Tag.articles]


class ArticleAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = PageSchema(label='文章管理', icon='fa fa-file')
    model = Article
    # 配置列表展示字段
    list_display = [Article.id, Article.title, Article.img, Article.status,
                    Category.name, User.username,
                    TableColumn(type='tpl', label='自定义模板列',
                                tpl='<a href="${source}" target="_blank">ID:${id},Title:${title}</a>'),
                    Article.create_time, Article.description,
                    ]
    # 配置模糊搜索字段
    search_fields = [Article.title, Category.name, User.username]
    # 配置关联模型
    link_model_fields = [Article.tags]

    # 自定义查询选择器
    async def get_select(self, request: Request) -> Select:
        sel = await super().get_select(request)
        return sel.join(Category, isouter=True).join(User, isouter=True)

    # 权限验证
    async def has_page_permission(self, request: Request) -> bool:
        return True

    async def has_list_permission(
            self, request: Request, paginator: Paginator,
            filter: BaseModel = None, **kwargs
    ) -> bool:
        # 用户未登录,不可按标题过滤文章,并且最多每页最多只能查看10条数据.
        return bool(
            await self.site.auth.requires(response=False)(request)
            or (paginator.perPage <= 10 and filter.title == '')
        )

    async def has_create_permission(
            self, request: Request, data: BaseModel, **kwargs
    ) -> bool:
        # 用户已登录,并且注册时间大于3天,才可以发布文章
        return bool(
            await self.site.auth.requires(response=False)(request)
            and request.user.create_time < datetime.now() - timedelta(days=3)
        )

    async def has_delete_permission(
            self, request: Request, item_id: List[str], **kwargs
    ) -> bool:
        # 必须管理员才可以删除文章.
        return await self.site.auth.requires(roles='admin', response=False)(request)

    async def has_update_permission(
            self, request: Request, item_id: List[str],
            data: BaseModel, **kwargs
    ) -> bool:
        if await self.site.auth.requires(response=False)(request):
            if item_id is None:
                return True
            async with self.site.db.session_maker() as session:
                # 管理员可以修改全部文章, 并且可以批量修改.
                if await request.user.has_role(['admin'], session):
                    return True
                # 非管理员,只能修改自己的文章,并且不可批量修改.
                result = await session.execute(
                    select(Article.id).where(
                        Article.id == item_id[0], Article.user_id == request.user.id
                    ).limit(1)
                )
            if result.first():
                return True
        return False

    async def on_create_pre(
            self, request: Request, obj: BaseModel, **kwargs
    ) -> Dict[str, Any]:
        data = await super().on_create_pre(request, obj, **kwargs)
        # 创建新文章时,设置当前用户为发布者
        data['user_id'] = request.user.id
        return data
