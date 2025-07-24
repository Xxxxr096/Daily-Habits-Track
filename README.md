# 📆 Daily Habits Tracker

Une application web simple pour suivre ses habitudes quotidiennes.  
Les utilisateurs peuvent :

- ✅ Créer un compte
- ✅ Se connecter
- ✅ Ajouter des habitudes à suivre
- ✅ Marquer une habitude comme faite pour aujourd’hui
- ✅ Supprimer une habitude

---

## 🚀 Fonctionnalités

- Authentification sécurisée avec Flask-Login
- Stockage des données avec SQLite + SQLAlchemy
- Hashing des mots de passe avec Flask-Bcrypt
- Interface moderne avec Tailwind CSS
- Suivi quotidien simple et visuel

---

## 🗂️ Structure du projet

```
/daily_habits_tracker/
│
├── app.py                 # Application principale Flask
├── app.db                 # Base de données SQLite
├── .env                   # Clé secrète et config
├── requirements.txt       # Liste des dépendances
│
├── /templates/            # Fichiers HTML (Jinja2)
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── main.html
```

---

## ⚙️ Installation

### 1. Cloner le projet

```bash
git clone https://github.com/ton-utilisateur/daily-habits-tracker.git
cd daily-habits-tracker
```

### 2. Créer un environnement virtuel (optionnel mais recommandé)

```bash
python -m venv venv
source venv/bin/activate      # Sous Windows : venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 🔐 Configuration

Créer un fichier `.env` à la racine avec :

```
SECRET_KEY=une_clé_ultra_secrète
```

---

## 💾 Initialiser la base de données

Lancer Python dans le terminal :

```bash
python
```

Puis dans l'interpréteur :

```python
from app import db
db.create_all()
exit()
```

---

## ▶️ Lancer l’application

```bash
python app.py
```

Accède ensuite à :  
👉 http://127.0.0.1:5000/

---

## 🔁 Routes principales

| Route                  | Description                   |
| ---------------------- | ----------------------------- |
| `/`                    | Page d’accueil                |
| `/register`            | Inscription utilisateur       |
| `/login`               | Connexion utilisateur         |
| `/main`                | Tableau de bord des habitudes |
| `/logout`              | Déconnexion                   |
| `/delete_habit/<id>`   | Supprimer une habitude        |
| `/complete_habit/<id>` | Marquer comme faite           |

---

## ✨ Améliorations possibles

- Modifier une habitude
- Ajouter une date de début/fin
- Statistiques hebdomadaires
- Notifications (email ou mobile)
- Mode sombre 🌙

---

## 📄 Licence

Projet open-source à but pédagogique.  
Utilisation libre pour projets personnels.

---
