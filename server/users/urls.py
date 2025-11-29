from django.urls import path
from users.presentation.views.logout_view import LogoutView
from users.presentation.views.login_view import LoginView
from users.presentation.views.register_admin_view import RegisterAdminView
from users.presentation.views.register_candidate_view import RegisterCandidateView
from users.presentation.views.user_profile_view import UserProfileView

urlpatterns = [
    path("auth/register/admin/", RegisterAdminView.as_view(), name="register_admin"),
    path("auth/register/candidate/", RegisterCandidateView.as_view(), name="register_candidate"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/profile/", UserProfileView.as_view(), name="profile"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
]