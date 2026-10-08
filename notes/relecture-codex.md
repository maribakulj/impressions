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
| C3 | Les questions « que représente l'image ? » et « quelle œuvre ? » étaient posées dans le même appel : la dissociation peut venir du questionnaire. | **Fait.** Seconde manche, sujet demandé seul : livre et écran restent à 0/30. Mais la question double faisait disparaître l'œuvre de la première réponse (absente 20/30 au livre), la question seule la garde comme complément (30/30) ; au mur, 30 % → 100 %. Écrit en 4.3. Une consigne « documentaire » (décrire la page) n'est pas testée. |
| C4 | « L'œuvre devient un complément » confond omission et subordination. | **Fait.** Trois issues par condition (4.3, figure 1, `results/E10c/round2.json`). |
| C5 | « Identifier le sujet » est jugé contre la lecture de l'original par le même lecteur (*Erminia* lue Minerve). | **Fait** comme limite (§ 6, avec l'exemple). La référence écrite par des humains est prévue dans l'étude humaine. |
| C6 | Intervalles bootstrap dégénérés à 0/30 et 30/30. | **Fait.** Wilson pour les proportions, paires discordantes et McNemar exact pour les contrastes (`blind_round2_analyse.py`). |
| C7 | « Le cadre seul ne fait rien » n'est pas démontré par un plafond. | **Fait.** « Un cadre doré change peu ces mesures », avec la dérive cosinus et la réserve du plafond (4.2). |
| C8 | Le nombre de couches mélange des relations différentes ; les visiteurs ajoutent une couche *et* un autre sujet. | **Fait.** Limite écrite en 4.4 ; sensibilité « personnes visibles » recalculée : l'effet des couches n'est plus établi (+0,89 [−0,15 ; 1,93]), les personnes pèsent (+1,98 [0,51 ; 7,85]). |
| C9 | « À surface égale » sur le réel est un ajustement d'une étude d'observation. | **Fait** (4.4). |
| C10 | Le juge (Opus) et le lecteur (Sonnet) sont de la même famille ; les contrôles « à l'œil » sont faits par un agent. | Déclaré. Validation humaine : voir C13. |
| C11 | Le témoin d'encombrement recentre l'œuvre ; des fonds montrent eux-mêmes des cadres. | **Fait.** `degclut` garde exactement les pixels, la place et la perspective du livre. Planche des 30 fonds regardée : 3 montrent un motif d'encadrement (médaillon de Washington, vitrail, arcade d'une miniature) ; sans eux, 0/27, le résultat ne change pas. |
| C12 | Reproductibilité : Makefile, caches sans empreintes, « premier rang 99–100 % ». | **Fait** pour le Makefile (`make analyses figures`, sans appel aux modèles). Empreintes : limite déclarée. « Premier rang » : la phrase dit « dans les dix premiers ». |
| C13 | L'étude humaine teste une hypothèse abandonnée. | **Fait.** Refaite (`human_study/PROTOCOLE.md`, `scripts/e7_build_study.py`) : 72 images de la seconde manche, carré latin à 6 conditions, question du sujet seule d'abord, référence écrite par des humains, validation du juge, marge fixée d'avance. Passation : **pour Marcel**. |
| C14 | Encodeurs et modèle descriptif ne font pas la même tâche. | **Fait** (limite, § 6). |

## Cadre théorique et originalité

| # | Constat | Statut |
|---|---|---|
| T1 | Schapiro, Genette, Derrida réunis sous une « théorie qui isole » ; le *parergon* n'est pas une faculté. | **Fait.** Titre changé ; § 1 et § 5 distinguent les fonctions ; la discussion dit que ce n'est pas une réponse à Derrida. |
| T2 | Ne pas dire que les littératures ne se sont jamais rencontrées. | **Fait** (§ 2, § 2.4). |
| T3 | Antécédents proches. | **Fait** : vérifiés en ligne et présents dans l'article et `references.bib` (Wang, Larson & Zhao 2026, arXiv 2609.18345 ; Redies & Groß 2013 ; Lang & Ommer 2018, *Arts* 7(4) 64 ; Impett & Offert, *Visual Resources* 38(2), numéro daté 2022, en ligne 2024 ; Caraffa). Doublon de Wang retiré. Chung et al. 2014, 15cILLUSTRATION, Wilkinson et al. 2021 concernent la piste doctorale, pas l'article. |

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
