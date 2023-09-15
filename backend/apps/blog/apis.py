import datetime

from fastapi import APIRouter
from fastapi_amis_admin.globals.deps import AsyncSess
from fastapi_user_auth.globals.deps import CurrentUser

from apps.blog.models import Article

# 通过注册依赖方式验证用户权限,当前路由注册器下全部路由都将进行权限验证.
router = APIRouter(prefix="/articles", tags=["ArticleAPI"])


@router.get("/update/{id}", response_model=Article, summary="更新文章")
async def update_article(id: int, session: AsyncSess, user: CurrentUser):
    article = await session.get(Article, id)
    if article:
        article.user_id = user.id
        article.create_time = datetime.datetime.now()
        await session.flush()
    return article
