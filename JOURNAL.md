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

## 2026-10-05 — E3 (1/2) : les couches déjà présentes dans les « originaux »

Claude (Sonnet, lecture d'image) a annoté les 300 œuvres :
[`data/annotations/existing_layers.jsonl`](data/annotations/existing_layers.jsonl), script
[`scripts/annotate_existing_layers.py`](scripts/annotate_existing_layers.py), 0 erreur.
Contrôle à l'œil sur 15 tirées au hasard ([planche](figures/E3-existing-layers-check.jpg)) :
juste partout (miniature Q19913961 dans un cadre doré sur coussin rose → 4 couches ;
stéréo-daguerréotype Q97013011 dans son étui ; cyanotype Q96181857 vu dans l'album ouvert) ;
léger excès sur « fond de studio » attribué à un simple fond clair.

**Résultat** (part des œuvres, par type) :

| couche présente | peinture | estampe | dessin | sculpture | photographie |
| --- | --- | --- | --- | --- | --- |
| cadre | 12 % | 0 % | 2 % | 3 % | 7 % |
| montage / carton | 8 % | 15 % | 20 % | 2 % | 60 % |
| bords de la feuille | 2 % | 98 % | 73 % | 0 % | 80 % |
| inscriptions hors image | 5 % | 67 % | 27 % | 2 % | 33 % |
| fond de studio | 32 % | 68 % | 45 % | 93 % | 43 % |
| socle / support | 5 % | 0 % | 2 % | 40 % | 3 % |
| reliure / album | 0 % | 0 % | 2 % | 0 % | 20 % |
| **nombre moyen de couches** | **0,72** | **2,25** | **1,47** | **1,50** | **2,18** |

Seules 48 images sur 300 n'ont aucune couche. **Les musées traitent les types différemment** :
la peinture est rognée au bord de la toile (le cadre est retiré de l'image), l'estampe et la
photographie sont montrées *avec* leur feuille, leur carton, leurs inscriptions. Ce n'est pas
neutre pour la machine : le type d'objet est lisible dans les couches mêmes, avant tout sujet.
À tester en E4 : une partie de ce que les modèles appellent « estampe » ou « photographie »
est-elle la marge ?

## 2026-10-05 — E3 (2/2) : le pilote regardé

Pool encodé par les trois modèles (`data/cache/pool-*.npz`, 18 405 images, ~50 min chacun dans
la file partagée). Pilote [`scripts/pilot.py`](scripts/pilot.py) : 3 œuvres (une peinture de
Boucher ovale Q19912481, un bronze Q139858606, une gravure de Dürer Q18338511) × 9 chaînes, rang
de l'œuvre elle-même parmi les 18 405 images, 3 voisins, lecture de Claude. Planches :
[peinture](figures/E3-pilot-Q19912481.jpg), [bronze](figures/E3-pilot-Q139858606.jpg),
[gravure](figures/E3-pilot-Q18338511.jpg) ; données [`results/E3/pilot.jsonl`](results/E3/pilot.jsonl).

**Ce qu'on voit** (rang de l'œuvre retrouvée, CLIP / SigLIP / DINOv2) :

1. **Le cadre seul ne change rien.** Cadre doré, passe-partout, réduction, JPEG : rang 1-2 pour
   les 3 œuvres et les 3 modèles. La trame d'impression non plus (1-21). Si cela tient sur 300
   œuvres, H1 est réfutée dans sa forme « recherche d'images ».
2. **La bascule vient quand l'œuvre devient un objet dans une scène** : accrochée au mur (k=2 :
   Boucher 249/296/31, Dürer 5335/1768/859), dans un livre photographié (k=2 : 240/72/93,
   2833/308/383), dans une page web pour CLIP seulement (k=1 : 53, 5, 347 ; SigLIP reste à 1).
   Chaîne profonde k=4-6 : rangs 1 800 à 17 600 sur 18 405, c'est-à-dire perdue.
3. **Les voisins après la bascule sont des objets qui sont eux-mêmes des supports.** Le tableau au
   mur rouge a pour voisins des daguerréotypes dans leur étui, des miniatures encadrées, un
   retable ; le livre photographié a pour voisins des albums de cyanotypes, des manuscrits
   enluminés, une photographie d'étagères de livres ; la page web, avec sa rangée de vignettes,
   a pour voisins des lots de petits objets photographiés en grille (monnaies, fragments). La
   machine ne voit plus l'œuvre : elle range l'image avec les objets de musée dont la forme est
   celle du support.
4. **Le bronze résiste plus longtemps** (rang 1 même au mur), peut-être parce que sa silhouette sur
   fond gris est déjà « un objet posé quelque part ». À vérifier par type sur 300.
5. **Claude ne perd pas le sujet jusqu'à k=5 et décrit toute la chaîne** (« un écran affichant
   une page de collection en ligne montrant un livre ouvert dont la page de droite reproduit une
   gravure encadrée accrochée sur un mur bleu »). À k=6, sa réponse à « que représente cette
   image ? » **devient le support** : « Une photo de livre ouvert montrant une reproduction d'un
   tableau encadré (portrait ou scène sombre) ». Le sujet a glissé d'un cran.
6. **Biais à corriger avant de mesurer :** à k=2 l'œuvre ne couvre plus que ~13 % de l'image, à
   k=6 0,3 %. La bascule peut être un effet de taille, pas de cadre. Ajouté :
   `content_mask` (où sont les pixels de l'œuvre à chaque étape : la chaîne rejouée sur une image
   blanche puis noire avec la même graine) et `area_matched` (l'œuvre seule sur gris, même
   surface, même toile) ; E4 compare chaque étape à son témoin. Constat au passage : l'ancien
   contrôle `shrink_neutral` (38 % de surface) réduisait *plus* que le cadre doré (66-71 %).
7. **Claude repère la fabrication** : « le cadre semble ajouté numériquement ». Nos couches
   synthétiques sont reconnaissables comme telles par un modèle vision-langage → H3/H4 doivent
   être confirmées sur le réel (E6).

Lancé : [`scripts/e4_embed_stages.py`](scripts/e4_embed_stages.py) (300 œuvres × 37 images =
11 100 images × 3 modèles, reprenable œuvre par œuvre) dans la file des calculs lourds.

## 2026-10-05 — E5 (1/2) : ce que Claude dit que l'image *est*

30 œuvres (6 par type) × 9 étapes = 270 lectures, 0 erreur, puis un jugement par œuvre (le
sujet nommé à chaque étape est-il celui de l'original ?). Script
[`scripts/e5_readings.py`](scripts/e5_readings.py), analyse
[`scripts/e5_analyse.py`](scripts/e5_analyse.py) → [`results/E5/claude.json`](results/E5/claude.json).
Étapes regardées avant de compter : [planche](figures/E5-stages-check.jpg) ; le témoin
`match|deep 6` est bien l'œuvre seule, minuscule, au centre d'un fond gris.

| étape | couches vraies* | couches dites | sujet : même / partiel / **support** / autre | type d'œuvre juste |
| --- | --- | --- | --- | --- |
| original | 1,6 | 1,0 | — | 93 % |
| cadre doré (k=1) | 2,6 | 2,0 | 30 / 0 / 0 / 0 | 93 % |
| mur (k=2) | 3,6 | 2,8 | 23 / 6 / 1 / 0 | 93 % |
| livre photographié (k=2) | 3,6 | 3,9 | 16 / 9 / 5 / 0 | 93 % |
| écran (k=2) | 3,6 | 4,0 | 17 / 12 / 1 / 0 | 87 % |
| trame + rephoto (k=2) | 3,6 | 2,2 | 10 / 17 / 0 / 3 | 73 % |
| chaîne profonde k=4 | 5,6 | 5,0 | 1 / 12 / **14** / 3 | 73 % |
| chaîne profonde k=6 | 7,6 | 6,4 | 0 / 0 / **27** / 3 | 47 % |
| **témoin même surface que k=6** | 2,6 | 1,7 | 0 / 9 / **0** / 21 | 63 % |

*couches vraies = couches déjà présentes dans l'image de musée (annotation E3, elle aussi faite
par Claude : la mesure n'est pas indépendante) + couches ajoutées.

**H3 (compter les couches) : soutenue pour Claude.** Rang de Spearman 0,75 entre couches dites et
vraies ; erreur moyenne 0,95 couche contre 1,44 pour la règle triviale (toujours la moyenne) ;
76 % à une couche près. Il sous-compte les couches déjà présentes (1,0 dit contre 1,6).
Limite : il déclare **toutes** les images transformées « montées numériquement » (100 %) et
aucun original (0 %) — il reconnaît notre fabrication ; le réel (E6) est indispensable.

**H4 (le sens change, pas seulement le style) : soutenue, et le témoin la rend nette.** À 6
couches, la réponse à « que représente l'image ? » parle du support dans 27 cas sur 30 (« un
écran d'ordinateur affiche une page web de collection en ligne montrant la photo d'un livre
ouvert… »). Dans le témoin, l'œuvre seule *aussi petite* (0,3 % de l'image) : 0 sur 30. Quand
l'œuvre devient illisible sans support, Claude décrit une vignette illisible (« une minuscule
peinture sombre au centre d'un grand fond gris ») ; quand elle devient illisible *dans* des
supports, **le support prend la place du sujet**. La perte du sujet est un effet de taille ; son
remplacement par le support est un effet des couches.

**Inattendu : la trame est la couche qui trompe le plus sur le médium.** Trame + rephotographie
fait tomber le type d'œuvre juste de 93 % à 73 % et donne 3 « autre sujet » : une Résurrection
peinte devient « un haut-relief gothique sculpté et doré » (Q116377829), une caricature devient
« deux hommes qui courent sous l'orage » (Q97733002). Le cadre doré, lui, ne trompe jamais.

Reste pour E5 : le même comptage par CLIP et SigLIP en zéro-coup (attend les encodages d'E4).

## 2026-10-05 — E5 (2/2, partiel) : CLIP et SigLIP en zéro-coup, 51 premières œuvres

[`scripts/e5_zeroshot.py`](scripts/e5_zeroshot.py), lisible sur le cache partiel d'E4 (les 51
premières œuvres sont toutes des **peintures** : le fichier est rangé par type ; résultats finaux
à refaire sur les 300).

- **Support extérieur reconnu** (précision équilibrée sur 10 classes, hasard 10 %) : SigLIP 49 %,
  CLIP 22 %. Bien reconnus : cadre doré (SigLIP 96 %), page web (95-98 %), écran photographié
  (SigLIP 89 %), page de livre (SigLIP 75 %). Mal reconnus : mur de musée, livre photographié,
  passe-partout, rephotographie. H3 en partie seulement pour les encodeurs.
- **Le support change le médium lu.** Type d'œuvre « peinture » lu juste à 86-88 % sur l'original ;
  **dans une page de livre, la peinture devient « une estampe »** (CLIP 45/51 au livre
  photographié, SigLIP 40/51 à la page seule) ; à 5-6 couches, 0 % de « peinture ». Ce n'est pas
  une erreur au sens strict : une reproduction imprimée *est* une estampe photomécanique — le
  modèle lit le médium de l'enveloppe extérieure, pas celui de l'œuvre. Au mur, au contraire,
  « peinture » monte à 98-100 %. À tester sur les 300 : **accrocher une estampe ou une photo au
  mur en fait-il « une peinture » ?** (le cadre comme fabrique du médium).

## 2026-10-05 — E7 : l'enquête humaine, prête mais non menée

[`human_study/`](human_study/) : 40 images (8 œuvres du sous-échantillon d'E5 × 5 étapes :
original, cadre doré, livre photographié, profondeur 4, profondeur 6), 5 listes en carré latin
(chaque personne voit chaque œuvre une seule fois, 8 images), un formulaire hors ligne
[`form.html`](human_study/form.html) (aucun serveur, les réponses se téléchargent en CSV), et
[`PROTOCOLE.md`](human_study/PROTOCOLE.md) avec l'analyse fixée d'avance et ce qui réfuterait
l'asymétrie humain / machine. Les questions sont exactement celles posées à Claude en E5 :
comparaison directe possible. Vérifié : le script du formulaire se charge, les 40 images sont
là. **H5 reste non testée** : il faut ~40 participants, ce que la boucle ne peut pas faire.

## 2026-10-06 — E5 terminé : zéro-coup sur les 300 œuvres

Encodages d'E4 et d'E4b finis dans la nuit (11 100 + 1 800 images × 3 modèles). Zéro-coup refait
sur les 300 œuvres ([`results/E5/zeroshot-clip.json`](results/E5/zeroshot-clip.json),
[`zeroshot-siglip.json`](results/E5/zeroshot-siglip.json)).

- **Support extérieur reconnu** (précision équilibrée, 10 classes, hasard 10 %) : SigLIP 53 %,
  CLIP 24 %. Les deux reconnaissent la page web (93-98 %) ; SigLIP aussi l'écran photographié
  (93 %) et la page de livre (74 %) ; aucun ne reconnaît le livre photographié (0-9 %) ni le
  passe-partout (3-14 %). **H3 pour les encodeurs : partielle**, et bien en dessous de Claude.
- **Le médium lu suit l'enveloppe — attendu, contrôlé, une phrase dans l'article.** Type lu sur
  300 œuvres :

| étape | CLIP « peinture » | CLIP « estampe » | SigLIP « peinture » | SigLIP « estampe » |
| --- | --- | --- | --- | --- |
| original | 69 | 91 | 65 | 80 |
| cadre doré seul | 81 | 89 | 84 | 85 |
| **au mur** (k=2) | **256** | 9 | **112** | 61 |
| témoin même surface | 90 | 98 | 69 | 96 |
| **livre photographié** (k=2) | 7 | **232** | 3 | **150** |
| témoin même surface | 88 | 103 | 67 | 103 |
| profondeur 6 | 18 | **212** | 0 | **240** |
| témoin même surface | 230 | 0 | 0 | 2 (297 « dessin ») |

  Le cadre doré seul déplace à peine ; le mur fait de presque tout « une peinture », le livre
  « une estampe ». Les témoins de même surface gardent la répartition de l'original : c'est le
  support, pas la taille. À profondeur 6, les deux échouent mais pas de la même façon : devant
  la vignette minuscule ils répondent par défaut (CLIP « peinture », SigLIP « dessin ») ; devant
  la chaîne réelle, « estampe ».

## 2026-10-06 — E4b : la trame, enveloppe ou imprégnation ? (fait)

Variantes de la couche « impression » sur les 300 œuvres (CLIP, SigLIP, DINOv2) et sur les 30
œuvres d'E5 (Claude, même consigne, même juge). Planche des variantes :
[`figures/E4b-screens-detail.jpg`](figures/E4b-screens-detail.jpg). Scripts
[`e4b_embed_screens.py`](scripts/e4b_embed_screens.py), [`e4b_analyse.py`](scripts/e4b_analyse.py),
[`e4b_claude.py`](scripts/e4b_claude.py) ; résultats [`results/E4b/screens.json`](results/E4b/screens.json),
lectures `data/annotations/e4b_readings.jsonl`.

**Retrouver l'œuvre** (part des 300 où l'image de musée est dans les 10 premiers voisins) :

| variante | CLIP | SigLIP | DINOv2 |
| --- | --- | --- | --- |
| ancienne trame CMJ (dominante violet/jaune) | 0,75 | 0,70 | 0,79 |
| sa couleur seule, sans points | 0,60 | 0,73 | **0,97** |
| CMJN fine (3 px) | 0,69 | 0,69 | 0,87 |
| CMJN moyenne (5 px) | 0,84 | 0,79 | **0,54** |
| CMJN grosse (8 px, journal) | 0,32 | **0,08** | **0,04** |
| rephotographie seule | 0,90 | 0,97 | 0,99 |

**Claude** (30 œuvres ; sujet même / partiel / support / autre ; type d'œuvre juste) :

| variante | sujet | type juste |
| --- | --- | --- |
| original | — | 28/30 |
| ancienne trame CMJ | 5 / 18 / 2 / 5 | 22/30 |
| couleur seule | **18 / 12 / 0 / 0** | 22/30 |
| CMJN moyenne | 1 / 15 / 4 / 10 | 19/30 |
| CMJN grosse | 0 / 10 / **10** / 10 | 14/30 |

**Ce que cela dit.**
- Le soupçon de Marcel était fondé : une partie du premier résultat venait de ma fausse couleur.
  La lecture « haut-relief doré » de la Résurrection (Q116377829) persiste avec la couleur seule :
  c'était la dominante jaune, pas la trame.
- Mais la trame agit bien, et **autrement que le cadre**. Les points (pas la couleur) font perdre
  le sujet à Claude ; à gros grain, **la trame devient le sujet** (« une image très tramée
  de… », 10/30) — l'équivalent, par imprégnation, du support qui remplace le sujet en profondeur.
- Chaque modèle est sensible à une composante différente : DINOv2 (images seules) aux points,
  comme le biais de texture de Geirhos et al. ; CLIP à la couleur ; tous à la taille du grain.
  La rephotographie seule ne fait presque rien.
- Le médium lu bouge modérément (vers « estampe », 91 → 116-127 pour CLIP) : la trame n'est pas
  un fabricant de médium aussi fort que le mur ou le livre.

## 2026-10-06 — E6 : le réel (fait)

Corpus [`data/real/manifest.jsonl`](data/real/manifest.jsonl) : **171 vraies reproductions de 22
œuvres** (10 peintures, 5 sculptures, 4 estampes, 1 dessin, 2 photographies ; 5 à 9 images par
œuvre, dont au moins une « propre »), prises sur Wikimedia Commons et annotées une à une
(support, chaîne de couches, part de l'image occupée par l'œuvre). Supports : en salle 47,
propre 40, livre 21, encadrée en gros plan 20, produit dérivé imprimé 20 (timbres, affiches,
panneaux), rephotographie 15, écran 4, autre 4. Contrôle à l'œil :
[planche](figures/E6-real-check.jpg), justes. Notes : [`notes/E6-corpus.md`](notes/E6-corpus.md).
Scripts [`e6_embed.py`](scripts/e6_embed.py), [`e6_analyse.py`](scripts/e6_analyse.py),
[`e6_readings.py`](scripts/e6_readings.py) ; résultats [`results/E6/real.json`](results/E6/real.json).

**Encodeurs** (l'image propre de l'œuvre est-elle parmi les 5 plus proches des 170 autres ?
hasard ≈ 4 %) : encadrée en gros plan 95-100 % (le cadre est inerte, comme en synthèse) ; **en
salle 30-40 %, et ses voisins sont les photos de salle d'autres œuvres (37-50 %)** ; livre
52-76 % ; dérivés imprimés 60-70 %. Par couches : 0-1 → 86 %, 4+ → 21-38 %, et « même support »
monte de 10-17 % à 39-51 %. **Mais la surface explique l'essentiel** : régression
log10(rang) ~ couches + log10(surface), bootstrap sur les œuvres : surface −0,56 à −0,69
(IC excluant 0 pour les trois) ; couches +0,10 à +0,17, IC excluant 0 pour SigLIP seulement.
Avec 22 œuvres et des couches corrélées à la petitesse, l'effet propre des couches pour les
encodeurs n'est **pas établi** sur le réel.

**Claude sur le réel.**
- **Il ne croit plus au montage** : « couches ajoutées numériquement » 0-10 % selon le support
  (contre 100 % sur nos images fabriquées). Il distingue le réel du synthétique ; la limite
  signalée en E5 est levée pour les conclusions qui tiennent ici.
- **Il compte toujours les couches** : Spearman 0,59, 80 % à une couche près, erreur 0,84 contre
  1,18 pour la règle triviale. H3 tient sur le réel.
- **Le support (ou la scène) prend la place du sujet avec les couches** : 0-1 couche 0/25 ;
  2 couches 1/44 ; 3 couches 12/46 ; 4+ couches 23/34. **À surface égale** : œuvre moyenne
  (15-50 % de l'image) 1/9 à ≤ 2 couches contre 11/30 à ≥ 3 ; grande œuvre 0/59 contre 2/14.
  Petits effectifs, mais même sens que le témoin synthétique d'E5. **H4 tient sur le réel.**
- **Nuance que le synthétique ne montrait pas** : sur les vraies photos, Claude *nomme*
  presque toujours l'œuvre, mais la rétrograde au rang de décor : « Des visiteurs se pressent
  dans une salle de musée devant La Nuit étoilée de Van Gogh » ; « Couverture du livre *A
  Mathematician's Lament*, qui reproduit la gravure Melencolia I » ; « Capture d'écran d'un
  écran de verrouillage d'iPhone » (la Grande Vague en fond d'écran). Ce n'est pas une perte :
  c'est **une inversion de hiérarchie** — l'œuvre passe de sujet à complément de lieu.

## 2026-10-06 — E4 : retrouver l'œuvre à travers les couches (fait)

La mesure attendait depuis des heures dans la file des calculs lourds, occupée par deux longs
calculs d'axel. Elle ne charge aucun modèle (produits de matrices par blocs, ~300 Mo) : je l'ai
sortie de la file et lancée en basse priorité (`taskpolicy -b`), comme l'analyse d'E4b ; 3 min
en tout. Résultats [`results/E4/`](results/E4/), figure
[`article/figures/fig-retrouver.png`](article/figures/fig-retrouver.png).

| étape | CLIP | SigLIP | DINOv2 | (témoin même surface) |
| --- | --- | --- | --- | --- |
| cadre doré | 1,00 | 1,00 | 1,00 | 1,00 / 1,00 / 1,00 |
| mur (k=2) | 0,12 | 0,38 | 0,52 | 0,30 / 0,65 / 0,80 |
| livre photographié (k=2) | 0,12 | 0,19 | 0,31 | 0,31 / 0,66 / 0,83 |
| page web → écran (k=2) | 0,12 | 0,33 | 0,70 | 0,39 / 0,79 / 0,87 |
| chaîne profonde k=6 | 0,00 | 0,00 | 0,00 | 0,00 / 0,00 / 0,00 |

(part des 300 œuvres retrouvées dans les 10 premiers sur 18 405)

- **H1 (le cadre est l'interrupteur) : réfutée**, comme prévu après la remarque de Marcel — le
  cadre intérieur ne change rien (Δ log10 rang +0,00 à +0,01).
- **À deux couches, les couches agissent au-delà de la taille** : Δ log10 rang étape − témoin
  au livre photographié +1,08 à +1,19 (IC 95 % > 0 ; pire pour 78-89 % des œuvres), au mur
  +0,53 à +0,77, à l'écran +0,41 à +1,16. Dès k=3 (surface ≤ 4 %), couches et témoins sont au
  plancher.
- **Mesure écartée** : « même support parmi les voisins » dans la galerie mêlée vaut 98-100 %
  pour les étapes *et* pour les témoins → nos couches se regroupent par gabarit (même table, même
  mur), pas par support. Biais de fabrication ; seul le réel (E6 : 37-50 %) fait foi.
- **Écart avec le réel à dire dans l'article** : sur la synthèse, l'effet des couches au-delà
  de la taille est net pour les trois encodeurs ; sur les 171 vraies images, il va dans le même
  sens mais n'est établi que pour SigLIP (22 œuvres).

Section 4.2 de l'article écrite ; limite « gabarits répétés » ajoutée.

## 2026-10-06 — E10 : la relecture adverse demande une révision majeure

[`notes/relecture.md`](notes/relecture.md) (sous-agent neuf, rôle de relecteur hostile mais
juste ; il a recalculé les chiffres depuis les fichiers bruts). Presque tous les nombres de
l'article se vérifient. Mais :
- **B1** les lectures de Claude n'étaient pas à l'aveugle : le nom du fichier donnait la
  condition (`…_deep_6.jpg`, `…_match-deep_6.jpg`, `mona-lisa-….jpg`), le juge voyait `deep:6` ;
- **B2** l'exemple de la consigne était la chaîne profonde elle-même ;
- **B3** « le support remplace le sujet » est vrai par construction contre un témoin sur gris
  qui ne contient aucun support ; à 6 couches 22/30 descriptions synthétiques nomment encore
  l'œuvre (la « nuance » n'est pas propre au réel) ; un verdict du juge est faux ;
- **B4** une phrase de la Discussion est fausse ;
- **I4** CLIP et DINOv2 recadrent au centre : ils ne voient pas le bord du fichier ;
- Spearman mal calculé (0,79 et 0,64), CLIP ne reconnaît pas l'écran, « CLIP réagit à la
  couleur » contredit (la « couleur seule » était aussi un flou), témoin non apparié en netteté,
  chiffres du réel sans script, pas d'intervalles, Wang et al. 2026 non cité.
Je l'accepte presque entièrement. Plan de révision : étape E10b de [`PLAN.md`](PLAN.md). Les
résultats de Claude écrits plus haut dans ce journal sont **suspendus** jusqu'aux relectures
à l'aveugle.

## 2026-10-06 — Pertinence de l'article (question de Marcel)

Marcel : « t'es sûr que l'article est pertinent là ? » Réponse honnête : **non, pas en l'état.**
Après la relecture, ce qui reste est surtout attendu (cadre intérieur inerte ; médium qui suit
l'enveloppe), déjà connu (DINOv2 sensible aux points = biais de texture, Geirhos 2019) ou
probablement trivial (« le support prend la place du sujet » : le témoin d'encombrement montre que
l'entourage, quel qu'il soit, prend la place de l'œuvre minuscule). Le cadre théorique habillait
des résultats qui n'en avaient pas besoin.
**Réorientation proposée, en attente de Marcel** : une thèse étroite, en partie négative pour
l'intuition de départ — *la machine n'a pas de parergon* : elle ne lit pas le cadre comme ce qui
isole et désigne, elle aplatit les supports emboîtés en une scène où compte ce qui occupe le plus
de place — si les témoins (même dégradation, encombrement) le confirment ; plus le protocole comme
contribution de méthode. Format court (communication en humanités numériques). Si rien de net ne
tient : un rapport honnête, pas un article.
