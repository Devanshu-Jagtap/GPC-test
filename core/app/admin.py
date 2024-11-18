from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = Category.DisplayList

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = SubCategory.DisplayList

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = User.DisplayList

@admin.register(News)
class NewAdmin(admin.ModelAdmin):
    list_display = News.DisplayList

@admin.register(NewsImages)
class NewsImagesAdmin(admin.ModelAdmin):
    list_display = NewsImages.DisplayList

