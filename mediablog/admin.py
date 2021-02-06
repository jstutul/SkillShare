from django.contrib import admin
from mediablog.models import *
# Register your models here.
class Mediaadmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ("title","author","post_on",)
    list_filter = ("author",)

admin.site.register(MediaBlog,Mediaadmin)

class CommentAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ("post","user","timestamp",)
admin.site.register(Comment,CommentAdmin)

class ReactAdmin(admin.ModelAdmin):
    list_display = ("post","user","reaction_type",)
admin.site.register(Reaction,ReactAdmin)
