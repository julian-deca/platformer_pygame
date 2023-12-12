import csv
import json


def read_csv(path):
    try:
        with open(path, 'r', newline='') as file:
            reader = csv.reader(file)
            data = [row for row in reader]
            return data
    except Exception:
        print(f"error los datos no existen o estan mal formateados")
        return None


def load_score(name: str, points: int):
    with open("test\scores.json") as file:
        file.seek(0)
        try:
            diccionario = json.load(file)
            reemplazo = False
            if diccionario:
                data = diccionario["scores"]
                for player in data:
                    if player["name"] == name:
                        player["points"] = points
                        reemplazo = True
                if reemplazo == False:
                    if len(data) >= 5:
                        minimum = min(data, key=lambda x: x["points"])
                        if points > minimum["points"]:
                            data[data.index(minimum)] = {
                                "name": name, "points": points}
                    else:
                        data.append({"name": name, "points": points})
                diccionario = {"scores": data}
        except Exception:
            diccionario = {"scores": [
                {"name": name, "points": points}]}
        file.close()
    with open("test\scores.json", "w") as file:
        try:
            json.dump(diccionario, file, indent=4, ensure_ascii=False)
            print("Los datos se cargaron con exito")
        except Exception:
            print("Ocurrio un error al cargar los datos")

        file.close()


def get_scores():
    with open("test\scores.json") as file:
        file.seek(0)
        try:
            lista_playeres = json.load(file)["scores"]
        except Exception:
            lista_playeres = False
        file.close()
        return lista_playeres
