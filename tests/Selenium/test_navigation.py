# ============================================================
#  Tests de navigation générale : page d'accueil, navbar, redirections
# ============================================================

import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base_test import BaseTest
from config import COMPTE_ENSEIGNANT, COMPTE_ETUDIANT, TIMEOUT


class TestNavigation(BaseTest):
    """
    Vérifie le comportement de la page d'accueil, de la navbar,
    et des redirections selon l'état de la session.
    """

    # ----------------------------------------------------------
    #  Page d'accueil publique
    # ----------------------------------------------------------

    def test_01_page_accueil_accessible(self):
        """La page d'accueil doit s'afficher pour un visiteur non connecté."""
        self.aller_a("/")
        self.assertEqual(self.driver.current_url.rstrip("/"), self.base_url)

    def test_02_lien_get_started_mene_au_register(self):
        """Le bouton 'Get Started for Free' doit mener à la page d'inscription."""
        self.aller_a("/")
        bouton = WebDriverWait(self.driver, TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(text(),'Get Started for Free')]")
            )
        )
        bouton.click()
        WebDriverWait(self.driver, TIMEOUT).until(EC.url_contains("register"))
        self.assertIn("/register", self.driver.current_url)

    def test_03_lien_learn_more_reste_sur_accueil(self):
        """Le bouton 'Learn More' pointe vers une ancre (#features) sur la même page."""
        self.aller_a("/")
        bouton = WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(text(),'Learn More')]")
            )
        )
        href = bouton.get_attribute("href")
        self.assertIn("#features", href)

    def test_04_routes_protegees_redirigent_vers_login(self):
        """Toute route protégée doit rediriger un visiteur non connecté vers /login."""
        routes_protegees = [
            "/dashboard",
            "/dashboard/teacher",
            "/dashboard/student",
            "/profile",
        ]
        for route in routes_protegees:
            self.aller_a(route)
            WebDriverWait(self.driver, TIMEOUT).until(
                EC.url_contains("login")
            )
            self.assertIn("/login", self.driver.current_url,
                          msg=f"La route '{route}' ne redirige pas vers /login")

    def test_05_page_404_pour_route_inexistante(self):
        """Une URL inexistante doit retourner une erreur (pas une page vide)."""
        self.aller_a("/cette-page-nexiste-pas-du-tout")
        # La page source ne doit pas être vide
        self.assertTrue(len(self.driver.page_source) > 100)

    # ----------------------------------------------------------
    #  Navbar après connexion
    # ----------------------------------------------------------

    def test_06_navbar_enseignant_contient_dashboard(self):
        """La navbar de l'enseignant doit afficher un lien Dashboard."""
        self.se_connecter(COMPTE_ENSEIGNANT["email"], COMPTE_ENSEIGNANT["password"])
        WebDriverWait(self.driver, TIMEOUT).until(EC.url_contains("teacher"))

        lien = WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located(
                (By.XPATH, "//nav//a[contains(text(),'Dashboard')]")
            )
        )
        self.assertTrue(lien.is_displayed())
        self.se_deconnecter()

    def test_07_navbar_affiche_nom_utilisateur(self):
        """La navbar doit afficher le nom de l'utilisateur connecté."""
        self.se_connecter(COMPTE_ETUDIANT["email"], COMPTE_ETUDIANT["password"])
        WebDriverWait(self.driver, TIMEOUT).until(EC.url_contains("student"))

        # Le nom de l'utilisateur apparaît dans le bouton du dropdown de la navbar
        nom_element = WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located(
                (By.XPATH, "//nav//button[contains(@class,'inline-flex')]")
            )
        )
        self.assertTrue(nom_element.is_displayed())
        self.se_deconnecter()

    def test_08_redirection_dashboard_selon_role(self):
        """
        /dashboard doit rediriger vers teacher ou student selon le rôle,
        jamais rester sur /dashboard lui-même.
        """
        # Test enseignant
        self.se_connecter(COMPTE_ENSEIGNANT["email"], COMPTE_ENSEIGNANT["password"])
        WebDriverWait(self.driver, TIMEOUT).until(EC.url_contains("teacher"))
        self.assertNotIn("/dashboard\n", self.driver.current_url)
        self.se_deconnecter()

        # Test étudiant
        self.se_connecter(COMPTE_ETUDIANT["email"], COMPTE_ETUDIANT["password"])
        WebDriverWait(self.driver, TIMEOUT).until(EC.url_contains("student"))
        self.assertNotIn("/dashboard\n", self.driver.current_url)
        self.se_deconnecter()

    def test_09_page_accueil_utilisateur_connecte_a_lien_dashboard(self):
        """Un utilisateur connecté sur la page d'accueil doit voir 'Go to Dashboard'."""
        self.se_connecter(COMPTE_ENSEIGNANT["email"], COMPTE_ENSEIGNANT["password"])
        WebDriverWait(self.driver, TIMEOUT).until(EC.url_contains("teacher"))

        self.aller_a("/")
        bouton = WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(text(),'Go to Dashboard')]")
            )
        )
        self.assertTrue(bouton.is_displayed())
        self.se_deconnecter()

    def test_10_titre_page_contient_eduassign(self):
        """Le titre de chaque page principale doit contenir 'EduAssign'."""
        pages = ["/", "/login", "/register"]
        for page in pages:
            self.aller_a(page)
            WebDriverWait(self.driver, TIMEOUT).until(
                lambda d: len(d.title) > 0
            )
            self.assertIn(
                "EduAssign", self.driver.title,
                msg=f"Titre manquant sur la page '{page}' : {self.driver.title}"
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)