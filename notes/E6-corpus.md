# E6 — Corpus réel (Wikimedia Commons)

Fichiers : [`data/real/manifest.jsonl`](../data/real/manifest.jsonl) (171 images gardées),
[`data/real/annotations.jsonl`](../data/real/annotations.jsonl) (annotations faites en regardant
chaque image, y compris les 8 rejets), [`scripts/fetch_real_corpus.py`](../scripts/fetch_real_corpus.py)
(`list`, `search`, `thumbs`, `sheets`, `select`, `fetch`, `manifest`). Les images elles-mêmes
(`data/real/images/`, 46 Mo, largeur 960) ne sont pas versionnées : `fetch` les retélécharge.

## Œuvres (22)

| type | œuvres (images gardées) |
| --- | --- |
| peinture (80) | Joconde 8, Ronde de nuit 8, Jeune Fille à la perle 8, Nuit étoilée 8, Naissance de Vénus 7, Ménines 9, Baiser 7, Époux Arnolfini 8, Cri 8, Liberté guidant le peuple 9 |
| sculpture (43) | Vénus de Milo 9, Victoire de Samothrace 9, David 9, Laocoon 9, Néfertiti 7 |
| estampe (27) | Melencolia I 7, Grande Vague 8, Rhinocéros 6, Chevalier, Mort et Diable 6 |
| dessin (8) | Homme de Vitruve 8 |
| photographie (13) | Migrant Mother 7, Point de vue du Gras 6 |

Chaque œuvre garde au moins une image « clean » de référence (pour les sculptures : une photo de
la statue sur fond neutre, il n'existe pas de référence « sans couche »).

## Supports (couche la plus extérieure)

| support | images | médiane surface de l'œuvre | couches moyennes |
| --- | --- | --- | --- |
| in_situ (salle, foule, vitrine) | 47 | 0,12 | 3,6 |
| clean | 40 | 0,97 | 0,1 |
| book (planche, livre ouvert, couverture) | 21 | 0,60 | 2,6 |
| framed (cadre / passe-partout / verre plein champ) | 20 | 0,70 | 2,4 |
| print_derivative (timbre, affiche, bâche, gravure d'interprétation, objet) | 20 | 0,57 | 2,5 |
| rephoto (tirage ancien, plaque de verre, diapositive, carte postale) | 15 | 0,40 | 2,1 |
| screen (capture d'écran, téléviseur, téléphone) | 4 | 0,21 | 3,0 |
| other (vitrine de souvenirs, collage, négatif, filigrane d'agence) | 4 | 0,69 | 2,2 |

Par type : les peintures sont surtout *in situ* (31/80) ; les sculptures *in situ* (15),
en tirage ancien (9) et en livre (9) ; les estampes surtout « clean » (17/27 : des épreuves
différentes, pas des reproductions).

## Difficultés

- **Débit** : `upload.wikimedia.org` limite les vignettes une par une (429, `Retry-After: 600`).
  `fetch` saute l'image et repasse après 5 min (4 passes). Les 179 fichiers choisis sont arrivés.
- **Rejets (8)** : une « Starry Night » qui est en fait *La Nuit étoilée sur le Rhône* (fichier
  mal nommé sur Commons, remplacée par la version du MoMA), trois détails recadrés (bannières,
  tête du David), une projection immersive de Klimt méconnaissable, un Laocoon redessiné sur un
  timbre soviétique, un Néfertiti invisible derrière un panneau, une bannière web de Vitruve.
- **Peu d'écrans** (4) : Commons contient très peu de captures d'écran ou de photos d'écran
  montrant ces œuvres. C'est la couche la moins représentée, alors que c'est la plus courante en
  pratique.
- **Catégories floues** : une photo de visiteur recadrée au ras d'une estampe est notée
  « clean » avec une couche (`n_layers` 1) ; les gravures d'interprétation du XIXᵉ s. sont
  « print_derivative » (reproduction, pas copie d'artiste) ; les estampes ont plusieurs épreuves
  originales, donc plusieurs « clean ».
- **Œuvres « difficiles »** : la plaque de Niépce est presque illisible en vrai ; la seule image
  lisible est la reproduction retouchée de 1952 (notée « rephoto »). Le Laocoon ancien porte
  l'ancienne restauration (bras tendu). Ces différences sont dans l'objet, pas dans le support.
- 4 images sans auteur dans les métadonnées Commons (champ `author` vide).

## Licences

Toutes sous licence libre : 93 domaine public / CC0 / « No restrictions », 56 CC BY-SA
(2.0 à 4.0, dont 1 GFDL), 22 CC BY. Les images ne sont pas poussées sur le dépôt ;
`manifest.jsonl` garde la page Commons, la licence et l'auteur de chacune pour l'attribution.

## Suite

Refaire sur ce corpus les mesures d'E4 (médium lu, distance à l'original) et d'E5 (comptage des
couches, zéro-coup CLIP/SigLIP, sous-échantillon Claude), en comparant support par support à la
simulation.
