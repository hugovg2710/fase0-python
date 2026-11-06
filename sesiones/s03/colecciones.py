from collections import Counter 

incidents = [
 {"id": 1, "plate": "1234BCD", "status": "open", "urgency": "high"},
 {"id": 2, "plate": "5678FGH", "status": "closed", "urgency": "high"},
 {"id": 3, "plate": "1234BCD", "status": "open", "urgency": "normal"},
]

open_ids = [i["id"] for i in incidents if i["status"] == "open"]
by_id = {i["id"]: i for i in incidents} 
plates = {i["plate"] for i in incidents}

print(open_ids)
print(by_id)
print(plates)

newest_first = sorted(incidents, key=lambda i: i["id"], reverse=True)
print(Counter(i["urgency"] for i in incidents))
print(by_id.get(99, "no existe")) # como $a[99] ?? 'no existe'
first, *rest = [10, 20, 30] # first = 10, rest = [20, 30]
print(first, rest)
