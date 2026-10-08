<!-- Rapport de Codex (session 01a11040, 06/10/2026), extrait tel quel du journal de session ; non modifié. -->

## 2026-10-06T08:12:04.404Z

**Il me manque le document de référence de Punctured Sky pour pouvoir en faire une critique fondée.** Je n’ai pas retrouvé le projet dans les fichiers locaux et les sources connectées consultés. Les recherches publiques renvoient principalement au film de Jon Rafman ; je ne peux pas présumer qu’il s’agit de ton projet.

**Indique-moi son emplacement — chemin local, dépôt, lien — ou joins le dossier ici.** Une version de travail suffit, idéalement avec la présentation, la bibliographie, le corpus envisagé et les éventuelles réalisations.

La revue examinera précisément :

- **Les prémisses** : concepts insuffisamment définis, présupposés contestables, contradictions et conclusions posées d’avance.
- **L’originalité** : confrontation aux travaux les plus proches, y compris ceux qui fragilisent la nouveauté revendiquée.
- **La méthode et les preuves** : constitution du corpus, biais, catégories d’analyse, articulation entre calcul et interprétation historique.
- **La contribution disciplinaire** : ce que le projet ferait effectivement comprendre autrement en histoire de l’art, du design ou en humanités numériques.
- **Les évolutions possibles** : plusieurs orientations comparées, avec leurs apports, leurs difficultés et les recherches nécessaires pour les éprouver.
- **La viabilité doctorale** : problématique resserrée, enquête pilote, périmètre soutenable et adéquation scientifique avec Cambridge.

J’ai vérifié un point structurant : Cambridge attend une **contribution significative à la connaissance**, pouvant notamment réviser des interprétations antérieures. Cela fournit un critère concret pour évaluer l’ambition du projet : identifier exactement quelle connaissance nouvelle ses résultats permettraient d’établir. [Critères doctoraux officiels](https://www.cambridgestudents.cam.ac.uk/your-course/postgraduate-research-students/requirements-research-degrees).

## 2026-10-06T08:46:05.632Z

**Mon verdict : Punctured Sky contient une observation intéressante et un dispositif expérimental exploitable, mais l’article actuel tire des conclusions théoriques plus fortes que ses mesures. Pour devenir le point de départ d’un doctorat exigeant, il faut construire une question historique précise autour de ce que les systèmes numériques conservent, transforment ou effacent dans les reproductions.**

J’ai retrouvé le dépôt dans [impressions](/Users/marcel/impressions), examiné l’article, les protocoles, le code, les annotations et les résultats, puis confronté le projet à la littérature. J’ai contre-vérifié les principaux décomptes et la régression initiale, sans relancer l’ensemble des inférences. Je prends aussi en compte les corrections intégrées par l’autre agent jusqu’au commit `552400d` : plusieurs problèmes ont effectivement été corrigés pendant cette revue. *Punctured Sky* est bien traité ici comme un nom de code.

Mon appréciation serait : **révision majeure pour l’ambition scientifique actuelle ; base prometteuse pour une enquête doctorale, à condition de déplacer et de resserrer sa problématique.**

**Ce qui mérite d’être conservé est substantiel.** La fabrication contrôlée de reproductions, les témoins de surface et de dégradation, la confrontation entre images synthétiques et documents réels, ainsi que le journal des hypothèses constituent de bons fondements. Le projet a également abandonné une interprétation séduisante lorsque les données indiquaient simplement une limite de résolution à six couches. C’est une correction scientifique importante.

Le phénomène observé au livre et à l’écran est net. La difficulté principale concerne désormais **ce qu’il signifie**, et la contribution que son explication peut apporter aux disciplines que tu vises.

**1. Le résultat central doit être formulé beaucoup plus précisément.**

Dans E10b, pour les trente œuvres, les jugements du champ de description générale donnent :

| Condition | Sujet de l’œuvre principal | Sujet en complément | Sujet absent |
|---|---:|---:|---:|
| Cadre doré | 30 | 0 | 0 |
| Mur de musée | 9 | 10 | 11 |
| Livre photographié | 0 | 10 | 20 |
| Écran | 0 | 10 | 20 |
| Témoin de même surface, pour le livre | 28 | 0 | 2 |
| Témoin de même dégradation | 27 | 0 | 3 |
| Témoin d’encombrement | 15 | 6 | 9 |

Ces chiffres étayent un déplacement du contenu sélectionné pour la description. Ils ne justifient pas exactement la formule récurrente selon laquelle « l’œuvre devient un complément » : **dans deux tiers des descriptions du livre et de l’écran, son sujet figuré est absent.**

Il faut distinguer trois phénomènes :

- le sujet figuré reste mentionné ;
- lorsqu’il est mentionné, il devient secondaire ;
- il peut être récupéré après une question dirigée.

Cette distinction change la portée de l’article. Une omission, une subordination grammaticale et une difficulté perceptive ne sont pas interchangeables.

Surtout, décrire une photographie de livre comme « un livre ouvert » peut être une réponse parfaitement adéquate. Le terme **« rétrogradation » suppose déjà que l’œuvre intérieure devrait avoir la priorité**. Cette norme doit devenir une question de recherche : priorité pour un historien de la peinture, un historien du livre, un conservateur de photographies, ou un chercheur étudiant les dispositifs d’exposition ?

Pour l’histoire du design, cette difficulté est centrale. Traiter la page, sa composition et ses inscriptions comme ce qui détourne de l’objet important reconduit précisément la hiérarchie que le projet pourrait interroger.

**2. L’« identification du sujet » reste insuffisamment validée, même après la correction du vocabulaire.**

Le remplacement récent de « reconnaître l’œuvre » par « identifier le sujet de l’œuvre » améliore l’article. Mais le jugement compare essentiellement les réponses à une description de référence produite par le même lecteur, sans référence iconographique indépendante.

Un cas concret le montre : Q27982670 correspond à *Erminia parmi les bergers* de Paolo de’ Matteis. Le modèle propose Minerve/Athéna, aussi bien pour l’original que pour la reproduction dans le livre ; cette dernière entre néanmoins dans les réponses validées. Les motifs peuvent être correctement décrits alors que l’identification iconographique est erronée. Voir [la notice du corpus](/Users/marcel/impressions/data/works.jsonl:6) et [les réponses enregistrées](/Users/marcel/impressions/data/annotations/blind_readings.jsonl:1).

La mesure actuelle renseigne donc surtout une **concordance descriptive entre versions**, avec une certaine tolérance aux erreurs d’identification.

Je séparerais explicitement :

| Objet de la mesure | Exemple |
|---|---|
| Identité de l’œuvre | Retrouver la bonne notice de catalogue |
| Identité iconographique | Erminia plutôt que Minerve |
| Description des motifs | Une guerrière devant un berger |
| Mention dans la réponse | Le sujet figuré est-il évoqué ? |
| Relation documentaire | Le livre reproduit une peinture |
| Pertinence pour la tâche | La réponse aide-t-elle à résoudre la question posée ? |

Il faut une validation humaine documentée, comprenant des cas négatifs difficiles : même iconographie mais autre œuvre, attribution incorrecte, motifs génériques, plusieurs œuvres visibles. Un second modèle d’une autre famille serait utile comme contrôle supplémentaire ; il ne remplacerait pas ce travail de référence.

**3. Le questionnaire peut produire une partie de la dissociation observée.**

Dans [le protocole E10b](/Users/marcel/impressions/src/punctured_sky/blind.py:25), la description générale et la description de l’œuvre sont deux champs du **même appel**. Le modèle peut distribuer l’information entre eux : la scène générale dans `subject`, la peinture dans `artwork`.

On ne peut donc pas encore inférer deux comportements indépendants, l’un perceptif et l’autre descriptif. La contrainte « en une phrase » favorise également la sélection d’un seul niveau de description.

L’autre agent a commencé à traiter ce problème avec `subject_only` dans [la nouvelle expérience](/Users/marcel/impressions/scripts/blind_round2.py). C’est une bonne évolution, mais ses résultats n’étaient pas encore disponibles au moment de ma vérification.

Le test décisif doit comparer, dans des appels indépendants :

- une description générale seule ;
- une demande d’identification de l’œuvre seule ;
- le questionnaire combiné actuel ;
- une demande explicitement documentaire : décrire la page, la photographie ou l’accrochage.

Si la différence dépend fortement de la consigne, cela peut produire un résultat intéressant sur **les conventions de description**. Cela affaiblirait en revanche l’interprétation actuelle d’un rapport général de « la machine » au support.

**4. L’expérience n’isole pas encore un effet propre de la « contenance ».**

Le livre diffère du témoin d’encombrement par plusieurs propriétés simultanées : position de l’œuvre, perspective, dégradation, cohérence de la scène, objet reconnaissable, titre et légende. Le texte *Histoire de l’art* constitue lui-même un signal documentaire.

Les témoins séparés de surface et de dégradation montrent que chacune de ces explications, prise isolément, est insuffisante. Ils ne neutralisent pas toutes leurs interactions.

Les nouveaux témoins — livre sans texte, mêmes pixels dégradés replacés dans un contexte encombré — vont dans la bonne direction. Il restera à varier les mises en page et les décors : trente œuvres dans un même gabarit ne constituent pas trente validations indépendantes d’une propriété générale du livre.

Je distinguerais quatre explications concurrentes :

1. **Disponibilité perceptive** : taille, résolution, dégradation.
2. **Organisation de la scène** : position, saillance, objets concurrents.
3. **Pragmatique de la consigne** : ce que la tâche invite à décrire.
4. **Convention documentaire** : ce qu’une légende, une mise en page ou une présentation institutionnelle fait comprendre de l’image.

La contribution la plus intéressante serait de montrer **ce que la quatrième explication ajoute après examen des trois premières**.

**5. Le « nombre de couches » est actuellement une variable trop hétérogène.**

Dans [le manifeste réel](/Users/marcel/impressions/data/real/manifest.jsonl:3), les couches peuvent inclure une photographie, une foule, un mur, une vitre, un cadre ou une page. Ailleurs interviennent inscriptions, éléments de paysage ou piédestaux.

Ces éléments correspondent à des relations différentes : reproduction, occlusion, voisinage, délimitation, inscription, exposition. Les additionner suppose une commensurabilité qui reste à démontrer.

Le problème affecte directement l’analyse : ajouter des visiteurs augmente parfois le nombre de couches **et** rend plus probable une description centrée sur les visiteurs. La variable explicative incorpore alors une partie de l’explication concurrente du résultat.

Je conserverais l’intuition de l’emboîtement, mais avec des relations explicites :

> reproduit — porte — encadre — légende — occulte — jouxte.

Il faut aussi séparer **l’emboîtement visible** et **la généalogie documentée des reproductions**. Une numérisation recadrée peut ne montrer aucune couche tout en résultant de plusieurs opérations de reproduction.

Cette formalisation serait utile, mais sa seule existence ne constituerait pas une nouveauté scientifique : VRA Core distingue déjà œuvres, images et collections. L’apport devrait porter sur les relations nécessaires à une enquête précise et sur les conséquences de leur conservation ou de leur effacement. [Documentation officielle VRA Core](https://www.loc.gov/standards/vracore/VRA_Core4_Intro.pdf)

**6. Les résultats réels soutiennent une association, avec une portée plus limitée que la thèse générale.**

La dernière correction exclut les images de référence « propres » : l’analyse porte désormais sur 131 reproductions. Le coefficient associé aux couches est d’environ **+1,03**, avec un intervalle de **[0,14 ; 2,04]**. Sans les photographies de salle, sur 84 images, il passe à **+0,82**, avec un intervalle de **[−0,07 ; 1,80]**.

Cela ne démontre pas que l’effet disparaît hors des salles. Cela indique que son estimation devient trop incertaine pour soutenir la même conclusion.

Plusieurs limites demeurent :

- les 131 images concernent seulement 22 œuvres célèbres ;
- la surface occupée par l’œuvre est estimée, avec une erreur possible ;
- les supports et les nombres de couches sont inégalement distribués ;
- un bootstrap par œuvre traite une dépendance statistique, mais ne contrôle pas automatiquement les différences propres aux œuvres.

L’expression « à surface égale » devrait être explicitée comme un **ajustement statistique**, et non comme une comparaison expérimentale parfaitement appariée.

Par ailleurs, le corpus initial de 300 œuvres est très dominé par le Met — environ 81 %. Cela n’empêche pas une étude valide, mais appelle une délimitation précise. Il renseigne d’abord certaines conventions de collections numériques, pas « les images d’art » en général.

**7. Une confusion sur l’identité des objets révèle probablement la meilleure piste doctorale.**

Le corpus regroupe sous le même identifiant *Rhinocéros* une première édition de Dürer et une septième édition de 1620, accompagnée d’un autre dispositif textuel. Il rassemble également différentes épreuves du *Chevalier, la Mort et le Diable*. Ces différences sont déjà visibles dans [les notices du manifeste](/Users/marcel/impressions/data/real/manifest.jsonl:140).

Pour l’expérience actuelle, cela fragilise l’idée de « la même œuvre, dont seul le support change ».

Pour une recherche historique, c’est beaucoup plus intéressant : **un système peut retrouver correctement le motif tout en confondant des éditions, des états ou des exemplaires que l’historien doit distinguer.**

Il faut donc distinguer :

> motif ou composition → matrice et état → édition → épreuve physique → document photographique → fichier numérique.

La distinction exacte dépendra du terrain. Mais ici, la différence matérielle n’est plus un bruit résiduel : elle peut constituer l’objet même de la recherche.

C’est aussi une manière de donner au design un rôle véritable : légendes, composition de la page, séquence, échelle et voisinages contribuent à requalifier une image transmise.

**8. L’argument théorique doit être reconstruit autour de fonctions distinctes.**

L’article tend à réunir plusieurs auteurs sous une « théorie du cadre » supposant que celui-ci isole l’œuvre. Cette unification est trop forte.

Chez **Schapiro**, les fonctions des limites, inscriptions et véhicules matériels sont déjà variables et historiques. Son texte ne permet pas de réduire tous les cadres à une fonction isolante. Chez **Genette**, le paratexte engage notamment l’émetteur, le destinataire et l’autorité du message ; il ne se réduit pas à une couche supplémentaire. Chez **Derrida**, le parergon problématise la distinction entre l’œuvre et son extérieur : ce n’est pas une faculté perceptive dont un modèle pourrait simplement être dépourvu. [Schapiro, texte primaire](https://aisviavs.wordpress.com/wp-content/uploads/2024/09/schapiro-english.pdf), [Genette, extrait éditorial](https://assets.cambridge.org/97805214/24066/excerpt/9780521424066_excerpt.pdf), [Derrida, « Passe-Partout »](https://press.uchicago.edu/dam/ucp/books/pdf/course_intro/978-0-226-50462-9_course_intro.pdf)

Je leur donnerais des fonctions différentes :

- Schapiro : historiciser les opérations visuelles.
- Genette : analyser les fonctions éditoriales et documentaires.
- Derrida : interroger les frontières que le protocole construit lui-même.

La stabilité d’un classement après ajout d’un cadre doré ne réfute aucune de ces propositions. Elle renseigne une transformation visuelle particulière, évaluée par une tâche particulière.

La formule « le cadre seul ne fait rien » devrait donc être remplacée par une conclusion bornée aux mesures. Un résultat proche du plafond exige aussi de définir quel changement serait scientifiquement significatif avant de conclure à une absence d’effet.

**La littérature oblige également à reformuler l’adversaire et l’originalité.**

La recherche en vision peut chercher l’invariance au support pour une tâche donnée sans soutenir que le support est dépourvu de sens. L’article confond parfois cet objectif technique avec une position générale sur les images.

Plusieurs travaux sont particulièrement importants pour préciser la place du projet :

| Travail | Conséquence pour Punctured Sky |
|---|---|
| Redies et Groß, *Frames as visual links between paintings and museum environment* | Les relations entre peinture, cadre et environnement muséal ont déjà fait l’objet d’une étude visuelle multiscalaire. |
| Lang et Ommer, *Reconstructing Histories* | La vision computationnelle a déjà été employée pour étudier les contextes d’exposition, et non simplement les éliminer. |
| Caraffa, *Objects of Value*, et PHAROS | Le statut historique et matériel des photographies documentaires est déjà un problème central des photothèques. |
| Impett et Offert, *There Is a Digital Art History* | Une critique des conditions computationnelles de l’histoire de l’art existe déjà ; il faut lui apporter un mécanisme et un cas précis. |
| Wang, Larson et Zhao, *Visual Input and Its Framing…* | Un préprint récent étudie l’effet du cadrage de l’entrée sur des descriptions par modèles visuels ; l’effet général de contexte ne suffit donc pas à établir l’originalité. |

Sources : [Redies et Groß](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2013.00831/full), [Lang et Ommer](https://ommer-lab.com/research/computer-vision-in-the-digital-humanities/object-detection/reconstructing-histories/), [Caraffa](https://www.mprl-series.mpg.de/studies/12/2/index.html), [PHAROS](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/AC7D9F996BDA0526AF7EF4072A16C364/S0307472219000348a.pdf/pharos-a-digital-research-space-for-photo-archives.pdf), [Impett et Offert](https://doi.org/10.1080/01973762.2024.2362466), [Wang et ses collègues](https://arxiv.org/abs/2609.18345).

Ces travaux n’épuisent pas la question. Ils indiquent où chercher une contribution défendable : **les effets spécifiques de conventions documentaires sur les distinctions historiques que les instruments permettent de retrouver**.

Je retirerais les formulations selon lesquelles deux littératures ne se seraient jamais rencontrées, ou selon lesquelles les chercheurs en vision considéreraient uniformément le contexte comme un obstacle. Elles rendent l’article vulnérable sans renforcer son résultat.

**Quelques problèmes techniques et de validation restent importants, avec une priorité inférieure à cette reconstruction conceptuelle.**

| Point | Action nécessaire |
|---|---|
| DINOv2 recadre encore après mise au carré | Vérifier et enregistrer les entrées effectivement vues ; comparer le prétraitement natif à une condition conservant tout le champ. La limite est maintenant déclarée, mais pas résolue expérimentalement. |
| Proportions de 0/30 ou 30/30 | Éviter les intervalles bootstrap dégénérés donnant une certitude artificielle. |
| Comparaison encodeurs / modèle descriptif | Aligner davantage les tâches : recherche globale ou régionale, identification exacte ou description générique. |
| Référence, annotation et jugement issus principalement de Claude | Ajouter un codage humain aveugle avec cas difficiles et analyse des désaccords. |
| Caches et versions successives | Figer les empreintes des images, consignes, modèles et paramètres ; séparer acquisition et reproduction des analyses. |
| Exploration répétée du même corpus | Réserver des œuvres et des mises en page inédites à une validation finale, après fixation des hypothèses. |

Le protocole humain demande une révision plus profonde. Il repose encore sur l’ancienne classification, une référence descriptive de Claude et une comparaison à six couches, alors que cette profondeur est désormais interprétée comme une limite de résolution. [Protocole actuel](/Users/marcel/impressions/human_study/PROTOCOLE.md:23)

Le principe du carré latin, qui évite de montrer plusieurs versions d’une même œuvre à une personne, mérite d’être conservé. Mais il faut reconstruire les tâches autour d’images lisibles et des nouvelles hypothèses. Une étude sur des humains contemporains permettra de comparer des pratiques descriptives actuelles ; elle ne permettra pas, à elle seule, de reconstituer une réception historique.

**La direction doctorale que je recommanderais est la suivante : étudier comment les conventions de reproduction deviennent des conditions d’accès au savoir.**

Une formulation possible :

> **Comment les choix de cadrage, de mise en page et de description définissent-ils l’identité des images dans une collection, et quelles distinctions historiques leur reprise par les systèmes de recherche visuelle conserve-t-elle ou efface-t-elle ?**

L’hypothèse à éprouver serait :

> Les opérations qui rendent une image plus facilement reconnaissable comme occurrence d’un motif peuvent simultanément rendre moins accessibles les différences d’édition, d’exemplaire, de présentation ou de provenance nécessaires à certaines enquêtes historiques.

Cette proposition reste à démontrer. Elle offre toutefois trois contributions articulées :

- **Historique** : expliquer, à partir de sources, pourquoi certaines présentations ont été produites.
- **Empirique** : déterminer leurs effets sur des tâches de recherche et de description.
- **Méthodologique** : montrer comment conserver les distinctions utiles, puis évaluer ce que cela change pour une question historique réelle.

Le troisième point est essentiel. Un meilleur score de classement ne suffit pas : il faudrait montrer, par exemple, qu’une méthode permet de distinguer des éditions auparavant amalgamées, de retrouver une circulation documentaire ou de corriger une interprétation fondée sur des reproductions mal identifiées.

Je vois trois trajectoires crédibles, avec un ordre de préférence.

| Trajectoire | Terrain raisonnable | Contribution possible | Condition de réussite |
|---|---|---|---|
| **Conventions de reproduction et numérisation** | Une collection principale, deux campagnes ou états documentés de présentation | Histoire de la constitution de l’image documentaire et de ses conséquences numériques | Accès aux consignes, versions datées et décisions institutionnelles |
| **Images, éditions et exemplaires** | Une série gravée, trois à cinq éditions liées historiquement | Histoire éditoriale articulée à une recherche visuelle respectant les variantes | Bibliographie matérielle et relations de transmission établies |
| **Conventions de description** | Un ensemble circonscrit de documents, plusieurs tâches et publics | Analyse de la sélection du niveau descriptif | Enquête documentaire suffisante pour dépasser l’évaluation de modèles |

**La première constitue le meilleur prolongement du projet actuel à travers les trois disciplines.** Un pilote pourrait examiner vingt à trente objets possédant plusieurs présentations attestées, puis reconstituer cinq biographies documentaires approfondies. Ces nombres servent à définir un travail préparatoire, pas à garantir une puissance statistique.

Les sources devraient inclure des photographies datées, anciens catalogues, consignes de reproduction, dossiers de numérisation, éventuellement maquettes et échanges de travail. Le choix du terrain doit dépendre de leur disponibilité. La commodité d’une API ne suffit pas à sélectionner un terrain doctoral.

**La deuxième serait particulièrement forte en histoire de l’art et du design.** Le *Rhinocéros* fournit déjà une alerte concrète ; le projet évoque aussi des éditions d’Holbein, dont il faudrait établir précisément les relations. Une seule série bien documentée serait préférable à une collection d’exemples traversant cinq siècles sans continuité démontrée.

**La troisième peut devenir le prochain article.** Elle permettrait de stabiliser la méthode avant de lui demander de soutenir une histoire plus ambitieuse.

**Pour avancer, je ferais un trimestre de préparation structuré autour de décisions vérifiables.**

1. **Semaines 1–2 : fixer les objets et les mesures.**  
   Distinguer motif, œuvre, exemplaire et reproduction ; corriger les références ; séparer mention, identification et rôle descriptif. Stabiliser une version de l’expérience.

2. **Semaines 3–5 : établir un pilote historique.**  
   Choisir un terrain accessible, documenter quelques transformations précises et identifier une question dont la réponse dépend effectivement des marges, légendes, montages ou variantes.

3. **Semaines 6–8 : conduire l’expérience décisive.**  
   Croiser consignes indépendantes, présence des inscriptions et contextes à pixels comparables. Employer plusieurs gabarits et des œuvres réservées. Valider humainement les critères.

4. **Semaines 9–10 : tester une conséquence pour la recherche.**  
   Comparer recherche globale, recherche sur régions et description des relations entre objets. Évaluer séparément la récupération du motif et celle de l’édition ou de l’exemplaire.

5. **Semaines 11–12 : écrire l’article et la proposition doctorale à partir de ce qui tient.**  
   Si l’effet dépend surtout du questionnaire, l’article portera sur les conventions de description. Si une propriété documentaire subsiste après contrôle, il pourra avancer une explication plus substantielle. La proposition historique devra rester intéressante même si un modèle particulier change.

Ce programme évite que le doctorat dépende de la survie d’un résultat obtenu sur une version de Claude.

**Pour Cambridge, la question décisive sera la nature de la contribution, puis la possibilité réelle de l’encadrer.**

Les critères officiels insistent sur une contribution originale à la connaissance et une maîtrise des méthodes. Une démonstration sur un corpus circonscrit, capable de modifier une interprétation ou une pratique de recherche, répond mieux à cette exigence qu’une généralisation sur « les machines et le cadre » insuffisamment étayée. [Exigences officielles des diplômes de recherche](https://www.cambridgestudents.cam.ac.uk/your-course/postgraduate-research-students/requirements-research-degrees)

Le choix de rattachement doit suivre l’argument principal :

- **Digital Humanities** si la thèse porte d’abord sur les conditions numériques de constitution et d’accès aux connaissances visuelles.
- **History of Art** si une démonstration historique sur des objets, acteurs et pratiques organise l’ensemble.

Les deux voies existent, mais elles appellent des propositions différentes. [PhD in Digital Humanities](https://www.postgraduate.study.cam.ac.uk/courses/directory/elelpddgh), [PhD in History of Art](https://www.postgraduate.study.cam.ac.uk/courses/directory/ahhapdhoa)

Leonardo Impett constitue une proximité intellectuelle évidente. **Sa page actualisée indique cependant un congé jusqu’en 2030 et une disponibilité limitée pour de nouveaux doctorants** : il ne faut donc pas bâtir le projet sur l’hypothèse de son encadrement. Caroline Bassett présente une proximité avec les questions d’épistémologie numérique et de cultures de connaissance ; l’environnement ArCH de Cambridge University Library est également pertinent pour une enquête sur les collections. Cela indique des affinités, sans garantir de direction ni de collaboration. [Impett](https://intranet.english.cam.ac.uk/people/Leonardo.Impett), [Bassett](https://www.english.cam.ac.uk/people/Caroline.Bassett/), [ArCH](https://www.ai.cam.ac.uk/blog/from-fragments-to-findings-how-ai-is-transforming-access-to-collections/)

**Ma priorité serait maintenant de choisir une distinction historique que le système actuel efface et d’en établir les conséquences sur un petit corpus documenté.** Le mélange entre motif, édition et exemplaire offre déjà un point de départ concret. C’est à cet endroit que Punctured Sky peut devenir davantage qu’une expérience sur la description automatique : une recherche sur la façon dont les instruments numériques déterminent les objets que l’histoire de l’art et du design peut connaître.

## 2026-10-06T15:47:07.344Z

**La suite de l’enquête fait émerger une question plus exigeante : à quelles conditions une reproduction numérique permet-elle de retrouver une image tout en conservant les indices nécessaires pour l’utiliser comme preuve historique ?**

J’ai approfondi cette piste à partir des documents du corpus et des travaux antérieurs. Trois résultats changent la réflexion : un nouveau problème expérimental, un cas documentaire particulièrement instructif autour du *Rhinocéros*, et des antécédents qui obligent à préciser davantage l’originalité.

**Une correction est d’abord nécessaire dans l’expérience actuellement en cours.**

Le nouveau témoin « livre sans texte » ne conserve pas exactement la géométrie du livre avec texte. Dans [layers.py](/Users/marcel/impressions/src/punctured_sky/layers.py:239), retirer le texte supprime aussi des tirages aléatoires. La transformation de perspective intervient ensuite avec un état différent du générateur : employer la même graine ne suffit donc pas.

J’ai reproduit le problème sans appel à un modèle. Pour Q27982670 :

| Propriété | Livre avec texte | Livre sans texte |
|---|---:|---:|
| Rectangle occupé par l’œuvre | `(529,125)–(846,404)` | `(513,152)–(828,417)` |
| Part de l’image occupée | 12,63 % | 11,85 % |
| Recouvrement des deux masques | \multicolumn{2}{c}{77,0 %} |

Ainsi, le contraste prévu entre ces conditions mélange **texte, position et transformation de l’œuvre**. Le contraste avec le témoin d’encombrement n’est pas non plus exactement apparié comme l’annonce [le script d’analyse](/Users/marcel/impressions/scripts/blind_round2_analyse.py:38).

Il faut tirer les paramètres géométriques indépendamment du rendu du texte, vérifier l’identité des masques et des pixels pertinents, puis régénérer les conditions concernées avec des caches distincts. Ce point ne supprime pas les observations antérieures ; il empêche cette nouvelle expérience de départager proprement leurs causes.

**Le cas du *Rhinocéros* fournit maintenant un véritable exercice de critique des sources.**

En consultant les notices institutionnelles et en regardant directement les images correspondantes, j’ai relevé une discordance croisée :

| Notice BnF | Description dans le catalogue | Image associée consultée |
|---|---|---|
| « 7e édition, 1620 » | Impression en clair-obscur, bois de teinte vert | Texte néerlandais au-dessus ; adresse de Hendrick Hondius au-dessous |
| « 6e édition » | Publication Hondius vers 1620, avec texte néerlandais | Impression verte en clair-obscur, sans ces textes |

Les deux couples sont vérifiables : [première notice](https://catalogue.bnf.fr/ark:/12148/cb42115190d) et [son image](https://gallica.bnf.fr/ark:/12148/btv1b53215326f) ; [seconde notice](https://catalogue.bnf.fr/ark:/12148/cb421152090) et [son image](https://gallica.bnf.fr/ark:/12148/btv1b532163188).

La formulation prudente est **une discordance compatible avec une interversion des descriptions ou des liens, dont la cause demande confirmation**. L’annotation locale mentionnant le néerlandais et l’adresse correspond bien à l’image utilisée.

Ce cas met en évidence une limite fondamentale : **une notice institutionnelle ne devient pas automatiquement une vérité de référence incontestable**. Le protocole doit permettre de conserver une contradiction entre notice, inscription et observation matérielle.

Il faut également distinguer cette discordance des variations légitimes de numérotation. La Library of Congress indique que le tirage Hondius est appelé sixième édition dans une classification et septième chez Dodgson. Un système qui traiterait ces deux étiquettes comme des identités nécessairement différentes créerait lui-même une erreur. [Examen technique de la Library of Congress](https://www.loc.gov/preservation/conservators/durer/index.html)

**L’intérêt historique du cas dépasse toutefois la correction d’un catalogue.**

La même étude de conservation explique que, vers 1620, Hondius réemploie le bois de Dürer et modifie le texte : il corrige la date d’arrivée du rhinocéros à Lisbonne, mais ajoute à tort que Dürer l’aurait dessiné d’après nature. Le motif reste reconnaissable tandis que change la revendication de vérité qui l’accompagne. La Library of Congress documente aussi le rognage de l’adresse inférieure sur son exemplaire, ainsi que l’intérêt des fissures du bois et du filigrane pour son identification. [Étude de conservation](https://www.loc.gov/preservation/conservators/durer/index.html)

Nous avons donc trois questions différentes :

- **Reconnaissance :** est-ce le *Rhinocéros* de Dürer ?
- **Identification documentaire :** de quel tirage et de quel exemplaire s’agit-il ?
- **Interprétation historique :** que prétend cette publication concernant l’origine et l’autorité de l’image ?

Une réponse correcte à la première peut coexister avec une erreur sur les deux autres.

Ce fait historique concernant Hondius est déjà connu. Son intérêt pour Punctured Sky est de fournir un **cas de validation documenté** : nous savons quelle information chercher, où elle se trouve et quelle interprétation sa disparition rend impossible ou trompeuse.

**Je resserre aussi deux propositions de ma première revue.**

D’abord, la proximité de deux images dans un classement ne signifie pas que leurs notices sont fusionnées. Un moteur peut rapprocher deux éditions tout en conservant leurs identifiants et leur provenance. Il faudra observer précisément à quel endroit une distinction se perd : extraction, indexation, classement, affichage ou interprétation des résultats.

Ensuite, motif, matrice, état, édition et exemplaire ne forment pas une hiérarchie linéaire. Une matrice peut traverser plusieurs éditions ; une édition comprend plusieurs exemplaires ; une copie regravée n’est pas simplement un nouvel état de la matrice originale. Le modèle documentaire doit représenter ces relations sans les rabattre sur une seule catégorie « même œuvre ».

Ces précisions empêchent de construire une thèse dont le protocole aurait déjà décidé que la recherche visuelle efface nécessairement l’histoire.

**La recherche bibliographique révèle des antécédents beaucoup plus proches que ceux mobilisés jusqu’ici.**

Trois sont particulièrement importants :

| Travail | Ce qu’il établit déjà |
|---|---|
| Chung et ses collègues, *Re-presentations of Art Collections*, 2014 | Recherche d’illustrations, distinction entre impressions d’un même bois et bois copiés, exploitation des dommages pour étudier leur succession |
| Malaspina et Zhong, puis 15cILLUSTRATION | Recherche de réemplois d’illustrations entre textes et éditions, avec maintien des liens bibliographiques |
| Wilkinson, Briggs et Gorissen, *Computer Vision and the Creation of a Database of Printers’ Ornaments*, 2021 | Usage des ornements comme indices bibliographiques ; limites des reproductions pour distinguer matrices et copies ; différence entre repérage et attribution |

Sources : [Chung et ses collègues](https://www.robots.ox.ac.uk/~vgg/publications/2014/Chung14/chung14.pdf), [15cILLUSTRATION](https://www.robots.ox.ac.uk/~vgg/projects/seebibyte/case_studies/15cillustration/index.html), [Wilkinson et ses collègues](https://dhq-static.digitalhumanities.org/pdf/000537.pdf).

**La distinction entre similarité iconographique et identité matérielle n’est donc pas une contribution nouvelle en elle-même.** Ni la reconnexion d’une image extraite à son livre d’origine.

Le différentiel plausible devient plus étroit :

> **Mesurer comment des choix précis de reproduction et de traitement numérique modifient la fiabilité d’une inférence historique, puis établir les conditions permettant de conserver les preuves nécessaires à cette inférence.**

Cette formulation contient une expérience réfutable. Certains recadrages pourraient améliorer l’identification ; certaines métadonnées pourraient compenser la perte du contexte ; certaines distinctions pourraient rester impossibles sans examen de l’original.

**Je construirais le premier pilote autour de six à huit feuilles du *Rhinocéros*, avec trois tâches séparées.**

Les collections offrent déjà des points de départ identifiés : un tirage de 1515 au Met, une impression en clair-obscur après 1620, les deux documents BnF, l’exemplaire étudié par la Library of Congress et un témoin du British Museum dont la notice conserve une incertitude sur le rognage. [Met, 1515](https://www.metmuseum.org/art/collection/search/356497), [Met, après 1620](https://www.metmuseum.org/art/collection/search/388409), [British Museum](https://www.britishmuseum.org/collection/object/P_1877-0609-71)

Pour chaque feuille, il faudrait établir :

- l’identifiant et la cote de l’exemplaire ;
- la date attribuée au bois et celle attribuée à l’impression ;
- les inscriptions effectivement visibles ;
- les indices matériels accessibles dans la reproduction ;
- la source justifiant chaque attribution ;
- les contradictions et les informations inconnues.

Puis comparer plusieurs présentations du **même document** : feuille entière, motif seul, détails pertinents, et motif accompagné de son contexte documentaire. Il faudrait séparer le bénéfice pratique du recadrage — qui agrandit le motif — de son effet propre à résolution comparable.

Les tâches seraient :

| Tâche | Réussite attendue |
|---|---|
| Retrouver le motif | Identifier les occurrences de la composition |
| Identifier le document | Proposer une attribution éditoriale justifiée, ou reconnaître l’incertitude |
| Restituer sa valeur de témoignage | Identifier ce que les inscriptions affirment, sans transformer cette affirmation en fait historique |

La dernière distinction est cruciale : un modèle devrait pouvoir dire **« la légende affirme que Dürer a dessiné l’animal d’après nature »**, sans conclure **« Dürer a dessiné l’animal d’après nature »**.

Ce serait une contribution plus substantielle que de mesurer seulement si le rhinocéros apparaît dans la phrase principale.

Les comparateurs devraient inclure une recherche par caractéristiques locales, les encodeurs actuels, l’OCR seul, les métadonnées seules et une combinaison simple. Si l’OCR accompagné d’une référence bibliographique résout le problème, ce résultat doit être accepté : il indique quelle information était nécessaire.

**Trois hypothèses permettraient de décider si cette direction mérite d’être poursuivie.**

1. **Le recadrage produit des effets différents selon la tâche.**  
   Il peut améliorer la recherche du motif tout en réduisant la capacité à identifier ou interpréter le document. Cette hypothèse serait affaiblie si aucune perte pertinente n’apparaissait après contrôle de la résolution.

2. **Les indices contextuels apportent une information historique transférable.**  
   Leur utilité doit subsister sur un autre exemplaire ou une autre numérisation. Sinon, le système pourrait reconnaître un fond de scanner ou une marque institutionnelle.

3. **Une représentation conservant les relations entre motif, feuille et notice améliore la justification des réponses.**  
   Elle doit permettre de citer le bon indice, de conserver les désaccords et de s’abstenir lorsque la preuve manque. Un simple gain de classement ne suffirait pas.

Ce pilote serait trop petit pour une généralisation statistique ambitieuse. Il servirait à vérifier la faisabilité documentaire et à découvrir les véritables variables avant de constituer un corpus plus large.

**Pour la thèse elle-même, deux terrains restent crédibles, avec des enjeux différents.**

Le terrain **Holbein et l’édition illustrée** est désormais plus concret. Deux éditions françaises numérisées sont identifiées : les *Simulachres* de 1538, exemplaire BnF RES-Z-1990, et l’édition de 1542, exemplaire Arsenal 8-T-7960, signalé incomplet. Le changement de titre, de la réalisation des images vers la médecine de l’âme et la consolation des malades, ouvre une question sur les usages prescrits du livre. [Notice de 1538](https://catalogue.bnf.fr/ark:/12148/cb306116444), [notice de 1542](https://catalogue.bnf.fr/ark:/12148/cb39307236c)

Mais les rapports entre gravures, langues et typographie chez Trechsel et Frellon ont déjà été étudiés. L’enquête devrait identifier une difficulté historiographique précise. Le corpus local contient bien 36 images réparties en cinq groupes appelés « éditions », mais son [manifeste](/Users/marcel/caypollard/data/derived/copies/manifest.json) ne documente pas encore suffisamment les exemplaires, pages et relations de transmission. Il constitue un matériau exploratoire.

Le terrain **photothèque et histoire de l’attribution** me paraît particulièrement cohérent avec les prémisses de Punctured Sky. La Witt Library offre un cas instructif : son protocole de numérisation conserve volontairement les montages et les versos portant des inscriptions. Le Courtauld a annoncé l’achèvement de la publication de plus de deux millions d’images en avril 2025. [Protocole de numérisation](https://courtauld.ac.uk/library/collections-and-image-libraries/image-libraries/witt-library/), [achèvement du projet](https://courtauld.ac.uk/news-blogs/2025/the-courtauld-completes-major-project-to-digitise-the-witt-library/)

Cela permettrait de poser une question précise :

> **Comment les opérations de montage, de classement et d’indexation organisent-elles l’accès aux attributions successives d’une œuvre, et dans quelles conditions la recherche numérique permet-elle encore de reconstituer leurs désaccords ?**

La différence avec une critique générale de la dématérialisation est importante : ici, les institutions préservent déjà le contexte. Il reste à examiner **sa mobilisation effective dans la recherche**.

Le design interviendrait alors dans la disposition des reproductions, annotations et rapprochements ; l’histoire de l’art dans la constitution des attributions ; les humanités numériques dans les conditions de leur recherche et de leur restitution.

**Voici la formulation doctorale provisoire que je retiendrais à ce stade :**

> Cette recherche étudie les conditions dans lesquelles les reproductions d’œuvres deviennent des preuves pour l’histoire de l’art. À partir d’un fonds documentaire circonscrit, elle reconstitue les opérations de présentation, d’annotation et de classement qui relient une image à des affirmations concernant son auteur, sa date ou sa circulation. Elle examine ensuite comment l’extraction, l’indexation et la description automatiques modifient l’accès à ces relations. L’enquête associe critique des sources, histoire des pratiques documentaires et expérimentations contrôlées. Elle distingue la reconnaissance d’un motif, l’identification d’un objet et la justification d’une interprétation. Sa contribution attendue est d’établir quelles transformations numériques permettent de conserver des distinctions historiquement pertinentes, lesquelles les rendent inaccessibles, et comment représenter les incertitudes sans les convertir en identifications artificiellement certaines.

**La prochaine priorité scientifique est le petit dossier comparatif du *Rhinocéros*.** Il permet de vérifier immédiatement que la méthode sait traiter une inscription, un rognage, une attribution et une contradiction documentaire. Ensuite seulement, un terrain plus vaste pourra être choisi pour la découverte historique qu’il rend possible.

