from django.contrib import admin
from django.db.models import Avg

from journal.models import Journal,JournalOrder,RatedJournal,JournalComment,JournalPayment,RequestWithdraw
# Register your models here.
class JournalAdmin(admin.ModelAdmin):
    list_display = ("journal_title","journal_category","document_type","journal_type","AVG_ratings")
    list_filter = ("jornal_author","journal_category","document_type","journal_type",)
    list_per_page = 10

    def AVG_ratings(self,obj):
        sum = 0
        a = []
        ratings = RatedJournal.objects.filter(journal_r=obj)
        for r in ratings:
            a.append(str(r))
        for i in a:
            sum += int(i)
        print(sum)
        if len(ratings) > 0:
            return sum / len(ratings)
        else:
            return 0
admin.site.register(Journal,JournalAdmin)

class JournalorderAdmin(admin.ModelAdmin):
    list_display = ("journal", "created",)
    list_filter = ("journal", "created",)
    list_per_page = 10
admin.site.register(JournalOrder,JournalorderAdmin)
class RatedAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ("journal_r","user_r","ratting_r",)
admin.site.register(RatedJournal,RatedAdmin)

admin.site.register(JournalComment)

class PaymentAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ("jouenal_owner","income")
    list_filter =("jouenal_owner",)
admin.site.register(JournalPayment,PaymentAdmin)

class Withdrawadmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ("request_user", "paypal","payment")
    list_filter = ("request_user",)
admin.site.register(RequestWithdraw,Withdrawadmin)
