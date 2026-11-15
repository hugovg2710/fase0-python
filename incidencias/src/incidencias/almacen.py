import csv
import json
import os
import tempfile
from pathlib import Path
from dataclasses import MISSING


class StorageError(Exception):
    """Error al leer o escribir el almacén de incidencias."""


incidencias = [
    {"id": 1, "titulo": "Fallo de red", "abierta": True},
    {"id": 2, "titulo": "Pantalla rota", "abierta": False},
]

ruta = Path("sesiones/s04/datos/incidencias.json")


def save_incidents(path: Path, incidents: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)  # Crea la carpeta del path (path.parent)
    data = json.dumps(incidents, ensure_ascii=False, indent=2)  # Convierte a json conservando las tildes
    # Escritura atómica: se escribe un temporal en la misma carpeta y se reemplaza.
    # Si el programa falla a mitad, el fichero original sigue intacto
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, suffix=".tmp")  # Crea un "numero" que represenata el fichero abierto (fd) y tmp_name(el nombre aleaotrio del fichero)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as tmp:  # abre el fichero que devolvio mkstemp para que sea "legible" y le da el nombre tmp
            tmp.write(data)  # Escribe el archivo temporal creado con el json `data`
        os.replace(tmp_name, path)  # renombra al archivo temporal que contenia el json al nombre del archivo dado en path, sustituyendo su contenido y creando el archivo con el contenido
    except BaseException:
        Path (tmp_name).unlink(missing_ok=True)
        raise


def load_incidents(path: Path):
    try:
        text = path.read_text(encoding="utf-8") # abr eel fichero, lo lee y devuelve como un str
    except FileNotFoundError:
        return [] 
    try:
        data = json.loads(text) # Lo "convierte" a un list[dict]
    except json.JSONDecodeError as exc:
        raise StorageError(f"{path} no contiene JSON válido (línea {exc.lineno})") from exc
    if not isinstance(data, list):
        raise StorageError(f"{path} debería contener una lista")
    return data


save_incidents(ruta, incidencias)
print(load_incidents(ruta))


def export_csv(path: Path, incidents: list[dict]) -> None:
    fields = ["id", "plate", "status", "urgency"]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(incidents)
