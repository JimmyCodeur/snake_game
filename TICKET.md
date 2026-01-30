## Objectif
Modifier la couleur du serpent dans le jeu Snake pour qu'il soit orange au lieu de la couleur actuelle.

## Critères d'acceptation
- Le corps du serpent s'affiche en orange
- La tête du serpent s'affiche en orange (ou dans une nuance d'orange légèrement différente pour la distinguer)
- Le changement est visible immédiatement au lancement du jeu
- Aucun impact sur les autres éléments visuels (nourriture, fond, etc.)

## Détails techniques
- Localiser la définition des couleurs dans `snake.py`
- Modifier la valeur RGB pour le serpent vers une couleur orange (ex: RGB(255, 165, 0) ou RGB(255, 140, 0))
- Tester que la couleur s'affiche correctement sur différents fonds
- S'assurer que la lisibilité reste bonne

## Notes
- Couleur orange suggérée : `(255, 165, 0)` pour un orange classique
- Possibilité d'utiliser `(255, 140, 0)` pour un orange plus foncé si meilleur contraste