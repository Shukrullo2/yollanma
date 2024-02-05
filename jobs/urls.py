from django.urls import path
from . import views


urlpatterns = [
    path('', views.jobs, name="jobs"),
    path('job/<str:pk>', views.job, name="job"),
    path('create-job/', views.createJob, name="create-job"),
    path('delete-job/<str:pk>', views.deleteJob, name="delete-job"),
    path('update-job/<str:pk>', views.updateJob, name='update-job'),

    path('addclick/<str:pk>', views.addClick, name="add-click"),
    path('clikcs/<str:pk>', views.clicks, name="clicks"),
    path('assignjob/<str:pk>/<str:sk>', views.assignJob, name="assign-job"),
    path('deactivate/<str:pk>', views.changeJobStatus, name="change-status"),
    path('create-contract/<str:pk>/<str:sk>', views.createContract, name="create-contract"),
    path('contract/<str:pk>', views.contract, name='contract')
    ]
