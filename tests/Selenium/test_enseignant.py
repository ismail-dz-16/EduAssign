# ============================================================
#  Tests du tableau de bord enseignant
# ============================================================

import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from base_test import BaseTest
from config import COMPTE_ENSEIGNANT, TIMEOUT


class TestTableauBordEnseignant(BaseTest):
    """Vérifie les fonctionnalités principales de l'espace enseignant."""

    @classmethod
    def setUpClass(cls):
        """Connexion en tant qu'enseignant avant tous les tests de la classe."""
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
    #  Tableau de bord
    # ----------------------------------------------------------

    def test_01_dashboard_affiche_titre(self):
        """Le tableau de bord doit afficher le titre 'Teacher Dashboard'."""
        self.aller_a("/dashboard/teacher")
        titre = WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(),'Teacher Dashboard')]")
            )
        )
        self.assertTrue(titre.is_displayed())

    def test_02_bouton_creer_devoir_visible(self):
        """Le bouton 'Create Assignment' doit être visible sur le tableau de bord."""
        self.aller_a("/dashboard/teacher")
        bouton = WebDriverWait(self.driver, TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "a[href*='assignments/create']")
            )
        )
        self.assertTrue(bouton.is_displayed())

    def test_03_acces_page_creation_devoir(self):
        """Cliquer sur 'Create Assignment' doit mener au formulaire de création."""
        self.aller_a("/dashboard/teacher")
        bouton = WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a[href*='assignments/create']")
            )
        )
        # Scroll vers le bouton puis clic via JavaScript pour éviter
        # les problèmes de viewport sur certaines résolutions
        self.driver.execute_script("arguments[0].scrollIntoView(true);", bouton)
        self.driver.execute_script("arguments[0].click();", bouton)

        WebDriverWait(self.driver, TIMEOUT).until(EC.url_contains("assignments/create"))
        self.assertIn("assignments/create", self.driver.current_url)

    # ----------------------------------------------------------
    #  Formulaire de création d'un devoir
    # ----------------------------------------------------------

    def test_04_formulaire_creation_vide_bloque(self):
        """Soumettre le formulaire vide ne doit pas créer de devoir."""
        self.aller_a("/dashboard/teacher/assignments/create")
        WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))
        )
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        self.assertIn("create", self.driver.current_url)

    def test_05_champs_formulaire_presents(self):
        """Les champs essentiels du formulaire de création doivent exister dans le DOM."""
        self.aller_a("/dashboard/teacher/assignments/create")
        WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[name='title']"))
        )
        for champ in ["title", "description", "estimated_date"]:
            elements = self.driver.find_elements(By.CSS_SELECTOR, f"[name='{champ}']")
            self.assertTrue(len(elements) > 0, msg=f"Champ '{champ}' absent du DOM")

    # ----------------------------------------------------------
    #  Protection des routes
    # ----------------------------------------------------------

    def test_06_route_etudiante_interdite_pour_enseignant(self):
        """Un enseignant ne doit pas accéder au dashboard étudiant."""
        self.aller_a("/dashboard/student")
        WebDriverWait(self.driver, TIMEOUT).until(
            lambda d: "/dashboard/student" not in d.current_url
                      or "403" in d.page_source
        )
        self.assertNotIn("/dashboard/student", self.driver.current_url)


if __name__ == "__main__":
    unittest.main(verbosity=2)