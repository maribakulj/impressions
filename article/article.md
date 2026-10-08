# Ce qui entoure l'œuvre : supports emboîtés et lecture automatique des reproductions

*Projet *punctured sky*, octobre 2026 — https://github.com/maribakulj/punctured-sky. Chaque chiffre
renvoie à un fichier de `results/` ou `data/annotations/` ; `make analyses figures` refait chaque
chiffre et chaque figure à partir des lectures en cache, sans appel aux modèles.*

## Résumé

Une œuvre nous parvient emboîtée dans des supports : cadre, mur, photographie, page de livre,
écran. Une partie de la théorie du cadre prête au cadre une fonction d'isolement ; la vision par
ordinateur, pour reconnaître, cherche à être insensible aux supports. Nous avons fait passer
300 œuvres de musée à travers des chaînes de supports fabriqués, en comparant chaque étape à des
témoins qui gardent la surface de l'œuvre (l'œuvre seule ; les mêmes pixels dégradés à la même
place, sur du gris ou sur un autre tableau), puis regardé 131 vraies reproductions de 22 œuvres.
Trois encodeurs (CLIP, SigLIP, DINOv2) et un modèle descriptif (Claude, lu et jugé à l'aveugle par
un autre modèle) ont été interrogés. Un cadre doré change peu ces mesures. Dans un livre
photographié ou sur un écran, le modèle descriptif identifie encore le sujet de l'œuvre quand on le
lui demande, mais n'en fait plus le sujet de sa description (0 sur 30) — exactement comme lorsque
les mêmes pixels, à la même place, sont posés sur un autre tableau (0 sur 30), alors que sur du
gris ils restent le sujet (30 sur 30) ; un livre sans aucun texte fait de même (2 sur 30). Ce qui
décide est la saillance de l'œuvre dans l'image, non la nature de ce qui l'entoure. Sur les vraies
reproductions, l'œuvre passe au second plan surtout quand des personnes sont visibles. Pour ces
machines et ces tâches, le support ne joue pas de rôle propre : il fait partie de la scène.

## 1. La question

Une œuvre ne nous parvient presque jamais seule. Un tableau est dans un cadre ; le cadre est sur
un mur ; le mur est photographié ; la photographie est imprimée dans un livre ; le livre est
photographié, numérisé, affiché sur un écran, et l'écran à son tour est parfois photographié. Les
supports s'emboîtent comme des poupées russes. Une partie de la théorie du cadre (Simmel, Ortega
y Gasset) lui prête une fonction d'isolement : en séparant l'œuvre, il dit « ceci est une image »
et enveloppe une part de son sens. D'autres auteurs historicisent cette fonction (Schapiro) ou
interrogent la limite même entre l'œuvre et son dehors (Derrida). L'intuition de départ de ce
projet est la première : le cadre isole le support et le rend déterminant.

La vision par ordinateur, pour beaucoup de ses tâches, cherche autre chose. Quand une même chose
apparaît peinte, dessinée, photographiée ou imprimée, elle parle de « changement de domaine » et
cherche des modèles *invariants*, qui reconnaissent la chose quel que soit son support (PACS,
DomainNet, ImageNet-R). C'est un objectif de tâche, pas une thèse selon laquelle le support
n'aurait pas de sens ; d'autres travaux étudient justement les contextes d'exposition (section 2.4). Les travaux sur la reconnaissance d'œuvres
d'art rendent des tableaux avec cadres, reflets et vues obliques de salle — mais pour apprendre au
modèle à les ignorer (SynGallery, 2026). Le support y est un bruit.

Cet article prend le support comme objet. Il fait passer les mêmes œuvres à travers des chaînes
contrôlées de supports emboîtés et demande, à chaque couche, ce que la machine prend l'image pour
*être* : l'œuvre, son sujet, son médium — ou le support lui-même.

Une remarque fixe le cadre de l'enquête. Pour un modèle, il n'y a jamais d'« objet en lui-même » :
ce qu'il reçoit est toujours déjà une photographie, cadrée par quelqu'un, et le seul cadre qu'il
connaisse avec certitude est le bord du fichier. Une peinture photographiée dans une salle n'est,
pour lui, qu'un élément de cette photographie. Qu'un cadre doré *intérieur* pèse peu est donc
attendu ; la question est ce qui se passe quand les couches s'accumulent, et lesquelles comptent.
Les musées eux-mêmes ne livrent pas d'objets nus : sur 300 images de collections que nous avons
annotées, 48 seulement ne montrent aucune couche autour de l'œuvre (section 4.1).

## 2. Ce qu'on sait déjà

Deux littératures parlent du support des images. L'histoire et la théorie de l'art tiennent le
cadre et la reproduction pour des lieux de sens. La vision par ordinateur, quand elle vise la
reconnaissance, les traite le plus souvent comme un décalage à surmonter. Elles se sont déjà
croisées (section 2.4). Cette section les résume l'une après l'autre, puis dit ce qui manque
entre les deux.

### 2.1 Le cadre

Le texte fondateur est un court essai de Simmel (1902). Pour lui, le cadre ferme l'œuvre sur
elle-même et la coupe de son entourage. Il trace une frontière qui isole. Ortega y Gasset (1921)
reprend l'idée avec une image : le tableau est une « île imaginaire », et le cadre la sépare de la
mer du réel. Sans cadre, dit-il, l'image se mêle au mur. Ces deux textes donnent le premier sens du
mot : une limite qui sépare l'image de ce qui n'est pas elle.

Schapiro (1969) historicise cette limite. Le champ préparé, avec sa surface lisse, ses bords
réguliers et son cadre, est une invention tardive, pas une donnée naturelle. Schapiro traite le
champ et le « véhicule », c'est-à-dire le support matériel, comme des signes à part entière. C'est
ce qui nous autorise à demander ce que signifie un support, et pas seulement ce qu'il cache.

Derrida (1978) déplace la question. Le cadre est un *parergon* : ni dedans ni dehors de l'œuvre,
il travaille à la limite. La question « le cadre fait-il partie de l'image ? » n'a donc pas de
réponse simple. Elle n'en a pas davantage pour une machine. Marin (1982, 1988) décrit les
opérations du cadre : clôture, autonomie, mise en présence. Son vocabulaire permet de classer des
couches selon ce qu'elles *font*, et non selon ce qu'elles *sont*. Stoichita (1993) fait l'histoire
de la métapeinture : cabinets d'amateurs, trompe-l'œil, cadres peints, tableaux qui montrent des
tableaux. Ces images d'images sont les ancêtres directs de notre matériau. Le recueil dirigé par
Duro (1996) rassemble enfin la discussion savante sur les bords de l'œuvre, du côté de l'histoire
de l'art comme de la philosophie.

### 2.2 L'emboîtement

Ces auteurs pensent surtout un cadre unique. Notre question porte sur des cadres emboîtés : une
image dans une page, la page dans une photographie, la photographie dans un écran. D'autres
traditions ont pensé cet empilement.

Bateson (1955) invente le cadre au sens psychologique. Un message comme « ceci est un jeu » dit
comment lire les autres messages. C'est un message sur le message. Une bordure dorée est un
méta-message de ce type : elle dit « ceci est une image ». Goffman (1974) prolonge l'idée en
sociologie. Un cadre d'expérience peut être transformé, puis transformé encore : un geste devient
jeu, le jeu devient répétition, la répétition devient citation. Chaque transformation ajoute une
couche. Goffman appelle cet empilement des « laminations ». Les couches se comptent, et l'on peut
demander combien d'entre elles un observateur perçoit. C'est exactement la structure des poupées
russes de notre titre : chaque poupée en contient une autre, et l'on n'atteint la dernière qu'en
ouvrant toutes les précédentes. Nos chaînes de supports sont des laminations matérielles.

Genette (1987) décrit le même phénomène pour le livre. Le paratexte (titre, préface, couverture,
légende) entoure le texte et en commande la lecture. Notre couche « page de livre » ajoute une
légende : c'est du paratexte au sens de Genette. McLuhan (1964) avait donné la formule la plus
connue de l'emboîtement : le contenu d'un média est toujours un autre média. Bolter et Grusin
(1999) l'ont précisée sous le nom de remédiation. Chaque média en reprend un autre selon deux
logiques. L'immédiateté cherche à faire oublier le média. L'hypermédiateté, au contraire, l'exhibe.
Nos couches vont de l'une à l'autre : un passe-partout se fait discret, un écran photographié avec
son moiré se montre. La question est de savoir laquelle des deux logiques la machine perçoit.

### 2.3 La reproduction

Pour une machine, il n'existe pas d'œuvre « en elle-même ». Il n'existe que des reproductions.
Une longue littérature montre que la reproduction n'a jamais été neutre.

Wölfflin (1896, 1897, 1915) se plaignait déjà que les photographes trahissent les statues par le
mauvais angle et la mauvaise lumière. La première couche, la photographie, décide déjà de l'œuvre
que l'on verra. Benjamin (1936) soutient que la reproduction détache l'œuvre de son « ici et
maintenant », qu'il nomme son aura. Malraux (1947) observe que le livre d'art met côte à côte, au
même format, des objets de tailles et de matières différentes. La photographie y crée des « arts
fictifs ». Une galerie d'images pour un modèle comme CLIP est un musée imaginaire au sens de
Malraux : tout y a la même taille et la même matière, celle du fichier.

Latour et Lowe (2011) proposent de voir une œuvre comme une trajectoire de copies, bonnes ou
mauvaises. L'aura peut migrer vers une copie soignée. Une couche n'est donc pas bruit ou signal en
soi : elle peut enrichir la trajectoire ou l'appauvrir. Steyerl (2009) défend l'image pauvre,
compressée, recadrée, rephotographiée. Ce n'est pas une image ratée : sa pauvreté raconte sa
circulation. C'est la version critique de l'idée que le support porte du sens.

Les études sur les photothèques d'histoire de l'art donnent à cette idée un terrain concret
(Caraffa 2011 ; Caraffa et Serena 2015). Chaque tirage y a un carton, des annotations, un tampon.
Ces objets ont leur propre histoire. Ce sont exactement les couches que nous trouvons déjà autour
des œuvres dans les images de musée (section 4.1).

### 2.4 La machine et le support

La vision par ordinateur part d'une position opposée. Quand une même chose apparaît peinte,
dessinée ou photographiée, elle parle de changement de domaine. Le but est un modèle invariant,
qui reconnaisse la chose quel que soit son support. Le support y est un bruit.

Le point de départ est un constat de Torralba et Efros (2011). Un classifieur sait dire de quel
jeu de données vient une image. La manière de faire l'image est donc visible par la machine. La
réponse du domaine a été de construire des bancs d'essai pour neutraliser cet effet. PACS réunit
photo, peinture, dessin animé et croquis d'un même sujet (Li et al. 2017). DomainNet étend la
logique à six domaines et 345 classes (Peng et al. 2019). ImageNet-R rassemble peintures,
sculptures, broderies et tatouages d'objets ordinaires (Hendrycks et al. 2021). ImageNet-Sketch
fait de même avec des croquis (Wang et al. 2019). ImageNet-C applique flou, bruit et compression
par programme (Hendrycks et Dietterich 2019). Dans tous les cas, le mode de représentation est un
décalage à surmonter.

Plusieurs travaux montrent pourtant que les modèles encodent le support malgré tout. Le plus
proche de notre idée est celui de Ramos et al. (2025). Sur 47 encodeurs, dont CLIP et DINO, le
niveau de compression JPEG, l'accentuation, le redimensionnement et même le modèle d'appareil sont
lisibles dans les représentations. Ces traces peuvent renverser les prédictions sur le contenu.
Mais il s'agit de traces numériques presque invisibles, pas de supports physiques emboîtés. Xiao
et al. (2021) montrent que le fond seul suffit souvent à classer une image. Un fond choisi exprès
renverse la décision dans jusqu’à environ 88 % des cas. Leur titre pose notre alternative, « bruit ou
signal », mais pour le fond et non pour le support.

Geirhos et al. (2019) ont montré que les réseaux entraînés sur ImageNet décident davantage d'après
la texture que d'après la forme. Ce résultat compte directement pour nous. Une trame d'imprimerie
ou un moiré d'écran sont des textures ajoutées à l'image. Ils peuvent donc peser lourd dans ce que
la machine croit voir, en particulier dans le médium qu'elle attribue à l'œuvre (section 4.4). Goh
et al. (2021) ont décrit les « attaques typographiques » : une étiquette « iPod » collée sur une
pomme fait dire « iPod » à CLIP. Les légendes de nos pages de livre et les cartels de nos murs sont
de ce type ; il faut les contrôler. Kamath et al. (2023), enfin, montrent que les modèles
vision-langage confondent gauche et droite, dessus et dessous. Il y a donc de bonnes raisons de
douter qu'ils sachent dire ce qui est dans quoi.

La reconnaissance d'œuvres d'art suit la même ligne d'invariance. Le jeu de données du Met
entraîne sur des photographies de studio et teste sur des photographies de visiteurs, avec cadres,
reflets et angles obliques (Ypsilantis et al. 2021). Ces couches y sont un décalage à surmonter.
SynGallery rend des peintures du Met avec cadres, reflets, éclairage de salle et vues obliques
(Bartkowiak et al. 2026). Le matériau est très proche du nôtre. Le but est opposé : apprendre au
modèle à ignorer ces couches.

### 2.5 Critique de la vision machine

Un dernier ensemble de travaux, venu des humanités, refuse de voir la vision machine comme un
regard neutre. Offert et Bell (2021) parlent de « biais perceptif » : la manière dont un modèle se
représente le monde visuel est un biais en soi, indépendamment des données. Ils proposent aussi la
notion de « méta-image technique », très proche de nos images d'images. MacKenzie et Munster (2019)
soutiennent que la machine ne voit pas une image, mais un ensemble d'images. Les plus proches
voisins d'une image dans une galerie, que nous mesurons, sont une forme de ce voir par ensembles.

Zylinska (2023) décrit la photographie comme un processus partagé entre l'œil humain et la
machine. Wasielewski (2023) montre que l'apprentissage automatique fait revenir un formalisme à la
Wölfflin. Mesurer des distances entre images n'est pas un geste théoriquement neutre. Impett (2024)
demande que l'histoire de l'art numérique devienne une critique de l'intelligence artificielle
elle-même. Notre projet s'inscrit dans cette ligne : il interroge les modèles à partir d'une notion
d'historien, le cadre. Impett et Offert (2024) notent enfin que les grands modèles encodent un canon
d'images non photographiques tel que médié par internet, c'est-à-dire par des reproductions. C'est
directement notre sujet.

**Le creux.** Les trois familles proches s'arrêtent chacune en chemin. La robustesse traite le
mode de représentation, le fond et le contexte comme un biais à neutraliser. La reconnaissance
d'œuvres cherche l'invariance aux cadres et aux médiums. Ramos et al. (2025) montrent que le
support est encodé et peut l'emporter sur le sujet, mais pour des traces quasi invisibles.
Wang, Larson et Zhao (2026) montrent que le cadrage photographique — le sujet seul ou en
situation — change les descriptions d'un modèle vision-langage : c'est le plus proche de notre
question, mais leur « cadre » est celui de la prise de vue, pas une suite de supports physiques
emboîtés. Une bordure de pixels optimisés suffit à détourner un classifieur ou CLIP (Elsayed et al.
2019 ; Zolna et al. 2019 ; Bahng et al. 2022), un cercle rouge dessiné dirige son attention
(Shtedritski et al. 2023), un mot écrit dans l'image commande sa lecture (Goh et al. 2021 ;
Materzyńska et al. 2022) : le bord et l'inscription agissent, mais ce sont des marques ajoutées,
non des supports. La criminalistique sait depuis quinze ans reconnaître une photo d'écran ou de
tirage (Cao et Kot 2010 ; Gao et al. 2010) : le support se voit, sans qu'on demande ce qu'il fait
au sens. Enfin, Lang et Ommer (2018) retrouvent des œuvres dans des vues d'exposition, en traitant
la salle comme ce qu'il faut traverser, mais pour reconstituer l'histoire des expositions : le
contexte y est un document. Redies et Groß (2013) mesurent sur des statistiques d'image, sans
modèle, comment le cadre fait transition entre le tableau et le musée. La photothèque comme
archive matérielle est étudiée de près (Caraffa 2011 ; PHAROS), et Impett et Offert (2024)
demandent une critique des conditions computationnelles de l'histoire de l'art. À notre connaissance, aucun travail
ne fait passer une même œuvre par une chaîne contrôlée de supports emboîtés pour demander à des
modèles ce qu'est l'image : la chose représentée, l'œuvre, ou le support. Notre recherche a été
large mais n'est pas exhaustive. C'est ce creux que l'article tente de remplir.

## 3. Protocole

### 3.1 Les œuvres

300 œuvres tirées d'un pool de 18 405 images de collections muséales (huit collections, via Wikidata et Wikimedia Commons ; construit dans le projet frère
*caypollard*). 242 des 300 œuvres viennent du Metropolitan Museum (81 %) : les conventions
photographiques d'un seul musée dominent l'échantillon. Le préfixe `rijksmuseum:` des identifiants
est un héritage du pipeline de caypollard, pas la collection d'origine : 60
peintures, 60 estampes, 60 dessins, 60 sculptures, 60 photographies ; une par groupe de
quasi-doublons ; tirage tournant sur les divisions Iconclass ; côté court ≥ 600 px. Le pool entier
sert de galerie de recherche (les 18 405 images).

### 3.2 Les couches

Neuf couches composables et déterministes : cadre doré, passe-partout, mur de musée avec cartel,
page de livre (marges, légende qui ne nomme jamais le sujet, folio), livre ouvert photographié sur
une table, page web de collection en ligne, écran photographié dans une pièce, impression tramée,
rephotographie au téléphone. Elles s'enchaînent en chaînes (cadre ; cadre → mur ; page → livre
photographié ; page web → écran ; trame → rephoto) et en une chaîne profonde de six couches
(cadre → mur → page → livre photographié → page web → écran). Chaque type de couche a été regardé
sur des planches avant toute mesure ; un défaut de fabrication (taches « camouflage » sur les
papiers) a été corrigé à cette étape.

### 3.3 Les témoins

À deux couches, l'œuvre ne couvre plus que 12 à 15 % de l'image ; à six, 0,2 %. Toute perte
pourrait donc venir de la taille, de la dégradation des pixels ou du simple fait d'être entourée.
Chaque étape a trois témoins, qui gardent exactement la même surface d'œuvre (mesurée en rejouant
la chaîne sur une image blanche puis noire avec la même graine) :

- **même surface** : l'œuvre seule, nette, centrée sur un gris uni ;
- **même dégradation** : l'étape elle-même, dont tous les pixels qui ne sont pas l'œuvre sont
  remplacés par du gris — même position, mêmes rééchantillonnages, flous, perspectives et moirés,
  sans aucun support ;
- **encombrement** : l'œuvre, à la même surface, posée sans cadre sur le détail d'un autre
  tableau (le centre seulement, pour qu'il ne montre lui-même ni cadre ni montage) — quelque chose
  l'entoure, mais pas un support qui la contient.
- **mêmes pixels sur un autre tableau** : l'étape elle-même, dont tous les pixels qui ne sont pas
  l'œuvre sont remplacés par le détail d'un autre tableau — même place, même dégradation, même
  entourage riche, mais aucun support ; et le **livre photographié sans aucun texte**.

La trame est décomposée à part (section 4.5) : sa dominante de couleur seule, le flou seul, des
points sans dominante à trois finesses, la rephotographie seule.

### 3.4 Les machines

- **Trois encodeurs** qui résument une image en un vecteur : CLIP ViT-B/32 et SigLIP base,
  entraînés avec des légendes ; DINOv2 base, entraîné sur des images seules. Chaque image est
  complétée en carré avant l'encodage : sans cela, CLIP et DINOv2 recadrent au centre et ne voient
  pas le bord de l'image.
- **Un modèle qui décrit** : Claude Sonnet (`claude-sonnet-5-5`, identifiant enregistré à chaque
  lecture), interrogé **à l'aveugle** : chaque image est copiée sous un nom opaque ; le sujet
  (« que représente cette image ? » et « quelle œuvre est reproduite, et que
  représente-t-elle ? ») et les supports (chaîne, nombre de couches) sont demandés dans deux
  appels séparés, sans exemple ; dans une seconde manche, la question du sujet est posée seule.
- **Un juge** d'un autre modèle (Claude Opus), lui aussi à l'aveugle (identifiants opaques, ordre
  mélangé), qui dit pour chaque description si le sujet de l'œuvre y est nommé, et s'il est le
  sujet *principal* de la phrase ou seulement un complément (« un livre qui reproduit… »).

### 3.5 Les mesures

- *Retrouver l'œuvre* (encodeurs) : rang de l'image de musée de l'œuvre parmi les 18 405 ; écart
  au témoin en log10 du rang.
- *Identifier l'œuvre* (Claude) : la réponse à « quelle œuvre est reproduite, et que
  représente-t-elle ? » désigne-t-elle le sujet de l'œuvre ? (le titre n'est pas exigé)
- *La place de l'œuvre dans la description* (Claude) : le sujet de l'œuvre est-il nommé ? est-il
  le sujet principal de la phrase ?
- Sur le réel : régressions (log10 du rang ; probabilité que l'œuvre ne soit pas le sujet
  principal) sur le nombre de couches annoté, la surface de l'œuvre et le type de support.
- Intervalles de confiance à 95 % : intervalle de Wilson pour une proportion sur 30 œuvres (le
  rééchantillonnage donne des intervalles nuls à 0/30 et 30/30) ; pour comparer deux conditions
  sur les mêmes œuvres, les paires discordantes et un test exact de McNemar ; pour les régressions
  sur le réel, rééchantillonnage groupé par œuvre (2 000 tirages), qui traite la dépendance entre
  images d'une même œuvre mais ne contrôle pas les différences entre œuvres.

## 4. Résultats

### 4.1 Le musée livre déjà des poupées russes

Avant d'ajouter la moindre couche, nous avons relevé celles que les images de musée portent déjà.
Sur 300 images, 48 seulement montrent l'œuvre sans rien autour. La peinture est le plus souvent
rognée au bord de la toile (35 sur 60 sans aucune couche) ; l'estampe et la photographie sont
montrées avec leur feuille, leurs marges, leur carton, leurs inscriptions (2,25 et 2,18 couches en
moyenne) ; la sculpture est détourée sur un fond de studio (93 %). Le type d'objet se lit dans les
marges avant de se lire dans l'œuvre. La « couche zéro » n'existe pas : nos mesures partent de
l'image telle que le musée la donne. (Annotation faite par Claude, contrôlée à l'œil par l'agent de la
boucle — Claude encore, pas un humain — sur 15 images ; voir `notes/verifications.md`.)

### 4.2 Un cadre doré change peu ces mesures

Un cadre doré autour de l'œuvre change peu ce que les encodeurs retrouvent (l'œuvre reste dans
les dix premiers pour 99 à 100 % des œuvres ; le vecteur ne s'éloigne que d'environ 0,1 en
distance cosinus) et ne change pas ce que Claude décrit (le sujet de l'œuvre est le sujet
principal de 30 descriptions sur 30, Wilson [89 % ; 100 %]). Ce n'est pas la preuve qu'un cadre
« ne fait rien » : ces mesures sont proches de leur plafond et ne disent rien d'autres tâches.
C'est en tout cas attendu : pour une machine, le seul cadre
certain est le bord de l'image, et un cadre *dans* l'image n'est qu'un motif de plus autour de
l'œuvre. Le médium lu suit d'ailleurs l'enveloppe la plus extérieure, comme on pouvait s'y
attendre : accrochée au mur, presque toute œuvre devient « une peinture » pour CLIP ; dans un livre
photographié, « une estampe » ; les témoins de même surface gardent la répartition d'origine.

### 4.3 Ce qui fait passer l'œuvre au second plan

Nous avons posé au modèle descriptif une seule question, dans un appel à part : « que représente
cette image ? ». Un juge, à l'aveugle, dit si le sujet de l'œuvre est le sujet principal de la
réponse, un complément, ou s'il est absent (figure 1).

Seule, centrée, à la surface qu'elle occupe dans le livre photographié, l'œuvre est le sujet
principal dans 30 cas sur 30 (Wilson [89 % ; 100 %]). Encadrée et accrochée au mur, aussi. Dans le
livre photographié, dans **aucun** (0/30, [0 % ; 11 %]) : « un livre ouvert intitulé *Histoire de
l'art*, avec… la reproduction d'un tableau » ; dans une page web affichée sur un écran, dans
aucun non plus. L'œuvre n'y disparaît pas : elle est nommée, mais comme un complément (30 fois sur
30 au livre, 27 à l'écran).

Faut-il en conclure que le support qui *contient* l'œuvre la rétrograde ? Une seconde série de
témoins répond non. Nous avons gardé exactement les pixels de l'œuvre tels qu'ils sont dans le
livre photographié — même place, même taille, même perspective, même flou — et remplacé tout le
reste, soit par du gris, soit par le détail d'un autre tableau. Sur du gris, l'œuvre reste le
sujet principal dans 30 cas sur 30 ; sur un autre tableau, dans **0 sur 30**, comme dans le livre
(30 paires discordantes sur 30, McNemar exact p < 10⁻⁸). Le même livre photographié, à géométrie
identique mais sans aucun texte, la laisse sujet principal dans 2 cas sur 30 seulement : le texte
lisible ne change rien de mesurable (2 paires discordantes, p = 0,5), et être contenue par un
livre ne fait pas plus qu'être entourée d'un tableau. L'œuvre *centrée* sur un autre tableau reste
sujet principal dans la moitié des cas (14/30).

Ce qui fait passer l'œuvre au second plan n'est donc ni le support ni le fait d'être contenue, mais
sa **saillance** dans l'image : un élément petit et décentré, dans une image dont le reste se
décrit lui-même — livre, écran ou n'importe quel tableau — devient un complément. Le modèle
identifie toujours le sujet de l'œuvre quand on le lui demande (98 à 100 %) ; il change seulement
le niveau auquel il décrit l'image.

*Une correction.* Une première version de ce témoin « sans texte » ne gardait pas exactement la
géométrie du livre (en retirant le texte, le programme sautait des tirages au hasard et la
perspective changeait ; recouvrement des surfaces 77 à 89 %). La relecture de Codex l'a relevé.
Avec cette géométrie fausse, le livre sans texte laissait l'œuvre sujet principal 6 fois sur 30,
et nous en avions tiré un petit effet du texte (−0,20) qui n'existe pas. Toute la série a été
rejugée : le juge rend le même verdict pour 98 % des 210 descriptions communes aux deux passages.

Deux réserves. Le format de la question pèse. Dans une première manche, où l'on demandait dans le
même appel « que représente l'image ? » et « quelle œuvre est reproduite ? », le sujet de l'œuvre
était *absent* de la première réponse 20 fois sur 30 au livre et à l'écran (complément 10 fois) :
le modèle répartissait l'information entre les deux questions. Au mur, il était sujet principal
dans 30 % des cas avec la question double, dans 100 % avec la question seule. Et à six couches,
quand l'œuvre ne couvre plus que 0,2 % de l'image, tout s'éteint, témoins compris : c'est un
plancher de résolution, dont nous ne tirons rien.

### 4.4 Sur de vraies reproductions

Sur 131 vraies reproductions de 22 œuvres célèbres (photos de salle, pages de livres, timbres,
affiches, écrans ; figure 3 ; les images de musée « propres » servent de référence et sont
exclues), Claude identifie le sujet de l'œuvre presque toujours, quel que soit le nombre de
couches (98 à 100 %). Mais l'œuvre cesse d'être le sujet principal à mesure que les couches
s'accumulent : 75 % à deux couches, 28 % à trois, 6 % à quatre et plus. C'est une étude
d'observation, pas une expérience : dans une régression logistique (intervalles par
rééchantillonnage des œuvres), l'association avec le nombre de couches subsiste après ajustement
sur la surface estimée de l'œuvre et sur la présence d'une salle (+1,03 [0,14 ; 2,04] ; surface
−3,34 [−6,06 ; −2,15]), mais de justesse. Elle est portée surtout par les photos de salle : sans
elles (84 images), elle devient trop incertaine pour conclure (+0,82 [−0,07 ; 1,80]). Le nombre de
couches est d'ailleurs une variable hétérogène : il additionne des relations différentes
(reproduire, contenir, encadrer, occulter, jouxter) et compte les visiteurs comme une couche,
alors que des visiteurs sont aussi un autre sujet possible pour la phrase. Si l'on ajoute une
indicatrice « personnes visibles » (foule, visiteurs ; 33 images), l'association avec le nombre
de couches n'est plus établie (+0,89 [−0,15 ; 1,93]), tandis que la présence de personnes pèse
nettement (+1,98 [0,51 ; 7,85]). Sur le réel, nous ne pouvons donc pas séparer l'effet des couches
de celui d'un autre sujet présent dans l'image ; c'est cohérent avec la seconde manche (4.3) :
ce qui compte est ce que l'image offre d'autre à décrire. Les descriptions disent la même chose que la synthèse :
« des visiteurs se pressent dans une salle de musée devant *La Nuit étoilée* de Van Gogh ».

Les encodeurs perdent aussi l'œuvre avec les couches, au-delà de sa surface : dans une régression
du log10 du rang de l'image propre de l'œuvre, groupée par œuvre, chaque couche coûte +0,19
[0,05 ; 0,32] (CLIP), +0,14 [0,02 ; 0,27] (SigLIP), +0,20 [0,08 ; 0,33] (DINOv2). Avant que les
images soient complétées en carré, seul SigLIP montrait cet effet : le recadrage central de CLIP
et DINOv2 en masquait une partie.

[À COMPLÉTER — encodeurs sur la synthèse, contre les trois témoins (E4 v2).]

### 4.5 La trame

La trame d'impression n'entoure rien : elle couvre toute l'œuvre. Ce sont ses points, et surtout
leur grosseur, qui comptent. Le flou seul et la dominante de couleur seule laissent l'œuvre sujet
principal des descriptions (87 et 77 %) ; une trame en quadrichromie moyenne la fait tomber à
40 %, une trame grosse à 23 %. Pour les encodeurs, seule la trame grosse fait vraiment perdre
l'œuvre (SigLIP la retrouve dans les dix premiers pour 21 % des œuvres, DINOv2 pour 7 %), ce qui
rejoint le poids de la texture décrit par Geirhos et al. (2019). Les effets des trames fines sont
petits et non monotones : après réduction à 224 pixels, leurs points ne mesurent plus que 0,7 à
1,9 pixel et se replient en moiré.

### 4.6 Compter les couches

À l'aveugle et sans exemple, Claude compte les couches dans le bon ordre (Spearman 0,85 sur la
synthèse, 0,68 sur le réel, où 80 % des comptes sont justes à une couche près). Mais une règle qui
connaîtrait seulement la condition fait aussi bien (erreur 0,73 contre 0,85), et à condition
égale il suit mal les couches que l'image de musée portait déjà. Il distingue les situations
plus qu'il ne compte. Il reconnaît enfin nos couches fabriquées comme des montages (presque 100 %)
et les vraies photos comme vraies (3,5 % de « montage ») : c'est pourquoi les conclusions
retenues sont celles qui tiennent sur le réel.

## 5. Discussion

**Le support comme élément de la scène.** Une partie de la théorie du cadre décrit une limite qui
isole l'œuvre et la désigne. Dans nos mesures, rien ne joue ce rôle pour ces machines. Un cadre
doré change peu ce qu'elles retrouvent et ne change pas ce qu'elles disent. Un livre, un écran, une
salle ne font pas plus qu'un autre tableau posé autour de l'œuvre : ils ne la contiennent pas, ils
l'entourent. Le modèle descriptif choisit le niveau de sa description selon ce qui domine l'image ;
l'encodeur résume l'image entière en un vecteur où tout entourage dilue l'œuvre. Ni l'un ni l'autre
ne traite le support comme un bruit à ignorer, mais aucun ne le traite comme un cadre. Ce n'est pas
une réponse à Derrida : le *parergon* problématise la frontière entre l'œuvre et son dehors, ce
n'est pas une faculté qu'un modèle aurait ou n'aurait pas. Notre protocole, lui, trace cette
frontière d'avance (le masque de l'œuvre), et c'est sur cette frontière construite que nous
mesurons.

**Ce que cela dit de l'intuition de départ.** L'idée que le cadre « enveloppe une partie du sens »
est vraie de la peinture et du regard humain que décrit la théorie ; nos mesures disent qu'elle ne
l'est pas, telle quelle, pour ces machines. Ce n'est pas un résultat négatif sans intérêt : il dit
que la fonction du cadre — séparer, désigner — est précisément ce qui manque à la lecture
automatique des images, et qu'elle devra être apportée de l'extérieur (détection de l'œuvre,
recadrage) pour qu'une machine lise une reproduction comme une reproduction.

**Conséquence pratique.** Dans des archives de reproductions (photos de salle, livres numérisés,
captures d'écran), une recherche par encodeur retrouvera moins bien les œuvres à mesure qu'elles
se perdent dans la scène, et une description automatique les nommera comme des détails. Il faut
localiser l'œuvre avant de la décrire ou de la chercher.

**Ce qui reste attendu**, et que nous ne développons pas : le cadre intérieur change peu les mesures ; le
médium lu suit l'enveloppe ; une œuvre trop petite n'est plus reconnue.

## 6. Limites

- **Couches fabriquées et reconnues comme telles.** Claude voit nos couches comme des montages ;
  les conclusions retenues sont confirmées sur 171 vraies reproductions, mais de 22 œuvres très
  célèbres, que les modèles connaissent sans doute par cœur.
- **Un seul modèle descriptif, une seule famille.** Lecteur (Sonnet), juge (Opus), annotation des
  couches présentes : tout passe par Claude. Aucun codage humain ne valide le juge.
- **« Identifier le sujet » veut dire : concorder avec la lecture de l'original par le même
  lecteur.** Deux versions peuvent partager la même erreur : *Erminia parmi les bergers* de Paolo
  de' Matteis (Q27982670) est lue « Minerve » sur l'original comme dans le livre, et compte comme
  identifiée. C'est une mesure de stabilité de la description, pas d'identification iconographique.
- **Deux tâches différentes.** Les encodeurs résument toute l'image en un vecteur et doivent
  retrouver une image exacte ; Claude répond à une question. Comparer « leur » rapport au support
  compare aussi deux tâches.
- **Reproductibilité.** Les caches sont indexés par œuvre et condition, sans empreinte des images
  ni des consignes ; les réponses brutes des appels ne sont pas toutes conservées.
- **L'annotation du réel** (couches, surface) a été faite par un agent Claude en connaissant les
  hypothèses, sans aveugle.
- **Un seul tirage par œuvre** : le décor (couleur du mur, largeur du cadre) est confondu avec
  l'œuvre ; une seule chaîne profonde, un seul ordre des couches.
- **Gabarits répétés** : nos couches synthétiques réutilisent les mêmes décors ; elles se
  ressemblent par fabrication, et nous n'avons pas utilisé de mesure qui en dépende.
- **Trois encodeurs de taille moyenne.** D'autres modèles peuvent différer. Même complétée en
  carré, l'image est encore recadrée de 12,5 % par DINOv2 (environ 6 % sur chaque bord).
- **Pas d'humains.** L'enquête qui comparerait des personnes et des machines sur les mêmes images
  est prête (`human_study/`) mais n'a pas été menée ; c'est sans doute là que se trouve la suite :
  savoir si les humains, eux, rétrogradent l'œuvre.

## Références

Voir `references.bib` (85 références vérifiées) et `notes/litterature.md`.
