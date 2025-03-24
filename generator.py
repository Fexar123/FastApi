def createGenerator():
    for i in range(3):
        if i != 0:
            yield i*i

Generator = (i*i 
             for i in range(3)
                if i != 0)

pizda = createGenerator()

print(next(pizda))
print(next(pizda))