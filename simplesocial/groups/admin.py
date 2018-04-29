from django.contrib import admin
from . import models
# Register your models here.

# This class allows editing groupmembers under group in admin view.
class GroupMemberInline(admin.TabularInline):
    model = models.GroupMember

admin.site.register(models.Group)
