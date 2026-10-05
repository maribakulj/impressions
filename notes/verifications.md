# Vérifications à l'œil (relecture m4)

Toutes ces vérifications ont été faites **par l'agent de la boucle (Claude), en regardant les
images** avec l'outil de lecture d'image — pas par un humain. Elles valent contrôle de cohérence,
pas validation indépendante.

| quoi | échantillon | planche | désaccords | règle |
| --- | --- | --- | --- | --- |
| E3 — couches déjà présentes dans les images de musée | 15 œuvres tirées au hasard (graine 3) | `figures/E3-existing-layers-check.jpg` | 0 erreur franche ; « fond de studio » attribué parfois à un simple fond clair (2-3 cas) | une annotation est juste si chaque couche listée est visible et aucune couche visible n'est omise |
| E2 — chaque couche fabriquée | 5 œuvres × 11 couches | `figures/E2-layers-*.jpg` | taches « camouflage » sur papier, dorure, mur de pièce → corrigé ; dominante violette de la trame CMJ → gardée puis décomposée (E4b) | une couche est acceptée si elle ressemble à l'objet réel qu'elle imite |
| E6 — annotation du corpus réel | 20 images tirées au hasard (graine 4) | `figures/E6-real-check.jpg` | 0 | idem E3 ; la surface de l'œuvre est une estimation à l'œil |
| E10b — témoins nouveaux | 1 œuvre × 3 étapes × 4 ; 8 œuvres × 3 fonds | `figures/E10b-controls.jpg`, `figures/E10b-clutter.jpg` | un fond « encombré » était un kakemono avec sa bordure (un support) → centre 60 % seulement ; une bordure résiduelle sur un bord dans 1 cas sur 24 | le fond ne doit montrer ni cadre, ni montage, ni marge |

Le juge des descriptions n'a **pas** été validé par un codage humain (relecture B3) ; voir
`human_study/` pour le protocole qui le permettrait.
