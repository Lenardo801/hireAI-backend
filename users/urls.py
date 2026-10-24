from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    AdminUsersView,
    AdminRecruitersView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),

    path(
        "admin/users/",
        AdminUsersView.as_view(),
        name="admin-users",
    ),

    path(
        "admin/recruiters/",
        AdminRecruitersView.as_view(),
        name="admin-recruiters",
    ),
]