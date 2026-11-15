from collections import Counter
from collections import defaultdict
import csv
import json
import os
import tempfile
from pathlib import Path

class StorageError(Exception):
    """Error al leer o escribir el almacén de incidencias."""


FRAGIL_WORDS = ("cristal", "frágil", "líquido", "cerámica")


def normalizar_tracking(texto: str) -> str:
    texto_normalizado = texto.strip().upper()
    return texto_normalizado

def tracking_valido(texto: str) -> bool:
    return texto[:2].isalpha() and texto[2:].isdigit() and (len(texto) == 8)

def parsear_peso(texto: str) -> float: 
    texto_normalizado = texto.replace(" ", "").strip().replace(",", ".")
    try:
        num_float = float(texto_normalizado)
        return num_float
    except ValueError:
        print(f"La cadena {texto_normalizado} no es un número")
        exit()
    
def es_fragil (descripcion: str) -> bool:
    for palabra in FRAGIL_WORDS:
        if palabra in descripcion:
            return True
    return False


def crear_paquete(paquetes, tracking, peso_kg, descripcion):
    id_new = len(paquetes) +1
    if es_fragil:
        prioridad = "fragil"
    else:
        prioridad = "normal"

    paquete_nuevo = {"id": id_new, "tracking": tracking, "peso_kg": peso_kg, "descripcion": descripcion, "prioridad": prioridad,
                     "estado": "pendiente"}

    paquetes.append(paquete_nuevo)

    return paquete_nuevo

def marcar_entregado(paquetes, id):
    for paquete in paquetes:
        if paquete["id"] == id:
            if paquete["estado"] == "pendiente":
                paquete["estado"] = "entregado"
            return False

def contar_por_prioridad(paquetes):
    prioridad = Counter(i["prioridad"] for i in paquetes)
    return prioridad

def agrupar_por_tracking(paquetes):
    tracking = defaultdict(list)
    for paquete in paquetes:
        tracking[paquete["tracking"]].append(paquete["id"])
    return tracking

def leer_paquetes_json(ruta: Path) -> list[dict]:
    try:
        texto = ruta.read_text(encoding="utf-8")
    except FileNotFoundError:    
         return []
    try:
        list = json.loads(texto)
    except json.JSONDecodeError as exc:
        raise StorageError(f"{ruta} no contiene JSON válido (línea {exc.lineno})") from exc
    return list