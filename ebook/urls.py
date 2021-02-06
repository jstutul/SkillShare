from django.urls import path
from .import views
urlpatterns =[
    path('',views.EHome,name="ebbok"),
    path('category/<str:cat>',views.CategoryView,name="category"),
    path('readbook/<str:book_name>',views.Readbook,name="readbook"),
    path('subscription/',views.Subscription,name="subscription"),
    path('checkout/<str:pack>', views.Checkout, name="ebookcheckout"),
    path('subscription-complete',views.SubscriptionCompleted,name="scomplete"),
]
