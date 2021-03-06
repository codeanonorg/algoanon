from collections import defaultdict
import json
import argparse
import sys

def check_cond(e_cond: bool, e_message: str) -> None:
    if not e_cond:
        print(f'[Erreur] - {e_message}', file=sys.stderr)
        exit(1)


def open_file(filename: str):
    with open(filename, 'r') as json_file:
        try:
            data = json.load(json_file)
        except ValueError:
            print('Une erreur de parsing est survenue')
            exit(1)
        
    return data


def validate_solution_file_format(solution_file: str, n_days: int) -> int: 
    data = open_file(solution_file)

    check_cond(
        'solution' in data.keys(),
        'Le format du fichier ne correspond pas à ce qui est attendu')

    check_cond(
        len(data['solution']) == n_days,
        f"Erreur, le nombre de jour dans la solution ne correspond pas au nombre de jours attendues\n" +
        f"    N'oubliez pas les jours sans bénévoles dans votre solutions")

    for e in data['solution']:
        check_cond('day' in e.keys(), "La clé 'day' n'apparait pas dans la solution")
        check_cond('assigned_volunteers' in e.keys(), "La clé 'assigned_volunteers' n'apparait pas dans la solution")
        check_cond(
            type(e['day']) == str,
            f"Une valeur associé à la clé 'day' ne correspond au type attendu.\n" +
            f"    format attendu '01/01/2001', de type string")
        check_cond(
            len(e['day']) == 10 and (e['day'][2] == e['day'][5] == '/'),
            f"Le fomat de la date ne correspond pas.\n" +
            f"  format attendu '01/01/2001', de type string."
        )
        check_cond(
            type(e['assigned_volunteers']) == list,
            f"Une valeur associé à la clé 'assigned_volunteers' ne correspond au type attendu.\n" +
            f"    format attendu: ['s1', 's2'], de type liste de string")
        for b in e['assigned_volunteers']:
            check_cond(type(b) == str, "Une valeur dans une liste 'assigned_volunteers' n'est pas du bon type\n    Une string est attendu")

    print(f"\n[Log] - Le fichier '{solution_file.split('/')[-1]}' est correct\n")
    return 0


def validate_solution(solution_file: str, reference_dateset: str):
    data = open_file(solution_file)
    data_days = []
    reference_data = open_file(reference_dateset)
    reference_days = reference_data['days']
    reference_volunteers = {o['name']:o['days_unavailable'] for o in reference_data['volunteers']}
    max_shifts_per_month = reference_data['max_shifts_per_month']
    volunteers_per_shift = reference_data['volunteers_per_shift']

    validate_solution_file_format(solution_file=solution_file, n_days=len(reference_days))
    # sort dict values: 31/01/2022 to 20220131
    data['solution'].sort(key=(lambda d: d['day'].split('/')[2] + d['day'].split('/')[1] + d['day'].split('/')[0]))
    
    # Treat the list of volunteers as sets, removing duplicate
    m_unique = lambda l: list(set(l))

    # get all volunteers
    volunteer_dict = defaultdict(int)
    for day in data['solution']:
        data_days.append(day['day'])

        # Vérifie que le nombre de bénévoles correspond à la contrainte de base
        check_cond(
                len(m_unique(day['assigned_volunteers'])) == 0 
            or  len(m_unique(day['assigned_volunteers'])) == volunteers_per_shift,
            f"Le nombre de bénévoles nécessaire au bon fonctionnement de la cafétéria n'est pas respecté au jour {day['day']}."+
            f"\n    La solution n'est pas valide"
        )
        for volunteer in day['assigned_volunteers']:
            # check that volunteer does exist in dataset
            check_cond(
                volunteer in reference_volunteers.keys(),
                f"Le bénévole '{volunteer}' n\'apparait pas dans le dateset et ne peut donc être assigné."+
                f"\n    La solution n'est pas valide"
            )
            # count number of assigned days per volunteer
            volunteer_dict[volunteer] += 1
            check_cond(
                volunteer_dict[volunteer] <= max_shifts_per_month,
                f'Le bénévole "{volunteer}" travaille trop!\n    La solution proposée n\'est pas valide.'
            )
            # vérifier que les assignations correspondent au contraintes des bénévoles
            check_cond(
                day['day'] not in reference_volunteers[volunteer],
                f"Le volontaire {volunteer} ne souhaite pas travailler le {day['day']}.\n"+
                f"  La solution n'est pas valide"
            )

    # check if all days are present
    for ref_day in reference_days:
        check_cond(
            ref_day in data_days,
            f"Le jour {ref_day} n'apparait pas dans le fichier solution."
        )
    # check that there are no consecutive day of work for a volunteer
    for i, day in enumerate(data['solution'][:-1]):
        for v in day['assigned_volunteers']:
            check_cond(
               v not in data['solution'][i + 1]['assigned_volunteers'],
                f"Le bénévole \"{v}\" ne peut pas être assigner à 2 jours consécutifs ({day['day']} et {data['solution'][i + 1]['day']})\n    La solution proposée n\'est pas valide."
            )

    print(f'Le fichier solution est valide')
    exit(0)


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description='Suite de validation des fichiers solutions au format json')
    cli.add_argument('solution_file', help='Fichier au format json contenant la solution', type=str)
    cli.add_argument('dataset_file', help='Fichier au format json contenant le dataset utilisé', type=str)
    args = cli.parse_args()

    validate_solution(args.solution_file, args.dataset_file)
        