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
