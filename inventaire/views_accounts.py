from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator as token_generator


def activate(request, uidb64, token):
    try:
        uid  = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None
    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save(update_fields=["is_active"])
        messages.success(request, "Compte activé, vous pouvez vous connecter.")
        return redirect("accounts:login")
    messages.error(request, "Lien d'activation invalide ou expiré.")
    return render(request, "accounts/activation_invalid.html", {})


def _admin_required(request):
    return request.user.is_authenticated and request.user.is_staff


def _has_other_active_admin(exclude_user):
    return User.objects.filter(is_staff=True, is_active=True).exclude(pk=exclude_user.pk).exists()


# ── Middleware-like : forcer changement de mot de passe temporaire ──
def _must_change_password(user):
    return getattr(user, 'profile', None) and user.profile.must_change_password


# ── Profil ──────────────────────────────────────────────────────────
@login_required
def profile(request):
    # Forcer changement si mot de passe temporaire
    if request.user.profile.must_change_password and request.path != '/accounts/change-password/':
        return redirect("accounts:change_password")

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "info":
            request.user.first_name = request.POST.get("first_name", "").strip()
            request.user.last_name  = request.POST.get("last_name",  "").strip()
            email = request.POST.get("email", "").strip()
            if email and email != request.user.email:
                if User.objects.exclude(pk=request.user.pk).filter(email=email).exists():
                    messages.error(request, "Cet email est déjà utilisé.")
                    return redirect("accounts:profile")
                request.user.email = email
            request.user.save()
            messages.success(request, "Profil mis à jour.")

        elif action == "password":
            old     = request.POST.get("old_password", "")
            new     = request.POST.get("new_password", "")
            confirm = request.POST.get("confirm_password", "")
            if not request.user.check_password(old):
                messages.error(request, "Mot de passe actuel incorrect.")
            elif len(new) < 8:
                messages.error(request, "8 caractères minimum.")
            elif new != confirm:
                messages.error(request, "Les mots de passe ne correspondent pas.")
            else:
                request.user.set_password(new)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "Mot de passe modifié.")

        return redirect("accounts:profile")

    return render(request, "accounts/profile.html", {"user": request.user})


# ── Changement mot de passe temporaire (obligatoire) ────────────────
@login_required
def change_password_forced(request):
    if request.method == "POST":
        new     = request.POST.get("new_password", "")
        confirm = request.POST.get("confirm_password", "")
        if len(new) < 8:
            messages.error(request, "8 caractères minimum.")
        elif new != confirm:
            messages.error(request, "Les mots de passe ne correspondent pas.")
        else:
            request.user.set_password(new)
            request.user.save()
            update_session_auth_hash(request, request.user)
            request.user.profile.must_change_password = False
            request.user.profile.save()
            messages.success(request, "Mot de passe défini. Bienvenue !")
            return redirect("dashboard")

    return render(request, "accounts/change_password_forced.html")


# ── Liste equipe ────────────────────────────────────────────────────
@login_required
def team_list(request):
    if not _admin_required(request):
        messages.error(request, "Accès réservé à l'administrateur.")
        return redirect("dashboard")
    # Autres utilisateurs seulement (pas soi-même)
    others = User.objects.exclude(pk=request.user.pk).order_by("username")
    return render(request, "accounts/team_list.html", {
        "users": others,
        "current_user": request.user,
    })


# ── Créer utilisateur ───────────────────────────────────────────────
@login_required
def team_create(request):
    if not _admin_required(request):
        messages.error(request, "Accès réservé à l'administrateur.")
        return redirect("dashboard")

    if request.method == "POST":
        username   = request.POST.get("username", "").strip()
        first_name = request.POST.get("first_name", "").strip()
        last_name  = request.POST.get("last_name",  "").strip()
        email      = request.POST.get("email", "").strip()
        password   = request.POST.get("password", "")
        role       = request.POST.get("role", "vendeur")

        if not username or not password:
            messages.error(request, "Nom d'utilisateur et mot de passe obligatoires.")
            return render(request, "accounts/team_form.html", {"mode": "new", "form": request.POST})
        if User.objects.filter(username=username).exists():
            messages.error(request, f"'{username}' est déjà pris.")
            return render(request, "accounts/team_form.html", {"mode": "new", "form": request.POST})
        if len(password) < 4:
            messages.error(request, "Le mot de passe temporaire doit faire au moins 4 caractères.")
            return render(request, "accounts/team_form.html", {"mode": "new", "form": request.POST})

        user = User.objects.create_user(
            username=username, email=email, password=password,
            first_name=first_name, last_name=last_name,
            is_staff=(role == "admin"), is_active=True,
        )
        # Marquer le mot de passe comme temporaire
        user.profile.must_change_password = True
        user.profile.save()

        messages.success(request, f"Utilisateur '{username}' créé. Mot de passe temporaire : {password}")
        return redirect("accounts:team")

    return render(request, "accounts/team_form.html", {"mode": "new", "form": {}})


# ── Modifier utilisateur ────────────────────────────────────────────
@login_required
def team_edit(request, user_id):
    if not _admin_required(request):
        messages.error(request, "Accès réservé à l'administrateur.")
        return redirect("dashboard")

    member = get_object_or_404(User, pk=user_id)

    # On ne peut pas s'éditer soi-même ici
    if member == request.user:
        messages.info(request, "Pour modifier votre propre compte, allez dans Mon profil.")
        return redirect("accounts:profile")

    if request.method == "POST":
        role      = request.POST.get("role", "vendeur")
        is_active = request.POST.get("is_active") == "1"

        # Protection dernier admin
        if member.is_staff and (role != "admin" or not is_active):
            if not _has_other_active_admin(member):
                messages.error(request, "Impossible : il doit rester au moins un administrateur actif.")
                return redirect("accounts:team_edit", user_id=user_id)

        member.first_name = request.POST.get("first_name", "").strip()
        member.last_name  = request.POST.get("last_name",  "").strip()
        member.email      = request.POST.get("email", "").strip()
        member.is_staff   = (role == "admin")
        member.is_active  = is_active

        new_pw = request.POST.get("password", "").strip()
        if new_pw:
            if len(new_pw) < 4:
                messages.error(request, "4 caractères minimum pour un mot de passe temporaire.")
                return redirect("accounts:team_edit", user_id=user_id)
            member.set_password(new_pw)
            member.profile.must_change_password = True
            member.profile.save()

        member.save()
        messages.success(request, f"'{member.username}' mis à jour.")
        return redirect("accounts:team")

    form = {
        "username":   member.username,
        "first_name": member.first_name,
        "last_name":  member.last_name,
        "email":      member.email,
        "role":       "admin" if member.is_staff else "vendeur",
        "is_active":  member.is_active,
    }
    return render(request, "accounts/team_form.html", {"mode": "edit", "form": form, "member": member})


# ── Supprimer utilisateur ───────────────────────────────────────────
@login_required
def team_delete(request, user_id):
    if not _admin_required(request):
        messages.error(request, "Accès réservé à l'administrateur.")
        return redirect("dashboard")

    member = get_object_or_404(User, pk=user_id)

    if member == request.user:
        messages.error(request, "Vous ne pouvez pas supprimer votre propre compte.")
        return redirect("accounts:team")

    if member.is_staff and not _has_other_active_admin(member):
        messages.error(request, "Impossible : il doit rester au moins un administrateur actif.")
        return redirect("accounts:team")

    if request.method == "POST":
        username = member.username
        member.delete()
        messages.success(request, f"'{username}' supprimé.")
        return redirect("accounts:team")

    return render(request, "accounts/team_confirm_delete.html", {"member": member})
