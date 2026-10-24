from django.urls import path

from .views import (
    InterviewListCreateView,
    InterviewStatusUpdateView
)


urlpatterns = [

    path(
        '',
        InterviewListCreateView.as_view(),
        name='interview-list-create'
    ),

    path(
        '<int:interview_id>/status/',
        InterviewStatusUpdateView.as_view(),
        name='interview-status-update'
    ),

]