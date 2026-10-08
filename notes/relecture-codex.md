# Revue de Codex (06/10/2026) — ce qui en est fait

Codex a relu le projet le 06/10 (snapshots `af1c9bc` puis `552400d`). Ses rapports sont gardés tels
quels dans [`notes/codex/`](codex/) : revue principale, audit empirique, critères de Cambridge,
contribution en humanités numériques. Codex n'a modifié aucun fichier du dépôt. Codex n'ayant
plus de crédits, je reprends seul ses constats le 08/10. Chaque point a un statut :
**fait** (avec la preuve), **à faire**, ou **pour Marcel** (décision qui ne m'appartient pas).

## Défauts d'expérience

| # | Constat de Codex | Statut |
|---|---|---|
| C1 | Le témoin « livre sans texte » de la seconde manche ne garde pas la géométrie du livre : sans texte, `book_page`/`book_photo` sautaient des tirages au hasard, la perspective changeait (IoU des masques 0,77–0,89). | **Fait.** `layers.py` tire maintenant les mêmes nombres avec ou sans texte (le livre avec texte est identique à l'octet près). Condition refaite sous la clé `book_notext2` : IoU = 1,0000 sur les 30 œuvres. Lectures et jugements refaits (`scripts/blind_round2_notext.py`, jugements dans un cache séparé `blind2b_judged.jsonl`). |
| C2 | DINOv2 recadre encore après la mise au carré (`do_center_crop`, 256 → 224 : 12,5 % perdu). | Déclaré en limite (§ 6). **À faire** : mesurer sur un sous-ensemble ce que change l'encodage sans recadrage. |
| C3 | Les questions « que représente l'image ? » et « quelle œuvre ? » étaient posées dans le même appel : la dissociation peut venir du questionnaire. | **Fait** en partie par la seconde manche (sujet demandé seul) : le résultat livre/écran tient (0/30). La sensibilité à la consigne est déclarée (mur : 30 % → 97 %). Une consigne « documentaire » (décrire la page) reste **à faire** si on garde la thèse. |
| C4 | « L'œuvre devient un complément » confond omission et subordination : au livre et à l'écran, le sujet est *absent* dans 20 cas sur 30, complément dans 10. | **À faire** dans l'article : donner les trois issues (principal / complément / absent) pour chaque condition. |
| C5 | « Identifier le sujet » est jugé contre la description de l'original par le même lecteur : deux versions peuvent partager la même erreur (Q27982670, *Erminia* lue comme Minerve). | Le vocabulaire a été corrigé (« concordance avec la lecture de l'original »). **À faire** : l'écrire comme limite avec cet exemple ; la référence humaine relève de l'étude humaine. |
| C6 | Intervalles bootstrap dégénérés à 0/30 et 30/30. | **À faire** : intervalles de Wilson pour les proportions. |
| C7 | « Le cadre seul ne fait rien » n'est pas démontré par un plafond ; il faudrait une marge d'équivalence. | **À faire** : formulation bornée aux mesures (dérive cosinus ≈ 0,09–0,10, rang inchangé). |
| C8 | Le nombre de couches mélange des relations différentes (reproduction, occlusion, voisinage, foule). Les visiteurs ajoutent une couche *et* un autre sujet. | **À faire** : limite explicite + sensibilité avec indicatrice « personnes » (Codex : coefficient 1,01). |
| C9 | « À surface égale » / « à type de support égal » sur le réel : c'est un ajustement statistique d'une étude observationnelle ; le modèle n'a que l'indicatrice salle. | **À faire** : reformuler. |
| C10 | Le juge (Opus) et le lecteur (Sonnet) sont de la même famille ; les contrôles « à l'œil » sont faits par un agent. | Déclaré. Validation humaine : voir C13. |
| C11 | Le témoin d'encombrement recentre l'œuvre propre sur un autre tableau ; des fonds montrent eux-mêmes des cadres. | **Fait** par la seconde manche : `degclut` garde exactement les pixels, la place et la perspective du livre. Fonds avec cadres : **à vérifier** à l'œil. |
| C12 | Reproductibilité : le Makefile ne refait pas les analyses E10 ; les caches n'ont pas d'empreintes ; « premier rang 99–100 % » ne correspond pas aux JSON (top-10). | **À faire** : Makefile, phrase corrigée après la mesure E4 v2. Empreintes : limite déclarée. |
| C13 | L'étude humaine préparée teste une hypothèse abandonnée (six couches, ancien juge). | **À faire** : refaire `human_study/PROTOCOLE.md` autour du résultat actuel. Passation par des humains : **pour Marcel**. |
| C14 | Encodeurs et modèle descriptif ne font pas la même tâche (vecteur global contre question dirigée). | **À faire** : le dire en discussion. |

## Cadre théorique et originalité

| # | Constat | Statut |
|---|---|---|
| T1 | Schapiro, Genette et Derrida sont réunis sous une « théorie du cadre qui isole » ; le *parergon* de Derrida n'est pas une faculté qu'un modèle pourrait ne pas avoir. | **À faire** : le titre « La machine n'a pas de parergon » tombe ; fonctions distinctes pour chaque auteur. |
| T2 | Ne pas dire que les deux littératures ne se sont jamais rencontrées ni que la vision tient uniformément le contexte pour un obstacle. | **À faire.** |
| T3 | Antécédents proches à citer : Redies & Groß 2013 (cadres et environnement muséal), Lang & Ommer (contextes d'exposition), Caraffa / PHAROS (photothèques), Impett & Offert 2024, Wang, Larson & Zhao (cadrage de l'entrée des VLM, préprint à vérifier), Chung et al. 2014, 15cILLUSTRATION, Wilkinson et al. 2021. | **À faire** : vérifier chaque référence avant de la citer. |

## Suites proposées par Codex (pour Marcel)

Codex propose de déplacer le projet vers une question doctorale : *à quelles conditions une
reproduction numérique permet-elle de retrouver une image tout en conservant les indices
nécessaires pour s'en servir comme preuve historique ?* Trois terrains, par ordre de préférence :
conventions de reproduction et de numérisation (ex. Witt Library) ; éditions et exemplaires
(Holbein, *Simulachres* 1538/1542) ; conventions de description. Premier pilote proposé : six à
huit feuilles du *Rhinocéros* de Dürer (tirage 1515, réemploi Hondius vers 1620, discordance
croisée de deux notices BnF), avec trois tâches séparées : retrouver le motif, identifier le
document, restituer ce que l'inscription affirme.

C'est un changement de projet, pas une correction : **décision pour Marcel**. Je ne le lance pas.
