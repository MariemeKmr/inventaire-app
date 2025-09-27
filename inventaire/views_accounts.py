from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator as token_generator

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save(update_fields=["is_active"])
        messages.success(request, "Votre compte est activé, vous pouvez vous connecter.")
        return redirect("accounts:login")
    else:
        messages.error(request, "Lien d’activation invalide ou expiré.")
        return render(request, "accounts/activation_invalid.html", {})
