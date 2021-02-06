from django.contrib import admin
from accounts.models import *

class ContactUSAdmin(admin.ModelAdmin):
    list_display = ("fullname", "email","post_on")
    list_filter = ("fullname","email","company")
    list_per_page = 10
    search_fields = ("fullname","email",)
admin.site.register(contactUs,ContactUSAdmin)

class RegularAdmin(admin.ModelAdmin):
    list_display = ("user_r","phone","city")
    list_filter = ("city",)
    list_per_page = 10
admin.site.register(RegularUser,RegularAdmin)

class OrganizationAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ("o_name","phone","city","web")
    list_filter = ("city",)
admin.site.register(OrganizationUser,OrganizationAdmin)