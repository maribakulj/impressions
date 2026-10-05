# Revue de littérature (étape E8)

*05/10/2026. Toutes les références ci-dessous ont été **ouvertes en ligne** : page d'éditeur,
notice DOI (Crossref), arXiv, actes CVF / NeurIPS / ACL, catalogue de la BnF ou Open Library,
fac-similé, dépôt d'auteur. Le lien donné est celui qui a servi à vérifier. Quand un détail
(page, numéro, année exacte) n'a pas pu être confirmé, c'est écrit **[non vérifié]**. Le
BibTeX est dans [`references.bib`](../references.bib).*

Rappel de la question (voir [`PLAN.md`](../PLAN.md)) : une œuvre passe de couche en couche (cadre
doré, page de livre, livre photographié, écran, tirage rephotographié). La vision par ordinateur
traite ces couches comme du bruit (« changement de domaine ») ; la thèse du projet est que le cadre
isole le support, le rend déterminant, et porte une part du sens.

---

## (a) Le cadre et le parergon

Ici, le cadre n'est pas un accessoire. Il sépare l'œuvre du monde, et en la séparant il dit
« ceci est une image ». C'est la base théorique de l'hypothèse H1 (« le cadre est l'interrupteur »).

- **Georg Simmel, « Der Bilderrahmen. Ein ästhetischer Versuch »**, *Der Tag* (Berlin),
  18 novembre 1902 [numéro du journal non vérifié]. Repris dans la *Gesamtausgabe*, t. 7, 1995,
  p. 101-108. Traduction anglaise : « The Picture Frame: An Aesthetic Study », *Theory, Culture &
  Society* 11(1), 1994, p. 11-17. https://doi.org/10.1177/026327694011001003
  → Le texte fondateur : pour Simmel, le cadre ferme l'œuvre sur elle-même et la coupe de son
  entourage. Il nous donne le premier sens de « cadre » : une frontière qui isole.

- **José Ortega y Gasset, « Meditación del marco »**, *El Sol*, 5 avril 1921 ; repris dans
  *El Espectador III*, Madrid, Calpe, 1921.
  https://www.alianzaeditorial.es/primer_capitulo/el-espectador-iii-y-iv.pdf
  → Le tableau est une « île imaginaire » et le cadre est ce qui la sépare de la mer du réel ;
  sans cadre, l'image se mêle au mur. C'est très exactement l'effet que nous mesurons chez la
  machine. (Attention : le texte n'est pas dans la *Revista de Occidente*.)

- **Meyer Schapiro, « On Some Problems in the Semiotics of Visual Art: Field and Vehicle in
  Image-Signs »**, *Semiotica* 1(3), 1969, p. 223-242.
  https://doi.org/10.1515/semi.1969.1.3.223
  → Schapiro montre que le champ préparé (surface lisse, bords réguliers, cadre) est une
  invention historique, pas une donnée naturelle. Il nous autorise à traiter le « champ » et le
  « véhicule » (le support matériel) comme des signes à part entière.

- **Jacques Derrida, *La Vérité en peinture***, Paris, Flammarion, 1978.
  https://catalogue.bnf.fr/ark:/12148/cb34609925z
  → La notion de *parergon* : le cadre n'est ni dedans ni dehors de l'œuvre, il travaille à la
  limite. Utile pour dire que la question « le cadre fait-il partie de l'image ? » n'a pas de
  réponse simple, ni pour l'humain ni pour la machine.

- **Louis Marin, « Du cadre au décor ou la question de l'ornement dans la peinture »**,
  *Rivista di estetica* 22, n° 12, 1982, p. 16-35 (référence donnée par Marin lui-même ; pas de
  notice de catalogue consultée).
  https://www.ikkm-weimar.de/site/assets/files/7028/2366767000071_zmk_16-1_07_marin.pdf
- **Louis Marin, « Le cadre de la représentation et quelques-unes de ses figures »**, *Les
  Cahiers du Musée national d'art moderne*, n° 24, été 1988 [pages non vérifiées : les sources
  donnent 24-81 ou 62-81]. Même lien (traduction allemande commentée, *ZMK* 7/1, 2016).
  → Marin décrit les opérations du cadre (clôture, autonomie, mise en présence). Il donne un
  vocabulaire précis pour classer nos couches selon ce qu'elles *font*, pas seulement selon ce
  qu'elles *sont*.

- **Victor I. Stoichita, *L'Instauration du tableau. Métapeinture à l'aube des Temps
  modernes***, Paris, Méridiens Klincksieck, 1993 ; 2e éd. Genève, Droz, 1999.
  https://catalogue.bnf.fr/ark:/12148/cb35608389f
  → L'histoire des tableaux qui montrent des tableaux (cabinets d'amateurs, trompe-l'œil, cadres
  peints). C'est la « méta-peinture » : l'ancêtre exact de nos images d'images.

- **Paul Duro (dir.), *The Rhetoric of the Frame: Essays on the Boundaries of the Artwork***,
  Cambridge, Cambridge University Press, 1996.
  https://catalogue.bnf.fr/ark:/12148/cb37506916h
  → Le recueil de référence en anglais sur le cadre (histoire de l'art, philosophie). Point
  d'entrée pour toute la discussion savante sur les bords de l'œuvre.

- **Eva Mendgen et al., *In Perfect Harmony: Picture + Frame 1850-1920***, Amsterdam, Van Gogh
  Museum / Zwolle, Waanders, 1995 (catalogue d'exposition).
  https://openlibrary.org/works/OL18368410W
  → Le cadre comme objet matériel, choisi par les peintres eux-mêmes. Rappelle que le cadre doré
  que nous fabriquons par programme a une histoire concrète.

- **Christoph Redies & Franziska Groß, « Frames as visual links between paintings and the museum
  environment: an analysis of statistical image properties »**, *Frontiers in Psychology* 4,
  2013, art. 831. https://doi.org/10.3389/fpsyg.2013.00831
  → Seule mesure empirique trouvée de l'idée « le cadre isole » : les statistiques d'image des
  cadres sont plus complexes que celles du tableau et de la salle, une « barrière de
  complexité ». Pas de modèle de vision, mais une méthode proche de la nôtre.

## (b) Cadres emboîtés, laminations, remédiation, paratexte

Ici on passe du cadre unique aux cadres **emboîtés** : une image dans une page, dans une photo,
dans un écran. C'est la base des hypothèses H2 (accumulation) et H3 (compter les couches).

- **Gregory Bateson, « A Theory of Play and Fantasy »**, *Psychiatric Research Reports* 2,
  p. 39-51 [année et pages non confirmées sur une page ouverte : le volume, *Approaches to the
  Study of Human Personality*, est daté 1956 par la Library of Congress et Open Library ; 1955
  est la date usuelle]. Repris dans *Steps to an Ecology of Mind*, 1972.
  https://openlibrary.org/works/OL33468251W
  → Invente la notion de « cadre » psychologique : un message (« ceci est un jeu ») qui dit
  comment lire les autres messages. Une bordure dorée est un tel méta-message.

- **Erving Goffman, *Frame Analysis: An Essay on the Organization of Experience***, New York,
  Harper & Row, 1974. https://openlibrary.org/works/OL3282038W
  → Les cadres de l'expérience s'empilent en **laminations**, chaque « modalisation »
  (*keying*) ajoutant une couche (jeu, répétition, citation…). C'est le modèle direct de nos
  chaînes de k couches, et la question « combien de couches voit-on ? » vient de là.

- **Gérard Genette, *Seuils***, Paris, Seuil, 1987.
  https://catalogue.bnf.fr/ark:/12148/cb366299171
  → Le **paratexte** (titre, préface, légende, couverture) entoure le texte et en commande la
  lecture. Notre couche « page de livre » ajoute une légende : c'est du paratexte au sens de
  Genette, et CLIP lit les mots (voir Goh et al. plus bas).

- **Marshall McLuhan, *Understanding Media: The Extensions of Man***, New York, McGraw-Hill,
  1964. https://openlibrary.org/works/OL871783W
  → « Le message, c'est le médium », et le contenu d'un média est toujours un autre média. C'est
  la formule la plus connue de l'emboîtement que nous testons.

- **Jay David Bolter & Richard Grusin, *Remediation: Understanding New Media***, Cambridge
  (Mass.), MIT Press, 1999. https://openlibrary.org/works/OL18349431W
  → Deux logiques : l'**immédiateté** (faire oublier le média) et l'**hypermédiateté** (le
  montrer). Nos couches vont de l'une à l'autre ; la question est de savoir laquelle la machine
  « voit ».

- **Anne Friedberg, *The Virtual Window: From Alberti to Microsoft***, Cambridge (Mass.), MIT
  Press, 2006. https://catalogue.bnf.fr/ark:/12148/cb40232332c
  → Du tableau-fenêtre d'Alberti aux fenêtres multiples de l'écran : une histoire du cadre comme
  fenêtre. Justifie de traiter l'écran et la fenêtre de navigateur comme des cadres au même titre
  que la bordure dorée.

## (c) Reproduction des œuvres et photographie de l'art

Pour une machine, il n'y a jamais d'œuvre « en elle-même » : seulement des reproductions. Cette
littérature dit que la reproduction n'a jamais été neutre.

- **Walter Benjamin, « L'œuvre d'art à l'époque de sa reproduction mécanisée »**, trad. Pierre
  Klossowski, *Zeitschrift für Sozialforschung* 5(1), Paris, Alcan, 1936, p. 40-66.
  https://monoskop.org/images/a/a0/Benjamin_Walter_1936_Loeuvre_dart_a_lepoque_de_sa_reproduction_mechanisee.pdf
  → La reproduction détache l'œuvre de son « ici et maintenant » (l'aura). Notre projet mesure
  ce que la machine garde ou perd de l'œuvre à chaque nouvelle reproduction.

- **André Malraux, *Psychologie de l'art. Le Musée imaginaire***, Genève, Skira, 1947.
  https://catalogue.bnf.fr/ark:/12148/cb324125906
  → Le livre d'art met côte à côte, au même format, des objets de tailles et matières
  différentes : la photographie crée des « arts fictifs ». Une galerie d'images pour CLIP est un
  musée imaginaire au sens de Malraux.

- **Heinrich Wölfflin, « Wie man Skulpturen aufnehmen soll »**, *Zeitschrift für bildende
  Kunst*, trois parties : N.F. 7, 1896, p. 224-228
  (https://archiv.ub.uni-heidelberg.de/artdok/7671) ; N.F. 8, 1897, p. 294-297
  (https://archiv.ub.uni-heidelberg.de/artdok/7672) ; N.F. 26, 1915, p. 237-244
  (https://archiv.ub.uni-heidelberg.de/artdok/7673). Traduction anglaise par Geraldine A. Johnson,
  « How One Should Photograph Sculpture », *Art History* 36(1), 2013, p. 52-71,
  https://doi.org/10.1111/j.1467-8365.2012.00926.x
  → Un historien de l'art qui se plaint que les photographes « trahissent » les statues par le
  mauvais angle et la mauvaise lumière. La première couche (la photo) décide déjà de l'œuvre.

- **Geraldine A. Johnson (dir.), *Sculpture and Photography: Envisioning the Third
  Dimension***, Cambridge University Press, 1998.
  https://catalogue.bnf.fr/ark:/12148/cb37711480k
  → Comment la photographie a façonné la connaissance de la sculpture. Utile pour notre type
  « sculpture », où le passage en 2D est la toute première couche.

- **Bruno Latour & Adam Lowe, « The Migration of the Aura, or How to Explore the Original
  through Its Facsimiles »**, dans T. Bartscherer & R. Coover (dir.), *Switching Codes*,
  University of Chicago Press, 2011 [pages non vérifiées]. Version de l'auteur :
  http://www.bruno-latour.fr/sites/default/files/108-ADAM-FACSIMILES-GB.pdf ; version française,
  *Intermédialités* 17, 2011, https://doi.org/10.7202/1005756ar
  → Une œuvre est une « trajectoire » de copies, bonnes ou mauvaises ; l'aura peut migrer vers
  une copie soignée. Cela nous donne un critère : une couche n'est pas « bruit » ou « signal »
  en soi, elle peut enrichir ou appauvrir la trajectoire.

- **Hito Steyerl, « In Defense of the Poor Image »**, *e-flux journal* n° 10, novembre 2009.
  https://www.e-flux.com/journal/10/61362/in-defense-of-the-poor-image/
  → L'image pauvre (compressée, recadrée, rephotographiée) n'est pas une image ratée : sa
  pauvreté raconte sa circulation. C'est la version critique de notre thèse « le support porte
  du sens ».

- **Costanza Caraffa (dir.), *Photo Archives and the Photographic Memory of Art History***,
  Berlin, Deutscher Kunstverlag, 2011. https://catalogue.bnf.fr/ark:/12148/cb45106472r
- **Costanza Caraffa & Tiziana Serena (dir.), *Photo Archives and the Idea of Nation***,
  Berlin/Boston, De Gruyter, 2015 [en ligne déc. 2014 ; année imprimée non confirmée].
  https://doi.org/10.1515/9783110331837
  → Les photothèques d'histoire de l'art (Florence, KHI) étudiées comme des objets : chaque
  tirage a un carton, des annotations, un tampon. Ce sont exactement les « couches déjà
  présentes » dans les originaux de notre corpus (étape E3).

- **Costanza Caraffa, Emily Pugh, Tracy Stuber & Louisa Wood Ruby, « PHAROS: A digital research
  space for photo archives »**, *Art Libraries Journal* 45(1), 2020, p. 2-11.
  https://doi.org/10.1017/alj.2019.34
  → Le consortium de photothèques où une même œuvre existe en de nombreuses photographies
  historiques, avec appariement d'images entre archives. Un terrain réel tout trouvé pour E6.

## (d) La vision par ordinateur et le changement de support

C'est le camp d'en face : le support est une source d'erreur, il faut que le modèle y soit
**invariant**. Ces travaux fournissent nos outils, nos jeux de données de comparaison, et la
position que la thèse conteste.

- **Antonio Torralba & Alexei A. Efros, « Unbiased Look at Dataset Bias »**, CVPR 2011,
  p. 1521-1528. https://people.csail.mit.edu/torralba/publications/datasets_cvpr11.pdf
  → Un classifieur reconnaît de quel jeu de données vient une image (« Name That Dataset »).
  Preuve ancienne que la « manière de faire l'image » est visible par la machine.

- **Da Li, Yongxin Yang, Yi-Zhe Song & Timothy M. Hospedales, « Deeper, Broader and Artier
  Domain Generalization »** (PACS), ICCV 2017, p. 5543-5551.
  https://openaccess.thecvf.com/content_iccv_2017/html/Li_Deeper_Broader_and_ICCV_2017_paper.html
  → Photo, peinture, dessin animé, croquis : quatre « domaines » d'un même sujet. La manière de
  représenter y est explicitement traitée comme un décalage à surmonter.

- **Xingchao Peng et al., « Moment Matching for Multi-Source Domain Adaptation »** (DomainNet),
  ICCV 2019, p. 1406-1415. https://arxiv.org/abs/1812.01754
  → 345 classes en six domaines (clipart, infographie, peinture, quickdraw, photo, croquis). Même
  logique que PACS, à plus grande échelle.

- **Dan Hendrycks et al., « The Many Faces of Robustness »** (ImageNet-R), ICCV 2021,
  p. 8340-8349.
  https://openaccess.thecvf.com/content/ICCV2021/html/Hendrycks_The_Many_Faces_of_Robustness_A_Critical_Analysis_of_Out-of-Distribution_ICCV_2021_paper.html
  → Peintures, sculptures, broderies, tatouages d'objets ImageNet, construits comme « décalage de
  distribution ». Aucune méthode n'améliore la robustesse à tous les décalages à la fois.

- **Haohan Wang, Songwei Ge, Zachary C. Lipton & Eric P. Xing, « Learning Robust Global
  Representations by Penalizing Local Predictive Power »** (ImageNet-Sketch), NeurIPS 2019.
  https://papers.nips.cc/paper_files/paper/2019/hash/3eefceb8087e964f89c2d59e8a249915-Abstract.html
  → Les réseaux s'appuient sur la texture locale ; un croquis les déroute. Rejoint notre question
  sur la trame d'imprimerie et le moiré, qui sont des textures ajoutées.

- **Dan Hendrycks & Thomas Dietterich, « Benchmarking Neural Network Robustness to Common
  Corruptions and Perturbations »** (ImageNet-C), ICLR 2019. https://arxiv.org/abs/1903.12261
  → Flou, bruit, compression, pixelisation appliqués de façon synthétique. C'est le modèle de nos
  couches « fabriquées par programme » — et la raison de les confirmer sur du réel (E6).

- **Robert Geirhos et al., « ImageNet-trained CNNs are biased towards texture… »**, ICLR 2019.
  https://arxiv.org/abs/1811.12231
  → La texture l'emporte sur la forme dans les décisions des réseaux classiques. Une trame ou un
  moiré peuvent donc peser lourd.

- **Benjamin Recht et al., « Do ImageNet Classifiers Generalize to ImageNet? »**, ICML 2019,
  p. 5389-5400. https://proceedings.mlr.press/v97/recht19a.html
  → Même en recollectant les images avec la même procédure, la précision chute de 11 à 14 points.
  Le moindre changement de fabrication compte.

- **Andrei Barbu et al., « ObjectNet »**, NeurIPS 2019.
  https://papers.nips.cc/paper_files/paper/2019/hash/97af07a14cacba681feacf3012730892-Abstract.html
  → En contrôlant fond, angle et rotation, la précision chute de 40 à 45 points : le contexte
  porte une grande part de la « reconnaissance ».

- **Kai Xiao, Logan Engstrom, Andrew Ilyas & Aleksander Madry, « Noise or Signal: The Role of
  Image Backgrounds in Object Recognition »**, ICLR 2021. https://arxiv.org/abs/2006.09994
  → Le fond seul suffit souvent à classer ; un fond choisi exprès renverse la décision jusqu'à
  ~88 % du temps. Le titre pose exactement notre alternative « bruit ou signal », mais pour le
  fond et non pour le support.

- **Sara Beery, Grant Van Horn & Pietro Perona, « Recognition in Terra Incognita »**, ECCV 2018.
  https://arxiv.org/abs/1807.04975
  → Le lieu de prise de vue décide de la reconnaissance des animaux. Exemple classique de
  dépendance au contexte.

- **Krishna Kumar Singh et al., « Don't Judge an Object by Its Context »**, CVPR 2020.
  https://arxiv.org/abs/2001.03152
  → Le contexte y est un biais à éliminer : c'est la position que notre thèse renverse.

- **Peter Hall, Hongping Cai, Qi Wu & Tadeo Corradi, « Cross-depiction problem: Recognition and
  synthesis of photographs and artwork »**, *Computational Visual Media* 1(2), 2015, p. 91-103.
  https://www.sciopen.com/article/10.1007/s41095-015-0017-1
  → Nomme le « problème de la dépiction croisée » : reconnaître le même objet dans une photo et
  dans un tableau. Le mode de représentation y est un obstacle.

- **Elliot J. Crowley & Andrew Zisserman, « In Search of Art »**, ECCV 2014 Workshops, LNCS,
  p. 54-70. https://www.robots.ox.ac.uk/~vgg/publications/2014/Crowley14a/
- **Elliot J. Crowley & Andrew Zisserman, « The Art of Detection »**, ECCV 2016 Workshops, LNCS,
  p. 721-737. https://www.robots.ox.ac.uk/~vgg/publications/2016/Crowley16/
  → Chercher des objets dans des peintures avec des modèles entraînés sur des photos ; mesure du
  décalage photo → peinture.

- **Nicholas Westlake, Hongping Cai & Peter Hall, « Detecting People in Artwork with CNNs »**,
  ECCV 2016 Workshops, LNCS, p. 825-841. https://arxiv.org/abs/1610.08871
  → Seules les premières couches d'un réseau entraîné sur des photos se transfèrent à l'art.

- **Alec Radford et al., « Learning Transferable Visual Models From Natural Language
  Supervision »** (CLIP), ICML 2021, p. 8748-8763.
  https://proceedings.mlr.press/v139/radford21a.html
  → Un de nos trois modèles. Entraîné sur 400 millions de paires image-texte du web, dont des
  légendes du type « a photo of a painting » : d'où le contrôle obligatoire sur les données
  d'entraînement.

- **Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov & Lucas Beyer, « Sigmoid Loss for
  Language Image Pre-Training »** (SigLIP), ICCV 2023, p. 11975-11986.
  https://openaccess.thecvf.com/content/ICCV2023/html/Zhai_Sigmoid_Loss_for_Language_Image_Pre-Training_ICCV_2023_paper.html
  → Deuxième modèle image-texte ; même famille que CLIP, autre fonction de perte.

- **Maxime Oquab et al., « DINOv2: Learning Robust Visual Features without Supervision »**,
  *Transactions on Machine Learning Research*, 2024 (prépublication 2023).
  https://arxiv.org/abs/2304.07193
  → Troisième modèle, **sans texte** : il permet de séparer ce qui vient des légendes du web et ce
  qui vient de l'image seule.

- **Alex Fang et al., « Data Determines Distributional Robustness in Contrastive Language Image
  Pre-training (CLIP) »**, ICML 2022, p. 6216-6234.
  https://proceedings.mlr.press/v162/fang22a.html
  → La robustesse de CLIP vient de la diversité des données, pas du langage. Argument pour
  attendre que CLIP connaisse les supports qu'il a vus en masse sur le web (écrans, livres).

## (e) Critique de la vision machine

Ces travaux, venus des humanités, refusent de voir la vision machine comme un regard neutre.
Ils fournissent le cadre interprétatif de nos résultats.

- **Fabian Offert & Peter Bell, « Perceptual bias and technical metapictures: critical machine
  vision as a humanities challenge »**, *AI & Society* 36(4), 2021, p. 1133-1144 (en ligne 2020).
  https://doi.org/10.1007/s00146-020-01058-z
  → Le « biais perceptif » : la manière dont un modèle se représente le monde visuel est un biais
  en soi, indépendamment des données. Et la notion de « méta-image technique », très proche de nos
  images d'images.

- **Fabian Offert, « Images of Image Machines. Visual Interpretability in Computer Vision for
  Art »**, ECCV 2018 Workshops, p. 710-715. https://doi.org/10.1007/978-3-030-11012-3_54
  → Regarder ce que le modèle « voit » dans une œuvre, comme objet d'étude en soi.

- **Adrian MacKenzie & Anna Munster, « Platform Seeing: Image Ensembles and Their
  Invisualities »**, *Theory, Culture & Society* 36(5), 2019, p. 3-22.
  https://researchportalplus.anu.edu.au/en/publications/platform-seeing-image-ensembles-and-their-invisualities/
  → La machine ne voit pas une image mais un ensemble d'images. Le voisinage dans la galerie
  (nos plus proches voisins) est précisément ce « voir par ensembles ».

- **Amanda Wasielewski, *Computational Formalism: Art History and Machine Learning***, MIT
  Press, 2023. https://doi.org/10.7551/mitpress/14268.001.0001
  → L'apprentissage automatique fait revenir un formalisme à la Wölfflin. Mise en garde utile :
  mesurer des distances entre images n'est pas neutre théoriquement.

- **Leonardo Impett, « Digital Art History as Critical AI »**, *The Art Bulletin* 106(2), 2024,
  p. 11-14. https://doi.org/10.1080/00043079.2024.2296270
  → L'histoire de l'art numérique doit devenir une critique de l'IA elle-même. Notre projet en
  est un exemple : interroger le modèle à partir d'une notion d'historien (le cadre).

- **Leonardo Impett & Fabian Offert, « There Is a Digital Art History »**, *Visual Resources*
  38(2), p. 186-209 (numéro daté 2022, publié en ligne le 7 août 2024).
  https://arxiv.org/abs/2308.07464
  → Les grands modèles encodent un « canon » d'images non photographiques **tel que médié par
  internet** — c'est-à-dire par des reproductions. Directement notre sujet.

- **Taylor Arnold & Lauren Tilton, *Distant Viewing: Computational Exploration of Digital
  Images***, MIT Press, 2023. https://doi.org/10.7551/mitpress/14046.001.0001
  → « Regarder » par ordinateur est déjà interpréter. Méthode et vocabulaire pour présenter nos
  mesures sans les naturaliser.

- **Joanna Zylinska, *The Perception Machine: Our Photographic Future between the Eye and AI***,
  MIT Press, 2023. https://doi.org/10.7551/mitpress/14471.001.0001
  → La photographie comme processus partagé entre humain et machine. Cadre pour l'hypothèse H5
  (humain contre machine).

## (f) Travaux les plus proches de ce projet

Recherche menée par une soixantaine de requêtes ; une cinquantaine de pages ouvertes. Classés
par familles, du plus proche au plus lointain.

### Le support encodé dans les modèles

- **Ryan Ramos, Vladan Stojnić, Giorgos Kordopatis-Zilos, Yuta Nakashima, Giorgos Tolias & Noa
  Garcia, « Processing and acquisition traces in visual encoders: What does CLIP know about your
  camera? »**, ICCV 2025. https://arxiv.org/abs/2508.10637
  → **Le plus proche conceptuellement.** Sur 47 encodeurs (CLIP, DINO…), le niveau de JPEG,
  l'accentuation, le redimensionnement et même le modèle d'appareil sont lisibles dans les
  représentations et peuvent renverser les prédictions sémantiques. Le support (ici numérique) est
  du signal, pas du bruit — mais seulement pour des traces quasi invisibles, pas pour des cadres
  physiques emboîtés.

### Même œuvre, autres photographies

- **Nikolaos-Antonios Ypsilantis, Noa Garcia, Guangxing Han, Sarah Ibrahimi, Nanne van Noord &
  Giorgos Tolias, « The Met Dataset: Instance-level Recognition for Artworks »**, NeurIPS Datasets
  and Benchmarks 2021.
  https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/5f93f983524def3dca464469d2cf9f3e-Abstract-round2.html
  → Photos de studio pour l'entraînement, photos de visiteurs (cadre, reflets, angle) pour le
  test : exactement notre couche `museum_photo`, mais traitée comme décalage à surmonter.

- **Patryk Bartkowiak, Jakub Markil, Bartosz Kotrys, Dominik Michels, Sören Pirk & Wojtek
  Palubicki, « SynGallery: A Synthetic Gallery of Real Paintings for Instance-Level Artwork
  Recognition »**, prépublication arXiv, juillet 2026. https://arxiv.org/abs/2607.18907
  → Rend des peintures du Met avec cadres, reflets, éclairage de salle et vues obliques — très
  proche de nos couches fabriquées — mais pour apprendre à les **ignorer**. Leur ablation : le gain
  vient de la variété des points de vue, pas du réalisme. Même matériau, but opposé.

- **Xi Shen, Alexei A. Efros & Mathieu Aubry, « Discovering Visual Patterns in Art Collections
  with Spatially-Consistent Feature Learning »**, CVPR 2019. https://arxiv.org/abs/1903.02678
  → Retrouve les mêmes motifs entre copies (atelier de Brueghel), en rendant le modèle invariant à
  l'huile, au pastel, au dessin.

- **Benoit Seguin, Carlotta Striolo, Isabella di Lenardo & Frédéric Kaplan, « Visual Link
  Retrieval in a Database of Paintings »**, ECCV 2016 Workshops, LNCS, p. 753-767.
  https://doi.org/10.1007/978-3-319-46604-0_52
  → Projet Replica sur la photothèque de la Fondation Cini : regrouper les reproductions d'une
  même composition « indépendamment de leur médium ». Encore l'invariance comme but.

- **Riccardo Del Chiaro, Andrew D. Bagdanov & Alberto Del Bimbo, « NoisyArt: A Dataset for
  Webly-supervised Artwork Recognition »**, VISIGRAPP 2019, p. 467-475.
  https://doi.org/10.5220/0007392704670475
  → Les reproductions du web (Flickr, etc.) d'une même œuvre y sont traitées comme du « bruit
  d'étiquette ».

- **Sabine Lang & Björn Ommer, « Reconstructing Histories: Analyzing Exhibition Photographs with
  Computational Methods »**, *Arts* 7(4), 2018, art. 64. https://doi.org/10.3390/arts7040064
  → Retrouver des œuvres accrochées dans des vues d'exposition du MoMA : œuvres encadrées dans un
  mur, c'est-à-dire notre couche `museum_photo` en vrai.

- **Sabine Lang & Björn Ommer, « Attesting similarity »**, *Digital Scholarship in the
  Humanities* 33(4), 2018, p. 845-856. https://doi.org/10.1093/llc/fqy006
  → Organiser des collections d'images d'art par similarité visuelle, avec les historiens.

- **Matthijs Douze et al., « The 2021 Image Similarity Dataset and Challenge »**, arXiv 2021.
  https://arxiv.org/abs/2106.09672
  → Détection de copies sous retouches, dont des images collées dans d'autres images
  (« image dans l'image » comme attaque).

### Bordures et marques qui commandent le modèle

- **Hyojin Bahng, Ali Jahanian, Swami Sankaranarayanan & Phillip Isola, « Exploring Visual
  Prompts for Adapting Large-Scale Models »**, arXiv 2022. https://arxiv.org/abs/2203.17274
  → Une **bordure apprise** de 30 pixels autour de l'image suffit à réorienter un CLIP gelé vers
  une nouvelle tâche. Littéralement : le cadre décide de la tâche. Mais c'est une bordure de
  pixels optimisés, pas un cadre doré.

- **Gamaleldin F. Elsayed, Ian Goodfellow & Jascha Sohl-Dickstein, « Adversarial Reprogramming
  of Neural Networks »**, ICLR 2019. https://arxiv.org/abs/1806.11146
  → L'image est posée au centre d'un « programme » qui l'entoure comme un cadre et change ce que
  le réseau calcule.

- **Konrad Zolna, Michał Zając, Negar Rostamzadeh & Pedro O. Pinheiro, « Adversarial Framing for
  Image and Video Classification »**, AAAI 2019. https://arxiv.org/abs/1812.04599
  → Ne modifier **que la bordure** suffit à tromper un classifieur.

- **Aleksandar Shtedritski, Christian Rupprecht & Andrea Vedaldi, « What does CLIP know about a
  red circle? Visual prompt engineering for VLMs »**, ICCV 2023. https://arxiv.org/abs/2304.06712
  → Un cercle rouge dessiné dirige l'attention de CLIP ; les auteurs y voient une convention
  apprise sur le web. Une convention graphique (comme un cadre) est comprise par le modèle.

- **Gabriel Goh, Nick Cammarata, Chelsea Voss, Shan Carter, Michael Petrov, Ludwig Schubert, Alec
  Radford & Chris Olah, « Multimodal Neurons in Artificial Neural Networks »**, *Distill*, 2021.
  https://distill.pub/2021/multimodal-neurons/
  → Les **attaques typographiques** : une étiquette écrite « iPod » collée sur une pomme fait
  dire « iPod » à CLIP. Nos légendes de page de livre sont de ce type ; contrôle indispensable.

- **Joanna Materzyńska, Antonio Torralba & David Bau, « Disentangling visual and written
  concepts in CLIP »**, CVPR 2022, p. 16410-16419. https://arxiv.org/abs/2206.07835
  → Dans CLIP, le mot écrit et la chose montrée sont emmêlés. Concerne cartels, légendes et
  cartons de photothèque.

- **Bang An, Sicheng Zhu, Michael-Andrei Panaitescu-Liess, Chaithanya Kumar Mummadi & Furong
  Huang, « PerceptionCLIP: Visual Classification by Inferring and Conditioning on Contexts »**,
  ICLR 2024. https://arxiv.org/abs/2308.01313
  → CLIP classe mieux s'il devine d'abord le contexte (fond, orientation). Le contexte est ici de
  l'information — mais le médium et le support ne font pas partie des attributs étudiés.

- **Amita Kamath, Jack Hessel & Kai-Wei Chang, « What's "up" with vision-language models?
  Investigating their struggle with spatial reasoning »**, EMNLP 2023, p. 9161-9175.
  https://aclanthology.org/2023.emnlp-main.568/
  → Les modèles vision-langage confondent gauche/droite, sur/sous. Raison de douter qu'ils
  sachent dire *quoi est dans quoi* (H3).

- **Xiaomeng Wang, Martha Larson & Zhengyu Zhao, « Visual Input and Its Framing Affect
  Attribute-based Descriptions Produced by Large Vision-Language Models »**, prépublication arXiv,
  septembre 2026. https://arxiv.org/abs/2609.18345
  → Le même sujet, cadré serré ou en situation, reçoit des descriptions différentes. « Cadrage »
  au sens photographique, pas cadre physique ; mais c'est une version de H4.

### Recapture : photos d'écrans et de tirages (criminalistique)

- **Hong Cao & Alex C. Kot, « Identification of recaptured photographs on LCD screens »**,
  ICASSP 2010. https://doi.org/10.1109/ICASSP.2010.5495419
  → Article fondateur : une photo d'écran laisse une trace détectable. Le support écran se voit.
- **Xinting Gao, Tian-Tsong Ng, Bo Qiu & Shih-Fu Chang, « Single-view recaptured image detection
  based on physics-based features »**, ICME 2010. https://doi.org/10.1109/ICME.2010.5583280
  → Modèle physique de la chaîne « image affichée ou imprimée → appareil photo ».
- **Thirapiroon Thongkamwitoon, Hani Muammar & Pier Luigi Dragotti, « An image recapture
  detection algorithm based on learning dictionaries of edge profiles »**, *IEEE Transactions on
  Information Forensics and Security* 10(5), 2015. https://spiral.imperial.ac.uk/handle/10044/1/32506
  → Le flou des contours dû à la seconde prise de vue comme signature ; base d'images ICL.
- **Changsheng Chen, Shuzheng Zhang, Fengbo Lan & Jiwu Huang, « Domain Generalization for
  Document Authentication against Practical Recapturing Attacks »**, arXiv 2021.
  https://arxiv.org/abs/2101.01404
  → Chaînes « impression → rephotographie » en faisant varier imprimante, papier et appareil :
  nos couches `halftone_print` + `rephotograph`, côté sécurité.
- **Seongbin Park et al., « Chimera: Creating Digitally Signed Fake Photos by Fooling Image
  Recapture and Deepfake Detectors »**, USENIX Security 2025, p. 4305-4324.
  https://www.usenix.org/conference/usenixsecurity25/presentation/park
  → Rephotographier un écran « blanchit » l'origine d'une image : la couche est apprise et
  compensée.
- **Yujing Sun, Yizhou Yu & Wenping Wang, « Moiré Photo Restoration Using Multiresolution
  Convolutional Neural Networks »**, *IEEE Transactions on Image Processing* 27(8), 2018.
  https://arxiv.org/abs/1805.02996
  → Le moiré d'écran comme pure salissure à effacer : la position « support = bruit » à l'état pur.
- **Tae-Hoon Kim & Sang Il Park, « Deep context-aware descreening and rescreening of halftone
  images »**, *ACM Transactions on Graphics* 37(4), 2018. https://doi.org/10.1145/3197517.3201377
  → Même chose pour la trame d'imprimerie : un artefact à défaire.

### Pages, livres, manuscrits

- **Benjamin Charles Germain Lee et al., « The Newspaper Navigator Dataset »**, CIKM 2020,
  p. 3055-3062. https://doi.org/10.1145/3340531.3412767
  → Extraire les images de 16 millions de pages de journaux : la page est un contenant à retirer.
- **Ryad Kaoua, Xi Shen, Alexandra Durr, Stavros Lazaris, David Picard & Mathieu Aubry, « Image
  Collation: Matching Illustrations in Manuscripts »**, ICDAR 2021. https://arxiv.org/abs/2108.08109
  → La même illustration d'un manuscrit à l'autre : une « même image » à travers des supports.
- **Ombretta Strafforello et al., « Have Large Vision-Language Models Mastered Art History? »**,
  arXiv 2024. https://arxiv.org/abs/2409.03521
  → Les modèles vision-langage face aux styles et périodes ; contexte, pas de couches.

---

## Ce qui manque dans la littérature

**À ma connaissance** (recherche large mais non exhaustive, menée le 05/10/2026), aucun travail
ne prend une même œuvre, ne la fait passer par une **chaîne contrôlée de supports emboîtés** —
cadre doré, passe-partout, page de livre, livre photographié, écran avec moiré, tirage tramé,
rephotographie — et ne demande à CLIP, SigLIP, DINOv2 et à un modèle vision-langage **ce qu'est
l'image** : la chose représentée, l'œuvre, ou le support.

Les trois familles proches s'arrêtent chacune en chemin :

1. **La criminalistique de la recapture** réduit le support à une étiquette binaire
   (« authentique » / « rephotographiée ») au service de la sécurité. Elle prouve que le support
   se voit, sans demander ce qu'il fait au sens.
2. **La robustesse** (PACS, DomainNet, ImageNet-R, « Noise or Signal », Terra Incognita) traite
   le mode de représentation, le fond et le contexte comme un décalage ou un biais à neutraliser.
3. **La reconnaissance d'œuvres** (Met, SynGallery, Replica, ArtMiner, NoisyArt) cherche
   l'invariance aux cadres et aux médiums.

Ramos et al. (2025) sont les plus proches de l'idée « le support est encodé et peut l'emporter
sur le sujet », mais seulement pour des traces numériques quasi invisibles. Les bordures apprises
(Bahng et al., Zolna et al.) montrent qu'un cadre peut commander le modèle, mais ce sont des
pixels optimisés, pas des cadres réels. Du côté des humanités, la théorie du cadre (Simmel,
Ortega, Schapiro, Derrida, Marin, Goffman) n'a, à ma connaissance, jamais été mise à l'épreuve
sur des modèles de vision ; la seule mesure empirique de « le cadre isole » trouvée (Redies &
Groß 2013) porte sur des statistiques d'image, sans modèle.

Recherches **restées sans résultat** (utile pour les formulations prudentes de l'article) :
banc d'essai pour « images d'images », « images emboîtées » ou « méta-images » chez CLIP ou les
modèles vision-langage ; étude de CLIP sur des photos d'écran ou de tirage comme *contenu* (et
non comme fraude) ; effet d'un vrai cadre de tableau, d'un passe-partout ou d'une page de livre
sur un classifieur ; capacité d'un modèle à distinguer « photo d'un tableau » de « tableau », ou
un tableau vu sur un téléphone de l'original ; effet de la trame d'imprimerie sur CLIP. Aucune
étude évaluée par les pairs sur la variation des couleurs entre reproductions en ligne d'une même
œuvre (le « syndrome de la Laitière jaune » du Rijksmuseum n'est documenté que par un livre blanc
Europeana de 2011, non ouvert, donc non retenu ici).

## Références non vérifiées ou écartées

- Bateson 1955 : l'année 1955 et les pages 39-51 n'ont pas été confirmées sur une page ouverte
  (le volume est daté 1956 par les catalogues).
- Marin 1988 : pages non confirmées.
- Latour & Lowe 2011 : pages du chapitre non confirmées.
- Simmel 1902 : numéro du journal *Der Tag* non confirmé ; traducteur anglais non confirmé.
- Non retenus faute de page ouverte : Bell & Ommer, « Digital Connoisseur? » (2016) ; thèse EPFL
  de B. Seguin sur la photothèque Cini ; Verwayen, Arnoldus & Kaufman, « The Problem of the Yellow
  Milkmaid » (Europeana, 2011).
- Plusieurs pages d'éditeurs (MIT Press, Springer, Wiley, SAGE, Taylor & Francis, IEEE) ont
  refusé l'accès automatique : pour ces titres, la vérification s'appuie sur la notice DOI
  (Crossref), arXiv ou le catalogue BnF, cités en lien.
