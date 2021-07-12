import sys

from divia_api import DiviaAPI
from os import system
from platform import system as pl_sys


def clear():
    if pl_sys() == "Windows":
        return system("cls")
    system("clear")


api = DiviaAPI()

clear()

print("Bienvenue dans la configuration de votre « Divia dashboard » !")
print("Veuillez tout d’abord renseigner les lignes et arrêts que vous souhaitez voir apparaitre dans l’application.\n\n")

data = []

while True:
    if len(data) > 0:
        line_input = input("Veuillez entrer le nom de la ligne (par exemple « T2 » ou « L6 »).\n \
        Si vous ne souhaitez pas ajouter plus de lignes, appuyez sur « Entrée » :\n")
        if line_input == "":
            clear()
            break
    else:
        line_input = input("Veuillez entrer le nom de la ligne (par exemple « T2 » ou « L6 ») :\n")
        if line_input == "":
            print("Vous devez au moins ajouter une ligne.\n\n")

    lineA = api.find_line(line_input, 'A')
    lineR = api.find_line(line_input, 'R')

    if lineA is None:
        if lineR is None:
            print("Nous n’avons pas trouvé cette ligne, veuillez réessayer.\n\n")
            continue
        line_id = lineR.line_data['id']
    else:
        if lineR is None:
            line = lineA
        else:
            dir_input = input(f"Quel direction ?\n \
            Tapez « A » pour « {lineA.line_data['nom'][3:]} » ;\n \
            Tapez « R » pour « {lineR.line_data['nom'][3:]} ».\n \
            Puis, appuyez sur « Entrée » :\n")
            if dir_input.lower() == 'a':
                line = lineA
            elif dir_input.lower() == 'r':
                line = lineR
            else:
                print("Nous n’avons pas trouvé cette direction, veuillez réessayer.\n\n")
                continue

        stop_input = input("Veuillez entrer le nom de l’arrêt :\n")
        stop = line.find_stop(stop_input)
        if stop is None:
            print("Nous n’avons pas trouvé cet arrêt, veuillez réessayer.\n\n")
            continue

        data.append({
            "line_id": line.line_data["id"],
            "stop_id": stop.stop_data["id"],
            "stop_name": stop.stop_data["nom"],
            "line_name": line.line_data["codetotem"],
            "terminus_name": line.line_data["nom"][3:]
        })

        print("C’est noté !")
        clear()

input_server = input("Veuillez entrer l’adresse de votre serveur, suivi du port si non standard.\n \
Par exemple, « http://12.32.450.68:32654 » :\n")

if input_server.endswith('/'):
    server_address = input_server
else:
    server_address = input_server + '/'

clear()
print("Nous générons votre projet…")

with open("get_data_template.dart", 'r') as f:
    get_data_template = f.read()

with open("widget_template.dart", 'r') as f:
    widget_template = f.read()

get_data = []
widgets = []

for index, the_data in enumerate(data):
    index_str = str(index)
    get_data.append(
        get_data_template
            .replace("{{ X }}", index_str)
            .replace("{{ LINE_ID }}", the_data["line_id"])
            .replace("{{ STOP_ID }}", the_data["stop_id"])
    )
    widgets.append(
        widget_template
            .replace("{{ STOP_NAME }}", the_data["stop_name"])
            .replace("{{ LINE_NAME }}", the_data["line_name"])
            .replace("{{ TERMINUS_NAME }}", the_data["terminus_name"])
            .replace("{{ FUTURE }}", "ls" + index_str)
    )
print(get_data)
with open("lib/main.dart", 'r') as f:
    original_content = f.read()

with open("lib/main.dart", 'w') as f:
    f.write(
        original_content
            .replace("{{ GET_DATA }}", "\n".join(get_data))
            .replace("{{ INSERT_WIDGETS }}", "\n".join(widgets))
            .replace("{{ SERVER_ADDRESS }}", server_address)
    )

clear()

print("Terminé ! Il ne vous reste plus qu’à compiler !")
