# Enquête humaine (H5) — préparée, non menée

**But.** Comparer ce que des personnes et Claude disent des *mêmes* images à travers les couches :
le sujet survit-il ? le support prend-il sa place ? combien de couches voit-on ? quel médium ?

**Matériel.** 40 images = 8 œuvres (2 peintures, 2 estampes, 1 dessin, 2 sculptures,
1 photographie) tirées du sous-échantillon d'E5 × 5 étapes (original, cadre doré, livre
photographié, profondeur 4, profondeur 6). `items.csv` dit quelle image est quoi. Claude a déjà
répondu aux mêmes questions sur ces images (`data/annotations/e5_readings.jsonl`).

**Plan.** 5 listes en carré latin (`lists.json`) : chaque participant voit chaque œuvre une
seule fois (sinon il reconnaîtrait l'original sous les couches) et 8 images en tout. Viser
au moins 8 personnes par liste, soit 40 participants, non spécialistes et spécialistes séparés si
possible.

**Passation.** Ouvrir `form.html` dans un navigateur (fichier local, aucun serveur, aucune donnée
envoyée) ; choisir la liste ; à la fin un CSV se télécharge.

**Questions** (les mêmes que pour Claude, en mots simples) : 1) que représente l'image ;
2) qu'est-ce qu'on regarde physiquement ; 3) combien de couches ; 4) type de l'œuvre.

**Analyse prévue** (fixée avant toute donnée) :
- Q1 : le même juge que pour Claude (même consigne, `scripts/e5_readings.py`, JUDGE) classe chaque
  réponse en same / partial / support / other par rapport à la description de l'original
  *donnée par Claude* (référence commune) ; on compare la part de « support » à profondeur 6
  chez les humains et chez Claude.
- Q3 : erreur absolue moyenne par rapport aux couches vraies (couches présentes + ajoutées).
- Q4 : part du type juste par étape (la peinture devient-elle « estampe » dans le livre pour
  les humains aussi ?).
- Intervalles de confiance par bootstrap sur les participants ; effet de l'étape par modèle
  mixte (participant et œuvre en effets aléatoires) si l'effectif le permet.

**Ce qui réfuterait l'asymétrie humain / machine** : des humains qui, à profondeur 6, décrivent
le support aussi souvent que Claude (≥ 27/30 en proportion), ou qui lisent l'œuvre comme
« estampe » dans le livre aussi souvent que CLIP.
