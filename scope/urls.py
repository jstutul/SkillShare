from django.urls import path
from.import views

urlpatterns = [
    path('',views.ScopeHome,name="scopehome"),
    path('details/<str:category>/<int:id>',views.ScopeView,name="scopeview"),
    path('scope-like/',views.scope_like,name="scope_like"),
    path('scope-love/',views.scope_love,name="scope_love"),

]
