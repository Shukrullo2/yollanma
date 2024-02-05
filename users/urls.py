from django.contrib import admin
from django.urls import path, re_path
from . import views



urlpatterns = [
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    path('', views.profiles, name="profiles"),
    path('user/<str:pk>', views.user_profile, name="user_profile"),
    path('account/', views.userAccount, name="account"),
    path('edit-account/', views.editAccount, name="edit-account"),
    path('create-skill/', views.createSkill, name="create-skill"),
    path('delete-skill/<str:pk>', views.deleteSkill, name='delete-skill'),
    path('edit-skill/<str:pk>', views.editSkill, name='edit-skill'),
    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>', views.viewMessage, name='view-message'),
    path('create-message/<str:pk>', views.createMessage, name='create-message'),
    path('no_user/<str:pk>', views.noUser, name='no-user'),
    path('set-profile-type/', views.setProfileType, name='set-type'),
    path('companies/', views.companies, name='companies'),
    path('user-agreement/<str:pk>', views.userAgreement, name='user-agreement')
    # path('activate/<uidb64>/<token>', views.activate, name='activate')

]

