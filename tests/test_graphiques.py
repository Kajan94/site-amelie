import unittest
from unittest.mock import patch

import pandas as pd

from utils import graphiques


class GraphiquesTests(unittest.TestCase):
    def test_histogramme_vertical_conserve_les_montants(self):
        data = pd.DataFrame({
            "libelle_poste_prescription": ["médicaments", "biologie"],
            "montant_moyen": [120_000, 30_000],
            "Annee": [2023, 2023],
        })
        with patch.object(graphiques.db, "montant_moyen_prescriptions", return_value=data), \
             patch.object(graphiques, "image_png", side_effect=lambda figure: figure):
            figure = graphiques.graphique(2023)
        ax = figure.axes[0]
        self.assertEqual([bar.get_height() for bar in ax.patches], [120_000, 30_000])
        self.assertEqual(ax.yaxis.get_major_formatter()(120_000, 0), "120")

    def test_anneaux_conservent_ile_et_hauts_de_france_et_separent_la_reunion(self):
        data = pd.DataFrame({
            "region": ["Ile-de-France", "Hauts-de-France", "Normandie", "La Réunion", "Mayotte"],
            "prescriptions_totales": [40, 20, 10, 6, 2],
        })
        with patch.object(graphiques.db, "comparaison_prescriptions_par_region", return_value=data), \
             patch.object(graphiques, "image_png", side_effect=lambda figure: figure):
            figure = graphiques.graphique_camembert_prescriptions(2023)
        metropole, outre_mer = figure.axes
        self.assertEqual(len(metropole.patches), 3)
        self.assertEqual(len(outre_mer.patches), 2)
        self.assertIn("Île-de-France", [text.get_text() for text in metropole.texts])
        self.assertIn("Hauts-de-France", [text.get_text() for text in metropole.texts])
        self.assertIn("La Réunion", [text.get_text() for text in outre_mer.texts])
        self.assertNotIn("La Réunion", [text.get_text() for text in metropole.texts])

    def test_annee_absente_ne_genere_pas_de_graphique(self):
        for query, plot in [
            ("montant_moyen_prescriptions", graphiques.graphique),
            ("comparaison_prescriptions_par_region", graphiques.graphique_camembert_prescriptions),
        ]:
            with self.subTest(query=query), patch.object(graphiques.db, query, return_value=pd.DataFrame()):
                self.assertIsNone(plot(2099))


if __name__ == "__main__":
    unittest.main()
