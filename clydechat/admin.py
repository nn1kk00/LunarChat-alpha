from django.contrib import admin
from .models import User, BannedUser, BannedIP
# Register your models here.

class AdminUsers(admin.ModelAdmin):
    last_display = ("name", "uid", "last_ip", "role")
class AdminBannedUsers(admin.ModelAdmin):
    last_display = ("name", "end_date")
class AdminBannedIPs(admin.ModelAdmin):
    last_display = ("id", "end_date")

admin.site.register(User, AdminUsers)
admin.site.register(BannedUser, AdminBannedUsers)
admin.site.register(BannedIP, AdminBannedIPs)