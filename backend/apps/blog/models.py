from datetime import datetime
from typing import Optional, List

import sqlmodel
from fastapi_amis_admin.amis.components import InputRichText, InputImage, ColumnImage
from fastapi_amis_admin.models.enums import IntegerChoices
from fastapi_amis_admin.models.fields import Field
from fastapi_user_auth.auth.models import User
from sqlalchemy import Column, String


class ArticleStatus(IntegerChoices):
    unpublished = 0, '未发布'
    published = 1, '已发布'
    inspection = 2, '审核中'
    disabled = 3, '已禁用'


# Create your models here.

class BaseSQLModel(sqlmodel.SQLModel):
    id: int = Field(default=None, primary_key=True, nullable=False)

    class Config:
        use_enum_values = True


class Category(BaseSQLModel, table=True):
    __tablename__ = 'blog_category'
    name: str = Field(title='CategoryName', sa_column=Column(String(100), unique=True, index=True, nullable=False))
    description: str = Field(default='', title='Description', amis_form_item='textarea')
    status: bool = Field(None, title='status')
    articles: List["Article"] = sqlmodel.Relationship(back_populates="category")


class ArticleTagLink(sqlmodel.SQLModel, table=True):
    __tablename__ = 'blog_article_tags'
    tag_id: Optional[int] = Field(
        default=None, foreign_key="blog_tag.id", primary_key=True
    )
    article_id: Optional[int] = Field(
        default=None, foreign_key="blog_article.id", primary_key=True
    )


class Tag(BaseSQLModel, table=True):
    __tablename__ = 'blog_tag'
    name: str = Field(..., title='TagName', sa_column=Column(String(255), unique=True, index=True, nullable=False))
    articles: List["Article"] = sqlmodel.Relationship(back_populates="tags", link_model=ArticleTagLink)


class Article(BaseSQLModel, table=True):
    __tablename__ = 'blog_article'
    title: str = Field(title='ArticleTitle', max_length=200)
    img: str = Field(None, title='ArticleImage', max_length=300,
                     amis_form_item=InputImage(maxLength=1, maxSize=2 * 1024 * 1024,
                                               receiver='post:/admin/file/upload'),
                     amis_table_column=ColumnImage(width=100, height=60, enlargeAble=True))
    description: str = Field(default='', title='ArticleDescription', amis_form_item='textarea')
    status: ArticleStatus = Field(ArticleStatus.unpublished, title='status')
    content: str = Field(..., title='ArticleContent', amis_form_item=InputRichText())
    create_time: Optional[datetime] = Field(default_factory=datetime.utcnow, title='CreateTime')
    source: str = Field(default='', title='ArticleSource', max_length=200)

    category_id: Optional[int] = Field(default=None, foreign_key="blog_category.id", title='CategoryId')
    category: Optional[Category] = sqlmodel.Relationship(back_populates="articles")

    tags: List[Tag] = sqlmodel.Relationship(back_populates="articles", link_model=ArticleTagLink)

    user_id: int = Field(default=None, foreign_key="auth_user.id", title='UserId')
    user: User = sqlmodel.Relationship()
