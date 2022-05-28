from fastapi_amis_admin import amis
from fastapi_amis_admin import amis_admin as admin
from fastapi_amis_admin.amis_admin.admin import AdminApp

from core.adminsite import site
# from .models import Category


@site.register_admin
class MsgApp(admin.AdminApp):
    page_schema = amis.PageSchema(label='Demo', icon='fa fa-bolt')
    router_prefix = '/demo'

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        # self.register_admin(CategoryAdmin)


# Register your models here.

# class CategoryAdmin(admin.ModelAdmin):
#     group_schema = None
#     page_schema = amis.PageSchema(label='Category', icon='fa fa-folder')
#     model = Category
#     search_fields = [Category.name]
