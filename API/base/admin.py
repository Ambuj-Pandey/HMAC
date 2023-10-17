from django.contrib import admin
from base.models import User
from base.models import FileModel

from base.models import FileComparisonModel
from base.models import AIDetection

admin.site.register(User)
admin.site.register(FileModel)
admin.site.register(FileComparisonModel)
admin.site.register(AIDetection)
