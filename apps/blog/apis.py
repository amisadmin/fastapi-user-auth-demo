import datetime
from fastapi import APIRouter, Depends
from sqlalchemy import update
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.requests import Request

from apps.blog.models import Article
from core.adminsite import site, auth

# 通过注册依赖方式验证用户权限,当前路由注册器下全部路由都将进行权限验证.
# router = APIRouter(prefix='/articles', tags=['ArticleAPI'],dependencies=Depends(auth.requires()()))

router = APIRouter(prefix='/articles', tags=['ArticleAPI'])


@router.get('/read/{id}', response_model=Article)
@auth.requires()  # 要求必须登录
async def read_article(request: Request, id: int,
                       session: AsyncSession = Depends(site.db.session_factory)):
    stmt = select(Article).where(Article.id == id)
    result = await session.execute(stmt)
    return result.scalar()


@router.get('/update/{id}', response_model=Article)
@auth.requires(roles='admin')  # 要求必须登录,并且是管理员角色
async def update_article(request: Request, id: int,
                         session: AsyncSession = Depends(site.db.session_factory)):
    stmt = update(Article).where(Article.id == id).values({'create_time': datetime.datetime.now()})
    result = await session.execute(stmt)
    await session.commit()
    return await read_article(request,id, session)
