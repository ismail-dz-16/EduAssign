# ============================================================
#  Tests d'authentification : connexion, déconnexion, inscription
# ============================================================

import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base_test import BaseTest
from config import COMPTE_ENSEIGNANT, COMPTE_ETUDIANT, NOUVEAU_COMPTE, TIMEOUT


class TestAuthentification(BaseTest):
    """Vérifie que les flux d'authentification fonctionnent correctement."""

    def setUp(self):
        """
        Assure une session vierge avant chaque test.
        On passe par /login car la page contient toujours un CSRF token,
        même sans utilisateur connecté.
        """
        self.aller_a("/login")
        # Si l'utilisateur est déjà connecté, Laravel redirige vers /dashboard
        # Dans ce cas on effectue un logout propre
        if "/login" not in self.driver.current_url:
            self.se_deconnecter()
            self.aller_a("/login")
        # Attendre que la page login soit chargée
        WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "email"))
        )

    # ----------------------------------------------------------
    #  Page de connexion
    # ----------------------------------------------------------

    def test_01_page_login_accessible(self):
        """La page de connexion doit s'afficher sans erreur."""
        self.assertIn("login", self.driver.current_url.lower())
        self.assertTrue(self.driver.find_element(By.ID, "email").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "password").is_displayed())

    def test_02_connexion_avec_mauvais_mot_de_passe(self):
        """Un mauvais mot de passe doit afficher un message d'erreur."""
        self.remplir_champ("email", COMPTE_ENSEIGNANT["email"])
        self.remplir_champ("password", "mauvais_mot_de_passe_123")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        self.assertIn("/login", self.driver.current_url)

    def test_03_connexion_enseignant_valide(self):
        """Un enseignant valide doit être redirigé vers son tableau de bord."""
        self.remplir_champ("email", COMPTE_ENSEIGNANT["email"])
        self.remplir_champ("password", COMPTE_ENSEIGNANT["password"])
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        self.attendre_url("teacher")
        self.assertIn("teacher", self.driver.current_url)
        self.se_deconnecter()

    def test_04_connexion_etudiant_valide(self):
        """Un étudiant valide doit être redirigé vers son tableau de bord."""
        self.remplir_champ("email", COMPTE_ETUDIANT["email"])
        self.remplir_champ("password", COMPTE_ETUDIANT["password"])
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        self.attendre_url("student")
        self.assertIn("student", self.driver.current_url)
        self.se_deconnecter()

    def test_05_deconnexion(self):
        """Après déconnexion, l'accès au dashboard doit être refusé."""
        self.remplir_champ("email", COMPTE_ENSEIGNANT["email"])
        self.remplir_champ("password", COMPTE_ENSEIGNANT["password"])
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        self.attendre_url("teacher")
        self.se_deconnecter()
        self.aller_a("/dashboard")
        self.assertIn("/login", self.driver.current_url)

    # ----------------------------------------------------------
    #  Page d'inscription
    # ----------------------------------------------------------

    def test_06_page_register_accessible(self):
        """La page d'inscription doit s'afficher correctement."""
        self.aller_a("/register")
        self.assertTrue(self.driver.find_element(By.ID, "name").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "email").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "password").is_displayed())

    def test_07_inscription_mots_de_passe_differents(self):
        """Des mots de passe non identiques doivent bloquer l'inscription."""
        self.aller_a("/register")
        self.remplir_champ("name", NOUVEAU_COMPTE["nom"])
        self.remplir_champ("email", NOUVEAU_COMPTE["email"])
        self.remplir_champ("password", "MotDePasse123!")
        self.remplir_champ("password_confirmation", "AutreMotDePasse456!")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        self.assertIn("/register", self.driver.current_url)

    def test_08_inscription_email_invalide(self):
        """Un format d'e-mail invalide doit empêcher la soumission du formulaire."""
        self.aller_a("/register")
        self.remplir_champ("name", NOUVEAU_COMPTE["nom"])
        self.remplir_champ("email", "email_invalide")
        self.remplir_champ("password", NOUVEAU_COMPTE["password"])
        self.remplir_champ("password_confirmation", NOUVEAU_COMPTE["password"])
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        self.assertIn("/register", self.driver.current_url)


if __name__ == "__main__":
    unittest.main(verbosity=2)