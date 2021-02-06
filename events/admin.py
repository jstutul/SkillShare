from django.contrib import admin
from events.models import *

class EventAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ("event_title","event_organizar","category","post_on","seat_limit","entry_fee")
    list_filter = ("event_organizar","category",)
admin.site.register(EventManager,EventAdmin)

class EventCommentAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ("post","user","timestamp",)
    list_filter = ("user",)
admin.site.register(EventComment,EventCommentAdmin)
