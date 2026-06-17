from django.urls import path
from django.contrib.auth import views as auth_views
from . import views_accounts

app_name = "accounts"

urlpatterns = [
    path("login/",   auth_views.LoginView.as_view(template_name="accounts/login.html"),  name="login"),
    path("logout/",  auth_views.LogoutView.as_view(), name="logout"),

    path("password-reset/", auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset_form.html",
        email_template_name="accounts/password_reset_email.html",
        subject_template_name="accounts/password_reset_subject.txt",
        success_url="/accounts/password-reset/done/",
    ), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_done.html",
    ), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_confirm.html",
        success_url="/accounts/reset/complete/",
    ), name="password_reset_confirm"),
    path("reset/complete/", auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_complete.html",
    ), name="password_reset_complete"),

    path("activate/<uidb64>/<token>/", views_accounts.activate, name="activate"),
    path("profile/",                   views_accounts.profile,               name="profile"),
    path("change-password/",           views_accounts.change_password_forced, name="change_password"),
    path("team/",                      views_accounts.team_list,    name="team"),
    path("team/new/",                  views_accounts.team_create,  name="team_create"),
    path("team/<int:user_id>/edit/",   views_accounts.team_edit,    name="team_edit"),
    path("team/<int:user_id>/delete/", views_accounts.team_delete,  name="team_delete"),
]
