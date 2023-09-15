from datetime import datetime
from typing import List, Optional

from fastapi_amis_admin.amis.components import ColumnImage, InputImage, InputRichText
from fastapi_amis_admin.models.enums import IntegerChoices
from fastapi_amis_admin.models.fields import Field
from fastapi_user_auth.auth.models import User
from fastapi_user_auth.mixins.models import PkMixin
from sqlalchemy import Column, String, select
from sqlalchemy.orm import Session
from sqlmodel import Relationship
from sqlmodelx import SQLModel


class ArticleStatus(IntegerChoices):
    unpublished = 0, "未发布"
    published = 1, "已发布"
    inspection = 2, "审核中"
    disabled = 3, "已禁用"


# Create your models here.


class Category(PkMixin, table=True):
    __tablename__ = "blog_category"
    name: str = Field(title="CategoryName", sa_column=Column(String(100), unique=True, index=True, nullable=False))
    description: str = Field(default="", title="Description", amis_form_item="textarea")
    status: bool = Field(False, title="status")
    articles: List["Article"] = Relationship(back_populates="category")


class ArticleTagLink(SQLModel, table=True):
    __tablename__ = "blog_article_tags"
    tag_id: Optional[int] = Field(default=None, foreign_key="blog_tag.id", primary_key=True)
    article_id: Optional[int] = Field(default=None, foreign_key="blog_article.id", primary_key=True)


class Tag(PkMixin, table=True):
    __tablename__ = "blog_tag"
    name: str = Field(..., title="TagName", sa_column=Column(String(255), unique=True, index=True, nullable=False))
    articles: List["Article"] = Relationship(back_populates="tags", link_model=ArticleTagLink)


class Article(PkMixin, table=True):
    __tablename__ = "blog_article"
    title: str = Field(title="ArticleTitle", max_length=200)
    img: str = Field(
        None,
        title="ArticleImage",
        max_length=300,
        amis_form_item=InputImage(maxLength=1, maxSize=2 * 1024 * 1024, receiver="post:/admin/file/upload"),
        amis_table_column=ColumnImage(width=100, height=60, enlargeAble=True),
    )
    description: str = Field(default="", title="ArticleDescription", amis_form_item="textarea")
    status: ArticleStatus = Field(ArticleStatus.unpublished, title="status")
    content: str = Field(..., title="ArticleContent", amis_form_item=InputRichText())
    create_time: Optional[datetime] = Field(default_factory=datetime.utcnow, title="CreateTime")
    source: str = Field(default="", title="ArticleSource", max_length=200)

    category_id: Optional[int] = Field(default=None, foreign_key="blog_category.id", title="CategoryId")
    category: Optional[Category] = Relationship(back_populates="articles")

    tags: List[Tag] = Relationship(back_populates="articles", link_model=ArticleTagLink)

    user_id: int = Field(default=None, foreign_key="auth_user.id", title="UserId")
    user: User = Relationship()

    @staticmethod
    def check_update_permission(session: Session, user: User, item_id: List[str]):
        # 管理员可以修改全部文章, 并且可以批量修改.
        if user.has_requires(session, roles=["admin"]):
            return True
        # 非管理员,只能修改自己的文章,并且不可批量修改.
        if len(item_id) > 1:
            return False
        stmt = select(1).where(Article.id == item_id[0], Article.user_id == user.id)
        return bool(session.scalar(stmt))
