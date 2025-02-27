from django.contrib import admin
from .models import * 

admin.site.register(FileStack)
admin.site.register(ImageStack)
admin.site.register(ReviseStack)
admin.site.register(ReportStack)
admin.site.register(Task)