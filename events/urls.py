from django.urls import path
from.import views

urlpatterns = [
    path('',views.EventHome,name="eventhome"),
    path('details/<str:category>/<int:id>',views.DetailsEvent,name="eventdetails"),
    path('interested_event',views.interested_event,name="interested_event"),
]
