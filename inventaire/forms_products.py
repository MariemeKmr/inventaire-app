from django import forms
from .models import Produit, Categorie

class ProductForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = [
            "nom", "categorie", "prix_achat", "prix_vente", "quantite",
            "image_file", "image_url", "barcode"
        ]
        labels = {
            "nom": "Nom du produit",
            "categorie": "Catégorie",
            "prix_achat": "Prix d'achat (CFA)",
            "prix_vente": "Prix de vente (CFA)",
            "quantite": "Quantité",
            "image_file": "Photo (fichier)",
            "image_url": "URL image (Cloudinary)",
            "barcode": "Code-barres",
        }
        help_texts = {
            "categorie": "Ex: Parfums, Encens, Brumes…",
        }
