from django.urls import path
from .import views
urlpatterns =[
    path('',views.JournalHome,name="JournalHome"),
    path('details/<str:title>/<int:id>',views.JournalDetails,name="journaldetails"),
    path('download/',views.Download,name="download"),
    path('checkout/<int:id>',views.Checkout,name="checkout"),
    path('completed/',views.paymentComplated,name="completed"),
    path('download/<int:journal_id>/', views.download_journal,name="downpdf"),
    path('rated/',views.Rated,name="rated"),
    path('ratting/',views.AddRatting,name="addratting"),
    path('add-journal/',views.Add_Journal,name="addjournals"),
    path('manage-journal/',views.JournalManage,name="managejournal"),
    path('delete-journal/<int:id>',views.DeleteJournal,name="deletejournal"),
    path('update-journal/<int:id>',views.UpdateJournal,name="updatejournal"),
    path('view-journal-info/<int:id>',views.ViewJournalInfo,name="viewjounalinfo"),
    path('request-payment/',views.RequestPayment,name="requestpayment"),
]
