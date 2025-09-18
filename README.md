# 📦 Inventaire App

Application web d’inventaire pour gérer un magasin (produits, ventes, dettes, statistiques).  
Développée avec **Django**, **MariaDB/MySQL**, et intégration **Cloudinary + Remove.bg** pour les images.  

👥 Projet développé par **Marieme KAMARA** et **Idrissa MASSALY**.

---

## 🚀 Fonctionnalités

- **Produits** : ajout, modification, suppression, photos (fond supprimé via API Remove.bg).
- **Ventes** : enregistrement rapide, décrémentation automatique du stock.
- **Dettes** : suivi des dettes clients, remboursement total ou partiel.
- **Statistiques** : chiffre d'affaires, top ventes, comparatifs achats/ventes.
- **Historique** : traçabilité des actions (qui a fait quoi, quand).
- **Alertes** : stock faible, messages d'information.

---

## 👥 Profils utilisateurs

- **Admin (propriétaire)** : accès complet (produits, ventes, dettes, statistiques, historique).
- **Vendeur** : enregistrement ventes et dettes, consultation des produits.  

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
│── inventaire/ # App Django (produits, ventes, dettes…)
│── inventaire_app/ # Config principale Django
│── static/ # Fichiers CSS/JS
│── templates/ # Vues HTML
│── sql/ # Script SQL de création de la base
│── .gitignore
│── .gitattributes
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
python -m venv .venv
# Linux/Mac
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer la base de données
Importer le script SQL **sql/inventaire.sql** dans MariaDB/MySQL.
Mettre à jour **inventaire_app/settings.py** → section **DATABASES**.

### 5. Variables d’environnement
Créer un fichier .env (non versionné) avec :
```bash
DB_NAME=inventaire
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306

CLOUDINARY_URL=cloudinary://...
REMOVEBG_API_KEY=...
```

### 6. Migrations et superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 7. Lancer le serveur
```bash
python manage.py runserver
```

## 🌱 Workflow Git (collaboration)
- main → code stable
- dev → intégration en cours
- feature/… → une branche par tâche
  
```bash
git checkout -b feature/produits
# coder…
git add .
git commit -m "feat: page produits"
git push -u origin feature/produits
```
Puis ouvrir une Pull Request vers dev.

## 📜 Licence
Projet privé – réservé à un usage interne.
Développé par Marieme KAMARA et Idrissa MASSALY.
