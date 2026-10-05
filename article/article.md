# Poupées russes : ce que les cadres emboîtés font à la lecture d'une image par la machine

*Projet `impressions`, octobre 2026 — https://github.com/maribakulj/impressions. Chaque chiffre
renvoie à un fichier de `results/` ou `data/annotations/` ; `make all` reproduit les mesures.*

## Résumé

Une œuvre nous parvient emboîtée dans des supports : cadre, mur, photographie, page de livre,
écran. La vision par ordinateur traite ces supports comme un bruit à ignorer ; la théorie du cadre
soutient qu'ils enveloppent une part du sens. Nous avons fait passer 300 œuvres de musée à travers
des chaînes contrôlées de supports fabriqués, avec pour chaque étape un témoin où l'œuvre seule
occupe la même surface, puis vérifié les résultats sur 171 vraies reproductions de 22 œuvres
célèbres. Trois encodeurs (CLIP, SigLIP, DINOv2) et un modèle vision-langage (Claude) ont été
interrogés. Le cadre intérieur ne change rien : pour la machine, seul compte le bord le plus
extérieur, celui de l'image. Quand l'œuvre devient un objet dans une scène, elle se perd bien
au-delà de ce qu'explique sa petite taille : à deux couches, son rang de recherche est 3 à 15 fois
moins bon que celui du témoin. Au-delà, le support prend la place du sujet : à six couches, Claude
décrit le support dans 27 cas sur 30, contre 0 pour l'œuvre seule aussi petite ; sur de vraies
photos, il nomme l'œuvre mais la rétrograde en décor (« des visiteurs se pressent devant La Nuit
étoilée »), et cet effet persiste à surface égale. La trame d'impression agit autrement : elle
n'enveloppe pas, elle imprègne ; ses points font perdre le sujet et, à gros grain, deviennent le
sujet. Les supports agissent donc de deux façons, par le bord et par la surface. Sur le réel, pour
les encodeurs, la part propre des couches face à la taille n'est établie que pour SigLIP.

## 1. La question

Une œuvre ne nous parvient presque jamais seule. Un tableau est dans un cadre ; le cadre est sur
un mur ; le mur est photographié ; la photographie est imprimée dans un livre ; le livre est
photographié, numérisé, affiché sur un écran, et l'écran à son tour est parfois photographié. Les
supports s'emboîtent comme des poupées russes. La théorie du cadre, de Simmel à Derrida, soutient
que le cadre n'est pas un accessoire : en isolant l'œuvre, il dit « ceci est une image », et il
enveloppe une part de son sens. Le cadre isole le support et le rend déterminant.

La vision par ordinateur a, sur ce point, une position opposée et rarement formulée comme telle.
Quand une même chose apparaît peinte, dessinée, photographiée ou imprimée, elle parle de
« changement de domaine » et cherche des modèles *invariants*, qui reconnaissent la chose quel
que soit son support (PACS, DomainNet, ImageNet-R). Les travaux sur la reconnaissance d'œuvres
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

Deux littératures parlent du support des images. Elles ne se lisent presque jamais. L'histoire et
la théorie de l'art tiennent le cadre et la reproduction pour des lieux de sens. La vision par
ordinateur les tient pour des obstacles. Cette section les résume l'une après l'autre, puis dit ce
qui manque entre les deux.

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
support est encodé et peut l'emporter sur le sujet, mais pour des traces quasi invisibles. Du côté
des humanités, la théorie du cadre n'a, à notre connaissance, jamais été mise à l'épreuve sur des
modèles de vision ; la seule mesure empirique trouvée de l'idée que « le cadre isole » porte sur
des statistiques d'image, sans modèle (Redies et Groß 2013). À notre connaissance, aucun travail
ne fait passer une même œuvre par une chaîne contrôlée de supports emboîtés pour demander à des
modèles ce qu'est l'image : la chose représentée, l'œuvre, ou le support. Notre recherche a été
large mais n'est pas exhaustive. C'est ce creux que l'article tente de remplir.

## 3. Protocole

### 3.1 Les œuvres

300 œuvres tirées d'un pool de 18 405 images de collections muséales (Rijksmuseum, Met et sept
autres, via Wikidata et Wikimedia Commons ; construit dans le projet frère *caypollard*) : 60
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

### 3.3 Les contrôles

- **Même surface sans support.** À deux couches, l'œuvre ne couvre plus que ~13 % de l'image ; à
  six, 0,3 %. Pour séparer « encadrée » de « devenue petite », chaque étape a un témoin : l'œuvre
  seule, centrée sur un gris uni, couvrant exactement la même part de la même toile. La surface
  réelle de l'œuvre à chaque étape est mesurée en rejouant la chaîne sur une image blanche puis
  noire avec la même graine.
- **Dégâts de pixels sans cadre** (rééchantillonnage + JPEG), terrain de Ramos et al.
- **Trame décomposée** (section 4.4) : couleur seule, points seuls à trois finesses,
  rephotographie seule.
- **Trois modèles** : CLIP ViT-B/32 et SigLIP base, entraînés avec des légendes (ils ont vu « a
  photo of a painting… ») ; DINOv2 base, entraîné sur des images seules.
- **Un modèle vision-langage** (Claude Sonnet) qui décrit, compte et nomme.
- **Le réel** : de vraies reproductions des mêmes œuvres (section 4.5).

### 3.4 Les mesures

- *Retrouver l'œuvre* : rang de l'image de musée de l'œuvre parmi les 18 405, pour chaque étape.
- *Ce que la machine range avec l'image* : part des 10 plus proches voisins de même sujet
  (Iconclass) et de même type d'objet ; dans une galerie mêlée d'images transformées, part des
  voisins qui partagent le même support extérieur.
- *Ce que la machine dit* : en zéro-coup, quel support extérieur et quel type d'œuvre (CLIP,
  SigLIP) ; pour Claude, le sujet, la chaîne de supports, le nombre de couches, le type d'œuvre ;
  un second appel juge si le sujet nommé est celui de l'original (même / partiel / support / autre).
- Intervalles de confiance à 95 % par rééchantillonnage des œuvres (2 000 tirages).

## 4. Résultats

### 4.1 Le musée livre déjà des poupées russes

Avant d'ajouter la moindre couche, nous avons demandé à Claude de relever celles que les
images de musée portent déjà (vérifié à l'œil sur un échantillon de 15). Sur 300 images, 48
seulement montrent l'œuvre sans rien autour. Surtout, les musées ne traitent pas les types de
la même façon : la peinture est presque toujours rognée au bord de la toile (0,72 couche en
moyenne ; le cadre n'apparaît que dans 12 % des cas), alors que l'estampe et la photographie
sont montrées avec leur feuille, leurs marges, leur carton et leurs inscriptions (2,25 et
2,18 couches ; bords de feuille visibles dans 98 % et 80 % des cas). La sculpture est détourée
sur un fond de studio (93 %). Le type d'objet est donc lisible dans les marges avant de l'être
dans l'œuvre. Pour une machine qui apprend sur ces images, « estampe » veut dire en partie
« feuille avec des bords ». La couche zéro n'existe pas : toutes nos mesures partent de l'image
telle que le musée la donne.

### 4.2 Retrouver l'œuvre à travers les couches

Pour chacune des 300 œuvres et chaque étape, nous cherchons l'image de musée de l'œuvre parmi
les 18 405 du pool (figure 2, `article/figures/fig-retrouver.png`). Avec le cadre doré seul,
l'œuvre est retrouvée dans les dix premiers pour 99 à 100 % des œuvres, avec les trois modèles :
le cadre intérieur ne compte pas. Dès que l'œuvre devient un objet dans une scène — accrochée au
mur, imprimée dans un livre photographié, affichée dans une page web — elle se perd : dans les
dix premiers pour 12 % des œuvres avec CLIP au mur, 19 % avec SigLIP dans le livre.

Le témoin de même surface répond à la question de la taille. À deux couches, l'œuvre seule,
aussi petite, sur un fond gris, est bien mieux retrouvée que l'œuvre prise dans son support. Le
rang de l'œuvre dans le livre photographié est 12 à 15 fois moins bon que celui de son témoin
(différence de log10 du rang : +1,08 à +1,19 selon le modèle, intervalle à 95 % entièrement
positif, l'œuvre est moins bien retrouvée que son témoin pour 78 à 89 % des œuvres) ; au mur, 3
à 6 fois (+0,53 à +0,77). Sur la synthèse, les couches agissent donc au-delà de la taille. À
partir de trois couches, l'œuvre ne couvre plus que 4 % de l'image ou moins, et couches comme
témoins tombent au plancher : on ne peut plus départager.

Une mesure prévue a dû être écartée. Dans une galerie mêlant les images transformées de toutes
les œuvres, les voisins d'une image sont presque tous des images de même support (98 à 100 %) —
mais les témoins aussi se regroupent entre eux. Nos couches réutilisent les mêmes gabarits (même
table, même mur, même navigateur) : elles se ressemblent par fabrication. Sur cette question,
seul le réel fait foi (section 4.5).

### 4.3 Le support prend la place du sujet

Claude a lu 30 œuvres (6 par type) à neuf étapes ; un second appel juge si le sujet qu'il nomme
est celui de l'original (figure 1, `article/figures/fig-sujet-support.png`). Le cadre doré seul ne
change rien : 30 descriptions sur 30 restent les mêmes. Au mur, dans le livre photographié, à
l'écran, le sujet survit dans une majorité de cas. À quatre couches, 14 descriptions sur 30
parlent du support plutôt que du sujet ; à six couches, 27 sur 30 : « un écran d'ordinateur
affiche une page web de collection en ligne montrant la photo d'un livre ouvert… ».

Le témoin tranche. À six couches, l'œuvre ne couvre que 0,3 % de l'image. Montrée seule, à la
même taille, au centre d'un gris uni, elle n'est pas reconnue non plus — mais Claude décrit
alors honnêtement « une minuscule peinture sombre au centre d'un grand fond gris » : 0 fois sur
30 il ne parle d'un support. **La perte du sujet est un effet de taille ; son remplacement par le
support est un effet des couches.**

Claude compte d'ailleurs ces couches : rang de Spearman 0,75 entre couches dites et couches
réelles, 76 % des réponses à une couche près, erreur moyenne 0,95 contre 1,44 pour une règle
triviale. Les encodeurs reconnaissent moins bien le support extérieur en zéro-coup (précision
équilibrée sur dix classes : SigLIP 53 %, CLIP 24 %, hasard 10 %) ; ils reconnaissent la page web
et l'écran, pas le livre photographié ni le passe-partout.

Le médium lu suit l'enveloppe, comme on pouvait s'y attendre : au mur, CLIP lit « une
peinture » pour 256 œuvres sur 300 (69 sur l'original), dans le livre photographié « une
estampe » pour 232 ; les témoins de même surface gardent la répartition de l'original (90 et
103). C'est le support, non la taille, qui fixe le médium — un fait attendu, que nous ne
développons pas.

### 4.4 La trame : envelopper ou imprégner

Le cadre enveloppe : il agit par le bord. La trame d'impression n'entoure rien ; elle imprègne
toute la surface. Un premier essai, avec une trame à trois encres sans noir, donnait des
résultats spectaculaires (une Résurrection peinte lue comme « un haut-relief sculpté et doré »).
Ils étaient en partie faux : cette trame jaunissait et violaçait l'image. Nous avons donc
décomposé la couche : la même dominante de couleur sans points ; des points sans dominante (vraie
quadrichromie) à trois finesses ; la rephotographie seule.

La couleur seule ne fait pas perdre le sujet à Claude (18 descriptions identiques sur 30, aucune
autre) ; c'est elle, en revanche, qui produit le « relief doré ». Les points, eux, font perdre
le sujet (trame moyenne : 1 description identique, 10 autres), et à gros grain **la trame devient
le sujet** : « une image très tramée de… » (10 sur 30). C'est l'équivalent, par imprégnation, de ce
que les couches emboîtées font par enveloppement.

Les encodeurs ne réagissent pas à la même composante. DINOv2, entraîné sur des images seules,
réagit aux points (retrouvé dans les 10 premiers : 97 % avec la couleur seule, 54 % avec la trame
moyenne, 4 % avec la grosse), ce qui rejoint le biais de texture décrit par Geirhos et al. (2019).
CLIP réagit surtout à la couleur (60 % avec la dominante seule, 84 % avec la trame moyenne en
couleurs justes). Tous perdent l'œuvre à gros grain (SigLIP 8 %). La rephotographie seule ne fait
presque rien (90-99 %).

### 4.5 Sur de vraies reproductions

Nos couches sont fabriquées, et Claude le voit : il déclare « montées numériquement » toutes les
images transformées. Nous avons donc réuni 171 vraies reproductions de 22 œuvres célèbres sur
Wikimedia Commons (photos de visiteurs, pages de livres, timbres, affiches, écrans,
rephotographies), annotées une à une : chaîne de couches et part de l'image occupée par l'œuvre.
Sur ces images, Claude ne parle presque plus de montage (0 à 10 % selon le support).

Il compte encore les couches (Spearman 0,59 ; 80 % à une couche près). Et le remplacement du sujet
se retrouve (figure 3, `article/figures/fig-reel.png`) : 0 cas sur 25 à zéro ou une couche, 1 sur 44 à deux, 12 sur 46 à trois, 23 sur 34
à quatre et plus. À surface égale, l'effet des couches demeure : pour une œuvre qui occupe entre
15 et 50 % de l'image, 1 cas sur 9 à deux couches ou moins, 11 sur 30 à trois ou plus.

Le réel ajoute une nuance que la synthèse ne montrait pas. Claude *nomme* presque toujours
l'œuvre, mais il la rétrograde : « des visiteurs se pressent dans une salle de musée devant La
Nuit étoilée de Van Gogh » ; « couverture du livre *A Mathematician's Lament*, qui reproduit la
gravure Melencolia I » ; « capture d'écran d'un écran de verrouillage d'iPhone » (la Grande
Vague en fond d'écran). L'œuvre ne disparaît pas : elle passe de sujet à complément de lieu.

Pour les encodeurs, le réel confirme que le cadre en gros plan est inerte (l'image propre de
l'œuvre est parmi les cinq plus proches dans 95 à 100 % des cas) et qu'en salle l'œuvre se perd
(30 à 40 %), ses voisins devenant les photos de salle d'autres œuvres (37 à 50 %). Mais la surface
explique l'essentiel : dans une régression du rang sur le nombre de couches et la surface, la
surface pèse nettement pour les trois modèles, les couches n'ajoutent un effet net que pour
SigLIP. Avec 22 œuvres, l'effet propre des couches sur les encodeurs n'est pas établi.

## 5. Discussion

**Le cadre le plus extérieur décide.** Pour une machine, le seul cadre certain est le bord du
fichier. Un cadre doré *à l'intérieur* de ce bord ne change rien : l'œuvre est retrouvée, son
sujet est nommé, en synthèse comme sur de vraies photos en gros plan. Ce n'est pas une objection à
la théorie du cadre, c'en est une confirmation déplacée : Simmel et Derrida décrivent la limite
qui sépare l'œuvre du monde ; pour le modèle, cette limite est celle de l'image qu'il reçoit, et
tout ce qui est en deçà — cadre, mur, page — est déjà du monde.

**Quand les couches s'accumulent, le support prend la place du sujet.** Ce n'est pas seulement
que l'œuvre devient trop petite : à surface égale, l'œuvre seule sur un fond neutre est décrite
comme une vignette illisible, l'œuvre prise dans des supports est décrite *comme* ces supports. Le
cadre isole, et ce qu'il isole devient ce dont on parle. Les laminations de Goffman deviennent
ici quelque chose qu'on peut compter : Claude compte les couches presque juste, sur la synthèse
comme sur le réel, et c'est précisément lorsqu'il en compte trois ou plus que la hiérarchie
s'inverse.

**Sur le réel, l'œuvre n'est pas perdue mais rétrogradée.** Les descriptions de vraies photos
nomment l'œuvre et la placent en complément de lieu : la Nuit étoilée devient l'endroit devant
lequel des visiteurs se pressent. La reproduction, chez Malraux, rendait toutes les œuvres
comparables en les arrachant à leur lieu ; la photographie de visiteur fait l'inverse, elle rend
l'œuvre à un lieu, et la machine suit la photographie.

**La trame imprègne au lieu d'envelopper.** Elle ne sépare rien, mais à gros grain elle devient
le sujet ; et chaque modèle y réagit par une autre voie (DINOv2 par la texture, CLIP par la
couleur). Les supports agissent donc de deux façons distinctes : par le bord et par la surface.
La première est celle de la théorie du cadre ; la seconde est celle de la reproduction
photomécanique, que Benjamin et Malraux décrivaient sans pouvoir la mesurer.

**Conséquences pratiques.** Les modèles apprennent sur des images du web, pleines de photos de
salles, de livres et d'écrans. Ce qu'ils appellent « peinture » est en partie « chose accrochée
au mur », ce qu'ils appellent « estampe » en partie « page imprimée ». Qui les utilise pour
chercher dans des collections ou des archives de reproductions doit savoir que l'enveloppe la
plus extérieure pèse sur ce qui est retrouvé et sur ce qui est nommé.

## 6. Limites

- **Couches fabriquées.** Nos neuf couches sont des simulations ; Claude les reconnaît comme
  telles. Les conclusions retenues sont celles qui tiennent sur 171 vraies reproductions.
- **Taille et couches liées sur le réel.** Sur les vraies photos, plus il y a de couches, plus
  l'œuvre est petite. Pour Claude, l'effet des couches demeure à surface égale, mais sur de petits
  effectifs ; pour les encodeurs, il n'est pas établi (22 œuvres).
- **Un juge automatique.** Le classement « même / partiel / support / autre » est fait par un
  modèle ; relu à la main sur un échantillon, il est juste, mais « support » range aussi des
  descriptions qui nomment l'œuvre en la plaçant dans un lieu.
- **Couches déjà présentes annotées par le même modèle.** Le nombre « vrai » de couches de l'image
  de musée vient d'une annotation de Claude : la mesure du comptage n'est pas indépendante sur la
  synthèse (elle l'est sur le réel, annoté séparément).
- **Gabarits répétés.** Nos couches synthétiques réutilisent les mêmes décors ; elles se
  regroupent entre elles par fabrication. La mesure « même support parmi les voisins » n'est
  interprétable que sur le réel.
- **Une seule chaîne profonde**, un seul ordre des couches ; d'autres ordres pourraient agir
  autrement.
- **Pas d'humains.** L'enquête qui comparerait des personnes et des machines sur les mêmes images
  est prête (`human_study/`) mais n'a pas été menée.
- **Trois encodeurs de taille moyenne et un modèle vision-langage.** D'autres modèles, plus grands
  ou entraînés autrement, peuvent différer.

## Références

Voir `references.bib` (85 références vérifiées) et `notes/litterature.md`.
