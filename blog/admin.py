from django.contrib import admin
from blog.models import Page,Category
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'date_print')

admin.site.register(Page, PageAdmin)
admin.site.register(Category,CategoryAdmin)