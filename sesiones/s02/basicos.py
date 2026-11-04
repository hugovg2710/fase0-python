DANGER_WORDS = ("freno", "humo", "fuego", "combustible", "dirección") 


def mileage_category(km: int) -> str: 
    if km > 200_000:
        return "muy alto"
    elif km > 100_000:
        return "alto"
    else:
        return "normal"


def mentions_danger(description: str) -> bool:
    text = description.lower()
    for word in DANGER_WORDS: 
        if word in text:
            return True
    return False

print(mileage_category(128_100)) #Alto
print(mentions_danger("sale HUMO del capó")) #True
print(bool("0"), bool(""), 7/2, 7 // 2) #True, False, 3,5, 3

plate = "   1234 bcd "
print(plate.strip().upper().replace(" ", "")) #1234BCD

status = "in_progress"
match status: 
    case "open" | "in_progress":
        print("activa")
    case "closed":
        print("cerrada")
    case _:
        print("estado desconocido")

#activa

for position, part in enumerate(["aceite", "filtro"], start = 1):
    print(position, part) #1 filtro