from django.contrib import admin
from community.models import Blog,BlogComment,SubComment

class Blogadmin(admin.ModelAdmin):
    list_display = ("title","author","post_on")
    list_per_page = 10
    search_fields = ("title",)
    list_filter = ("author",)
admin.site.register(Blog,Blogadmin)

class BlogCommentadmin(admin.ModelAdmin):
    list_display = ("post","user","time")
    list_per_page = 10
    search_fields = ("post",)
    list_filter = ("post","time")
admin.site.register(BlogComment,BlogCommentadmin)

class BlogSubCommentadmin(admin.ModelAdmin):
    list_display = ("post","comment","user","time")
    list_per_page = 10
    list_filter = ("post","user")
admin.site.register(SubComment,BlogSubCommentadmin)
