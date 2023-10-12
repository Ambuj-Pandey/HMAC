from django.contrib import admin
from base.models import User
from base.models import FileModel
from base.models import FileComparisonModel
from base.models import FileTxt

admin.site.register(User)
admin.site.register(FileModel)
admin.site.register(FileComparisonModel)
admin.site.register(FileTxt)
# Register your models here.
