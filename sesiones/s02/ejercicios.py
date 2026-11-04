#Ejercicio 1
matriculas = [
    "1234 abc",    # espacio + minúsculas
    "5678-DEF",    # guion
    " 9012 - ghi ",# espacios sobrantes en los bordes y guion
    "3456jkl",     # todo junto
    "12-34 MNO",   # guion y espacio en medio de las cifras
    "123 ABC",     # solo tres cifras (inválida)
    "12345 AB",    # cinco cifras y dos letras (inválida)
    "ABCD 123",    # al revés: letras primero (inválida)
    "1234 AB1",    # un dígito donde debería ir una letra (inválida)
    "",            # cadena vacía (inválida)
]



for matricula in matriculas:
    matricula_normalizada = matricula.upper().strip().replace(" ", "").replace("-", "")
    if not (matricula_normalizada[:4]).isdigit() or not (matricula_normalizada[4:]).isalpha():
        print(f"Matricula: {matricula_normalizada} (MATRICULA INVÁLIDA)")
    else:
        print(f"Matricula: {matricula_normalizada} (MATRICULA VÁLIDA)")
#Ejercicio 2
km_actuales = input("Introduce los km actuales del coche: ")
km_actuales = km_actuales.strip()
while not km_actuales.isdigit():
    km_actuales = input("Introduce los km actuales del coche: ")
    km_actuales = km_actuales.strip()
km_actuales = int(km_actuales)


km_ultimo_cambio = input("Introduce los km del último cambio de aceite: ")
km_ultimo_cambio = km_ultimo_cambio.strip()
while not km_ultimo_cambio.isdigit():
    km_ultimo_cambio = input("Introduce los km del último cambio de aceite: ")
    km_ultimo_cambio = km_ultimo_cambio.strip()
km_ultimo_cambio = int(km_ultimo_cambio)

km_diferencia = km_actuales - km_ultimo_cambio

match km_diferencia:
    case km if km >= 15000:
        km_pasados = km_diferencia - 15000
        print(f"Ya toca cambio, te has pasado {km_pasados} kilometros")
    case km if km < 15000:
        km_restantes = 15000 - km_diferencia
        print(f"Aún no toca cambio, te quedan {km_restantes} kilometros")
    case _:
        print("Respuesta invalida")

#Ejercicio 3
STATE_CODES = ("open", "in_progress", "closed")

for codigo in STATE_CODES:
    match codigo:  
        case "open":
            print("Estado abierto")
        case "in_progress":
            print("Estado en proreso")
        case "closed":
            print("Estado cerrado")
        case _:
            print("Codigo de estado desconodido")