<!-- Rapport de Codex (session 01a11040, 06/10/2026), extrait tel quel du journal de session ; non modifié. -->

## 2026-10-06T08:27:23.400Z

**Il me manque le document de référence de Punctured Sky pour pouvoir en faire une critique fondée.** Je n’ai pas retrouvé le projet dans les fichiers locaux et les sources connectées consultés. Les recherches publiques renvoient principalement au film de Jon Rafman ; je ne peux pas présumer qu’il s’agit de ton projet.

**Indique-moi son emplacement — chemin local, dépôt, lien — ou joins le dossier ici.** Une version de travail suffit, idéalement avec la présentation, la bibliographie, le corpus envisagé et les éventuelles réalisations.

La revue examinera précisément :

- **Les prémisses** : concepts insuffisamment définis, présupposés contestables, contradictions et conclusions posées d’avance.
- **L’originalité** : confrontation aux travaux les plus proches, y compris ceux qui fragilisent la nouveauté revendiquée.
- **La méthode et les preuves** : constitution du corpus, biais, catégories d’analyse, articulation entre calcul et interprétation historique.
- **La contribution disciplinaire** : ce que le projet ferait effectivement comprendre autrement en histoire de l’art, du design ou en humanités numériques.
- **Les évolutions possibles** : plusieurs orientations comparées, avec leurs apports, leurs difficultés et les recherches nécessaires pour les éprouver.
- **La viabilité doctorale** : problématique resserrée, enquête pilote, périmètre soutenable et adéquation scientifique avec Cambridge.

J’ai vérifié un point structurant : Cambridge attend une **contribution significative à la connaissance**, pouvant notamment réviser des interprétations antérieures. Cela fournit un critère concret pour évaluer l’ambition du projet : identifier exactement quelle connaissance nouvelle ses résultats permettraient d’établir. [Critères doctoraux officiels](https://www.cambridgestudents.cam.ac.uk/your-course/postgraduate-research-students/requirements-research-degrees).

## 2026-10-06T08:35:26.233Z

Audit réalisé sur le snapshot **af1c9bc**, sans modifier le dépôt actif, sans inférence payante ni téléchargement. Le résultat empirique est réel mais la conclusion ontologique dépasse actuellement les mesures.

**Ce que j’ai vérifié indépendamment**

- 1 332 lectures E10b : 420 sujets synthétiques, 420 supports synthétiques, 171 sujets réels, 171 supports réels, 150 trames. Aucun doublon de clé ni erreur enregistrée ; toutes indiquent `claude-sonnet-5-5`.
- Les deux ensembles de jugements comprennent chacun 52 groupes, tous `claude-opus-5-5`, sans verdict manquant.
- Livre à deux couches : **0 sujets principaux, 10 compléments, 20 absences**, avec 30/30 réponses dirigées jugées similaires à la référence.
- Écran à deux couches : **même répartition 0/10/20**.
- Mur à deux couches : **9 principaux, 10 compléments, 11 absences**.
- Régression logistique réelle recalculée avec Python standard uniquement : coefficient couches **1,152288815455**, surface **−3,340595937065**, salle **0,383905618185**, exactement les résultats enregistrés.
- Sensibilités exploratoires : coefficient couches **1,0346** après exclusion des reproductions supplémentaires « clean », **1,2674** avec tous les types de support en indicatrices, **1,0149** avec une indicatrice de présence de personnes. Pas d’IC recalculés pour ces sensibilités. Elles ne font donc pas disparaître l’association observée.
- En retrait successif d’une œuvre, coefficient couches entre **0,8694 et 1,3181** : aucun seul cas ne porte entièrement le résultat.

Les problèmes les plus importants :

1. **Bloquant — « reconnaître l’œuvre » ne mesure pas l’identification de l’œuvre.**

   `src/impressions/blind.py:35-43` demande au juge de comparer le *sujet figuré* à une description de référence. `scripts/blind_judge_artwork.py:27-33` prend cette référence dans la réponse du même lecteur Sonnet à l’image originale, sans vérité de référence curatoriale.

   Exemple décisif : `data/works.jsonl:6` identifie Q27982670 comme **Erminia parmi les bergers**, Paolo de’ Matteis ; les réponses originale et livre l’interprètent comme **Minerve/Athéna** (`data/annotations/blind_readings.jsonl:1` et `:3`). Le livre est compté parmi les 30/30 œuvres « reconnues » parce que sa description ressemble à la description originale — elles peuvent partager la même erreur.

   Ce n’est pas nécessairement un défaut de la mesure de *stabilité iconographique descriptive* ; c’est un défaut de son nom et des inférences qui en sont tirées. Il faut séparer : identification de l’objet/catalogue ; identification iconographique ; présence de motifs ; stabilité par rapport à l’original ; statut discursif. Conserver une référence rédigée par deux lecteurs humains à partir des notices, avec désaccords documentés.

2. **Bloquant — La dissociation description/reconnaissance peut être partiellement fabriquée par le questionnaire.**

   Les questions « que représente cette image ? » et « quelle œuvre… ? » sont deux champs du **même appel**, `src/impressions/blind.py:25-28`. Seul le questionnaire des supports est séparé. Le lecteur peut répartir spontanément l’information entre champs : le livre dans `subject`, l’image intérieure dans `artwork`, pour éviter la répétition.

   Les résultats prouvent la disponibilité de l’information sous une sollicitation dirigée, pas une séparation indépendante entre deux capacités perceptives. L’article décrit correctement les deux appels mais sa discussion extrapole (`article/article.md:371-379`).

   Test nécessaire : trois appels indépendants, contextes vierges et ordre randomisé — description libre seule ; description ciblée de l’œuvre seule ; sortie combinée actuelle. Ajouter plusieurs formulations et une contrainte de longueur comparable. L’effet qui subsiste dans la description libre devient bien plus convaincant.

3. **Bloquant — « Rétrogradation en complément » confond actuellement omission et subordination.**

   Livre et écran donnent chacun 20/30 **absences** du sujet figuré dans la phrase libre, contre seulement 10/30 compléments. La variable régressée est simplement `role != main` (`scripts/blind_analyse.py:123-129`).

   L’article passe de « n’est plus principal » à « fait de l’œuvre un complément » (`article/article.md:317-320`, `:371-374`). Cette seconde proposition n’est pas la description majoritaire des observations.

   Analyser séparément **principal / secondaire / omis**, puis la récupération après question dirigée. Une modélisation multinomiale, ou deux estimands annoncés — mention du sujet ; statut conditionnellement à sa mention — évite de transformer une omission en relation syntaxique. Nommer précisément le phénomène : **sélection du niveau de description**.

4. **Majeur — Le contraste contenant/entourage n’isole pas causalement la contenance.**

   Le contrôle d’encombrement recentre l’original propre sur un autre tableau (`src/impressions/layers.py:525-547`, notamment `:540`), tandis que le livre présente une version dégradée, oblique et décentrée, accompagnée de texte et d’une structure éditoriale. Les contrôles séparés de dégradation et d’encombrement ne constituent pas un plan factoriel qui élimine leurs interactions.

   De plus, l’affirmation « fond sans support » reste incertaine : les lectures parlent d’un retable avec saint « dans un cadre doré » (`blind_readings.jsonl:74`), ou du portrait de Washington dans un cadre ovale et couvert d’emblèmes (`:704`). Ces descriptions de modèles ne suffisent pas à valider les images, mais justifient une inspection indépendante.

   Le livre contient systématiquement « HISTOIRE DE L’ART » (`layers.py:240`) et des termes curatoriaux. Une légende ne nommant pas le sujet n’est pas une absence de signal sémantique.

   Construire des manipulations appariées gardant **exactement les pixels, position, perspective et résolution de l’œuvre** : contexte livre/écran ; contexte matériel non artistique ; contexte brouillé ; contexte voisin d’encombrement équivalent. Croiser présence/absence des inscriptions et lisibilité du contenant. Plusieurs décors par œuvre sont indispensables.

5. **Bloquant pour la portée théorique — Le nombre de couches mêle des relations différentes.**

   `data/real/manifest.jsonl:3-5` compte comme couches photographie, foule/visiteurs, mur, vitre et cadre. Ailleurs apparaissent signature, lettres, arbres et ciel, piédestal, etc. Certaines relèvent de la reproduction, d’autres de l’occlusion, du voisinage spatial, du texte ou de l’accrochage.

   Ajouter des personnes augmente à la fois le nombre annoté de couches et la probabilité que la phrase parle de personnes. Le prédicteur incorpore donc une partie de l’explication alternative de l’issue. Dans un indicateur exploratoire construit à partir des listes, 31/32 images avec personnes explicitement listées hors de la première entrée photographique ne prennent plus l’œuvre pour sujet principal.

   Les photographies de sculpture montrent aussi que la première photographie ou le socle peuvent être exclus du décompte selon le cas ; cette convention peut être défendable mais réclame un codebook. **45/171** lignes ne correspondent pas à `len(layers)-1` : ce n’est pas nécessairement une erreur arithmétique, mais cela interdit de reconstruire la règle à partir du seul inventaire.

   Proposition forte pour le projet : passer du nombre scalaire à un **graphe de relations typées** — reproduit, contient, encadre, porte, occulte, jouxte, légende — puis distinguer profondeur de reproduction et complexité de scène. C’est aussi une contribution potentielle en humanités numériques.

6. **Majeur — Les régressions sont plus limitées que leur présentation.**

   L’article annonce « à type de support égal » (`article/article.md:332-334`) ; le modèle réel de description ne contient que l’indicatrice `in_situ` (`blind_analyse.py:127-128`). Livres, cadres, captures, reproductions imprimées et rephotographies sont tous confondus dans l’autre niveau. La régression des encodeurs ne contient **aucun type de support**, seulement nombre de couches et log-surface (`scripts/e6_analyse.py:71-87`).

   Un bootstrap par œuvre traite la dépendance de l’incertitude ; il ne contrôle pas les différences de contenu, de notoriété ou de photographie propres aux œuvres. « Régression groupée par œuvre » peut suggérer à tort un modèle multiniveau ou des effets fixes.

   Ajouter un modèle à effets œuvre, type complet de support, présence humaine et surface mesurée plutôt qu’estimée ; examiner les distributions et le recouvrement des covariables avant de parler d’appariement. Présenter l’étude réelle comme **observationnelle**, non comme identification causale des couches. Mes recalculs montrent néanmoins que l’association n’est pas manifestement un artefact d’un seul cas.

7. **Majeur — Validité du jugement non établie et risque de circularité de famille.**

   Opus est bien différent de Sonnet mais appartient à la même famille. Référence, lecture, annotation des couches et jugement restent majoritairement produits par Claude. `notes/verifications.md:3-5` précise honnêtement que toutes les vérifications « à l’œil » furent réalisées par un agent, pas par une personne ; `article/article.md:291-292` dit encore « contrôlée à l’œil par nous ».

   Le juge voit un groupe entier de descriptions de la même œuvre ; il peut être influencé par les autres versions. Il n’a aucun exemple négatif permettant d’évaluer sa propension à accepter une scène générique ou un mauvais sujet voisin.

   Constituer un ensemble de validation humaine aveugle, comportant cas difficiles et négatifs : même type de scène mais œuvre différente, mauvaise attribution, sujet partiellement décrit, sujets multiples. Publier désaccords, catégories, accord interannotateurs et matrice de confusion. Utiliser un second juge d’une autre famille seulement comme analyse de sensibilité, pas comme substitut à cette validation.

8. **Majeur, bug confirmé — DINOv2 recadre encore après la correction de remplissage carré.**

   `src/impressions/encoders.py:30-33`, `:48`, `:69-73` affirment que le remplissage carré empêche tout recadrage. Le processeur reste celui de `facebook/dinov2-base`.

   J’ai vérifié la configuration **réellement en cache** :
   `/Users/marcel/.cache/huggingface/hub/models--facebook--dinov2-base/snapshots/f9e44c814b77203eaa57a6bdbbd535f21ede1415/preprocessor_config.json` :
   `do_center_crop: true`, `shortest_edge: 256`, `crop_size: 224`.

   Même carrée, l’entrée est agrandie/réduite à 256 puis recadrée à 224 : DINO conserve **87,5 % de chaque dimension du carré complété**. Le bord externe est toujours perdu. Pour un carré d’origine, 23,44 % de sa surface disparaît.

   Corriger explicitement le processeur ou le remplissage, vérifier des repères aux quatre coins après prétraitement et enregistrer les images effectivement vues. Recalculer les résultats concernés. La comparaison v1/v2 ne permet pas encore d’affirmer une expérience réellement sans recadrage.

9. **Majeur — Incertitude mal calibrée aux proportions extrêmes et absence d’équivalence.**

   `grouped_boot`, `blind_analyse.py:34-41`, donne nécessairement `[1,1,1]` pour 30 succès sur 30, `[0,0,0]` pour aucun succès. Les résultats et figures affichent ainsi une précision artificielle aux plafonds/planchers.

   Pour 30 observations indépendantes, Wilson donnerait environ **[88,6 % ; 100 %]** pour 30/30 et **[0 ; 11,4 %]** pour 0/30. Le réel nécessite une méthode tenant compte des groupes et de la séparation.

   « Le cadre seul ne fait rien » n’est pas démontré par un résultat au plafond. Il faut définir une différence pratiquement pertinente et une analyse d’équivalence, distinguer rang, dérive du vecteur, sélection discursive et compréhension relationnelle. Les résultats E4 enregistrés donnent une dérive cosinus d’environ 0,09–0,10 au cadre.

10. **Majeur — L’étude humaine préparée teste désormais une hypothèse abandonnée.**

   `human_study/PROTOCOLE.md:23-26` utilise encore l’ancien juge `same/partial/support/other`, l’ancien E5 et une comparaison à profondeur six. `:33-35` fixe la réfutation à « ≥ 27/30 », alors que l’article `:322-324` reconnaît que cette profondeur mesure un plancher de résolution.

   Le questionnaire ne comporte ni la question dirigée de reconnaissance, ni les nouveaux contrôles. Toutes les questions sur le support sont simultanément visibles aux humains (`form.html:21-26`), alors que les supports sont séparés dans E10b. Huit œuvres ne peuvent soutenir seules une généralisation ambitieuse à l’histoire de l’art.

   Conserver le bon principe du carré latin évitant de montrer plusieurs versions d’une œuvre à une personne. Refaire le protocole autour de l’effet à résolution suffisante, avec contrôles actuels, tâches indépendantes, formulation de l’hypothèse d’équivalence, référence humaine, puissance calculée sur variation des œuvres et participants. Distinguer experts/non-experts seulement avec effectif permettant cette comparaison.

11. **Majeur pour la reproductibilité, partiellement dû au chantier en cours — Article, calculs et fichiers ne représentent pas encore une version unique.**

   - `Makefile:28-33` annonce reproduire tous les nombres mais n’exécute ni `blind_analyse.py`, ni le lecteur ou juge E10b. Les figures lisent pourtant ses résultats.
   - Les JSON E4 enregistrés portent le schéma ancien `stage_minus_area_matched_log10_rank`, tandis que le code actuel écrit `stage_minus_control_log10_rank`. L’article indique lui-même E4 v2 à compléter (`:343`).
   - `article/article.md:297` affirme premier rang dans 99–100 % des cas. Les résultats JSON fournissent **self_top10** à 99,67–100 % et un **rang médian** de 1 ; ils ne fournissent pas la proportion au premier rang. À recalculer, sans considérer les métriques équivalentes.
   - Les caches sont indexés par œuvre/condition, sans hash des images, prompts ni paramètres (`blind.py:84-95`, `e4_embed_stages.py:75-78`). Des modifications peuvent laisser des résultats antérieurs silencieusement réutilisés.
   - Les sorties brutes des appels agent ne sont pas conservées : impossible de vérifier a posteriori les appels d’outils et le contexte exact. Les noms opaques constituent un progrès réel, pas une preuve d’isolation complète.

   Figer un manifeste d’expérience versionné, avec hashes, modèle exact, prétraitement, prompts, seeds et environnement ; séparer acquisition coûteuse et analyse hors ligne ; ajouter une commande de reproduction sans appel modèle. Ne pas surinterpréter les écarts de chantier comme une négligence définitive : un autre agent poursuit E4.

12. **Majeur pour la comparaison des architectures — Les deux « rapports au support » comparent aussi deux tâches.**

   Les encodeurs fournissent un vecteur global et doivent retrouver une référence exacte ; Claude dispose d’une question dirigée qui lui demande de chercher une œuvre dans la scène. La différence peut résulter du protocole autant que des modèles.

   Comparer également recherche globale versus recherche sur régions, description libre versus ciblée, identification exacte versus sujet générique. Pour DINO/CLIP/SigLIP, l’opposition « texte versus sans texte » change aussi architecture, données, objectifs et prétraitement ; elle ne règle pas causalement la question des légendes d’entraînement.

**Ce qui est déjà solide et doit être conservé**

La construction contrôlée, les témoins par extraction des pixels dégradés, les corpus synthétique/réel distincts, les seeds, les données annotées ouvertes, la stratification initiale et le journal d’autocritique sont de bons fondements. E10b corrige effectivement plusieurs gros problèmes de la première relecture : noms révélateurs, exemples inducteurs de chaînes, juge identique au lecteur, modèle non enregistré, Spearman avec ex æquo, absence du contrôle de dégradation. La reconnaissance de la limite de résolution à six couches est une correction scientifique importante. L’effet descriptif brut à deux couches est massif et ne disparaîtra vraisemblablement pas sous une petite correction statistique ; **sa signification reste la vraie question**.

**Formulation scientifiquement défendable dès maintenant**

> Dans ce corpus et pour ce modèle, l’ajout de certains contextes de reproduction déplace le niveau privilégié de la description libre, tandis qu’une question explicitement orientée vers l’image intérieure permet souvent d’en récupérer des éléments iconographiques. Les contrôles rendent insuffisante une explication par la seule réduction ou dégradation des pixels ; ils n’identifient pas encore un effet propre de la contenance.

La contribution doctorale prometteuse consiste à expliquer **quelles conventions historiques de reproduction et quelles relations entre images gouvernent cette sélection du niveau descriptif**, et à montrer ses conséquences sur des pratiques documentaires réelles. Elle ne réside pas dans la simple démonstration qu’un modèle décrit un livre lorsqu’on lui montre un livre.

## 2026-10-06T09:00:35.616Z

**Point nouveau décisif : le contrôle « livre sans texte » de round2 n’est pas géométriquement apparié.** Dans `src/punctured_sky/layers.py`, `book_page(text=False)` retourne avant plusieurs tirages aléatoires ; `book_photo(text=False)` saute également les tirages des lignes. La perspective suivante change donc malgré la graine identique.

Vérification sans inférence sur trois œuvres : IoU des masques œuvre livre/sans-texte **0,770 ; 0,892 ; 0,882**. Pour Q27982670, le rectangle passe de `(529,125,846,404)` à `(513,152,828,417)` ; surface **12,63 % → 11,85 %**. Le contraste `book_notext − degclut`, annoncé « mêmes pixels, même place » dans `scripts/blind_round2_analyse.py:38`, ne l’est pas. Il faut conserver les mêmes tirages ou séparer paramètres géométriques et rendu textuel, puis versionner les caches concernés.

À mon dernier relevé : **115/270 lectures round2**, aucun jugement ni résultat agrégé. Les exemples `subject_only` mentionnent parfois le contenu précédemment omis : indice qualitatif d’un effet du questionnaire, pas validation quantitative.

Tests E10b appariés recalculés, pour remplacer Fisher :

| Contraste sujet principal | Discordances | McNemar exact bilatéral |
|---|---:|---:|
| Livre − encombrement | 0 / 15 | 0,0000610 |
| Mur − encombrement | 3 / 9 | 0,1460 |
| Livre − dégradation | 0 / 27 | 0,0000000149 |

Les corrections de `552400d` sont effectivement intégrées : ne plus les présenter comme défauts ignorés.

**Le pilote historique devrait examiner une tension entre deux bonnes identifications : retrouver le même motif et distinguer ses objets historiques.**

Ce n’est pas une hiérarchie linéaire unique. Un même état de matrice peut traverser plusieurs éditions ; une édition comprend plusieurs exemplaires ; un exemplaire peut être photographié plusieurs fois. Une copie regravée n’est pas automatiquement un nouvel « état ». Les relations doivent être documentées séparément. Les distinctions manifestation/item d’[IFLA LRM](https://repository.ifla.org/handle/123456789/40) et contenu visuel/objet matériel de [Linked Art](https://linked.art/model/profile/class_analysis/) constituent des points d’appui, pas un schéma à appliquer mécaniquement.

**Matériau immédiatement réutilisable**

Le corpus `caypollard/data/derived/copies/manifest.json` contient réellement **36 images, 10 scènes, cinq groupes appelés `edition`**, avec seulement **quatre scènes communes aux cinq groupes**. Les groupes comportent 10, 8, 8, 5 et 5 images. Le manifeste ne contient que `id`, `scene`, `edition` : aucun identifiant d’exemplaire, état, page source ou numérisation.

Les 26 pages de `copies/pages/` et les dix pages *Icones* conservées ailleurs rendent possible une comparaison page/cadrage. Les descriptions, images et matrices existantes servent au développement. Le résultat enregistré de recherche de motif est déjà proche du plafond : DINO et pose **97,1 % top-1**, avec respectivement mAP **0,839 et 0,808** (`results/pose-copies/report.json`). La recherche du motif seule serait donc une faible nouvelle démonstration.

Le verrou initial est documentaire : les étiquettes actuelles d’édition ne suffisent pas à séparer **édition, exemplaire et fichier provenant d’une institution**.

**Plan opérationnel**

1. **Commencer par motif versus édition/exemplaire**, et réserver les états aux cas explicitement établis dans les catalogues. Un objectif de faisabilité serait huit motifs, trois ensembles bibliographiques, deux exemplaires identifiés par ensemble : environ 48 pages. Ce nombre organise le travail ; il ne constitue pas un calcul de puissance. Deux exemplaires permettent au moins de tester une édition sur un exemplaire jamais utilisé pour régler la méthode.

2. **Construire une vérité de référence avant les modèles.** Pour chaque témoin : identifiant d’objet physique et cote ; volume/édition revendiquée ; feuille/page ; motif ; matrice ou relation de copie lorsqu’établie ; état documenté ; fichier numérique et parent ; institution ; source et passage justifiant chaque assertion. Deux spécialistes arbitrent les cas de référence. Une relation inconnue reste inconnue, pas « différente ».

3. **Produire des vues appariées du même document** : page complète ; pictura seule ; contexte sans pictura ; pictura et contexte fournis séparément ; page avec inscriptions historiques masquées. Les fichiers d’origine restent conservés. Distinguer l’effet pratique du recadrage — qui agrandit la pictura — d’une expérience contrôlée maintenant sa résolution effective.

4. **Fixer deux tâches séparées.** Retrouver d’autres témoins du même motif ; distinguer le groupe bibliographique ou l’exemplaire parmi des témoins du même motif. Les bons et mauvais voisins changent entre ces tâches. La galerie doit contenir les vrais cas difficiles : même motif/autre édition et autre motif/même édition.

5. **Baselines indispensables** : hasard tenant compte des effectifs ; rapprochement perceptuel simple ; DINO/CLIP sur pictura ; sur page ; OCR seul ; métadonnées seules ; combinaison simple pictura+contexte. Une combinaison transparente est préférable à un nouveau modèle avant d’avoir compris le phénomène. L’OCR n’est pas une « fuite » si la question porte explicitement sur le document historique ; en revanche, les marques modernes de plateforme doivent être testées séparément.

**Hypothèses réfutables**

- **H1 — Compromis entre identités.** Le cadrage sur la pictura favorise la recherche du motif mais supprime une information utile à la distinction bibliographique. Réfutation : aucune perte bibliographique pertinente, à résolution contrôlée et hors exemplaires connus.
- **H2 — Spécificité historique des marges.** Le bénéfice du contexte subsiste sur un autre exemplaire et après neutralisation des marques modernes de numérisation. Réfutation : le bénéfice disparaît hors du volume ou de l’institution d’origine ; on détectait une signature de scanner.
- **H3 — Conservation conjointe.** Une représentation séparant pictura et contexte améliore la distinction documentaire sans dégrader au-delà d’une marge prédéfinie la recherche du motif. Réfutation : aucun avantage face à la meilleure baseline simple.

Comparer les résultats **par requête appariée**, avec effet et intervalle ; regrouper l’incertitude par motif et exemplaire/volume. Les milliers de paires d’images ne sont pas des observations indépendantes. Réserver des exemplaires, puis si possible une collection entière, avant tout réglage.

**Provenance et données manquantes**

Publier une matrice de disponibilité : combien de témoins disposent d’une édition, d’un exemplaire et d’un état vérifiables ; pourquoi les autres manquent. Séparer résultat sur relations certaines et sensibilité incluant relations plausibles. Un document non catalogué ne devient pas un négatif de recherche. Ne pas extrapoler le sous-corpus documenté à tout ce qui a circulé : conservation et numérisation sélectionnent déjà les objets observables.

**Décision go/no-go**

- **Go pour un pilote**, si trois ensembles peuvent être reliés à plusieurs exemplaires réels et si le recadrage efface des indices documentaires historiquement interprétables.
- **No-go pour une conclusion sur édition/exemplaire**, si chaque étiquette reste liée à un seul scan ou un seul volume.
- **Go doctoral**, si les erreurs de regroupement modifient une enquête précise — circulation d’une composition, succession des réélaborations, attribution d’un témoin, rôle éditorial du paratexte — et si ce changement est montré sur des sources vérifiables.
- Un gain de score, ou la redécouverte qu’une marge aide à identifier une page, ne suffirait pas seul. Le résultat recherché est **ce qu’une pratique de traitement des reproductions rend historiquement connaissable ou méconnaissable**.

