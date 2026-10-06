# Seconde relecture adverse (E10b.7) — 6 octobre 2026

Relecteur : sous-agent neuf, rôle de relecteur hostile mais juste. Lu : `notes/relecture.md`,
`PLAN.md` (E10b, Garde-fou), fin de `JOURNAL.md`, `article/article.md` (version révisée ; le
paragraphe « [À COMPLÉTER — encodeurs sur la synthèse…] » est ignoré), `src/punctured_sky/blind.py`,
`layers.py`, `encoders.py`, `scripts/blind_*.py`, `scripts/e6_analyse.py`, `scripts/e4b_analyse.py`,
`results/E10b/blind.json`, `results/E6/real-v2.json`, `results/E4b/screens-v2.json`,
`data/annotations/blind_*.jsonl`, `data/blind/map.jsonl`. J'ai aussi parcouru les **transcriptions
des sessions du lecteur** (`~/.claude/projects/-Users-marcel-impressions/*.jsonl`) pour vérifier ce
que Sonnet a réellement vu. Tous les recalculs : `.venv/bin/python`, scripts dans le dossier
temporaire de la session (non versionnés).

## Verdict

**Révision mineure à moyenne — pas encore acceptable en l'état, mais le travail a changé de nature.**
Les fuites de la première version sont réparées pour de bon : noms opaques, juge à identifiants
opaques, aucun exemple, sujet et supports dans deux appels, identifiant du modèle enregistré. Les
transcriptions le confirment : sur 1 335 sessions de lecture abouties, le lecteur n'a ouvert que
l'image demandée ; aucun contexte de projet n'apparaît dans son invite système. Presque tous les
chiffres de l'article se retrouvent dans les fichiers bruts.

Ce qui reste porte sur **l'interprétation**. Le résultat central, 0/30 au livre contre 15/30
pour l'encombrement, est solide (Fisher p ≈ 6·10⁻⁶). Mais la thèse qu'on en tire dépasse la
mesure, pour trois raisons :
- le témoin d'encombrement n'isole pas « contenue par un support » ;
- l'œuvre au livre est le plus souvent **absente** de la phrase, et non « un complément » ;
- la « salle » est rangée parmi les supports contenants sans que les données le montrent.

---

## 1. Les points de la première relecture

| point | état | preuve |
| --- | --- | --- |
| **B1** fuite par le nom de fichier | **corrigé** | `blind.py:51-65` : noms `secrets.token_hex(6)`, 746 copies dans `data/blind/img/`. Transcriptions : 1 335 appels `Read`, tous sur l'image demandée, 1 seul `Bash`. Aucun Read de `map.jsonl`. Juge : ids `d<hex>`, ordre mélangé (`blind.py:109-113`). Restes mineurs : voir m1-m2. |
| **B2** exemple = chaîne profonde | **corrigé** | `blind.py:25-33` : aucun exemple ; sujet et supports dans deux appels. Mais le **sujet et l'œuvre** sont demandés dans le même appel (voir I1). |
| **B3** « le support remplace le sujet » par construction | **en partie** | Deux mesures (nommé / principal), question « quelle œuvre ? », témoins dégradation et encombrement, juge Opus : faits. Pas faits : codage humain (≥ 60 paires, kappa), juge d'une autre famille. La thèse n'est pas reformulée comme attendue (voir B1 et I1 ci-dessous). |
| **B4** phrase fausse de la Discussion | **corrigé** | « trois ou plus » n'apparaît plus. |
| **I1** Spearman, règles de base | **corrigé pour l'essentiel** | `blind_analyse.py:102-109` : `spearmanr`, règle « toujours 1 », règle informée, ρ par condition. Recalculé : 0,846 ; erreur 0,85 contre 0,73 ; réel 0,675 ; 80 %. Il manque l'IC bootstrap du Spearman. |
| **I2** zéro-coup CLIP | **sans objet / en partie** | Le passage a disparu, mais §4.2 (médium lu par CLIP) repose encore sur le zéro-coup v1, avec recadrage, sans P/R/F1 (voir I5). |
| **I3** trame | **corrigé pour l'essentiel** | Témoin flou seul, « CLIP par la couleur » retiré, période en px d'entrée (`screens-v2.json` : 0,7 / 1,17 / 1,87). Une seule graine ; pas de correction pour comparaisons multiples. |
| **I4** recadrage central | **en partie** | `encoders.py:30-38` complète en carré : bon pour CLIP. **DINOv2 recadre encore** : `shortest_edge 256` puis `crop 224` sur le carré, soit 6,25 % de chaque bord perdus (voir I4). §4.2 cite encore E4 v1. |
| **I5** réel | **en partie** | Script et logistique groupée faits. L'annotation n'est toujours pas indépendante, il n'y a pas d'œuvres moins célèbres, et 18 images « propres » sont mêlées aux reproductions (voir B2). |
| **I6** témoin de dégradation | **corrigé** | `layers.py:516-522`. |
| **I7** intervalles | **en partie** | IC au §4.3 et pour la logistique. Pas d'IC pour les bins du réel (100/75/28/6), le 9/30 du mur, le 30/30, la trame (87/77/40/23), le comptage. Pas de figures avec barres d'erreur. |
| **I8** littérature | **corrigé** | Wang, Larson & Zhao 2026 et les familles manquantes sont dans « Le creux ». |
| **I9** un seul modèle | **en partie** | Identifiant enregistré : 1 332 × `claude-sonnet-5-5`, 104 × `claude-opus-5-5`. Juge de la même famille ; aucun humain. C'est bien dit dans les Limites. |
| m1, m3, m7, m10 | corrigés | 0,2 % ; « le plus souvent » ; une référence par œuvre ; plus de figure 2 citée. |
| m2 | corrigé, mais phrase cassée | article.md:219-221 (voir m4). |
| m4 | consigné, mais mal rapporté | voir I6. |
| m5 | **non** | Le `Makefile` ne lance ni `blind_readings.py`, ni `blind_judge_artwork.py`, ni `blind_analyse.py` (voir I7). |

## 2. Chiffres recalculés

Tout se retrouve dans les fichiers bruts, sauf deux points.

**Sujet principal (synthèse, n = 30).** Comptes recalculés, en principal / complément / absent :

| condition | principal | complément | absent |
| --- | --- | --- | --- |
| cadre | 30 | 0 | 0 |
| mur | 9 | 10 | 11 |
| livre | **0** | 10 | **20** |
| écran | 0 | 10 | 20 |
| même surface (livre) | 28 | 0 | 2 |
| même dégradation (livre) | 27 | 0 | 3 |
| encombrement (livre) | 15 | 6 | 9 |
| profondeur 3 / 4 / 6 | 0 | 5 / 2 / 1 | 25 / 28 / 29 |
| témoins à k = 6 (surface / dégradation / encombrement) | 11 / 1 / 0 | — | — |

Les pourcentages et les IC de l'article (93 [83 ; 100], 90 [77 ; 100], 50 [33 ; 67]) sont justes.

**Œuvre reconnue.** Recalculé : 30/30 pour le livre, l'écran, le mur, les témoins à k = 2 et le
cadre. Profondeur 3 : 27/30. Profondeur 4 : 16/30. Profondeur 6 : 5/30. Témoins à k = 6 : surface
8/30, dégradation 1/30, encombrement 2/30. Réel : 100 / 100 / 97,8 / 100 %. Juste.

**Réel, sujet principal.** 25/25 ; 33/44 ; 13/46 ; 2/34, soit 100 / 75 / 28 / 6 %. Juste.
Logistique : +1,15 [0,52 ; 2,07] ; surface −3,34 ; salle +0,38. Juste. Ma réestimation, avec une
autre graine, donne [0,53 ; 2,14].

**E6-v2 (régression des encodeurs).** Recalculé : CLIP 0,192, SigLIP 0,144, DINOv2 0,199 ;
surface −0,476 / −0,661 / −0,590. Juste.

**E4b-v2 (dans les 10 premiers).** Grosse trame : 0,72 / 0,21 / 0,07. Flou seul :
0,99 / 0,98 / 1,00. Juste.

**Écarts :**
- **§4.2, article.md:296-297.** « l'œuvre reste au **premier rang** pour 99 à 100 % » est faux.
  Le chiffre est `self_top10`, c'est-à-dire **dans les dix premiers**. Il vient de
  `results/E4/*.json`, donc d'E4 **v1, avec recadrage central** (fichiers du 6/10 à 01:14), et
  non de la version complétée en carré.
- **« 149 vraies reproductions » (§4.4).** Ce total contient 18 images de musée « propres » (non
  référence), toutes codées « principal » (voir B2).

## 3. Constats classés

### Bloquant

**B1. Le témoin d'encombrement n'isole pas « contenue par un support » ; « salle » n'est pas
soutenue.**

- **Où.** article.md:312-320 (§4.3), 11-20 (Résumé), 368-375 (§5). Code :
  `layers.py:525-548`, `scripts/e4_embed_stages.py:29-34, 59-61`.
- **Problème.**
  1. Le fond d'encombrement est un **autre tableau** : un détail figuratif qui occupe environ 88 %
     de l'image. Le lecteur le décrit comme le sujet. Exemples : « Un détail agrandi d'une
     peinture baroque montrant une figure aux longs cheveux… avec en incrustation au centre une
     petite scène » ; « Un portrait… Un petit tableau… incrusté au centre de son visage ». C'est
     une image *dans* une image, collée sans perspective ni éclairage commun. Ce n'est pas un
     « entourage qui ne contient pas ».
  2. Le livre diffère de ce témoin sur bien d'autres points que « contenir » :
     - un objet du quotidien nommable ;
     - une scène photographique cohérente, avec perspective et ombre ;
     - du **texte lisible** qui annonce la reproduction : « Histoire de l'art », « Fig. 44. —
       Musée, inv. 7258 » ;
     - une position décentrée, alors que le témoin d'encombrement est centré par `area_matched`.
     Aucun de ces facteurs n'est séparé.
  3. La « salle de musée » est mise dans la même classe que le livre et l'écran (§4.3, §5,
     Résumé). Or le mur synthétique donne 9/30 contre 15/30 pour l'encombrement : Fisher
     **p = 0,19**. Sur le réel, le coefficient « photo de salle » vaut +0,38 [−1,30 ; 2,59].
- **Correction.**
  - Restreindre la thèse au livre et à l'écran, et retirer « une salle » des phrases-thèses.
  - Ajouter un témoin d'encombrement **photographique et non contenant** : l'œuvre posée dans une
    scène de rue ou de bureau, avec la même perspective, une ombre et un décentrement.
  - Ajouter un livre **sans texte lisible** (légende et titre floutés), pour mesurer la part du
    paratexte (Goh et al. 2021 s'applique ici).
  - Ou bien présenter le résultat comme un contraste observé, sans le présenter comme isolé.

**B2. Le réel mêle 18 images de musée « propres » aux « reproductions ». Hors photos de salle,
l'effet des couches n'est plus établi.**

- **Où.** `scripts/blind_readings.py:107-113` et `blind_judge_artwork.py:30-32` : seule la
  référence est exclue. `blind_analyse.py:117-146`. article.md:328-333.
- **Problème.**
  - Le bin « 0-1 couche » (25/25 principal) contient 18 images « propres ». L'analyse des
    encodeurs (`e6_analyse.py:42`) les exclut toutes. Les deux populations diffèrent : n = 7
    contre 25 dans le bin 0-1.
  - Ma réestimation **sans les images propres** (n = 131) : couches +1,03 [0,23 ; 2,13]. L'effet
    tient, mais plus faiblement.
  - **Sans images propres ni photos de salle** (n = 84) : +0,82 [**−0,08** ; 1,75].
  - « À type de support égal » (l. 333) est faux. Le modèle n'a qu'une indicatrice
    « salle ». Or les photos de salle ont presque toutes 3 couches ou plus (45/47, d'après le
    manifeste) : la colinéarité est forte. Le bin 0-1, entièrement « principal », crée aussi une
    quasi-séparation, que la crête de 1e-3 (`blind_analyse.py:46-50`) traite à peine.
- **Correction.**
  - Exclure les images `clean`, ou les rapporter à part.
  - Donner la logistique avec et sans photos de salle.
  - Remplacer « à type de support égal » par « en contrôlant le seul fait d'être une photo de
    salle ».
  - Écrire que hors salle, l'intervalle touche zéro.

### Important

**I1. « Rétrogradée en complément » décrit mal les données ; la mesure dépend de la consigne.**

- **Où.** article.md:304-320, 371-374. Code : `blind.py:25-28`.
- **Problème.**
  1. Au livre, l'œuvre est **absente** de la phrase dans 20 cas sur 30, et complément dans 10
     seulement. Même chose à l'écran (20/10). « Fait de l'œuvre un complément » et « l'œuvre
     devient ce que le support montre » ne valent que pour un tiers des cas.
  2. Le même appel demande `subject` (« en une phrase, ce que représente cette image ») puis
     `artwork` (« si une œuvre est reproduite… laquelle et ce qu'elle représente »). Le champ
     `artwork` offre un emplacement réservé à l'œuvre. Le modèle peut donc dédier `subject` à la
     scène entière : c'est une division du travail entre deux champs, pas une hiérarchie
     perceptive. Pour les témoins sur gris, il n'existe aucune autre chose à décrire. Seul le
     témoin d'encombrement teste vraiment la consigne.
  3. Décrire une photo de livre comme « un livre ouvert » est la bonne réponse à « que
     représente cette image ? ». C'est attendu. Le Garde-fou demande de le présenter ainsi.
  4. Le « en une phrase » force le choix d'un seul nom-tête. Le rôle « principal » mesure en
     partie un effet de format.
  5. « La rétrogradation est syntaxique avant d'être perceptive » (l. 374) n'est pas étayé.
- **Correction.**
  - Rapporter la répartition principal / complément / absent.
  - Écrire « le support devient le sujet de la phrase ; l'œuvre, quand elle est nommée, en est
    un complément ».
  - Relancer la question du sujet **seule**, sans le champ `artwork`, au moins sur livre, écran,
    encombrement et témoins.
  - Retirer ou justifier la phrase « syntaxique ».
  - Présenter le fait comme en partie attendu.

**I2. « Reconnaît l'œuvre (100 %) » surestime.**

- **Où.** article.md:16, 309, 329.
- **Problème.**
  - Le juge vérifie que la réponse `artwork` décrit le même sujet figuré que la référence.
    Ce n'est pas une identification de l'œuvre.
  - Sur la synthèse, 71 des 120 réponses `artwork` au livre et à ses témoins disent ne pas
    reconnaître l'œuvre (« que je ne reconnais pas avec certitude… »).
  - Sur le réel, les 22 œuvres sont célèbres : 100 % y est attendu.
- **Correction.** Écrire « décrit correctement l'œuvre reproduite quand on le lui demande », et
  non « reconnaît ».

**I3. Validation du juge et famille unique.**

- **Problème.**
  - Aucun codage humain : le critère B3 (≥ 60 paires, kappa) n'est pas rempli.
  - Le juge (Opus) est de la même famille que le lecteur (Sonnet).
  - J'ai vu des verdicts discutables. Un mur : « …représentant une scène de genre champêtre
    devant une maison » est codé « absent ». Un encombrement : « Un petit tableau mythologique est
    incrusté… » est codé « absent ».
  - Le contraste central (0 contre 15) laisse de la marge. Mais le 9/30 du mur et le 50 % de
    l'encombrement en dépendent.
- **Correction.**
  - Faire coder par un humain au moins 60 paires tirées dans livre, mur, encombrement et
    témoins.
  - Ou prendre un juge non-Claude.
  - Ou, au minimum, faire rejuger le même lot dans un autre ordre (fiabilité test-retest).

**I4. DINOv2 recadre encore.**

- **Où.** `encoders.py:30-38, 72-73`.
- **Problème.** Le processeur DINOv2 a `shortest_edge=256` et `crop_size=224`, avec
  `do_center_crop=True` (vérifié). Sur le carré complété, il retire 12,5 % de chaque dimension.
  Le gris des marges part en premier, mais pour une image 4:3 complétée en carré, 6,25 % de
  chaque bord latéral du *contenu* sont perdus. « Chaque modèle voit l'image entière, bord
  compris » (docstring) et §3.4 sont faux pour DINOv2.
- **Correction.** Passer `do_center_crop=False` avec `size={"height":224,"width":224}`, ou
  compléter avec une marge de 256/224. Puis réencoder, ou le dire dans les Limites.

**I5. §4.2 cite des résultats v1, avec recadrage central.**

- **Où.** article.md:295-302.
- **Problème.**
  - « Premier rang » est en réalité dans les dix premiers.
  - Les chiffres sont ceux d'E4 v1.
  - Le médium lu par CLIP vient du zéro-coup v1 : recadré, sans précision ni rappel, gabarits
    différents (I2 de la première relecture).
- **Correction.** Attendre E4 v2 ; écrire « dans les dix premiers » ; relancer le zéro-coup
  avec complétion en carré et un gabarit commun, ou supprimer la phrase sur le médium.

**I6. « Contrôlée à l'œil par nous » (§4.1, article.md:291) est trompeur.**

- `notes/verifications.md:3-5` dit que les contrôles ont été faits par l'agent Claude, « pas par
  un humain ».
- **Correction.** Écrire « contrôlée par l'agent (Claude) sur 15 images, non validée par un
  humain ».

**I7. Reproductibilité des chiffres principaux.**

- **Où.** article.md:4 (« `make all` reproduit les mesures ») ; `Makefile:24-33`.
- **Problème.** Les cibles `claude` et `measures` lancent encore les anciens scripts non aveugles
  (`e5_readings.py`, `e6_readings.py`…) et jamais `blind_readings.py`,
  `blind_judge_artwork.py` ni `blind_analyse.py`.
- **Correction.** Ajouter ces trois scripts aux cibles ; retirer ou marquer comme obsolètes les
  cibles v1.

**I8. Comparaisons multiples et petit n.**

- **Problème.** 13 conditions synthétiques, 5 trames, 4 bins réels, 3 encodeurs × 7 variantes,
  sur 30 œuvres. Le contraste central survit à toute correction. Les phrases sur la trame (« ce
  sont les points, pas la couleur ») et sur le mur n'en survivent pas toutes. CMY 15/30 contre
  couleur seule 23/30 : p ≈ 0,06 sans correction.
- **Correction.** Désigner le contraste principal comme confirmatoire ; présenter le reste comme
  exploratoire, avec IC.

### Mineur

- **m1.** `blind.py:65`. Le chemin donné au lecteur est
  `/Users/marcel/impressions/data/blind/img/<hex>.jpg`. Les mots « impressions » et « blind »
  sont visibles. Le lecteur avait l'outil `Read` et pouvait ouvrir `data/blind/map.jsonl`, voisin
  du dossier. Il ne l'a pas fait (transcriptions), mais rien ne l'en empêchait. Correction :
  placer les copies hors du dépôt (par exemple `/tmp/<hex>/`) et la table ailleurs ; restreindre
  `Read` à ce dossier.
- **m2.** 46 images réelles gardent leur EXIF, XMP et IPTC (`shutil.copy`, `blind.py:61`), y
  compris `ImageDescription` (26 fichiers) et `Copyright`. L'outil Read ne transmet sans doute
  que les pixels, mais il faut réenregistrer les images sans métadonnées. Pour la synthèse, les
  tailles ne trahissent pas la condition : étapes et témoins ont la même taille.
- **m3.** `blind.py:51-65`, situation de concurrence. Avec 4 fils, `opaque()` relit puis ajoute à
  `map.jsonl` sans verrou. Résultat : **5 clés en double** (746 lignes pour 741 clés, par exemple
  `real|night-watch|night-watch-3f4b092538.jpg|0`). Les appels sujet et supports d'une même
  image ont pu lire deux copies différentes (même contenu). La table est ambiguë. Correction :
  copier toutes les images avant le pool de fils, ou ajouter un verrou. La relecture complète de
  la table à chaque appel est par ailleurs quadratique.
- **m4.** article.md:219-221 : phrase cassée (« …pas la collection d'origine : 60 peintures,
  60 estampes… »). La composition par type est rattachée au préfixe.
- **m5.** §3.5 dit « rang… parmi les 18 405 ». Pour le réel (§4.4), c'est le rang parmi les 170
  autres images du corpus réel. Le préciser.
- **m6.** Le choix du fond d'encombrement (`random.Random(seed + k).choice(backgrounds())`) peut
  tirer l'œuvre elle-même. La probabilité est négligeable, mais il faut l'exclure.
- **m7.** §5 : « ce que supposent les travaux sur l'invariance » (l. 380). Ces travaux ne
  *supposent* pas que les modèles ignorent le support : ils cherchent à le leur apprendre. Le
  résultat des encodeurs (le support dilue l'œuvre) est précisément le défaut qu'ils combattent.
  C'est un homme de paille ; reformuler.
- **m8.** Spearman de comptage : ajouter l'IC bootstrap groupé promis en I1.
- **m9.** Le Résumé dit « vérifié sur 171 vraies reproductions » ; les analyses de Claude en
  portent 149, ou 131 sans les images propres. Harmoniser.

## Ce qui tient

- Les lectures sont réellement aveugles.
- Au livre et à l'écran, l'œuvre n'est jamais le sujet principal de la phrase, alors que les
  témoins de surface et de dégradation le sont à environ 90 %, et le témoin d'encombrement à 50 %.
- Sur le réel, la part « principal » baisse avec les couches à surface égale, du moins avec les
  photos de salle.
- Les trois encodeurs perdent l'œuvre avec les couches au-delà de la surface (E6-v2).
- La trame grosse fait perdre l'œuvre à DINOv2 et à SigLIP.

La forme proposée en E10b.8, un article court et honnête, convient à ces résultats, à condition
de corriger B1, B2 et I1.
