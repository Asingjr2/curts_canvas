from django.contrib import admin
from django.contrib.auth.models import User

from .models import Picture, Rating


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    fields = ("name", "creator", "description", "price", "avg_rating", "total_rating")
    list_display = ["name"]


admin.site.register(Rating)