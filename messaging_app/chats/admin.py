from django.contrib import admin
from .models import User  # NOT Message

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass