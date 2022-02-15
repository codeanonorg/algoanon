# Problème de plannification

Ce problème est proposé dans le cadre des ateliers organisés par l'association étudiante [CodeAnon](https://codeanon.org).

![Bagnère pub](img/algoanon_chap_I.png)
## Comment participer

Pour participer, il suffit de fournir une solution dans n'importe quel langage, sur un dépôt git public et d'ouvrir une issue **avant la deadline** sur ce dépôt. L'issue doit contenir un lien vers la solution proposée, une courte  explication de ce qui a été fait et toutes autres informations utiles.

Les différentes entrées seront évalué une fois la date limite dépassé.

Si vos fichier solution ne sont pas dans un format valide ([voir script de validation](#script-de-validation-dune-solution)), vous serez immédiatement disqualifié.

## Problème

Pour que le local de l'association puisse être ouvert, il faut qu'un certain nombre de bénévoles se rendent disponible sur des créneaux au fil des semaines.

Partant d'une liste de jours et de bénévoles avec leurs disponibilités, il faut que le responsable du planning les répartisse équitablement sur le mois à venir pour garantir l'ouverture du local.

Sachant que plusieures contraintes sont imposées pour éviter de surcharger les bénévoles:
1. Un bénévole ne peut effectuer plus de 3 permanences par mois (`max_shifts_per_month`)
2. Un bénévole ne peut enchaîner 2 permanences de suite 
3. Il faut obligatoirement 3 bénévoles pour que le local puisse être ouvert (`volunteers_per_shift`)

## Objectifs

### Objectif 1

Proposez un algorithme qui génère une affectation.

> **Note:** L'afectation vide étant valide, l'objectif est donc d'ouvrir le plus de jour possible.
> 
> Votre tâche est donc de trouver une solution qui garantit le plus de jours d'ouverture.


### Objectif 2

> ⚠️ C'est un problème difficile, il est donc d'abord conseillé de trouver une solution valide avant de s'essayer à l'optimisation des critères ci-dessous.

Pour corser le problème, on demande de **répartir équitablement les bénévoles** sur le mois pour que tout les bénévoles participe, tout en **ouvrant le plus de jour possibles**.

#### Fonction d'évalution

On cherche une solution <img src="https://render.githubusercontent.com/render/math?math=S"> de répartition des bénévoles qui minimise la fonction d'évaluation suivante:

1. On ordonne deux solutions par jours de fermeture, la solution qui possède le moins de jour de fermeture est forcément meilleure.
2. Pour évaluer le second critère, on cherche à minimiser la fonction suivante: <img src="https://render.githubusercontent.com/render/math?math=\sum_{b\in B}n\_affectation_b^2"> avec <img src="https://render.githubusercontent.com/render/math?math=B"> l'ensemble des bénévoles.


> - Une solution est une fonction qui associe un jour à un ensemble de bénévole.
> <img src="https://render.githubusercontent.com/render/math?math=S: Jour ->">*Bénévoles*.
>
> - avec <img src="https://render.githubusercontent.com/render/math?math=Jour"> l'ensemble des jours du mois: "31/01/2022"<img src="https://render.githubusercontent.com/render/math?math=\in Jour">
>
> - *Bénévoles* l'ensemble des bénévoles affecté à le permanence de ce jour.

## Données d'entrée

- **data_february.json**
```json
{
    "max_shifts_per_month": 3,
    "volunteers_per_shift": 3,
    "days": [
        "31/01/2022",
        "04/02/2022",
        "07/02/2022",
        "11/02/2022",
        "14/02/2022",
        "18/02/2022",
        "21/02/2022",
        "25/02/2022",
        "28/02/2022",
        "04/03/2022"
    ],
    "volunteers" : [
        {
            "name": "Arthur",
            "days_unavailable": []
        },
        {
            "name": "Nathan",
            "days_unavailable": ["25/02/2022", "28/02/2022", "04/03/2022"]
        },
        {
            "name": "Lison",
            "days_unavailable": ["31/01/2022", "04/02/2022", "11/02/2022", "18/02/2022"]
        },
    ]
}
```

## Solution attendue

### Format de la solution attendu
Si aucun bénévoles n'est disponible pour un certain jour, il faut tout de même ajouter ce jour à la solution avec comme valeur une liste vide.

- **solution.json**
```json
{
    "solution": [
        {
            "day": "31/01/2022",
            "assigned_volunteers": ["Arthur", "Nathan", "Lison"]
        },
        {
            "day": "04/02/2022",
            "assigned_volunteers": ["Marc", "Jean", "Francine"]
        },
        {
            "day": "07/02/2022",
            "assigned_volunteers": ["Nathan", "Frederique", "Marie"]
        },
        {
            "day": "11/02/2022",
            "assigned_volunteers": ["Marc", "Arthur", "Lison"]
        },
        {
            "day": "14/02/2022",
            "assigned_volunteers": []
        },
    ]
}
```

## Pour aller plus loin

- Si je rajoute un jour dans la liste initiale, comment puis-je modifier la sortie en minimisant le nombre de calcul effectué?

- Ayant le planning du mois courant, suis-je capable de créer le planning du mois suivant tout en respectant les contraintes initiales? 

- L'algorithme proposé fonctionne t-il si le nombre de permanences maximales autorisées par mois ainsi que le nombre de bénévoles nécéssaire à l'ouverture du local est modifié?

- Certains jours doivent ouvrir en priorité par rapport à d'autres, comment gérer ce genre de situation ? 



## Script de validation d'une solution

Pour vérifier qu'une solution respecte le format défini ci-dessus et les contraintes de planification, un script python est mis à disposition.

```bash
$ python tests/validate_file.py fichier_json_solution.json dataset_de_reference.json
```
Le programme renvoie `0` si tout est correct et `1` si une erreur est détectée. Un message précisant le type d'erreur s'affiche également.

Pour vérifier la sortie du script:
```
$ echo $?
```

