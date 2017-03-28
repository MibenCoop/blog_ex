from django.contrib import admin
from blog.models import Page,Category, Comment ,UserProfile


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'date_print')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author',  'date_print','id')
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username','id')


#

admin.site.register(Page, PageAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
#admin.site.register(Like,LikeAdmin)