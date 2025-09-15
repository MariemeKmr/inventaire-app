# 📦 Inventaire App

Application web d’inventaire pour gérer un magasin (produits, ventes, dettes, statistiques).  
Développée avec **Django**, **MariaDB/MySQL**, et intégration Cloudinary + Remove.bg pour les images.  

👥 Projet développé par **Marieme KAMARA** et **Idrissa MASSALY**.

---

## 🚀 Fonctionnalités

- **Gestion Produits** : ajout, modification, suppression, photos (fond supprimé via API Remove.bg).  
- **Ventes** : enregistrement rapide, décrémentation automatique du stock.  
- **Dettes** : suivi des dettes clients, remboursement total ou partiel.  
- **Statistiques** : chiffre d’affaires, top ventes, comparatifs achats/ventes.  
- **Historique** : traçabilité des actions (qui a fait quoi, quand).  
- **Alertes** : stock faible, messages d’information.  

---

## 👥 Profils utilisateurs

- **Admin (propriétaire du magasin)** : accès complet (produits, ventes, dettes, statistiques, historique).  
- **Vendeur (personne de confiance)** : enregistrement ventes et dettes, consultation des produits.  

---

## 🛠️ Technologies

- **Backend** : Django (Python)  
- **Frontend** : Django Templates (HTML/CSS/JS, Bootstrap)  
- **Base de données** : MariaDB / MySQL  
- **Stockage images** : Cloudinary  
- **API** : Remove.bg (suppression de fond)  
- **Déploiement** : VPS, PythonAnywhere ou Heroku  

---

## 📂 Structure du projet

```bash
inventaire-app/
│── sql/                  # Script SQL de création de la base
│── app/                  # Code Django
│── static/               # Fichiers CSS/JS
│── templates/            # Vues HTML
│── .gitignore
│── README.md
│── requirements.txt
```

## ⚙️ Installation (local)

### 1. Cloner le projet
```bash
git clone https://github.com/MariemeKmr/inventaire-app.git
cd inventaire-app
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer la base de données
Importer le script SQL sql/inventaire.sql dans MariaDB/MySQL.
Adapter les informations de connexion dans settings.py (DATABASES).

### 5. Lancer le serveur
```bash
python manage.py runserver
```

## 📜 Licence
Projet privé – réservé à un usage interne.
Développé par Marieme KAMARA et Idrissa MASSALY.
