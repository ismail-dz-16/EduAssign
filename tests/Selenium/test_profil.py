# ============================================================
#  Tests de la page profil (enseignant et étudiant)
# ============================================================

import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base_test import BaseTest
from config import COMPTE_ENSEIGNANT, COMPTE_ETUDIANT, TIMEOUT


class TestProfil(BaseTest):
    """
    Vérifie que la page profil s'affiche correctement,
    que les formulaires sont présents et que les validations fonctionnent.
    """

    @classmethod
    def setUpClass(cls):
        """Connexion en tant qu'enseignant pour l'ensemble des tests profil."""
        super().setUpClass()
        cls.driver.get(f"{cls.base_url}/login")
        WebDriverWait(cls.driver, TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        cls.driver.find_element(By.ID, "email").send_keys(COMPTE_ENSEIGNANT["email"])
        cls.driver.find_element(By.ID, "password").send_keys(COMPTE_ENSEIGNANT["password"])
        cls.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        WebDriverWait(cls.driver, TIMEOUT).until(EC.url_contains("teacher"))

    # ----------------------------------------------------------
    #  Accès et affichage
    # ----------------------------------------------------------

    def test_01_page_profil_accessible(self):
        """La page profil doit être accessible via /profile."""
        self.aller_a("/profile")
        # Laravel redirige /profile vers teacher.profile ou student.profile
        WebDriverWait(self.driver, TIMEOUT).until(
            EC.url_contains("profile")
        )
        self.assertIn("profile", self.driver.current_url)

    def test_02_champs_info_pre_remplis(self):
        """Les champs nom et email doivent être pré-remplis avec les données de l'utilisateur."""
        self.aller_a("/profile")
        WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "name"))
        )
        valeur_nom   = self.driver.find_element(By.ID, "name").get_attribute("value")
        valeur_email = self.driver.find_element(By.ID, "email").get_attribute("value")

        # Les champs ne doivent pas être vides
        self.assertTrue(len(valeur_nom) > 0,   "Le champ nom est vide")
        self.assertTrue(len(valeur_email) > 0, "Le champ email est vide")

    def test_03_formulaire_info_present(self):
        """La section 'Profile Information' doit contenir les champs nom et email."""
        self.aller_a("/profile")
        WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "name"))
        )
        self.assertTrue(self.driver.find_element(By.ID, "name").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "email").is_displayed())

    def test_04_formulaire_mot_de_passe_present(self):
        """La section changement de mot de passe doit contenir les 3 champs requis."""
        self.aller_a("/profile")
        WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "current_password"))
        )
        champs = ["current_password", "password", "password_confirmation"]
        for champ in champs:
            element = self.driver.find_element(By.ID, champ)
            self.assertTrue(element.is_displayed(), msg=f"Champ '{champ}' non visible")

    def test_05_mise_a_jour_nom_invalide_bloquee(self):
        """Soumettre un nom vide doit bloquer la mise à jour du profil."""
        self.aller_a("/profile")
        WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "name"))
        )
        champ_nom = self.driver.find_element(By.ID, "name")
        # Effacer le nom et soumettre
        champ_nom.clear()
        # Trouver et cliquer sur le bouton 'Save Changes'
        bouton = self.driver.find_element(
            By.XPATH, "//button[contains(text(),'Save Changes')]"
        )
        self.driver.execute_script("arguments[0].click();", bouton)

        # Doit rester sur la page profil (validation HTML5 ou Laravel)
        self.assertIn("profile", self.driver.current_url)

    def test_06_changement_mdp_mauvais_ancien_bloque(self):
        """Un mauvais mot de passe actuel doit empêcher le changement de mot de passe."""
        self.aller_a("/profile")
        WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "current_password"))
        )
        self.driver.find_element(By.ID, "current_password").send_keys("mauvais_mdp_000")
        self.driver.find_element(By.ID, "password").send_keys("NouveauMdp123!")
        self.driver.find_element(By.ID, "password_confirmation").send_keys("NouveauMdp123!")

        bouton = self.driver.find_element(
            By.XPATH, "//button[contains(text(),'Update Password')]"
        )
        self.driver.execute_script("arguments[0].click();", bouton)

        # Doit rester sur la page profil avec une erreur
        WebDriverWait(self.driver, TIMEOUT).until(
            EC.url_contains("profile")
        )
        self.assertIn("profile", self.driver.current_url)

    # ----------------------------------------------------------
    #  Accès profil étudiant
    # ----------------------------------------------------------

    def test_07_profil_etudiant_accessible(self):
        """Le profil étudiant doit aussi être accessible après reconnexion."""
        # Déconnexion de l'enseignant
        self.se_deconnecter()

        # Connexion en tant qu'étudiant
        self.se_connecter(COMPTE_ETUDIANT["email"], COMPTE_ETUDIANT["password"])
        WebDriverWait(self.driver, TIMEOUT).until(EC.url_contains("student"))

        self.aller_a("/profile")
        WebDriverWait(self.driver, TIMEOUT).until(EC.url_contains("profile"))
        self.assertIn("profile", self.driver.current_url)

        # Remettre l'état initial (connecté en enseignant pour les autres tests)
        self.se_deconnecter()
        self.se_connecter(COMPTE_ENSEIGNANT["email"], COMPTE_ENSEIGNANT["password"])
        WebDriverWait(self.driver, TIMEOUT).until(EC.url_contains("teacher"))


if __name__ == "__main__":
    unittest.main(verbosity=2)