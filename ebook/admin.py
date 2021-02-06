from django.contrib import admin
from ebook.models import *
# Register your models here.

class EbookAdmin(admin.ModelAdmin):
    list_display = ("book_name","book_author","category","book_type","book_publish")
    list_filter =  ("book_author","category","book_type","book_publish")
    list_per_page = 10
    search_fields = ("book_name","book_author")
admin.site.register(Ebook,EbookAdmin)

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("subscriber","until_date","payment")
    list_filter = ("subscriber","until_date",)
    list_per_page = 10
admin.site.register(Subscriber,SubscriberAdmin)
