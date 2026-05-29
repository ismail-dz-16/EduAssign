# ============================================================
#  Tests du tableau de bord étudiant
# ============================================================

import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base_test import BaseTest
from config import COMPTE_ETUDIANT, TIMEOUT


class TestTableauBordEtudiant(BaseTest):
    """Vérifie les fonctionnalités principales de l'espace étudiant."""

    @classmethod
    def setUpClass(cls):
        """Connexion en tant qu'étudiant avant tous les tests de la classe."""
        super().setUpClass()
        cls.driver.get(f"{cls.base_url}/login")
        WebDriverWait(cls.driver, TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        cls.driver.find_element(By.ID, "email").send_keys(COMPTE_ETUDIANT["email"])
        cls.driver.find_element(By.ID, "password").send_keys(COMPTE_ETUDIANT["password"])
        cls.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        WebDriverWait(cls.driver, TIMEOUT).until(EC.url_contains("student"))

    # ----------------------------------------------------------
    #  Tableau de bord
    # ----------------------------------------------------------

    def test_01_dashboard_affiche_titre(self):
        """Le tableau de bord doit afficher le titre 'Student Dashboard'."""
        self.aller_a("/dashboard/student")
        titre = WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(),'Student Dashboard')]")
            )
        )
        self.assertTrue(titre.is_displayed())

    def test_02_onglets_presents(self):
        """Les onglets 'Pending Tasks' et 'My Submissions' doivent être visibles."""
        self.aller_a("/dashboard/student")
        onglet_pending = WebDriverWait(self.driver, TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "button[onclick*=\"'pending'\"]")
            )
        )
        onglet_completed = self.driver.find_element(
            By.CSS_SELECTOR, "button[onclick*=\"'completed'\"]"
        )
        self.assertTrue(onglet_pending.is_displayed())
        self.assertTrue(onglet_completed.is_displayed())

    def test_03_onglet_soumissions_cliquable(self):
        """Cliquer sur l'onglet 'My Submissions' doit l'activer et afficher son contenu."""
        self.aller_a("/dashboard/student")

        # Attendre que les onglets soient présents
        onglet = WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "button[onclick*=\"'completed'\"]")
            )
        )

        # Appeler switchTab via JavaScript exactement comme le ferait le navigateur
        # (évite les problèmes liés à l'événement onclick de Selenium)
        self.driver.execute_script(
            "switchTab({currentTarget: arguments[0]}, 'completed');", onglet
        )

        # Vérifier que la classe 'active' a été appliquée sur le bouton
        WebDriverWait(self.driver, TIMEOUT).until(
            lambda d: "active" in d.find_element(
                By.CSS_SELECTOR, "button[onclick*=\"'completed'\"]"
            ).get_attribute("class")
        )
        classe = self.driver.find_element(
            By.CSS_SELECTOR, "button[onclick*=\"'completed'\"]"
        ).get_attribute("class")
        self.assertIn("active", classe)

        # Vérifier aussi que la section 'completed' est devenue active
        section_active = self.driver.find_element(By.ID, "completed")
        self.assertIn("active", section_active.get_attribute("class"))

    # ----------------------------------------------------------
    #  Protection des routes
    # ----------------------------------------------------------

    def test_04_route_enseignant_interdite_pour_etudiant(self):
        """Un étudiant ne doit pas accéder au dashboard enseignant."""
        self.aller_a("/dashboard/teacher")
        WebDriverWait(self.driver, TIMEOUT).until(
            lambda d: "/dashboard/teacher" not in d.current_url
                      or "403" in d.page_source
        )
        self.assertNotIn("/dashboard/teacher", self.driver.current_url)

    def test_05_creation_devoir_interdite_pour_etudiant(self):
        """Un étudiant ne doit pas pouvoir accéder à la création de devoirs."""
        self.aller_a("/dashboard/teacher/assignments/create")
        WebDriverWait(self.driver, TIMEOUT).until(
            lambda d: "assignments/create" not in d.current_url
                      or "403" in d.page_source
        )
        self.assertNotIn("assignments/create", self.driver.current_url)


if __name__ == "__main__":
    unittest.main(verbosity=2)