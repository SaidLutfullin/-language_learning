from django.urls import path

from .views import (ChangePassword, ChangePasswordDone, LoginUser, MyProfile,
                    MyProfileEdit, PasswordResetComplete, PasswordResetConfirm,
                    PasswordResetDone, RegisterUser, ResetPassword,
                    logout_user)

urlpatterns = [
    path("login", LoginUser.as_view(), name="login"),
    path("register", RegisterUser.as_view(), name="register"),
    path("logout", logout_user, name="logout"),
    path("reset_password", ResetPassword.as_view(), name="reset_password"),
    path(
        "reset_password/<uidb64>/<token>/",
        PasswordResetConfirm.as_view(),
        name="password_reset_confirm",
    ),
    path("reset/done/", PasswordResetDone.as_view(), name="password_reset_done"),
    path(
        "reset/complete/",
        PasswordResetComplete.as_view(),
        name="password_reset_complete",
    ),
    path("change_password", ChangePassword.as_view(), name="password_change"),
    path(
        "change_password/done/",
        ChangePasswordDone.as_view(),
        name="password_change_done",
    ),
    path("my_pfofile", MyProfile.as_view(), name="my_profile"),
    path("my_pfofile/edit", MyProfileEdit.as_view(), name="my_profile_edit"),
]
