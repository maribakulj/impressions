# Relecture adverse (E10) — 6 octobre 2026

Relecteur : sous-agent neuf, en rôle de relecteur de revue hostile mais juste (histoire de l'art
numérique / vision par ordinateur). Matériel lu : `PLAN.md`, `JOURNAL.md`, `article/article.md`
(les sections 4.2 et Résumé n'étaient pas écrites et n'ont pas été relues), `src/impressions/`,
`scripts/`, `results/`, `data/annotations/`, `data/real/manifest.jsonl`, `notes/litterature.md`.
J'ai recalculé les chiffres à partir des fichiers bruts avec `.venv/bin/python` ; les scripts
de recalcul sont dans le dossier temporaire de la session et ne sont pas versionnés.

## Verdict

**Révision majeure.** Presque tous les chiffres de l'article se retrouvent dans les fichiers.
Les exceptions sont signalées plus bas : deux Spearman faux, un « 0,3 % » et une phrase sur
CLIP. Le problème est ailleurs. Le résultat présenté comme non prévisible, « le support prend la
place du sujet », repose sur des lectures de Claude qui ne sont pas aveugles. Le nom du fichier
donne la condition (`…_deep_6.jpg`, `…_match-deep_6.jpg`, `mona-lisa-….jpg`). L'exemple du
prompt recopie la chaîne profonde. Le juge voit les étiquettes de condition (`deep:6`). De plus,
le témoin ne peut pas produire de verdict « support », par construction. Une phrase centrale de
la Discussion est fausse quand on la recalcule. Le comptage des couches (H3) est surévalué. Dans
E4b, la conclusion « CLIP réagit à la couleur » est contredite par les données mêmes. Les
résultats sur les encodeurs dépendent aussi d'un recadrage central qui n'est pas signalé.
Certaines conclusions peuvent tenir. Sur le réel, un modèle logistique groupé par œuvre donne
un effet des couches à surface égale. Mais il faut refaire les lectures sans fuite avant de les
affirmer.

---

## Bloquant

### B1. La condition fuit dans le nom du fichier, chez le lecteur comme chez le juge

- **Où.** `src/impressions/claude_vision.py:16` met le chemin complet de l'image dans le prompt
  (« Lis l'image {image_path} »). Les noms de fichiers viennent de `scripts/e5_readings.py:60`
  (`{Qid}_{chaîne}_{k}.jpg`, par exemple `Q27982670_deep_6.jpg` ou
  `Q27982670_match-deep_6.jpg`) et de `scripts/e4b_claude.py:39` (`…_ht_cmyk_coarse.jpg`). Pour
  E6, les fichiers s'appellent `mona-lisa-2dbc12256e.jpg`, `night-watch-….jpg`, etc.
  (`scripts/e6_readings.py:27`). Le juge reçoit en plus les identifiants de version `deep:6`,
  `match|deep:6` et `ht_cmyk_coarse:1` (`e5_readings.py:110`, `e4b_claude.py:65`).
- **Ce qui ne va pas.** Le lecteur Claude connaît le nombre de couches ajoutées (« deep_6 ») et
  sait si l'image est un témoin (« match »). Sur le réel, il connaît le titre de l'œuvre. Le
  juge connaît la condition de chaque description. Ni H3 (comptage) ni H4 (sujet) ne sont donc
  mesurées à l'aveugle. La « nuance » de 4.5 (« Claude *nomme* presque toujours l'œuvre ») est
  en partie un effet du nom de fichier. Au moins 131 lectures réelles sur 171 contiennent un
  mot-clé du titre, et le compte réel est plus haut : ma liste de mots-clés ratait 4 œuvres.
- **Preuve.** Les clés de `data/annotations/e5_readings.jsonl` et `e6_readings.jsonl` sont
  exactement ces chemins. Je n'ai trouvé aucune réponse qui cite le nom de fichier. Mais on ne
  peut pas exclure qu'il ait été utilisé.
- **Correction.** Copier chaque image sous un nom opaque et aléatoire, par exemple
  `img_7f3a9c.jpg`, sans table de correspondance dans le dossier lu. Donner au juge des
  identifiants aléatoires, dans un ordre mélangé. Relancer E5, E4b et E6 (environ 270 + 120 +
  171 lectures et 82 jugements). Tant que ce n'est pas fait, ne rapporter aucun chiffre de
  Claude comme résultat.

### B2. L'exemple du prompt est la chaîne profonde elle-même

- **Où.** `scripts/e5_readings.py:32-34`. L'exemple de la clé `chain` est `["photo d'écran",
  "page web", "photo de livre", "page imprimée", "photo de musée", "cadre doré", "peinture"]`.
  C'est la chaîne `deep` couche pour couche, dans l'ordre (`chains.py:10`). Elle a 7 éléments,
  donc 6 couches.
- **Ce qui ne va pas.** À `deep|6`, Claude répond `n_layers = 6` dans 20 cas sur 30. Ses
  chaînes reprennent le vocabulaire de l'exemple (« photo d'un écran d'ordinateur », « page web
  de collection en ligne », « photo de livre ouvert », « page imprimée… », « cadre doré »). Le
  comptage, et le vocabulaire « support » qui se retrouve dans `subject`, sont amorcés par le
  prompt. Autre problème : `subject` et `chain` sont demandés dans le même appel. Le modèle,
  invité à énumérer les supports, en parle aussi quand on lui demande le sujet.
- **Correction.** Prendre un exemple neutre, qui ne ressemble à aucune condition. Mieux :
  aucun exemple, ou un exemple tiré au hasard parmi plusieurs. Poser la question du sujet dans
  un appel séparé, avant toute question sur les supports.

### B3. « Le support remplace le sujet » : la mesure ne sépare pas cette idée d'une description exacte de l'image

- **Où.** article.md, 4.3 (« Le témoin tranche… effet des couches ») ; 5, 2ᵉ paragraphe ;
  4.5 (« Le réel ajoute une nuance que la synthèse ne montrait pas »).
- **Ce qui ne va pas.**
  1. La consigne demande « ce que l'image représente ». À six couches, l'image *est* la photo
     d'un écran. La décrire comme telle est la bonne réponse, pas un remplacement. Le témoin
     (l'œuvre seule sur du gris) ne contient aucun support. Il ne peut donc pas produire de
     verdict « support ». Le contraste 27/30 contre 0/30 est vrai par construction. Ce n'est
     pas le résultat contre-intuitif que le Garde-fou demande.
  2. Dans la synthèse aussi, Claude rétrograde l'œuvre au lieu de la perdre. 22 descriptions
     `deep|6` sur 30 contiennent encore un terme de sujet (portrait, scène, personnages…).
     Exemple : « …la page de droite reproduit un tableau encadré… une scène de repas à
     plusieurs personnages, peut-être une Cène ». La phrase de 4.5 qui dit que la synthèse « ne
     montrait pas » cette nuance est donc fausse.
  3. Le juge se trompe sur des cas nets. `rijksmuseum:Q17334826`, `deep:6` : « Portrait peint
     d'une femme en buste, vêtue de sombre, dans un cadre doré accroché à un mur bleu… ».
     L'original dit : « Portrait en buste… d'une femme… robe noire ». Verdict : « support ». Le
     juge n'est pas aveugle (B1), il appartient à la même famille que le lecteur (Sonnet juge
     Sonnet), et aucune validation humaine n'est consignée. La phrase « relu à la main sur un
     échantillon, il est juste » (§6) n'a de trace ni dans `JOURNAL.md` ni dans `notes/`.
- **Correction.**
  - Remplacer le verdict « support » à 4 catégories par deux mesures séparées. (a) Le sujet de
    l'œuvre est-il encore nommé, n'importe où dans la description ? (b) Est-il nommé en
    proposition principale ou en complément ?
  - Ajouter une question dirigée vers l'œuvre : « quelle œuvre est reproduite, et que
    représente-t-elle ? ».
  - Ajouter un témoin d'encombrement : même surface, l'œuvre collée dans une scène qui n'est pas
    un support (rue, intérieur). Ou bien la même chaîne avec une autre œuvre, ou une œuvre
    blanche.
  - Faire coder par un humain un échantillon d'au moins 60 paires, à l'aveugle, et donner le
    kappa avec le juge. Prendre si possible un juge d'une autre famille de modèles.
  - Reformuler la thèse : *quand l'œuvre devient illisible, Claude décrit ce qui reste lisible,
    c'est-à-dire les supports, et y range l'œuvre en complément*. C'est intéressant, mais c'est
    attendu, et cela doit être présenté ainsi.

### B4. Une phrase de la Discussion est fausse quand on la recalcule

- **Où.** article.md §5 : « c'est précisément lorsqu'il en compte trois ou plus que la
  hiérarchie s'inverse ».
- **Preuve.** Le tableau croisé de 4.5 est classé selon les couches *annotées*
  (`manifest.jsonl`), pas selon celles que Claude compte. Classé selon le compte de Claude
  (`e6_readings.jsonl`, `n_layers`), le verdict « support » donne : 0-1 → 5/40 ; 2 → 14/51 ;
  3 → 11/41 ; 4+ → 6/17. Cela fait 21 % quand Claude compte ≤ 2 et 29 % quand il compte ≥ 3.
  Il n'y a pas d'inversion.
- **Correction.** Supprimer la phrase, ou écrire « lorsque l'image *a* trois couches ou plus
  (selon notre annotation) ».

---

## Important

### I1. Comptage des couches (H3) : Spearman mal calculé, règle de base trop faible, effet surtout entre conditions

- **Où.** `scripts/e5_analyse.py:51`. Le rang vient de `argsort(argsort(·))`, qui départage
  les ex æquo arbitrairement. Avec des entiers de 0 à 10, les ex æquo sont la règle. Le calcul
  de E6, qui n'est dans aucun script, a manifestement le même défaut.
- **Valeurs justes** (`scipy.stats.spearmanr`, rangs moyens) :
  - E5 : **0,79** au lieu de 0,75 (article §4.3).
  - E6 : **0,64** au lieu de 0,59 (article §4.5). La version argsort redonne bien 0,594.
  - Le reste se vérifie : E5 à une couche près 75,9 % ; MAE 0,948 contre 1,443. E6 à une couche
    près 80,1 % ; MAE 0,842 contre 1,176.
- **Ce qui ne va pas sur le fond.**
  - La règle triviale (« toujours la moyenne ») est faible. Une règle qui connaît la condition
    (couches ajoutées + moyenne des couches déjà présentes) a une erreur moyenne de **0,73**.
    Elle bat Claude (0,95). Et la condition est justement écrite dans le nom du fichier (B1).
  - Dans chaque condition, Claude suit les couches déjà présentes à k ≤ 2 (rho de 0,55 à 0,66).
    Mais rho vaut −0,003 à `deep|4`, −0,06 à `deep|6` et −0,20 à `web|2`. Le Spearman global
    mesure surtout l'écart entre conditions.
  - Les « couches vraies » à `deep|6` comptent les couches déjà présentes dans l'image de musée,
    alors que l'œuvre couvre 0,24 % de l'image et que ces couches sont invisibles. La vérité
    terrain est mal définie.
  - Pour le témoin, on compte « +1 » couche (le gris), ce qui se discute.
- **Correction.**
  - Utiliser `spearmanr`, avec un intervalle de confiance par bootstrap sur les œuvres.
  - Ajouter la règle informée et la règle « toujours 1 » de PLAN H3 (erreur 2,89).
  - Rapporter le rho à l'intérieur de chaque condition.
  - Écrire : « Claude compte les couches visibles à peu près juste. Il ne fait pas mieux qu'une
    règle qui connaîtrait la longueur de la chaîne. »

### I2. Zéro-coup : la « reconnaissance » de la page web par CLIP vient d'une classe par défaut ; l'écran n'est pas reconnu par CLIP

- **Où.** article.md §4.3 : « ils reconnaissent la page web et l'écran ».
- **Preuve** (`results/E5/zeroshot-clip.json`, `confusion`) :
  - Rappel de CLIP sur `screen_photo` : **4,7 %**.
  - CLIP répond `screenshot_ui` pour **5 389 images sur 11 100 (49 %)**. Sa précision sur cette
    classe est de **11 %**. Son rappel de 98 % vient de ce biais.
  - Sur la page de livre, la précision de CLIP est de 6 %. SigLIP est plus honnête : précision
    80 % sur la page web, 92 % sur l'écran.
  - Les autres chiffres se vérifient : précision équilibrée 0,238 et 0,532 ; livre photographié
    0 et 8,5 % ; passe-partout 3 et 14 %.
- **Autres défauts.**
  - Les gabarits de prompt diffèrent : CLIP a « a photo of … », SigLIP n'a rien
    (`e5_zeroshot.py:51`).
  - La classe « none » fait 57 % des images. Elle mélange les originaux, les témoins sur gris et
    les contrôles JPEG, sous l'étiquette « a museum photograph of an artwork ».
- **Correction.** Écrire : « SigLIP reconnaît la page web (93 %) et l'écran (93 %) ; CLIP ne
  reconnaît rien de façon fiable (il répond "site de collection" pour une image sur deux) ».
  Rapporter précision, rappel et F1 par classe. Utiliser le même gabarit de prompt, ou une
  moyenne sur plusieurs gabarits, pour les deux modèles.

### I3. E4b : « CLIP réagit à la couleur » est contredit ; la « couleur seule » est aussi un flou ; le grain n'est pas rapporté à la résolution du modèle

- **Où.** article.md §4.4, dernier paragraphe, et §5 (« DINOv2 par la texture, CLIP par la
  couleur ») ; `src/impressions/layers.py:497-503` (`colour_only`).
- **Preuve.**
  - La variante `ht_cmy` a *la même dominante* et des points. CLIP la retrouve dans les 10
    premiers à **75 %** [70-80]. La variante « couleur seule » (même dominante, sans points)
    tombe à **60 %** [54-65]. Si la couleur était en cause, les deux auraient le même score.
  - J'ai mesuré, sur 10 œuvres, l'écart moyen à l'original sur une image réduite à 56 px :
    17,3 (`ht_cmy`) contre 16,0 (`ht_cmy_colour`). Les deux ont la même couleur. La seule
    différence est que `colour_only` remplace les points par un `GaussianBlur(4,5 px)`. Ce que
    CLIP perd, c'est plutôt la netteté.
  - Par ailleurs, la quadrichromie a bien une couleur plus proche de l'original (écart 8,0-8,5
    contre 17,3).
  - Les cellules de 3, 5 et 8 px sont définies sur une image de 960 px. CLIP réduit le petit
    côté de 720 px à 224 px (facteur 3,2). Les périodes deviennent ≈ 0,9, 1,6 et 2,5 px, au
    voisinage de la limite de Nyquist. DINOv2 réduit à 256 px. D'où des résultats non
    monotones : CLIP fine 0,69 < moyenne 0,84 > grosse 0,32 ; DINOv2 fine 0,87 > moyenne 0,54.
    Claude voit l'image presque en pleine résolution. Les « voies différentes » selon les
    modèles peuvent venir de la résolution d'entrée, pas de la nature du modèle.
- **Correction.**
  - Ajouter un témoin « flou seul » (même `GaussianBlur` sur l'original).
  - Exprimer la finesse de trame en cycles par image d'entrée du modèle.
  - Faire plusieurs graines et corriger pour les comparaisons multiples : 6 variantes × 3
    modèles, choisies après coup.
  - Retirer « CLIP par la couleur ». Seule la sensibilité de DINOv2 aux points (97 → 54 → 4 %)
    tient.

### I4. Les encodeurs ne voient pas le bord du fichier : recadrage central de CLIP et DINOv2

- **Où.** `src/impressions/encoders.py:58-63`. Ce sont les processeurs Hugging Face par défaut.
  - CLIP : `size 224` puis `center_crop 224`.
  - DINOv2 : `shortest_edge 256` puis `crop 224`.
  - SigLIP : redimensionné en 224×224, déformé, sans recadrage.
- **Ce qui ne va pas.**
  - Une image 4:3 perd 25 % de sa largeur avec CLIP et 34 % avec DINOv2. « Le cadre le plus
    extérieur, c'est le bord du fichier » (Garde-fou, §1, §5) est faux pour deux des trois
    encodeurs. Le cadre qu'ils voient est celui du recadrage.
  - J'ai mesuré la part de l'œuvre conservée avec `content_mask`, sur 8 graines :
    - cadre doré : CLIP **92 %**, DINOv2 **80 %**. Le cadre est coupé sur deux côtés, et
      l'œuvre aussi.
    - `book|2` : DINOv2 **83-91 %**. Le témoin, centré, garde 100 %.
  - Le témoin « même surface » est apparié dans l'espace du fichier, pas dans celui que le
    modèle reçoit.
- **Correction.** Compléter chaque image en carré (marges grises) avant l'encodage, ou désactiver
  le recadrage. Sinon, le dire dans le Protocole et dans les Limites, et rapporter la surface
  vue par chaque modèle.

### I5. Réel (E6) : annotation non indépendante, œuvres trop célèbres, chiffres sans script ni intervalle

- **Où.** article.md §4.5 et §6 (« elle l'est sur le réel, annoté séparément »).
- **Ce qui ne va pas.**
  - `n_layers` et `work_area` de `manifest.jsonl` ont été annotés par l'agent de la boucle
    (Claude), sans aveugle, en connaissant les hypothèses et les résultats d'E5. L'annotation
    n'est pas « indépendante ».
  - Les 22 œuvres sont parmi les plus reproduites au monde : très mémorisées, nommées dans le
    nom du fichier (B1). La règle du PLAN « ne rien affirmer sur moins de 30 œuvres » n'est pas
    respectée.
  - Les chiffres de Claude sur le réel (0/25, 1/44, 12/46, 23/34 ; 1/9 contre 11/30 ;
    0-10 % de « montage » ; Spearman) ne sont produits par **aucun script** et ne figurent dans
    **aucun fichier de `results/`**. Je les ai retrouvés à la main ; les classes de surface
    sont [0,15 ; 0,5[.
  - Le test « à surface égale », 1/9 contre 11/30, donne un test exact de Fisher à **p = 0,23**.
    Ce n'est pas une preuve.
  - En revanche, une régression logistique (support ~ couches + log10 surface, bootstrap groupé
    par œuvre, 2 000 tirages) donne : couches **+1,58 [0,75 ; 2,64]**, log10 surface −1,55
    [−3,42 ; −0,13]. Les deux variables sont corrélées à −0,68.
  - L'effet est très concentré dans les photos de salle : 23/47 en salle contre 13/102
    ailleurs.
- **Correction.**
  - Écrire `scripts/e6_claude_analyse.py`, qui produit `results/E6/claude.json`.
  - Remplacer le 1/9 contre 11/30 par le modèle logistique groupé, avec son intervalle.
    Ajouter le type de support comme covariable.
  - Faire annoter un sous-échantillon par un humain, à l'aveugle (kappa).
  - Ajouter des œuvres moins célèbres.
  - Corriger la phrase des Limites.

### I6. Le témoin apparie la surface, pas la netteté ni l'encombrement

- **Où.** `layers.py:449-461` (`area_matched`).
- **Ce qui ne va pas.**
  - À `deep|6`, l'œuvre a été rééchantillonnée six fois. Elle a subi deux flous (0,6 et
    0,8 px), deux perspectives et un moiré. Le témoin est une seule réduction LANCZOS, nette.
  - L'écart entre la chaîne et le témoin mêle donc trois choses : les supports, la dégradation
    des pixels et l'encombrement de l'image.
- **Correction.** Ajouter un témoin « même surface + même dégradation » : faire subir à l'œuvre
  isolée la même suite de rééchantillonnages et de flous. Ajouter aussi un témoin
  d'encombrement (voir B3).

### I7. Aucun intervalle de confiance dans l'article, alors que §3.4 en annonce

- Toutes les proportions de Claude sont données sans intervalle. Exemples d'intervalles de
  Wilson :
  - 27/30 : [74 ; 97 %]
  - 14/30 : [30 ; 64 %]
  - 0/30 : [0 ; 11 %]
  - 1/9 : [2 ; 43 %]
  - 11/30 : [22 ; 54 %]
- Les images d'une même œuvre ne sont pas indépendantes (E6 : 5 à 9 images par œuvre). Il faut
  un bootstrap groupé par œuvre.
- **Correction.** Donner un intervalle pour chaque chiffre cité ; la figure 1 et la figure du
  réel doivent porter des barres d'erreur.

### I8. Littérature : antécédent direct non cité

- `notes/litterature.md:455` : **Wang, Larson & Zhao (2026)**, « Visual Input and Its Framing
  Affect Attribute-based Descriptions Produced by Large Vision-Language Models ». Les notes le
  qualifient de « version de H4 ». L'article ne le cite pas, et affirme ensuite « à notre
  connaissance, aucun travail… ».
- Manquent aussi des travaux présents dans les notes et utiles au « creux » :
  - les bordures qui commandent le modèle (Bahng et al. 2022 ; Zolna et al. 2019 ; Elsayed et
    al. 2019 ; Shtedritski et al. 2023, le cercle rouge) ;
  - la criminalistique de la recapture (Cao & Kot 2010 ; Gao et al. 2010), qui montre depuis
    quinze ans que le support écran ou tirage est détectable (lien direct avec H3) ;
  - Lang & Ommer 2018 (œuvres retrouvées dans des vues d'exposition) ;
  - Materzyńska et al. 2022, sur les cartels et légendes que CLIP lit.
- **Correction.** Citer Wang et al. dans §2.4 et dans « Le creux », en disant ce qui nous en
  distingue (cadres physiques emboîtés, et pas seulement le cadrage photographique). Ajouter
  une phrase pour chacune des familles ci-dessus.

### I9. Un seul modèle, en boucle

- Plusieurs étapes passent par Claude, ou par la même famille de modèles :
  - lecture (Sonnet) ;
  - juge (Sonnet) ;
  - annotation des couches déjà présentes (Sonnet) ;
  - annotation du réel (Claude, agent de la boucle) ;
  - rédaction (Claude).
- L'alias `--model sonnet` n'est pas figé : l'identifiant exact du modèle n'est enregistré nulle
  part, et la mesure n'est pas reproductible si l'alias change.
- **Correction.** Enregistrer l'identifiant du modèle dans chaque ligne d'annotation. Prendre un
  juge d'une autre famille, ou un juge humain. Dire clairement dans les Limites que la
  « vérité » comme la mesure viennent de Claude.

---

## Mineur

- **m1.** « 0,3 % » (§3.3, §4.3) : la surface de l'œuvre à `deep|6` est en moyenne **0,24 %**
  (médiane 0,24 %, de 0,16 à 0,33 %) sur les 300 œuvres (`data/cache/stages-clip.npz`,
  `area`). Écrire « 0,2 % ». Le « ~13 % » à deux couches est juste (11,6 à 14,7 % selon la
  chaîne).
- **m2.** §3.1, « Rijksmuseum, Met et sept autres » : le pool compte 8 collections, soit Met,
  Rijksmuseum et **six** autres. Il faut aussi dire que **242 des 300 œuvres viennent du Met**
  (81 %) : les conventions photographiques d'un seul musée dominent §4.1. Enfin, les 300
  identifiants commencent tous par `rijksmuseum:`, y compris ceux du Met. L'étiquette est
  trompeuse ; la corriger ou l'expliquer.
- **m3.** §4.1, « la peinture est presque toujours rognée au bord de la toile » : 35/60 (58 %)
  sans couche ; 32 % sur un fond de studio ; `cropped_object` 3 %. Écrire « le plus souvent ».
  Les autres chiffres de §4.1 se vérifient (48/300 ; 0,72 ; 12 % ; 2,25 et 2,18 ; 98 % et
  80 % ; 93 %).
- **m4.** « vérifié à l'œil sur un échantillon de 15 » (§4.1) et « relu à la main » (§6) :
  consigner l'échantillon, les désaccords et la règle de décision, dans `notes/`.
- **m5.** Reproductibilité.
  - Il n'y a pas de `Makefile`, alors que PLAN E9 le demande.
  - `CHAINS` contient maintenant les chaînes `ht_*` et `rephoto_only`. Relancer
    `e4_embed_stages.py` les encoderait comme étapes d'E4. `e5_zeroshot.outermost()` rendrait
    alors des étiquettes (`cmyk_fine`…) absentes de `SUPPORTS`, et les résultats changeraient
    sans erreur. Le « jeu mêlé » d'`e4_measure.py` changerait aussi.
  - Figer la liste des chaînes d'E4 (par exemple `E4_CHAINS`).
- **m6.** `e5_analyse.py:36` : le type juste est testé par sous-chaîne (« estampe »). « Gravure »
  ou « eau-forte » comptent donc comme faux. Cela touche les colonnes « type juste » du
  journal, pas l'article.
- **m7.** `e6_analyse.py:46-50` : `found` prend le meilleur rang parmi *toutes* les références
  propres. Les estampes en ont jusqu'à 17 sur 27 images, ce qui les rend plus faciles à
  retrouver. Les comparaisons par support sont donc biaisées par le nombre de références.
- **m8.** §4.5, « les couches n'ajoutent un effet net que pour SigLIP » : les estimations sont
  semblables pour les trois modèles (CLIP +0,16 [−0,01 ; 0,30] ; SigLIP +0,17 [0,03 ; 0,29] ;
  DINOv2 +0,10 [−0,04 ; 0,25]). Écrire : « même sens pour les trois modèles, intervalle qui
  frôle zéro ».
- **m9.** Garde-fou. Qu'une trame à gros grain soit décrite comme « une image très tramée »
  (§4.4, 10/30) est attendu. Ne pas en faire un pendant de l'enveloppement (« la trame devient
  le sujet »). Le cadre doré inerte et le médium qui suit l'enveloppe sont, eux, correctement
  présentés comme attendus.
- **m10.** Figures : l'article cite les figures 1 et 3, mais il n'y a pas de figure 2.
- **m11.** Pour la future section 4.2 (`e4_measure.py`) :
  - Le jeu mêlé contient l'étape `orig` des 299 autres œuvres, ce qui double des images du pool.
  - Tous les témoins portent l'étiquette de support « match ». Le score `same_support@10` des
    témoins sera gonflé (5 400 images « match »).
  - Ni les fichiers `results/E4/*.json` ni `notes/E4.md` n'existent encore.
- **m12.** Une seule graine par œuvre : le tirage des couches (couleur du mur, largeur du cadre)
  est confondu avec l'œuvre. Le dire, ou tirer 2 ou 3 graines sur un sous-échantillon.

---

## Chiffres vérifiés et justes

- E5 Claude, verdicts par étape : 30/0/0/0 ; 23/6/1/0 ; 16/9/5/0 ; 17/12/1/0 ; 10/17/0/3 ;
  1/12/14/3 ; 0/0/27/3 ; témoin 0/9/0/21.
- Erreur moyenne de comptage 0,95 contre 1,44 ; 76 % à une couche près.
- Zéro-coup : 0,53 et 0,24 ; médium lu 256/69, 232, 90 et 103.
- E4b, retrouvés dans les 10 premiers : DINOv2 97/54/4 ; CLIP 60/84 ; SigLIP 8 ; rephotographie
  90-99.
- E4b, Claude : 18/12/0/0 ; 1/15/4/10 ; 0/10/10/10.
- E6 encodeurs : cadre 95-100 % ; en salle 30-40 % ; même support 37-50 %.
- E6 Claude : 0/25, 1/44, 12/46, 23/34 ; 1/9 et 11/30 (classes [0,15 ; 0,5[) ; montage
  0-10 % ; 80 % à une couche près.
- 171 images, 22 œuvres ; 85 références.
