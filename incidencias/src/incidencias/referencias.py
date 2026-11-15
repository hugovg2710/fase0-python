a = [1, 2, 3]
b = a # b y a son la MISMA lista
b.append(4)
print(a) # [1, 2, 3, 4]
c = a.copy() # copia superficial (copy.deepcopy para estructuras anidadas)
c.append(5)
print(a, c) # [1, 2, 3, 4] [1, 2, 3, 4, 5]

def add_tag_wrong(tag, tags=[]): # el valor por defecto se crea UNA vez
    tags.append(tag)
    return tags
    
print(add_tag_wrong("x"), add_tag_wrong("y")) # ['x', 'y'] ['x', 'y'] (!)
tags = []

def add_tag(tag, tags=None):
    if tags is None:
        tags = []    
    tags.append(tag)
    return tags

print(add_tag("x", tags), add_tag("y", tags)) # ['x', 'y'] ['x', 'y'] (!)
