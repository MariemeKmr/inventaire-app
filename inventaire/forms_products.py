from django import forms

class ProductForm(forms.Form):
    nom = forms.CharField(label="Nom du produit", max_length=200)
    categorie = forms.CharField(label="Catégorie", max_length=100, required=False,
                                help_text="Ex: Parfums, Encens, Brumes…")
    prix_achat = forms.DecimalField(label="Prix d'achat (CFA)", min_value=0, decimal_places=2, max_digits=12)
    prix_vente = forms.DecimalField(label="Prix de vente (CFA)", min_value=0, decimal_places=2, max_digits=12)
    quantite = forms.IntegerField(label="Quantité", min_value=0, initial=0)
    # Deux options d'image : fichier local OU URL (Cloudinary) — laisse l'une des deux
    image_file = forms.ImageField(label="Photo (fichier)", required=False)
    image_url = forms.URLField(label="URL image (Cloudinary)", required=False,
                               help_text="Sera rempli après upload Cloudinary")
    barcode = forms.CharField(label="Code-barres", max_length=64, required=False)

    removebg_api_key = forms.CharField(label="Clé API Remove.bg", required=False,
                                       help_text="Laisse vide en local, à fournir côté serveur via .env")
    cloudinary_folder = forms.CharField(label="Dossier Cloudinary", required=False, initial="inventaire",
                                        help_text="Ex: inventaire/produits")

    def clean(self):
        cleaned = super().clean()
        pa = cleaned.get("prix_achat") or 0
        pv = cleaned.get("prix_vente") or 0
        if pv <= pa:
            self.add_error("prix_vente", "Le prix de vente doit être strictement supérieur au prix d'achat.")
        return cleaned
