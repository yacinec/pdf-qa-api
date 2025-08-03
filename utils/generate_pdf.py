import fitz

text = """
Rapport annuel de l’entreprise Acme Inc.

En 2023, le chiffre d'affaires s’élevait à 2 500 000 €.
En 2024, il a atteint un nouveau record de 3 800 000 €.
Les dépenses totales se sont stabilisées autour de 1 200 000 €.
La marge brute s'améliore d’année en année.

Merci à tous les collaborateurs.
"""

doc = fitz.open()
page = doc.new_page()
page.insert_text((72, 72), text, fontsize=12)
doc.save("tests/sample.pdf")
doc.close()
