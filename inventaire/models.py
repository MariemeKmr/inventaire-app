# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Alerte(models.Model):
    type = models.CharField(max_length=7)
    produit = models.ForeignKey('Produit', models.DO_NOTHING, blank=True, null=True)
    niveau = models.CharField(max_length=4)
    message = models.TextField()
    resolue = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'alerte'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Categorie(models.Model):
    nom = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'categorie'


class Dette(models.Model):
    nom_client = models.CharField(max_length=150)
    telephone = models.CharField(max_length=50, blank=True, null=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_dette = models.DateField()
    produits_txt = models.TextField(blank=True, null=True)
    remarques = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'dette'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Historique(models.Model):
    type_action = models.CharField(max_length=50)
    utilisateur = models.ForeignKey('Utilisateur', models.DO_NOTHING, blank=True, null=True)
    utilisateur_email = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_action = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'historique'


class PaiementDette(models.Model):
    dette = models.ForeignKey(Dette, models.DO_NOTHING)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'paiement_dette'


class Produit(models.Model):
    barcode = models.CharField(unique=True, max_length=100, blank=True, null=True)
    nom = models.CharField(max_length=200)
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.IntegerField()
    image_url = models.CharField(max_length=500, blank=True, null=True)
    date_ajout = models.DateTimeField()
    categorie = models.ForeignKey(Categorie, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'produit'


class Utilisateur(models.Model):
    nom_complet = models.CharField(max_length=150)
    email = models.CharField(unique=True, max_length=150)
    mot_de_passe = models.CharField(max_length=255)
    role = models.CharField(max_length=7)
    actif = models.IntegerField()
    date_creation = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'utilisateur'


class Vente(models.Model):
    produit = models.ForeignKey(Produit, models.DO_NOTHING)
    quantite = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date_vente = models.DateTimeField()
    utilisateur = models.ForeignKey(Utilisateur, models.DO_NOTHING)
    user_name_snapshot = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vente'
