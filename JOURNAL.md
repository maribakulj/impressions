# Journal

## 2026-10-05 — démarrage

Projet lancé à la demande de Marcel : les cadres emboîtés (poupées russes) et ce qu'ils font à
l'interprétation d'une machine. Plan dans `PLAN.md`. Corpus de départ : museums-v0.2 de caypollard
(10 168 peintures, 1 498 estampes, 801 photographies, 253 dessins, 230 sculptures, Iconclass).
Modèles en cache : CLIP ViT-B/32, SigLIP base, DINOv2 base. Boucle autonome lancée.

## 2026-10-05 — E0 et E1

**E0.** Environnement uv (`pyproject.toml`), versions alignées sur caypollard (torch 2.14,
transformers 5.17) pour réutiliser le cache. `src/impressions/encoders.py` : CLIP ViT-B/32, SigLIP
base, DINOv2 base (CLS + moyenne des patchs), tous hors ligne. Il manquait `spiece.model` de SigLIP
(téléchargé, 800 Ko). Test de fumée : 3 images encodées par les 3 modèles, textes encodés par CLIP
et SigLIP.

**E1.** [`data/works.jsonl`](data/works.jsonl) : 300 œuvres, 60 par type (peinture, estampe,
dessin, sculpture, photographie), une par groupe de quasi-doublons, tirage tournant sur les
divisions Iconclass, côté court ≥ 600 px (les images du pool font 960 px de large). Script
[`scripts/select_works.py`](scripts/select_works.py), planche [`figures/E1-works.jpg`](figures/E1-works.jpg).

**Vu sur la planche (important pour la suite).** Les « originaux » ne sont pas des objets nus :
ce sont déjà des photographies de musée, avec leurs propres couches. Un médaillon de marbre est
photographié *dans son cadre doré* (Q116373927) ; les photographies anciennes sont des tirages
collés sur carton, avec marges et inscriptions (Q96181612) ; les estampes et dessins gardent la
feuille, ses bords, ses taches (Q97853420, Q29384600) ; une « photographie » est la couverture
bleue d'un album fermé (Q96181868) ; un retable est montré volets ouverts (Q3999130) ; les
sculptures sont sur fond gris de studio. Conséquence : la couche 0 n'existe pas, il faut
**annoter les couches déjà présentes** dans chaque original (covariable), et mesurer les couches
ajoutées *par rapport à* l'image donnée. C'est aussi un résultat en soi pour l'article : le corpus
de musée est déjà une poupée russe.

Suite : E2, les fonctions de couches, + annotation des couches existantes des 300 œuvres.

## 2026-10-05 — E2, les couches

[`src/impressions/layers.py`](src/impressions/layers.py) : 9 couches composables et
déterministes (cadre doré, passe-partout, mur de musée avec cartel, page de livre, livre ouvert
photographié sur une table, page web de collection, écran photographié dans une pièce, impression
tramée CMJ, rephotographie au téléphone) + 2 contrôles (`shrink_neutral` : même réduction sur gris
sans cadre ; `jpeg_resample` : dégâts de pixels sans cadre). Les légendes ne nomment jamais le
sujet (« Fig. 40. — Reproduction autorisée. ») : sinon on testerait la lecture, pas le cadre.
4 tests verts ([`tests/test_layers.py`](tests/test_layers.py)).

**Regardé.** Planches : [cadres et contrôle](figures/E2-layers-gilt_frame-mat_border-museum_wall-shrink_neutral.jpg),
[livre et web](figures/E2-layers-book_page-book_photo-screenshot_ui.jpg),
[écran, trame, rephoto](figures/E2-layers-screen_photo-halftone_print-rephotograph-jpeg_resample.jpg),
[après correction](figures/E2-layers-gilt_frame-mat_border-book_photo-screen_photo.jpg).
Défaut trouvé à la première planche et corrigé : des taches « camouflage » sur le papier, la
dorure et le mur de la pièce (bruit flouté en 8 bits puis réamplifié → plateaux à bords nets) ;
flou refait en flottants. Restent visibles et assumés : la trame CMJ donne une dominante
violette/jaune (impression bon marché) ; une sculpture « au mur » est la *photo* de la sculpture
accrochée — on emboîte toujours la photo de musée, jamais l'objet, ce qui est la thèse même.

**Dépôt public** créé à la demande de Marcel : github.com/maribakulj/impressions. Les chemins
d'images de `data/works.jsonl` sont désormais relatifs au dépôt caypollard (plus de chemin
personnel).

Suite : E3, annoter les couches déjà présentes dans les originaux, puis pilote regardé sur 3 œuvres.

## 2026-10-05 — E8 fait en avance (pendant que l'encodage attend la file)

Revue vérifiée par un sous-agent : [`notes/litterature.md`](notes/litterature.md) (en français)
et [`references.bib`](references.bib), 85 références, chacune avec la page ouverte en `url`.
Corrections : l'essai d'Ortega paraît d'abord dans *El Sol* (5 avril 1921) ; « Digital Art History
as Critical AI » est d'Impett seul. Non confirmés et signalés : date/pages de Bateson (1955 ou
1956), pages de Marin 1988, pages de Latour et Lowe, numéro de *Der Tag* pour Simmel.

**Travaux les plus proches** (je les ai rouverts moi-même) :
- Ramos et al., [« What does CLIP know about your camera? »](https://arxiv.org/abs/2508.10637),
  ICCV 2025 : les encodeurs gardent la trace du JPEG, du redimensionnement, de l'appareil, et
  cela peut changer leur lecture sémantique. Mais ce sont des traces numériques quasi invisibles,
  pas des cadres physiques. → notre contrôle `jpeg_resample` est exactement leur terrain ; nos
  couches visibles sont l'autre moitié.
- Bartkowiak et al., [SynGallery](https://arxiv.org/abs/2607.18907), arXiv juillet 2026 : des
  peintures rendues avec cadres, reflets, vues obliques de salle — très proche de nos couches —
  mais pour apprendre au modèle à les **ignorer**. C'est la position que notre thèse renverse.
- Xiao et al., « Noise or Signal » (ICLR 2021) ; Goh et al. 2021 (attaques typographiques) ;
  bordures apprises (Bahng et al., Zolna et al.).

**Le creux** : à notre connaissance, personne ne fait passer une même œuvre dans une chaîne
contrôlée de supports emboîtés pour demander ce que l'image *est* (objet, œuvre ou support).

État des calculs : annotation des couches existantes en cours (≈ 240/300), encodage du pool CLIP
≈ 9 000/18 405 (lent : la file est partagée avec axel).
