import csv
import json
import os
import tempfile
from dataclasses import MISSING
from pathlib import Path
class StorageError(Exception):
    """Error al leer o escribir el almacén de incidencias."""



ruta = Path("sesiones/s04/datos/incidencias.json")
DANGER_WORDS = ("ampastra", "humo", "caliente", "quema")

def create_incidencias_json(path: Path, incidencias: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(incidencias, ensure_ascii=False, indent=2)
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, suffix=".tmp")

    try:
        with os.fdopen(fd, "w", encoding="utf-8") as tmp:
            tmp.write(data)
        os.replace(tmp_name, path)
    except BaseException:
        Path (tmp_name).unlink(missing_ok=True)
        raise

def read_incidencias(ruta: Path) -> list[dict]:
    try:
        texto = ruta.read_text(encoding="utf-8")
    except FileNotFoundError:
        return []
    try:
        incidencias = json.loads(texto)
    except json.JSONDecodeError as exc:
        raise StorageError(f"{ruta} no contiene JSON válido (línea {exc.lineno})") from exc
    if not isinstance(incidencias, list):
        raise StorageError(f"{ruta} debería contener una lista")
    return incidencias

def localizar_incidencia(descripcion):
    for palabra in DANGER_WORDS:
        if palabra in descripcion:
            return True
    return False

def create_incidencias(plate, kilometraje, descripcion):
    num_incidencia = len(incidencias) + 1

    if localizar_incidencia(descripcion):
        estado = "open"
        urgencia = "critical"
    else:
        estado = "open"
        urgencia = "normal"

    incidencia = {"id": num_incidencia, "matricula": plate, "kilometraje": kilometraje, "estado": estado, "urgencia": urgencia}
    incidencias.append(incidencia)

def comprobar_matricula(matricula: str) -> bool:
    if  (matricula[:4]).isdigit() and (matricula[4:7]).isalpha() and len(matricula) == 7:
        return True
    return False
 


incidencias = read_incidencias(ruta);

while(True):
    matricula = input("introduce la matricula: ")
    matricula_formalizada = matricula.strip().replace(" ", "").upper()
    while not comprobar_matricula(matricula_formalizada):
        print("Matricula en formato inválido \n")
        matricula = input("introduce la matricula: ")
        matricula_formalizada = matricula.strip().replace(" ", "").upper()
    descripcion = input("introduce una descripcción del problema: ")
    try:
        kilometros = int(input("introduce los kilometros: "))
    except ValueError as exc:
        print(f"Los kilometros tienen que ser un número")
        break
    
    descripcion_formalizada = descripcion.strip().replace(" ", "").lower()
    create_incidencias(matricula_formalizada, kilometros, descripcion_formalizada)
    print(incidencias)
    create_incidencias_json(ruta, incidencias)
    exit()