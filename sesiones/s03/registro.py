from collections import Counter

DANGER_WORDS = ("freno", "humo", "fuego", "combustible", "dirección") 
incidentes = []

def mentions_danger(description):
    text = description.lower()
    for word in DANGER_WORDS:
        if word in text:
            return True      
    return False


def create_incident(plate, description, mileage_km=None):
    num_incidencias = len(incidentes) + 1

    if mentions_danger(description):
        estado = "open"
        urgencia = "critical"
    else:
        estado = "open"
        urgencia = "normal"

    
    incident = {"id": num_incidencias, "matricula": plate, "kilometraje": mileage_km, "estado": estado, "urgencia": urgencia}
    incidentes.append(incident)
    return incident

    


create_incident("12347dsd", "sale mucho humo del motor", 1234567)
print(incidentes)

def find_by_plate(matricula):
    incidencias = {i["id"]:i for i in incidentes if i["matricula"] == matricula}
    return incidencias
def filter_incidents(*, status=None, urgency=None):
    incidencias = {
        i["id"]: i
        for i in incidentes
        if (status is None or i["estado"] == status)
        and (urgency is None or i["urgencia"] == urgency)
    }
    return incidencias

def count_by_urgency():
    num_incidendias = Counter(i["urgencia"] for i in incidentes)
    return num_incidendias

def close_incident(incident_id):
    for incidente in incidentes:
        if incidente["id"] == incident_id:
            if incidente["estado"] == "open":
                incidente["estado"] = "closed"
            return True
        
    return False


##Ejercicio 1

def agrupar_incidencias():
    group_incidencias = {}

    for incidencia in incidentes:
        if not incidencia["matricula"] in group_incidencias:
            group_incidencias[incidencia["matricula"]] = []
            group_incidencias[incidencia["matricula"]].append(incidencia["id"])
        else:
            if incidencia["id"] not in group_incidencias[incidencia["matricula"]]:
                group_incidencias[incidencia["matricula"]].append(incidencia["id"])
    return group_incidencias
            