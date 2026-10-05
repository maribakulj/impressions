# impressions — plan de recherche (piloté par une boucle autonome)

Nom : *Nouvelles Impressions d'Afrique* de Roussel, poème à parenthèses emboîtées jusqu'à cinq
niveaux — des poupées russes de cadres. Et « impression » : ce qu'on imprime, ce qu'on perçoit.

## Question

Le cadre (bordure, page, livre, écran, tirage) isole le support et le rend déterminant : il
enveloppe une partie du sens. Quand une œuvre passe de couche en couche (objet → photographie →
page de livre → livre photographié → écran → impression rephotographiée), que devient
l'interprétation qu'en fait une machine ? À quelle couche le support l'emporte-t-il sur l'objet ?

Pour une machine il n'y a jamais d'« objet en lui-même » : la première couche est toujours une
photographie cadrée par un humain. La vision par ordinateur traite le changement de support comme un
bruit (« domain shift », invariance) ; la thèse testée ici est qu'il porte du sens.

## Hypothèses (chacune avec ce qui la réfuterait)

- **H1 — Le cadre est l'interrupteur.** Un cadre *visible* (bordure dorée, marge de page, bord
  d'écran) déplace plus la représentation que le changement de support sans cadre visible.
  Réfutée si, à support égal, ajouter/retirer la bordure visible déplace moins que changer de
  support (photo ↔ gravure ↔ impression) sans bordure.
- **H2 — L'accumulation.** Au-delà d'un nombre k de couches, les voisins d'une image sont
  déterminés par le support (autres pages, autres écrans) plus que par le sujet (même Iconclass).
  Réfutée si la précision « même sujet » ne baisse pas avec k, ou si la précision « même
  support » ne la dépasse jamais.
- **H3 — La machine compte les couches.** Un modèle texte-image (CLIP, SigLIP) et un modèle
  vision-langage (Claude) savent dire combien de couches ils voient et lesquelles. Réfutée si
  le comptage ne fait pas mieux qu'une règle triviale (toujours « une photo »).
- **H4 — Le cadre change le sens, pas seulement le style.** La *description* (ce que le modèle
  dit que l'image représente) change avec les couches, pas seulement sa position dans l'espace
  des représentations. Réfutée si les descriptions du sujet restent stables alors que les
  représentations bougent.
- **H5 (humain vs machine)** — non testable sans participants. La boucle prépare le protocole et
  le paquet (images + questionnaire) mais ne le présente pas comme fait.

## Contrôles obligatoires

- **Régler la question des données d'entraînement** : CLIP et SigLIP ont vu des légendes du type
  « a photo of a painting of… » ; DINOv2 n'a pas de texte. Comparer les trois, et le dire.
- **Simulation ≠ réel.** Les couches fabriquées par programme (H1–H4) doivent être confirmées sur
  des couches réelles : la même œuvre dans de vraies reproductions (Wikimedia Commons : photos de
  visiteurs, vues de salle, livres numérisés ; caypollard : les 5 éditions de la *Danse macabre*
  d'Holbein ; livres d'art numérisés sur Internet Archive / Gallica).
- **Taille de l'image, compression, recadrage** : un effet « cadre » qui n'est qu'un effet de
  réduction de l'œuvre dans l'image doit être séparé (contrôle : même réduction, fond neutre,
  sans cadre).
- **Plancher et hasard** à chaque mesure ; intervalles de confiance par bootstrap sur les œuvres ;
  plusieurs modèles ; ne rien affirmer sur moins de 30 œuvres.
- **Regarder avant de mesurer** : chaque type de couche fabriquée est d'abord montré en planche
  (`figures/`) et inspecté visuellement (lire l'image avec l'outil Read) ; une couche qui ne
  ressemble pas à la chose réelle est refaite avant toute mesure.

## Étapes (cocher au fur et à mesure ; la boucle prend la première non cochée)

- [x] **E0 — Environnement.** `pyproject.toml` (uv) : numpy, pillow, torch, transformers,
      open-clip-torch, scipy, pandas, matplotlib. Modèles déjà en cache HF : CLIP ViT-B/32,
      SigLIP base, DINOv2 base. Test de fumée : encoder 3 images. Lien symbolique ou chemin vers
      le corpus caypollard (`~/caypollard/data/derived/museums-v0.2/manifest.jsonl`, images
      `~/caypollard/data/raw/...`) — lecture seule, ne jamais écrire dans caypollard.
- [x] **E1 — Corpus d'œuvres.** Échantillon stratifié : ≥ 40 œuvres par type (peinture,
      estampe, dessin, sculpture, photographie), sujets Iconclass variés, image ≥ 600 px.
      Galerie de recherche : tout le pool museums-v0.2 (18 405) + emblèmes si utile.
      Écrire `data/works.jsonl`. Regarder une planche de 25 œuvres.
- [x] **E2 — Les couches.** `src/impressions/layers.py` : fonctions composables, déterministes
      (graine) : `crop_tight`, `museum_photo` (œuvre dans un mur, petite perspective),
      `gilt_frame` (cadre doré procédural), `mat_border` (passe-partout), `book_page` (marges,
      légende en vraie typographie, papier), `book_photo` (page en perspective sur une table,
      ombre, courbure), `screen` (bord d'écran, reflet, moiré), `screenshot_ui` (fenêtre de
      navigateur), `halftone_print` (trame), `rephotograph` (perspective, flou, balance des
      blancs). Plus les contrôles : `shrink_neutral` (même réduction, fond gris, sans cadre).
      Planche de chaque couche sur 5 œuvres, regardée et jugée. Tests unitaires.
- [x] **E3 — Pilote regardé.** Ajouter d'abord l'annotation des couches déjà présentes
      dans chaque original (cadre, carton, feuille, fond de studio, reliure) — covariable d'E4. 3 œuvres × toutes les chaînes de couches ; pour chaque image :
      plus proches voisins dans la galerie (3 modèles) et description par Claude
      (`claude -p --model sonnet`). Planche HTML ou PNG. Écrire `notes/E3-pilote.md` : ce que
      l'on voit, ce qui surprend, ce qu'il faut corriger avant de mesurer.
- [ ] **E4 — H1 et H2 (mesures).** Chaînes de k = 0…6 couches, ≥ 200 œuvres. Mesures :
      déplacement cosinus par rapport à l'original ; précision@10 « même sujet » (Iconclass, à
      niveau 2-3) et « même type d'objet » ; un indice « support » = les voisins sont-ils des
      images transformées de même couche (ajouter à la galerie les versions transformées d'autres
      œuvres). Bootstrap. Résultats `results/E4/`, figures, `notes/E4.md`.
- [ ] **E5 — H3 et H4.** Comptage de couches : CLIP/SigLIP en zéro-coup (prompts « a photo of a
      book page showing a painting of … », etc.) ; Claude en lecture d'image sur un sous-
      échantillon (≤ 300 appels, `claude -p`, abonnement). Stabilité des descriptions du sujet
      (comparer la description de l'original à celles des couches : recouvrement des entités
      nommées, jugement par un second appel). `notes/E5.md`.
- [ ] **E6 — Réel.** Corpus de couches réelles : ≥ 15 œuvres célèbres avec ≥ 5 reproductions
      réelles chacune (Wikimedia Commons, catégories des œuvres ; ≥ 2 s entre requêtes,
      `Special:FilePath`), les éditions d'Holbein de caypollard, et si possible des pages de
      livres d'art numérisés. Annoter à la main (par lecture d'image) la chaîne de couches de
      chaque reproduction. Refaire les mesures d'E4/E5 sur ce réel. Dire où la simulation se
      trompe.
- [x] **E7 — H5 préparé.** Paquet pour une petite enquête humaine (≤ 40 images, questions :
      « que représente l'image ? », « combien de couches ? ») + protocole d'analyse. Non exécuté.
- [x] **E8 — Revue de littérature vérifiée.** Chaque référence ouverte en ligne (page
      d'éditeur, DOI, catalogue) : Goffman *Frame Analysis* (laminations), Bateson 1955,
      Bolter & Grusin *Remediation*, Genette *Seuils*, Wölfflin sur la photographie de sculpture,
      Malraux, Benjamin, Latour & Lowe « Migration of the Aura », Steyerl « Poor Image »,
      Schapiro, Derrida, Marin, Stoichita, Simmel ; côté machine : PACS, DomainNet,
      ImageNet-R/Sketch, Torralba & Efros 2011, attaques typographiques (Goh et al. 2021),
      Offert & Bell, Kamath et al. 2023 ; et chercher qui a déjà étudié des reproductions
      d'œuvres vues par la machine (recapture, « photo of a photo », art-history photo
      archives). `notes/litterature.md` + `references.bib`.
- [ ] **E9 — Article.** `article/article.md` en français (~8 000 mots) : question, état de
      l'art, protocole, résultats (avec figures et IC), ce qui est réfuté, limites, conclusion.
      Chaque chiffre renvoie à un fichier de `results/`. `make all` reproduit tout.
- [ ] **E10 — Relecture adverse.** Un sous-agent neuf relit l'article et le code comme un
      relecteur de revue hostile ; corriger ce qu'il trouve ; consigner dans `notes/relecture.md`.
- [ ] **E11 — Publication.** Publier l'article comme document (Claude Docs) ; mettre à jour le
      document « Arranger les images… » (lien en fin) ; résumé final dans `JOURNAL.md`.
      Arrêter la boucle.

## Règles de la boucle

1. À chaque réveil : lire `PLAN.md` et la fin de `JOURNAL.md`, prendre la première étape non
   cochée (ou continuer celle en cours), avancer d'un morceau qui se vérifie.
2. **Calculs lourds** (modèles sur > 100 images, Claude en masse) : via `~/outils-seg/lourd.sh
   <commande>` ; jamais plus de 2 calculs lourds sur le Mac (16 Go), long calcul en arrière-plan.
3. Réseau lent (~64 Ko/s) : pas de nouveau gros modèle ; Wikimedia ≥ 2 s entre requêtes ;
   Gallica ≥ 10 s.
4. Regarder les images (outil Read sur les planches) avant chaque mesure nouvelle. Ne jamais
   présenter un échec de construction comme une réfutation de l'idée.
5. Ne pas reprendre une conclusion de caypollard sans la revérifier.
6. Commit à chaque morceau vérifié et push sur `main` du dépôt public
   github.com/maribakulj/impressions (demandé par Marcel le 05/10/2026). Ne jamais écrire dans
   `~/caypollard`. Ne jamais pousser d'image sous droits ni de clé.
7. Journal : une entrée datée par réveil dans `JOURNAL.md` (fait / vu / chiffres / suite), en
   français simple, avec des chemins de fichiers cliquables.
8. Une étape bloquée (accès, droits, besoin humain) : le noter, passer à la suivante, ne pas
   tourner en rond. Si tout est bloqué : arrêter la boucle et l'écrire.
