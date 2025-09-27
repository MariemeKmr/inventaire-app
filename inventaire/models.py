from django.db import models
from django.core.validators import MinValueValidator


# ---------- Categorie ----------
class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "categorie"

    def __str__(self):
        return self.nom


# ---------- Utilisateur (métier, différent du User Django d'auth) ----------
class Utilisateur(models.Model):
    nom = models.CharField(max_length=150)
    email = models.CharField(max_length=150, unique=True)
    mot_de_passe = models.CharField(max_length=128)
    is_admin = models.IntegerField()

    class Meta:
        db_table = "utilisateur"

    def __str__(self):
        return self.nom


# ---------- Produit ----------
class Produit(models.Model):
    nom = models.CharField(max_length=200)
    # FK sur l'ID ENTIER de Categorie (PAS sur le nom) -> pas de to_field !
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.PROTECT,
        related_name="produits",
        null=True, blank=True,          # rends-le obligatoire plus tard si tu veux
    )
    prix_achat = models.DecimalField(max_digits=12, decimal_places=2,
                                     validators=[MinValueValidator(0)])
    prix_vente = models.DecimalField(max_digits=12, decimal_places=2,
                                     validators=[MinValueValidator(0)])
    quantite = models.PositiveIntegerField(default=0)
    image_file = models.ImageField(upload_to="products/", blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    barcode = models.CharField(max_length=128, blank=True, null=True, unique=False)
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "produit"
        ordering = ["-date_ajout"]
        indexes = [
            models.Index(fields=["nom"], name="ix_produit_nom"),
            models.Index(fields=["categorie"], name="ix_produit_categorie"),
        ]
        # Pour forcer prix_vente > prix_achat côté DB (MySQL 8+/MariaDB 10.4+) :
        # constraints = [
        #     models.CheckConstraint(check=models.Q(prix_achat__gte=0), name="chk_prix_achat_ge_0"),
        #     models.CheckConstraint(check=models.Q(prix_vente__gt=models.F("prix_achat")), name="chk_prix_vente_gt_achat"),
        #     models.CheckConstraint(check=models.Q(quantite__gte=0), name="chk_quantite_ge_0"),
        # ]

    def __str__(self):
        return self.nom


# ---------- Dette ----------
class Dette(models.Model):
    nom_client = models.CharField(max_length=150)
    telephone = models.CharField(max_length=50, blank=True, null=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2,
                                  validators=[MinValueValidator(0.01)])
    date_dette = models.DateField()
    produits_txt = models.TextField(blank=True, null=True)
    remarques = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=8)  # "EN_COURS" / "PARTIEL" / "PAYEE"

    class Meta:
        db_table = "dette"
        indexes = [
            models.Index(fields=["statut", "date_dette"], name="ix_dette_statut_date"),
            models.Index(fields=["date_dette"], name="ix_dette_date"),
        ]

    def __str__(self):
        return f"{self.nom_client} - {self.montant}€"


# ---------- Paiement de dette ----------
class PaiementDette(models.Model):
    dette = models.ForeignKey(Dette, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2,
                                  validators=[MinValueValidator(0.01)])
    date_paiement = models.DateTimeField()

    class Meta:
        db_table = "paiement_dette"
        indexes = [
            models.Index(fields=["dette"], name="ix_pay_dette"),
        ]

    def __str__(self):
        return f"Paiement {self.montant}€ sur dette #{self.dette_id}"


# ---------- Vente ----------
class Vente(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    quantite = models.IntegerField(validators=[MinValueValidator(1)])
    total = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(0)])
    date_vente = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.PROTECT)
    user_name_snapshot = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        db_table = "vente"
        indexes = [
            models.Index(fields=["produit", "date_vente"], name="ix_vente_prod_date"),
            models.Index(fields=["date_vente"], name="ix_vente_date"),
            models.Index(fields=["utilisateur", "date_vente"], name="ix_vente_user_date"),
        ]

    def __str__(self):
        return f"Vente #{self.id} - {self.quantite} x {self.produit}"


# ---------- Historique ----------
class Historique(models.Model):
    type_action = models.CharField(max_length=50)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL,
                                    blank=True, null=True)
    utilisateur_email = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_action = models.DateTimeField()

    class Meta:
        db_table = "historique"
        indexes = [
            models.Index(fields=["date_action"], name="ix_historique_date"),
        ]

    def __str__(self):
        return f"{self.type_action} - {self.date_action:%Y-%m-%d %H:%M}"


# ---------- Alerte ----------
class Alerte(models.Model):
    type = models.CharField(max_length=7)   # "REAPPRO" / "INFO"
    produit = models.ForeignKey(Produit, on_delete=models.SET_NULL,
                                blank=True, null=True)
    niveau = models.CharField(max_length=4)  # "INFO" / "WARN" / "CRIT"
    message = models.TextField()
    resolue = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = "alerte"
        indexes = [
            models.Index(fields=["produit", "created_at"], name="ix_alerte_prod_date"),
        ]

    def __str__(self):
        return f"[{self.niveau}] {self.type}"
