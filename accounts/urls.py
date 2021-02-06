from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path
from.import views

urlpatterns = [
    path('signup-user/', views.SIgnupView, name="signup"),
    path('login/', views.LoginView, name="login"),
    path('logout/', views.Logout_view, name="logout"),
    path('password-change/',views.PasswordChange,name="passwordchange"),
    path('regular/', views.RegularView, name="regular"),
    path('organization/', views.OrganizationView, name="organization"),
    path('activate/(<uidb64>[0-9A-Za-z_\-]+)/(<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         views.activate, name='activate'),
    path('reset-password',
         PasswordResetView.as_view(template_name='user/password_reset_form.html'), name='password_reset'),
    path('reset-password/done',
         PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>[0-9A-Za-z]+)-<token>/',
         PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset-password/complete/',
         PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'),
         name='password_reset_complete'),

    path('dashboard/', views.Dashboard, name="dashboard"),
    path('update-profile/',views.UpdateOrganization,name="updateorg"),
    path('update-regular-user/',views.UpdateRegular,name="updateregular"),

    path('post-media/', views.PostMedia, name="postmedia"),
    path('view-media/', views.ViewMedia, name="viewmedia"),
    path('view-media-post/<int:id>', views.Viewmediapost, name="viewmediapost"),
    path('edit-media-post/<int:id>', views.Updatepost, name="mediaupdate"),
    path('delete/<int:id>/', views.media_delete, name='media_delete'),

    path('add-event/', views.AddEvent, name="addevent"),
    path('view-event/',views.ViewEvent,name="viewevent"),
    path('view-event-post/<int:id>', views.Vieweventpost, name="vieweventpost"),
    path('edit-event-post/<int:id>', views.Updateeventpost, name="eventupdate"),
    path('event-delete/<int:id>',views.DeleteEvent,name="eventdelete"),

    path('dashboard/add-scope/',views.AddScope,name="addscope"),
    path('dashboard/manage-scope/',views.VieweScope,name="managescope"),
    path('dashboard/view-scope-post/<int:id>',views.VieweScopePost,name="viewscopepost"),
    path('dashboard/edit-scope-post/<int:id>',views.EditScopePost,name="editscopepost"),
    path('dashboard/delete-scope-post/<int:id>',views.DeleteScope,name="deletescope"),

    path('dashboard/add-book/',views.AddBook,name="addbook"),
    path('dashboard/manage-book/',views.ManageBook,name="managebook"),
    path('dashboard/edit-book/<int:id>',views.EditBook,name="editbook"),
    path('dashboard/delete-book/<int:id>',views.DeleteBook,name="deletebook"),


]
