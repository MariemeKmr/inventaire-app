from django import forms

class ReplenishForm(forms.Form):
    # En prod : product = ModelChoiceField(queryset=Product.objects.all())
    product = forms.ChoiceField(label="Produit", choices=(), required=True)
    quantity = forms.IntegerField(label="Quantité", min_value=1, initial=1)
    unit_cost = forms.DecimalField(label="Coût unitaire (CFA)", min_value=0, decimal_places=2, max_digits=12)
    supplier = forms.CharField(label="Fournisseur", max_length=120, required=False)
    reference = forms.CharField(label="Référence (facture/bon)", max_length=120, required=False)
    date = forms.DateField(label="Date", widget=forms.DateInput(attrs={"type": "date"}))
    note = forms.CharField(label="Remarque", widget=forms.Textarea(attrs={"rows":3}), required=False)

    def set_product_choices(self, products):
        """
        products: liste de dicts {"id":.., "nom":..} (stub) OU queryset en prod.
        """
        self.fields["product"].choices = [(str(p["id"]), p["nom"]) for p in products]
