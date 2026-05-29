#!/usr/bin/env python3
# ============================================================
#  Lanceur principal — exécute toutes les suites de tests
# ============================================================
#
#  Utilisation :
#    python run_tests.py
#
#  Prérequis :
#    pip install selenium
#    ChromeDriver installé et accessible dans le PATH
#    Application EduAssign lancée sur http://localhost
# ============================================================

import unittest
import sys

# Import de toutes les suites de tests
from test_authentification import TestAuthentification
from test_enseignant import TestTableauBordEnseignant
from test_etudiant import TestTableauBordEtudiant


def lancer_tests():
    """Regroupe toutes les suites et lance l'exécution complète."""

    suite_globale = unittest.TestSuite()

    # Ajout des suites dans l'ordre logique de test
    suites = [
        unittest.TestLoader().loadTestsFromTestCase(TestAuthentification),
        unittest.TestLoader().loadTestsFromTestCase(TestTableauBordEnseignant),
        unittest.TestLoader().loadTestsFromTestCase(TestTableauBordEtudiant),
    ]

    for suite in suites:
        suite_globale.addTests(suite)

    # Lancement avec un rapport détaillé
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    resultat = runner.run(suite_globale)

    # Code de sortie : 0 si tout passe, 1 sinon (utile pour CI/CD)
    sys.exit(0 if resultat.wasSuccessful() else 1)


if __name__ == "__main__":
    lancer_tests()
