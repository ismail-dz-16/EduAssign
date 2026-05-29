# ============================================================
#  Configuration générale des tests Selenium - EduAssign
# ============================================================

# URL de base de l'application
BASE_URL = "http://127.0.0.1:8000"

# Délai d'attente maximum (en secondes) pour les éléments
TIMEOUT = 10

# Comptes de test — à adapter selon la base de données locale
COMPTE_ENSEIGNANT = {
    "email": "teacher@test.com",
    "password": "password",
    "nom": "Prof Test",
}

COMPTE_ETUDIANT = {
    "email": "student@test.com",
    "password": "password",
    "nom": "Étudiant Test",
}

# Données utilisées lors des tests d'inscription
NOUVEAU_COMPTE = {
    "nom": "Selenium Utilisateur",
    "email": "selenium_user@test.com",
    "password": "Password123!",
}
