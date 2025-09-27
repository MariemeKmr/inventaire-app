from django.urls import path
from django.contrib.auth import views as auth_views
from . import views_accounts  # on crée ce fichier ci-dessous

app_name = "accounts"

urlpatterns = [
    # Auth
    path("login/",  auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"), 

    # Mot de passe oublié (flow complet)
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

    # Activation de compte via lien e-mail
    path("activate/<uidb64>/<token>/", views_accounts.activate, name="activate"),
]
