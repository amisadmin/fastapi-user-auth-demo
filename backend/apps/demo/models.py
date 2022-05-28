import sqlmodel
from fastapi_amis_admin import amis
from fastapi_amis_admin.models.fields import Field


# Create your models here.

class BaseSQLModel(sqlmodel.SQLModel):
    id: int = Field(default=None, primary_key=True, nullable=False)

    class Config:
        use_enum_values = True


# class Category(BaseSQLModel, table=True):
#     __tablename__ = 'blog_category'
#     name: str = Field(
#         title='Category Name',
#         sa_column=sqlmodel.Column(sqlmodel.String(100), unique=True, index=True, nullable=False)
#     )
#     description: str = Field(default='', title='Description', amis_form_item=amis.Textarea())
#     is_active: bool = Field(None, title='Is Active')
