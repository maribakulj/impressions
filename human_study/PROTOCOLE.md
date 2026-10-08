# Étude humaine — préparée, non menée (refaite le 08/10/2026)

La première version de ce protocole testait une hypothèse abandonnée : la chaîne à six couches,
où l'œuvre est trop petite pour être vue. La relecture de Codex l'a relevé. Cette version porte
sur le résultat actuel de l'article (section 4.3).

**Question.** Quand une œuvre est petite et décentrée dans une image dont le reste se décrit
lui-même (livre, écran, autre tableau), Claude n'en fait plus le sujet de sa description. Des
personnes font-elles de même ? Si oui, c'est une convention de description partagée, pas un trait
de la machine. Si non, c'est un écart entre humains et machine.

**Matériel.** 72 images = 12 des 30 œuvres de la seconde manche × 6 conditions, exactement les
images que Claude a lues (`data/blind/src2/`) :

| condition | ce que c'est |
|---|---|
| `degr` | les pixels de l'œuvre tels qu'ils sont dans le livre photographié, à la même place, sur du gris |
| `degclut` | les mêmes pixels, à la même place, sur le détail d'un autre tableau |
| `book` | le livre photographié |
| `book_notext2` | le même livre, même géométrie, sans aucun texte |
| `web` | une page web de collection, photographiée sur un écran |
| `wall` | l'œuvre encadrée, accrochée au mur |

`items.csv` dit quelle image est quoi ; les noms de fichiers sont opaques.

**Plan.** 6 listes en carré latin (`lists.json`) : chaque personne voit chaque œuvre une seule fois
(sinon elle la reconnaîtrait sous les couches) et chaque condition deux fois, 12 images en tout,
dans un ordre tiré au hasard. Viser au moins 10 personnes par liste, soit 60 personnes.

**Passation.** Ouvrir `form.html` dans un navigateur (fichier local, aucun serveur, aucune donnée
envoyée) ; choisir la liste ; à la fin un CSV se télécharge.

**Questions.** Pour chaque image, d'abord une seule question, seule à l'écran, comme pour Claude
dans la seconde manche : « Que représente cette image ? ». Une fois la réponse validée, elle ne
peut plus être modifiée, et deux autres questions viennent : « Y a-t-il une œuvre d'art reproduite
dans cette image ? Si oui, que représente-t-elle ? » et « Qu'est-ce que vous regardez,
physiquement ? ».

**Référence.** Avant toute passation, deux personnes écrivent pour chacune des 12 œuvres, à partir
de la notice du musée (pas de la lecture de Claude), ce que représente l'œuvre. Leurs désaccords
sont gardés. C'est la référence du juge, pour les humains comme pour Claude : on évite ainsi que
Claude soit jugé contre sa propre lecture (*Erminia* lue « Minerve » sur l'original comme dans le
livre).

**Analyse prévue** (fixée avant toute donnée) :

- Le juge de l'article (Claude Opus, à l'aveugle, identifiants opaques) classe chaque réponse à la
  première question : le sujet de l'œuvre y est-il le sujet *principal*, un *complément*, ou
  *absent* ? Les réponses humaines et celles de Claude sont mélangées dans les mêmes lots, sans
  indication de leur origine.
- **Validation du juge.** Deux personnes codent à l'aveugle un échantillon de 120 réponses (moitié
  humaines, moitié Claude) avec les mêmes trois catégories ; on publie l'accord entre elles,
  l'accord avec le juge (kappa de Cohen) et la matrice de confusion. Si l'accord avec le juge est
  inférieur à 0,6, l'analyse principale se fait sur le codage humain.
- **Critère principal** : la part de « sujet principal » par condition, chez les humains et chez
  Claude, avec intervalles par rééchantillonnage des personnes et des œuvres. Effet de la condition
  par modèle logistique mixte (personne et œuvre en effets aléatoires).
- **Contraste clé** : `degclut` contre `degr` (même pixels, même place ; seul change ce qui entoure).
  Chez Claude, la différence est de 30 cas sur 30.

**Ce qui départagerait les deux lectures** (marge fixée d'avance : 15 points de pourcentage) :

- Si, chez les humains, la part de « sujet principal » en `degclut` est inférieure de plus de
  15 points à celle de `degr`, l'effet de saillance est partagé : l'article parlera d'une
  convention de description, que la machine reproduit.
- Si la différence humaine est dans ±15 points, alors que celle de Claude est de 100 points,
  c'est un écart propre à la machine.
- Entre les deux, on le dit tel quel.

Ces humains sont des lecteurs contemporains : l'étude compare des pratiques de description
actuelles, elle ne dit rien de la réception historique des reproductions.

**Ce qui n'est pas fait.** Le recrutement et la passation demandent des personnes ; c'est à
Marcel de décider s'il les mène et avec qui.
