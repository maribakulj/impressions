# Mission pour l'agent Gemini — punctured sky, manche « cadre social » (pilote)

Tu es un second lecteur, indépendant de Claude. Le but : voir si un modèle d'une autre famille
lit les mêmes images de la même façon.

**Ce que tu dois faire**

1. Le dossier `/Users/marcel/impressions/data/social/gemini/img/` contient 100 images (JPEG),
   aux noms opaques. Regarde-les une par une.
2. Pour CHAQUE image, réponds aux DEUX questions de `PROMPTS.md`, comme si tu les découvrais :
   d'abord `subject_only` en ne regardant que l'image, puis `social`. Réponds à `subject_only`
   avant de lire la question `social`, et ne modifie pas ta première réponse ensuite.
3. Écris une ligne JSON par image et par question dans
   `/Users/marcel/impressions/data/social/gemini/readings.jsonl`, au fur et à mesure (ajoute
   les lignes, n'écrase pas le fichier) :
   `{"file": "013a4cb5ee5c.jpg", "which": "subject_only", "model": "<ton nom de modèle exact>", "answer": {...le JSON demandé...}}`
4. Si tu t'arrêtes en route, reprends là où tu en étais (ne refais pas les lignes déjà écrites).

**Règles d'aveugle — importantes**

- Ne lis AUCUN autre fichier du dépôt : pas `map.jsonl`, pas `items.json`, pas les scripts, pas
  les dossiers `data/social/img` ou `data/blind`. Les noms d'images sont opaques exprès.
- Ne cherche rien sur le web. Ne compare pas les images entre elles pour deviner l'expérience :
  chaque image doit être lue seule.
- Ne modifie, ne déplace et ne supprime aucun fichier, sauf `readings.jsonl` que tu crées.
- Pas de commit git.

Quand tu as fini, écris une dernière ligne `{"done": true, "n": <nombre de lignes>}` et dis-le.
