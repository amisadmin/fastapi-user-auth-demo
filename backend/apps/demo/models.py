

# Create your models here.


# class Category(PkMixin, table=True):
#     __tablename__ = 'blog_category'
#     name: str = Field(
#         title='Category Name',
#         sa_column=sqlmodel.Column(sqlmodel.String(100), unique=True, index=True, nullable=False)
#     )
#     description: str = Field(default='', title='Description', amis_form_item=amis.Textarea())
#     is_active: bool = Field(None, title='Is Active')
