# Journal

## 2026-10-05 — démarrage

Projet lancé à la demande de Marcel : les cadres emboîtés (poupées russes) et ce qu'ils font à
l'interprétation d'une machine. Plan dans `PLAN.md`. Corpus de départ : museums-v0.2 de caypollard
(10 168 peintures, 1 498 estampes, 801 photographies, 253 dessins, 230 sculptures, Iconclass).
Modèles en cache : CLIP ViT-B/32, SigLIP base, DINOv2 base. Boucle autonome lancée.

## 2026-10-05 — E0 et E1

**E0.** Environnement uv (`pyproject.toml`), versions alignées sur caypollard (torch 2.14,
transformers 5.17) pour réutiliser le cache. `src/impressions/encoders.py` : CLIP ViT-B/32, SigLIP
base, DINOv2 base (CLS + moyenne des patchs), tous hors ligne. Il manquait `spiece.model` de SigLIP
(téléchargé, 800 Ko). Test de fumée : 3 images encodées par les 3 modèles, textes encodés par CLIP
et SigLIP.

**E1.** [`data/works.jsonl`](data/works.jsonl) : 300 œuvres, 60 par type (peinture, estampe,
dessin, sculpture, photographie), une par groupe de quasi-doublons, tirage tournant sur les
divisions Iconclass, côté court ≥ 600 px (les images du pool font 960 px de large). Script
[`scripts/select_works.py`](scripts/select_works.py), planche [`figures/E1-works.jpg`](figures/E1-works.jpg).

**Vu sur la planche (important pour la suite).** Les « originaux » ne sont pas des objets nus :
ce sont déjà des photographies de musée, avec leurs propres couches. Un médaillon de marbre est
photographié *dans son cadre doré* (Q116373927) ; les photographies anciennes sont des tirages
collés sur carton, avec marges et inscriptions (Q96181612) ; les estampes et dessins gardent la
feuille, ses bords, ses taches (Q97853420, Q29384600) ; une « photographie » est la couverture
bleue d'un album fermé (Q96181868) ; un retable est montré volets ouverts (Q3999130) ; les
sculptures sont sur fond gris de studio. Conséquence : la couche 0 n'existe pas, il faut
**annoter les couches déjà présentes** dans chaque original (covariable), et mesurer les couches
ajoutées *par rapport à* l'image donnée. C'est aussi un résultat en soi pour l'article : le corpus
de musée est déjà une poupée russe.

Suite : E2, les fonctions de couches, + annotation des couches existantes des 300 œuvres.
