## Compte-rendu de l'exercice technique

### Rapport des heures passées
* 23/03/2024 : 3h
    - Prise en main du sujet
    - Ajout d'un superuser, mise en place d'une vue basique pour récupérer les articles et les ventes.
* 24/03/2024 : 8h
    - Écriture des unittests pour la validation des vues, des champs sérialisés et des ajout/suppression
    - Test coverage sur les lignes ajoutées dans l'app `sales`
* 25/03/2024 : 3h
    - Divers correctifs et améliorations
    - Ajout de l'agrégation des vues pour les ventes mais difficultés pour avoir les détails requis
* 26/03/2024 : 2h
    - Finalisation de la vue agrégée
    - Nettoyage, ajout de commentaires, test de linting, coverage

### Status des consignes

- [x] Possibilité d'ajouter un article via api et CRUD via admin panel
- [x] Possibilité d'ajout une vente via api et CRUD via admin panel
- [x] Possibilité de modifier / supprimer une vente par le créateur uniquement
- [x] Liste (paginée par 25 éléments) des ventes (date, catégorie article, code article, nom article, quantité, prix de vente unitaire, prix de vente total)
- [x] Bonus : liste agrégée des ventes (paginée par 25 éléments également) par article avec catégorie associée, totaux des prix de vente, pourcentage de marge, date de la dernière vente, ordonnée par totaux des prix de vente décroissants.


### Points d'améliorations

- Clarifier les unittests pour les rendre plus compacte avec le même 'coverage'
- Retirer la supposition d'une monnaie avec 2 décimales ce qui n'est pas toujours le cas
- Dans la plupart des cas, on renvoie l'url de l'objet comme bonne pratique mais parfois, il est peut-être plus pertinent de renvoyer le `code`, l'`id` ou le `display name`. A clarifier suivant l'usage des différentes vues.
