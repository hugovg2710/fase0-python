PELIGRO = ("humo", "temperatura", "calor", "chirrido")

def mileage_category(km: int) -> str:
    if km > 300_000:
        return "Muy alto"
    elif km > 250_000:
        return "alto"
    elif km > 200_000:
        return "normal"
    else:
        return "bajo"


def danger_signal(texto: str) -> bool:
    texto = texto.lower()

    for palabra in PELIGRO:
        if palabra in texto:
            return True
    return False


nombre = input("Introduce nombre del cliente: ")
nombre = nombre.strip().lower()

matricula = input("Introduce matricula: ")
matricula = matricula.strip().upper().replace(" ", "").replace("-", "")

Kilometros = input("Introduce los kilometros del vehículo: ")
Kilometros = Kilometros.strip()

while not str.isdigit(Kilometros):
    Kilometros = input("Introduce los kilometros del vehículo: ")
    Kilometros = Kilometros.strip()


descripción = input("Introduce una breve descripción de la avería: ")
descripción = descripción.strip().lower()

testigo = input("Tiene algún testigo encendido? (s/n)")
testigo = testigo.strip().lower().replace(" ", "")



Kilometros = int(Kilometros)






if danger_signal(descripción):
    print("REVISIÓN URGENTE: detén el vehículo en un lugar seguro y contacta con el taller")

print("---Resumen---")
print("-------------")
print(f"Nombre del cliente: {nombre}")
print(f"Matricula del vehículo: {matricula}")
print(f"Kilometros del vehiculo: {Kilometros} ({mileage_category(Kilometros)})")
print(f"Descripción del problema: {descripción}")
print(f"Testigo encendido: {testigo}")

