import json
import argparse
import sys


def check_cond(e_cond: bool, e_message: str) -> None:
    if e_cond:
        print(e_message, file=sys.stderr)
        exit(1)


def open_file(filename: str):
    with open(filename, 'r') as json_file:
        try:
            data = json.load(json_file)
        except ValueError:
            print('Une erreur de parsing est survenue')
        
    return data


def validate_solution_file(solution_file: str, n_days: int = 4) -> int: 
    data = open_file(solution_file)

    check_cond(
        'solution' not in data.keys(),
        'Erreur, le format du fichier ne correspond pas à ce qui est attendu')

    check_cond(
        len(list(data.values())[0]) != n_days,
        f"Erreur, le nombre de jour dans la solution ne correspond pas au nombre de jours attendues\n" +
        f"N'oubliez les jours sans bénévoles dans votre solutions")
    
    for e in list(data.values())[0]:
        check_cond('day' not in e.keys(), "La clé 'day' n'apparait pas dans la solution")
        check_cond('assigned_volunteers' not in e.keys(), "La clé 'assigned_volunteers' n'apparait pas dans la solution")
        check_cond(
            type(e['day']) != str,
            f"Une valeur associé à la clé 'day' ne correspond au type attendu.\n" +
            f"format attendu '01/01/2001', de type string")
        check_cond(
            type(e['assigned_volunteers']) != list,
            f"Une valeur associé à la clé 'assigned_volunteers' ne correspond au type attendu.\n" +
            f"format attendu: ['s1', 's2'], de type liste de string")
        for b in e['assigned_volunteers']:
            check_cond(type(b) != str, "Une valeur dans une liste 'assigned_volunteers' n'est pas du bon type\nUne string est attendu")

    print(f"\nLe fichier '{solution_file.split('/')[-1]}' est correct")
    return 0


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description='Valide le formatage json du fichier de solution')
    cli.add_argument('solution_file', help='Fichier json contenant la solution', type=str, nargs='+')
    args = cli.parse_args()
    # '../data/solution_template.json'
    for f in args.solution_file:
        validate_solution_file(f) 
        