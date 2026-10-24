from django.urls import path

from .views import (
    ApplicationListCreateView,
    ApplicationStatusUpdateView
)


urlpatterns = [

    path(
        '',
        ApplicationListCreateView.as_view(),
        name='application-list-create'
    ),

    path(
        '<int:application_id>/status/',
        ApplicationStatusUpdateView.as_view(),
        name='application-status-update'
    ),

]