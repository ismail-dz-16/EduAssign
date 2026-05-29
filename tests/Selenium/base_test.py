# ============================================================
#  Classe de base partagée par tous les tests Selenium
# ============================================================

import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config import BASE_URL, TIMEOUT


class BaseTest(unittest.TestCase):
    """
    Classe mère dont héritent tous les tests.
    Gère l'initialisation et la fermeture du navigateur.
    """

    @classmethod
    def setUpClass(cls):
        """Lance le navigateur Chrome avant chaque classe de test."""
        options = Options()
        # options.add_argument("--headless")   # Décommenter pour mode sans interface
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1280,800")

        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(TIMEOUT)
        cls.base_url = BASE_URL

    @classmethod
    def tearDownClass(cls):
        """Ferme le navigateur après chaque classe de test."""
        cls.driver.quit()

    def aller_a(self, chemin="/"):
        """Navigue vers un chemin relatif de l'application."""
        self.driver.get(f"{self.base_url}{chemin}")

    def attendre_url(self, fragment, timeout=None):
        """Attend que l'URL contienne un fragment donné."""
        WebDriverWait(self.driver, timeout or TIMEOUT).until(
            EC.url_contains(fragment)
        )

    def attendre_element(self, by, valeur):
        """Attend qu'un élément soit visible et le retourne."""
        return WebDriverWait(self.driver, TIMEOUT).until(
            EC.visibility_of_element_located((by, valeur))
        )

    def remplir_champ(self, id_champ, texte):
        """Efface un champ et y saisit du texte."""
        champ = self.driver.find_element(By.ID, id_champ)
        champ.clear()
        champ.send_keys(texte)

    def se_connecter(self, email, mot_de_passe):
        """Effectue la connexion via le formulaire de login."""
        self.aller_a("/login")

        # Attendre que le formulaire soit chargé
        WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        self.remplir_champ("email", email)
        self.remplir_champ("password", mot_de_passe)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    def se_deconnecter(self):
        """
        Déconnecte l'utilisateur en soumettant le formulaire logout via JavaScript.
        Le logout est une route POST protégée par CSRF — un simple GET ne suffit pas.
        """
        self.driver.execute_script("""
            // Récupérer le token CSRF depuis la balise meta
            const token = document.querySelector('meta[name="csrf-token"]')?.content
                        || document.querySelector('input[name="_token"]')?.value
                        || '';

            // Créer et soumettre un formulaire POST dynamiquement
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = '/logout';

            const csrfInput = document.createElement('input');
            csrfInput.type  = 'hidden';
            csrfInput.name  = '_token';
            csrfInput.value = token;

            form.appendChild(csrfInput);
            document.body.appendChild(form);
            form.submit();
        """)

        # Attendre la redirection vers la page d'accueil après déconnexion
        WebDriverWait(self.driver, TIMEOUT).until(
            EC.url_to_be(f"{self.base_url}/")
        )