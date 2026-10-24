from django.urls import path

from .views import (
    JobListCreateView,
    ApplicationCreateView,
    ApplicationListView,
    ApplicationStatusUpdateView,
    InterviewCreateView,
    InterviewListView,
    InterviewUpdateView,
    admin_analytics_view,
)

urlpatterns = [

    path(
        '',
        JobListCreateView.as_view()
    ),

    path(
        'apply/',
        ApplicationCreateView.as_view()
    ),

    path(
        'applications/',
        ApplicationListView.as_view()
    ),

    path(
        'applications/<int:application_id>/status/',
        ApplicationStatusUpdateView.as_view()
    ),


    path(
        "interviews/create/",
        InterviewCreateView.as_view(),
    ),

    path(
        "interviews/list/",
        InterviewListView.as_view()
    ),

    path(
        "interviews/<int:interview_id>/update/",
        InterviewUpdateView.as_view(),
        name="interview-update"
    ),



    path('api/admin/analytics/', admin_analytics_view, name='admin-analytics'),
]
