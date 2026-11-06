
DANGER_WORDS = ("freno", "humo", "fuego", "combustible", "dirección") 

incidentes = []

def mentions_danger(description):
    text = description.lower()
    for word in DANGER_WORDS:
        if word in text:
            return True      
    return False


def create_incident(plate, description, mileage_km=None):
    num_incidencias = len(incidentes)

    if mentions_danger(description):
        estado = "open"
        urgencia = "critical"
    else:
        estado = "open"
        urgencia = "normal"

    
    incident = {"id": num_incidencias, "matricula": plate, "kilometraje": mileage_km, "estado": estado, "urgencia": urgencia}

    incidentes.append(incident)


create_incident("12347dsd", "sale mucho humo del motor", 1234567)
print(incidentes)