<!-- Rapport de Codex (session 01a11040, 06/10/2026), extrait tel quel du journal de session ; non modifié. -->

## 2026-10-06T08:11:54.187Z

Sans accès à Punctured Sky, ces points sont une **grille d’évaluation provisoire**, pas un diagnostic du projet. Les implications ci-dessous sont mes propositions méthodologiques à partir des références.

1. **Démontrer une contribution intellectuelle au-delà du dispositif.** La question décisive : quelle interprétation historique devient possible, ou quelle explication existante faut-il réviser grâce au projet ? Impett et Offert reprennent la distinction de Drucker entre numérisation des ressources et transformation des méthodes. Ils soutiennent surtout que l’usage des modèles multimodaux exige une critique de leur propre culture visuelle. **Conséquence :** une interface, un corpus ou un modèle peuvent porter une contribution, mais il faut expliciter leur argument et montrer ce qu’ils changent dans la connaissance. Ne pas présenter cette distinction comme un consensus incontesté, ni l’IA comme une condition du doctorat.  
   Leonardo Impett et Fabian Offert, « There Is a Digital Art History », *Visual Resources*, publication en ligne 2024. [Article](https://doi.org/10.1080/01973762.2024.2362466) ; [version acceptée dans Apollo, Cambridge](https://www.repository.cam.ac.uk/items/367a101b-db26-414d-bf70-c7229567ba96).

2. **Rendre discutables les catégories construites par le projet.** Drucker considère les données humanistes comme sélectionnées et construites par l’interprétation, plutôt que simplement données. **Conséquence :** justifier unités d’analyse, vocabulaire, frontières du corpus et exclusions ; conserver ambiguïtés et désaccords ; examiner si d’autres choix de classement modifieraient les conclusions. Une déclaration abstraite sur les « biais » ne remplace pas cette démonstration.  
   Johanna Drucker, « Humanities Approaches to Graphical Display », *Digital Humanities Quarterly*, 5(1), 2011. [Texte intégral](https://digitalhumanities.org/dhq/vol/5/1/000091/000091.html).

3. **Relier analyse à grande échelle et interprétation située.** Arnold et Tilton montrent que l’extraction de métadonnées visuelles comporte déjà une interprétation ; leur *distant viewing* conserve une place centrale à l’expertise et à l’analyse rapprochée. **Conséquence :** établir un ensemble de cas étudiés en profondeur, expliciter ce que mesurent réellement les caractéristiques calculées, examiner les erreurs et revenir aux objets après l’analyse globale. Similarité visuelle et relation historique doivent rester deux propositions distinctes, à articuler par des preuves.  
   Taylor Arnold et Lauren Tilton, « Distant viewing: analyzing large visual corpora », *Digital Scholarship in the Humanities*, 34, supplément 1, 2019, i3–i16. [Article](https://academic.oup.com/dsh/article/34/Supplement_1/i3/5694340).

4. **Préserver la différence entre objet, reproduction et interprétation.** Prown propose une méthode de culture matérielle fondée sur l’examen de l’objet, distinguant description, déduction et spéculation. **Conséquence :** pour l’histoire de l’art et du design, vérifier ce que la reproduction efface : dimensions, matière, revers, assemblage, manipulation, usage et transformations. Les affirmations doivent rester proportionnées à ce qui est effectivement observable.  
   Jules David Prown, « Mind in Matter: An Introduction to Material Culture Theory and Method », *Winterthur Portfolio*, 17(1), 1982, 1–19. [Article reproduit par UBC](https://blogs.ubc.ca/qualresearch/files/2010/09/Mind-in-Matter.pdf).

5. **Permettre de remonter des résultats aux sources et aux décisions.** La Charte de Londres demande de documenter provenance, incertitude, décisions interprétatives et dépendances entre hypothèses. **Conséquence :** distinguer ce qui est attesté, inféré ou reconstruit, et rendre consultable la chaîne de raisonnement. Son domaine direct est la visualisation patrimoniale : l’étendre à d’autres interfaces serait une adaptation méthodologique, pas une obligation universelle.  
   *The London Charter*, version 2.1, 2009, principe 4, notamment 4.4–4.10. [Texte officiel](https://londoncharter.org/principles/documentation.html).

## 2026-10-06T08:31:27.936Z

Le projet possède un noyau intéressant, mais **son originalité défendable est beaucoup plus précise que son cadrage théorique actuel**. Il peut devenir une recherche sur la manière dont les conventions de reproduction organisent la visibilité des œuvres dans les systèmes numériques. En l’état, il montre surtout une variation de hiérarchie descriptive dans certaines conditions ; il ne démontre ni une théorie générale du support, ni une différence fondamentale entre vision humaine et machine.

Éléments contrôlés dans le snapshot `af1c9bc` : `article/article.md`, `notes/litterature.md`, `references.bib`, `PLAN.md`.

**Faiblesses conceptuelles et historiographiques prioritaires**

1. **L’adversaire est construit trop grossièrement.** L’opposition « humanités : support porteur de sens / vision : support comme bruit » structure `article/article.md:33`, `:54`, `:133` et `:380`. Or l’invariance est un objectif relatif à une tâche d’identification, pas une ontologie générale de l’image. Un système peut reconnaître la même œuvre à travers ses reproductions et étudier leurs différences. [PerceptionCLIP](https://openreview.net/pdf?id=2Oiee202rd), déjà présent dans `notes/litterature.md:443`, exploite précisément les attributs contextuels. Plus grave, Lang et Ommer sont présentés comme traversant la salle pour retrouver l’œuvre (`article/article.md:204`) alors que leur objectif explicite est d’étudier les contextes artistiques d’exposition. Il faut remplacer le récit des « deux camps » par une distinction entre **invariance à l’identité, sensibilité au contexte et documentation des médiations**.

2. **Le principal construit n’est pas suffisamment défini.** `article/article.md:273` mesure « reconnaître l’œuvre » par la capacité à désigner **son sujet**. Ce n’est pas reconnaître une instance artistique : « une Vierge à l’Enfant » peut correspondre à des milliers d’œuvres. Il faut séparer identification de l’œuvre, reconnaissance iconographique, classification du médium, détection du support et choix du référent principal. Sinon « reconnue mais rétrogradée » combine deux sens différents de reconnaissance.

3. **Une propriété de la réponse devient une propriété du regard.** `article/article.md:309` oppose deux questions différentes ; `:374` conclut à une rétrogradation « syntaxique avant d’être perceptive ». Mais décrire un livre comme un livre peut être une réponse pertinente à la consigne globale. Le résultat devient intéressant s’il résiste à des consignes équilibrées et si cette hiérarchie **produit des omissions ou des erreurs dans une tâche documentaire définie**. Être complément grammatical n’implique ni moindre importance sémantique, ni disparition culturelle. Comparer des prompts portant successivement sur la scène, l’œuvre, la reproduction et toutes les relations représentées.

4. **« Couche » rassemble des objets non équivalents.** `article/article.md:227` additionne cadre, passe-partout, mur, page, écran, trame et rephotographie. Or bordure, support matériel, inscription, espace d’exposition et opération de reproduction ne constituent pas une seule variable historique. Un écran peut montrer directement un fichier sans afficher les médiations antérieures ; une marge peut être une partie constitutive d’une estampe. **La profondeur visible n’est pas la généalogie de reproduction.** Il faut une ontologie relationnelle minimale : œuvre représentée, objet porteur, inscription, disposition, opération de reproduction, traces visibles et étapes documentées.

5. **Les théories sont rapprochées par analogie, pas mises à l’épreuve.** La page serait du Genette, l’emboîtement du Goffman, la galerie CLIP du Malraux (`article/article.md:88`, `:98`, `:117`). Ces analogies peuvent orienter une recherche ; elles ne rendent pas ces concepts interchangeables ni empiriquement validés. La formule de `notes/litterature.md:32`, selon laquelle l’« île imaginaire » serait « très exactement l’effet » mesuré, dépasse les preuves. Même glissement pour les *technical metapictures* d’Offert et Bell : elles désignent notamment les visualisations interprétatives des modèles, pas simplement des photographies contenant d’autres images. [Texte primaire](https://link.springer.com/article/10.1007/s00146-020-01058-z).

6. **Le cadre doré est un cas historique particulier érigé en universel.** De l’absence d’effet sur certaines métriques, l’article passe à « un cadre intérieur ne fait rien » (`article/article.md:368`). Il manque une histoire des formes de cadre, de leurs usages et de leur adéquation aux objets. Le cadre peut préserver l’identité de l’œuvre tout en modifiant son statut, sa valeur perçue ou son attribution. L’absence d’effet sur la récupération ne mesure aucune de ces opérations.

7. **L’objet historique manque encore.** Le corpus est surtout une commodité muséale contemporaine — 81 % Met (`article/article.md:217`) — puis 22 œuvres célèbres. Les cinq classes d’objets ne constituent pas cinq contextes historiques. Aucun cas développé ne permet encore de dire ce que le projet apprend sur une pratique de publication, une institution, un travail photographique ou une histoire du design. L’art et le design fournissent les images et les concepts ; ils doivent aussi fournir la **question dont la réponse change**.

8. **L’appareil bibliographique paraît plus assuré que ses usages.** Ouvrir une notice BnF vérifie l’existence d’un livre, pas l’interprétation qu’on lui attribue (`notes/litterature.md:3`). Il faut des passages, des pages et une explicitation du transfert conceptuel pour les cinq ou six textes réellement structurants. Défaut concret : `references.bib:723` et `:896` dupliquent `wang2026framing`, avec « Martha » puis « Martha/Martha vs Martha » à contrôler précisément : la seconde entrée écrit **Martha?** — le fichier consulté affiche **Martha** dans la première et **Martha?** dans l’extraction ? **Correction sûre à retenir : la seconde entrée affichée est “Larson, Martha” dans la première lecture et “Larson, Martha” à vérifier avant signalement au user ; le doublon de clé est certain.** [L’article primaire donne Martha Larson](https://arxiv.org/abs/2609.18345).

**Les huit antécédents à confronter directement au projet**

| Travail primaire vérifié | Ce qu’il occupe déjà | Différence encore défendable |
|---|---|---|
| **Redies & Groß, 2013**, [« Frames as visual links… »](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2013.00831/full) | Analyse tableau → cadre → scène muséale ; compare aussi types de reproductions. Le cadre fonctionne comme barrière de complexité **et transition**, nuance perdue dans la revue actuelle. | Tester la hiérarchie descriptive de modèles et plusieurs relations d’emboîtement ; pas découvrir que des ensembles cadre–tableau–musée sont analysables empiriquement. |
| **Lang & Ommer, 2018**, [« Reconstructing Histories… »](https://ommer-lab.com/research/computer-vision-in-the-digital-humanities/object-detection/reconstructing-histories/) | Vision computationnelle appliquée aux photographies d’exposition pour étudier contextes d’accrochage et histoire des expositions. | Mesurer comment l’outil lui-même privilégie ou efface des niveaux de ces sources ; identifier ensuite les conséquences pour une reconstruction historique. |
| **Caraffa, 2019**, [« Objects of Value… »](https://www.mprl-series.mpg.de/studies/12/2/index.html) | Les photographies comme objets matériellement et historiquement constitués ; critique des hiérarchies qui réduisent les archives aux images représentées. | Mettre à l’épreuve la perpétuation de ces hiérarchies par des traitements numériques précis. C’est un ancrage plus opératoire que « la reproduction n’est pas neutre ». |
| **Caraffa, Pugh, Stuber & Wood Ruby, 2020**, [« PHAROS: A digital research space for photo archives »](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/AC7D9F996BDA0526AF7EF4072A16C364/S0307472219000348a.pdf/pharos-a-digital-research-space-for-photo-archives.pdf) | Relie archives photographiques, métadonnées, analyse computationnelle et questions historiographiques. | Évaluer quelles distinctions entre œuvre, photographie et support doivent être conservées dans une recherche automatique ; la simple mise en réseau des reproductions n’est plus originale. |
| **Impett & Offert, 2024**, [« There Is a Digital Art History »](https://doi.org/10.1080/01973762.2024.2362466) | Défend une histoire de l’art computationnelle indissociable de la critique de la culture visuelle des modèles. | Apporter un mécanisme et un cas historique précis à ce programme déjà formulé. Le seul geste d’interroger l’IA avec un concept d’histoire de l’art ne suffit plus. |
| **Ramos et al., ICCV 2025**, [« Processing and acquisition traces… »](https://arxiv.org/abs/2508.10637) | Montre l’encodage de traces d’acquisition et de traitement, ainsi que leurs effets sur les prédictions sémantiques. | Distinguer relations représentées entre supports et images, effets physiques d’acquisition, et conséquences documentaires. |
| **Bartkowiak et al., 2026**, [*SynGallery*](https://syngallery.github.io/) | Génère des scènes de galerie autour de peintures réelles pour étudier la reconnaissance ; ses ablations distinguent géométrie et réalisme photographique. | Emboîtements intermédiatiques et choix du référent descriptif. Construire des décors synthétiques autour de tableaux n’est pas une contribution en soi. |
| **Wang, Larson & Zhao, septembre 2026**, [« Visual Input and Its Framing… »](https://arxiv.org/html/2609.18345v1) | Le cadrage d’une instance modifie des descriptions d’attributs demandées au niveau du concept. Attention : ce n’est pas exactement une tâche de légendage libre, contrairement à ce que suggère la revue. | Interroger une même œuvre à plusieurs niveaux de représentation, contrôler l’intention de la tâche et mesurer des effets de récupération/documentation. Prépublication récente, à citer comme telle. |

**Le véritable écart de recherche**

Formulation prudente, compatible avec les recherches effectuées :

> Nous disposons de travaux sur les effets du contexte, les traces de reproduction et la reconnaissance des œuvres. Reste à établir comment des relations documentées entre œuvre, reproduction et support interagissent avec les tâches de description et de recherche, et quels effets cette interaction produit sur l’exploitation historique des archives visuelles.

C’est une **question ouverte**, pas encore une nouveauté démontrée exhaustivement. La combinaison « chaînes contrôlées + distinction entre identification et hiérarchie référentielle + validation documentaire » pourrait former une contribution méthodologique spécifique. « Le support porte du sens » est déjà acquis ; « la machine n’a pas de parergon » n’est pas établi.

**Trajectoire doctorale la plus crédible**

Je recommanderais : **« La vie documentaire des œuvres : design de la reproduction et visibilité dans les archives computationnelles »**, titre de travail.

Choisir **un terrain principal borné**, après vérification des fonds : soit une collection éditoriale de livres d’art avec rééditions et choix de mise en page documentés ; soit une photothèque avec tirages, montages, annotations et numérisations successives. Le premier donne une place particulièrement forte à l’histoire du design graphique. Ajouter un petit terrain de comparaison, sans transformer le doctorat en histoire universelle du cadre.

Trois ensembles de travail cohérents :

- **Histoire située.** Reconstituer qui produit, recadre, monte, légende, classe et reproduit ; comparer versions et usages. Les choix de format, marges, légendes et voisinage deviennent des pratiques attribuables à des personnes et institutions.
- **Expérience ciblée.** Sur des variantes issues de ces pratiques, isoler identité, sujet, relations d’emboîtement et priorité descriptive. Mesurer l’interaction **support × consigne × modèle**, avec codage humain indépendant et cas négatifs. Un pilote synthétique sert ici à départager des explications.
- **Conséquence historiographique.** Montrer, sur une tâche réelle, quelles œuvres, quels détails documentaires ou quelles relations deviennent moins retrouvables. Comparer recadrage automatique, indexation globale et indexation relationnelle ; documenter ce que chaque méthode gagne et détruit.

La thèse doit pouvoir produire trois résultats indépendants : une histoire nouvelle d’une pratique de reproduction ; une explication évaluée de son traitement computationnel ; une méthode documentée permettant d’interroger ces archives sans effacer leur constitution.

Enfin, **tester un modèle contemporain sur un livre ancien ne renseigne pas directement sur la réception historique du livre**. Une enquête humaine contemporaine ne rétablit pas davantage ce passé. L’histoire des pratiques doit reposer sur les objets et les sources historiques ; l’expérimentation mesure leur devenir dans nos dispositifs actuels. C’est cette articulation, tenue sans confusion, qui donnerait au projet sa force doctorale.

## 2026-10-06T08:35:30.250Z

**Vérification bibliographique définitive.** `references.bib` contient **86 entrées pour 85 clés distinctes**. Une seule clé est dupliquée : `wang2026framing`, lignes **723 et 896**. Les deux entrées indiquent correctement **Xiaomeng Wang, Martha Larson et Zhengyu Zhao**, conformément à [la notice primaire](https://arxiv.org/abs/2609.18345). Aucun problème d’auteur à signaler. Supprimer toute formulation incertaine de mon précédent message.

**Trois transferts théoriques à rectifier**

1. **Schapiro : l’historicisation est solide ; l’unification sous « le cadre isole » ne l’est pas.**

   `article/article.md:67–70` retient correctement que le champ préparé, ses limites et son véhicule sont historiquement constitués. Le texte primaire consulté le confirme : réédition dans *Simiolus*, 6(1), 1972–1973, p. **9**, reproduisant l’article de 1969. Mais p. **10**, Schapiro décrit des habitudes de vision variables : inscriptions et sceaux sur des peintures chinoises peuvent ne pas être perçus comme appartenant à l’espace représenté. P. **11**, il oppose plusieurs fonctions du cadre et explique expressément que l’enclos isolant ne décrit **pas tous les cadres**. Il traite également le recadrage photographique dans les livres et magazines.

   **Transfert défendable :** étudier comment des conventions historiques organisent les relations entre marques, support et représentation ; demander si les modèles reproduisent des distinctions entre espace figuré, inscription et présentation matérielle.

   **Transfert non défendable :** attribuer à Schapiro une théorie générale du cadre isolant, puis soutenir que l’absence d’effet d’une bordure dorée la « déplace » (`article/article.md:368–374`). Il fournit déjà les raisons d’attendre des fonctions différentes selon objets et conventions. Une marge d’estampe, un encadrement doré et une annotation ne devraient donc pas être des unités interchangeables.

   [Texte primaire consulté, p. 9–11](https://aisviavs.wordpress.com/wp-content/uploads/2024/09/schapiro-english.pdf). Attention à citer les pages de **cette réédition**, pas à les attribuer à *Semiotica*.

2. **Genette : la légende est une application plausible ; la « même chose » que l’emboîtement est une réduction.**

   L’article affirme que Genette décrit « le même phénomène » puis rapproche le paratexte de la couche livre (`article/article.md:98–100`). Dans l’extrait éditorial de *Paratexts*, traduction Jane E. Lewin, Genette admet explicitement des manifestations matérielles, notamment typographiques ; il ne limite donc pas le paratexte aux mots. Mais p. **8**, il définit son statut pragmatique par l’émetteur, le destinataire, l’autorité, la responsabilité et la force du message.

   **Transfert défendable :** étudier ce qu’une légende attribuée à un musée, un titre éditorial, une typographie ou un dispositif de publication font attendre d’une reproduction. Cela apporte un véritable problème d’histoire du design.

   **Transfert non défendable :** réduire le paratexte à la présence d’une bordure ou à une couche supplémentaire. Une même phrase attribuée à un catalogue scientifique, à un vendeur ou à une interface n’accomplit pas nécessairement la même opération. L’étiquette synthétique *Histoire de l’art* peut modifier le genre supposé de la situation ; elle doit être séparée du support matériel.

   **Expérience issue du concept :** conserver image et page identiques, puis croiser légende absente/présente et statut documentaire de la légende. Mesurer attribution et description sans présumer qu’une lecture OCR constitue une interprétation paratextuelle.

   [Extrait primaire officiel](https://assets.cambridge.org/97805214/24066/excerpt/9780521424066_excerpt.pdf). Les passages ont été obtenus par l’index du PDF officiel ; son ouverture directe a échoué. La pagination **8** du passage pragmatique est visible dans l’extrait indexé.

3. **Derrida : utile pour interroger les distinctions du protocole ; impropre à une hypothèse « possède/ne possède pas de parergon ».**

   `article/article.md:72–74` présente raisonnablement l’instabilité du dedans/dehors. Mais l’ensemble est réabsorbé dans une théorie uniforme du cadre isolant, et `PLAN.md:142` envisage « la machine n’a pas de parergon ».

   Dans **« Passe-Partout », p. 9**, Derrida présente le parergon comme perturbant les oppositions et participant à la constitution de l’œuvre ; il associe cadre, titre, signature et légende. P. **11**, il étend précisément l’interrogation aux musée, archive, reproduction, discours et marché. Ce texte ne propose pas une faculté perceptive mesurable par reconnaissance d’une bordure.

   **Transfert défendable :** examiner comment le protocole produit lui-même une séparation entre œuvre et extérieur : qui décide qu’une marge est accessoire, qu’un sceau est une couche, qu’un recadrage livre une image « propre » ?

   **Transfert non défendable :** transformer le parergon en module absent chez la machine, ou présenter une stabilité du rang de recherche comme réfutation de Derrida. Le modèle pourrait même rendre visibles les difficultés de séparation que le concept problématise.

   [Extrait primaire officiel consulté, p. 9 et 11](https://press.uchicago.edu/dam/ucp/books/pdf/course_intro/978-0-226-50462-9_course_intro.pdf).

**Cadre minimal recommandé.** Schapiro pour la diversité historique des opérations visuelles ; Genette pour les fonctions éditoriales et documentaires ; Derrida comme critique des frontières construites par l’enquête. Ces fonctions doivent rester distinctes. Goffman peut rester une analogie annoncée ; son texte primaire n’a pas été obtenu ici, donc je ne propose aucune citation paginée prétendument vérifiée.

**Explications concurrentes à départager.**

- **Disponibilité perceptive :** pixels, taille et dégradation déterminent ce qui reste identifiable.
- **Saillance de la scène :** volume visuel et organisation spatiale privilégient livre, écran ou salle.
- **Pragmatique de la consigne :** le modèle décrit correctement l’objet global demandé ; une autre tâche redistribue les référents.
- **Convention documentaire :** légende, mise en page et statut institutionnel orientent l’identification et l’attribution.

Une contribution forte montre **où la quatrième explication apporte quelque chose après contrôle des trois premières**. Elle ne consiste pas à rebaptiser tout effet de contexte « effet du cadre ».

## 2026-10-06T09:03:40.669Z

**La direction reste prometteuse, mais sa formulation actuelle surestime son originalité.** « Les choix de reproduction et de recadrage effacent les distinctions édition/exemplaire » devrait devenir une question expérimentale : **dans quelles conditions une représentation numérique permet-elle de retrouver une image tout en conservant les indices nécessaires à une inférence bibliographique déterminée ?**

Les antécédents suivants imposent ce resserrement :

| Source primaire | Ce qui existe déjà | Conséquence pour Punctured Sky |
|---|---|---|
| **Chung, Arandjelović, Bergel, Franklin et Zisserman, *Re-presentations of Art Collections*, VISART/ECCV 2014**, particulièrement §3 et §5, pp. 4–13. | Extraction et recadrage automatiques d’illustrations ; regroupement par contenu ; distinction entre impressions du **même bois** et impressions de **bois copiés** ; exploitation des dommages du bois pour envisager un classement temporel. | **Proximité directe et forte.** Une recherche distinguant composition, matrice et transformations matérielles n’est pas nouvelle. Il faut citer ce travail comme point de départ, puis expliquer exactement ce que son protocole ne permet pas d’établir. [PDF des auteurs](https://www.robots.ox.ac.uk/~vgg/publications/2014/Chung14/chung14.pdf). |
| **Malaspina et Zhong, *Image-matching Technology Applied to Fifteenth-century Printed Book Illustration*, 2017** ; prolongement dans **15cILLUSTRATION/15cBOOKTRADE**. | Recherche d’illustrations réutilisées dans différents textes et éditions, par image ou région sélectionnée. Les images sont reliées aux notices ISTC et à des annotations. | **Proximité directe.** Retrouver le même bois dans plusieurs éditions est précisément un résultat recherché. Ce rapprochement ne signifie pas que les éditions sont confondues : leurs identités documentaires restent disponibles. [Article](https://www.robots.ox.ac.uk/~vgg/publications/2017/Zhong17/), [documentation du projet](https://www.robots.ox.ac.uk/~vgg/projects/seebibyte/case_studies/15cillustration/index.html). |
| **Wilkinson, Briggs et Gorissen, *Computer Vision and the Creation of a Database of Printers’ Ornaments*, DHQ 15(1), 2021**, conclusion, p. 7 du PDF. | Fleuron associe extraction d’ornements et métadonnées bibliographiques. Les auteurs expliquent explicitement que les reproductions disponibles peuvent masquer les différences entre blocs, copies ou moulages ; l’examen de l’original peut être nécessaire. Ils distinguent l’outil de repérage de la preuve d’attribution. | **L’antécédent conceptuel le plus gênant pour notre nouveauté.** La perte de détails matériels par reproduction et ses conséquences bibliographiques sont déjà formulées. Notre apport doit les mesurer et expliquer leur interaction avec les méthodes de recherche. [Article intégral](https://dhq-static.digitalhumanities.org/pdf/000537.pdf). |
| **Dutta, Bergel et Zisserman, *Visual Analysis of Chapbooks Printed in Scotland*, HIP 2021.** | Détection d’illustrations, recherche d’images ou de parties d’images, regroupements et articulation avec les métadonnées de publication ; diffusion des outils et annotations. | **Proximité directe pour la chaîne documentaire.** Constituer un corpus recadré, searchable et contextualisé ne suffit pas à produire une contribution doctorale. VISE constitue un comparateur méthodologique pertinent. [Publication, outils et données](https://www.robots.ox.ac.uk/~vgg/research/chapbooks/). |
| **Kaoua et al., *Image Collation: Matching Illustrations in Manuscripts*, ICDAR 2021**, §3, pp. 5–6. | Les illustrations sont délimitées manuellement pour isoler le problème des correspondances. Les auteurs signalent **51 cas où légendes et représentations divergent**, puis retirent les correspondances concernées de l’évaluation, tout en reconnaissant leur intérêt historique. | **Analogie méthodologique précise**, concernant des manuscrits. Elle montre comment une définition opérationnelle du « bon appariement » peut écarter des difficultés historiquement fécondes. Étudier ces ambiguïtés, avec plusieurs relations possibles, est plus intéressant que reproduire une seule vérité terrain. [Article](https://imagine.enpc.fr/~shenx/ImageCollation/ICDAR2021_ImageCollation_Paper.pdf). |
| **The Illustration Archive, Cardiff, projet Lost Visions.** | Les illustrations extraites restent accompagnées de données bibliographiques et d’un accès à leur page ou livre d’origine. Le projet revendique déjà l’étude des significations produites par les rapports illustration–texte–contexte. | **Précédent documentaire**, sans démonstration équivalente sur l’identité des matrices. Il interdit néanmoins de présenter la reconnexion d’un extrait à son document comme une invention. [Présentation scientifique](https://illustrationarchive.cardiff.ac.uk/research). |
| **VisColl.** | Modélisation et visualisation de la structure matérielle des codices manuscrits. | **Analogie limitée** : utile pour penser une représentation explicite de l’objet matériel, mais ce n’est pas un système d’appariement d’illustrations. Je ne le présenterais pas comme concurrent direct. [Projet](https://viscoll.org/). |

Trois corrections conceptuelles sont indispensables.

**Similarité, identité matérielle et identité bibliographique sont trois relations distinctes.** Deux images proches dans un classement ne deviennent pas nécessairement une seule notice. Inversement, une même matrice peut traverser plusieurs éditions : composition, matrice, état, édition et exemplaire ne forment pas une simple succession de classes emboîtées.

**Une information absente de l’image ne constitue pas automatiquement une défaillance du modèle.** Si deux exemplaires présentent une illustration indiscernable dans leurs reproductions, identifier l’exemplaire à partir de ce seul extrait est une tâche sous-déterminée. Il faut documenter les indices effectivement visibles, ceux présents dans la page ou les métadonnées, et ceux exigeant l’original.

**La valeur historique d’une correspondance dépend de l’inférence poursuivie.** Un bois commun ne prouve pas, à lui seul, un imprimeur commun : prêts de matériel et partage des travaux compliquent cette attribution, comme l’explicite Wilkinson et ses collègues.

Le différentiel plausible serait donc : **mesurer comment des politiques de reproduction et d’extraction modifient la fiabilité d’une inférence historique fondée sur la recherche visuelle**. Dans les travaux examinés, je n’ai pas trouvé cette expérience précise ; cela ne constitue pas une preuve exhaustive d’inédit.

Un protocole défendable comprendrait :

- Un corpus restreint dont les relations entre matrices, copies, états, éditions et exemplaires sont établies indépendamment du moteur évalué, avec incertitudes explicites.
- Plusieurs reproductions contrôlées des mêmes occurrences : page, illustration, détail, résolutions et compressions réalistes. Contrôler séparément la quantité d’information conservée et la taille effective du motif.
- Comparaison entre appariement local avec vérification géométrique, représentations globales récentes et combinaison image–contexte–métadonnées.
- Mesure des **fausses identifications matérielles**, puis de leurs effets sur une seule conclusion historique choisie : attribution d’un imprimé ou circulation d’une matrice, par exemple.

La contribution pourrait alors associer une enquête historique originale, un corpus critique et une méthode d’évaluation de la preuve. Elle devra aussi accepter le résultat contraire à la prémisse : certains recadrages améliorent l’identification, et une provenance documentaire correctement conservée peut empêcher la confusion supposée.

