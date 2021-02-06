from django.contrib import admin
from scope.models import ScopeManage,ScopeComment
# Register your models here.

class ScopeAdmin(admin.ModelAdmin):
    list_display = ("scope_title","user","category","post_date","end_date",)
    list_per_page = 10
    list_filter = ("category",)
    search_fields = ("scope_title","user","category")
admin.site.register(ScopeManage,ScopeAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "timestamp",)
    list_per_page = 10

admin.site.register(ScopeComment,CommentAdmin)
