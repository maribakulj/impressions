# Poupées russes : ce que les cadres emboîtés font à la lecture d'une image par la machine

*Brouillon — projet `impressions`, octobre 2026. Les chiffres renvoient aux fichiers de
`results/` ; les sections marquées [À ÉCRIRE] attendent la fin des calculs.*

## Résumé

[À ÉCRIRE quand les résultats seront fixés.]

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

[Condenser `notes/litterature.md` en ~1 500 mots, en quatre paragraphes :]

**Le cadre.** Simmel (1902) : le cadre ferme l'œuvre et la sépare du monde. Ortega y Gasset (1921) :
le cadre comme isolant entre réel et fiction. Schapiro (1969) : le champ lisse et la bordure sont
des signes, apparus tard dans l'histoire. Derrida (1978) : le parergon, ni dedans ni dehors. Marin
(1982, 1988) et Stoichita (1993) : les figures du cadre et la métapeinture.

**L'emboîtement.** Goffman (1974) décrit des « laminations » : un cadre d'expérience peut être
transformé, puis transformé encore, et chaque transformation ajoute une couche que l'on peut
compter. Bateson (1955/1956) : le cadre comme message sur le message. Genette (1987) : le paratexte,
cadre du livre. Bolter et Grusin (1999) : chaque média en remédie un autre, entre transparence
(immédiateté) et exhibition du médium (hypermédiateté).

**La reproduction.** Wölfflin sur la manière de photographier la sculpture ; Benjamin sur l'œuvre
à l'époque de sa reproduction ; Malraux et le musée imaginaire, où la photographie unifie les
échelles et les médiums ; Latour et Lowe sur la « migration de l'aura » ; Steyerl sur l'image
pauvre qui se dégrade en circulant.

**La machine.** Le support comme bruit (Torralba et Efros 2011 ; PACS ; DomainNet ; ImageNet-R ;
ImageNet-C). Le support encodé malgré tout : Ramos et al. (ICCV 2025) montrent que CLIP et DINO
gardent la trace du JPEG, du redimensionnement et de l'appareil, et que ces traces peuvent changer
la lecture sémantique — mais ce sont des traces quasi invisibles, pas des supports. Le fond
décide parfois de la classe (Xiao et al., ICLR 2021) ; la texture l'emporte sur la forme (Geirhos
et al., ICLR 2019) ; un mot écrit dans l'image commande CLIP (Goh et al. 2021). Les modèles
vision-langage lisent mal les relations spatiales (Kamath et al., EMNLP 2023).

**Le creux.** À notre connaissance, personne n'a fait passer une même œuvre dans une chaîne
contrôlée de supports emboîtés pour demander ce que l'image *est*.

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

[Tableau d'E3 : couches présentes par type ; peinture 0,72 couche en moyenne, estampe 2,25,
photographie 2,18 ; seules 48/300 sans couche. Le type d'objet est lisible dans les marges.]

### 4.2 Retrouver l'œuvre à travers les couches

[À ÉCRIRE — E4 : rang de l'œuvre par étape et par modèle, contre le témoin de même surface.]

### 4.3 Le support prend la place du sujet

[E5 Claude : à 6 couches, 27/30 descriptions parlent du support ; témoin de même surface 0/30.
E5 zéro-coup : la peinture dans le livre devient « estampe ».]

### 4.4 La trame : envelopper ou imprégner

[À ÉCRIRE — E4b.]

### 4.5 Sur de vraies reproductions

[À ÉCRIRE — E6.]

## 5. Discussion

[À ÉCRIRE. Fil : le cadre *enveloppe* — la machine lit le bord le plus extérieur, et quand les
couches s'accumulent le support remplace le sujet, ce qui n'est pas un effet de taille ; la
trame *imprègne* — elle ne sépare rien mais change le médium lu (si E4b le confirme). Ce que cela
dit de la théorie du cadre ; ce que cela dit des modèles entraînés sur le web, où les images de
livres et d'écrans abondent ; limites (couches synthétiques reconnues comme telles par Claude ;
une seule chaîne profonde ; enquête humaine non menée).]

## 6. Limites

[À ÉCRIRE.]

## Références

Voir `references.bib` (85 références vérifiées) et `notes/litterature.md`.
