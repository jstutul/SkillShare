from django.urls import path
from.import views

urlpatterns = [
    path('',views.CommunityHome,name="communityhome"),
    path('add-post',views.AddPost,name="addcommunity"),
    path('manage-community',views.ManageC,name="managec"),
    path('delete-community/<int:id>',views.DeleteC,name="communitydelete"),
    path('update-community/<int:id>',views.UpdateC,name="communityupdate"),
    path('view-community/<int:id>',views.ViewC,name="communityview"),


]
