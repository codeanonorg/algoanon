# Problème de plannification

Ce problème est proposé dans le cadre des ateliers organisés par l'association étudiante [CodeAnon](https://codeanon.org).

## Comment participer

Pour participer, il suffit de fournir une solution dans n'importe quel langage sur un dépôt git public.

Les différentes entrées seront évalué une fois la date limite dépassé.

Si votre fichier solution n'est pas dans un format valide ([voir script de validation](#script-de-validation-dune-solution)), vous serez immédiatement disqualifié.

## Problème

Pour que le local de l'association puisse être ouvert, il faut qu'un certain nombre de bénévoles se rendent disponible sur des créneaux au fil des semaines.

Partant d'une liste de jours et de bénévoles avec leurs disponibilités, il faut que le responsable du planning les répartisse équitablement sur le mois à venir pour garantir l'ouverture du local.

Sachant que plusieures contraintes sont imposées pour éviter de surcharger les bénévoles:
1. Un bénévole ne peut effectuer plus de 3 permanences par mois (`max_shifts_per_month`)
2. Un bénévole ne peut enchaîner 2 permanences de suite 
3. Il faut obligatoirement 3 bénévoles pour que le local puisse être ouvert (`volunteers_per_shift`)

## Objectif

Proposez un algorithme qui génère une affectation pour faciliter la tâche du responsabe du planning, sachant que l'**on souhaite ouvrir le plus de jour possible** et **répartir équitablement les bénévoles** sur le mois pour que tout le monde participe.


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