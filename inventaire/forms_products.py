from django import forms
from .models import Produit, Categorie

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = [
            "nom", "categorie", "prix_achat", "prix_vente",
            "quantite", "barcode", "image_url", "image_file"
        ]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control"}),
            "categorie": forms.Select(attrs={"class": "form-select"}),
            "prix_achat": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "prix_vente": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "quantite": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
            "barcode": forms.TextInput(attrs={"class": "form-control"}),
            "image_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "URL Cloudinary (facultatif)"}),
            "image_file": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

class ProduitFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        label="Recherche",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nom ou code-barres"})
    )
    categorie = forms.ModelChoiceField(
        required=False,
        queryset=Categorie.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"})
    )
    include_archived = forms.BooleanField(required=False, label="Inclure archivés")

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ["nom"]
        widgets = {"nom": forms.TextInput(attrs={"class": "form-control"})}
