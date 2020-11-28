names = ["adam", "brian", "craig", "adam"]

res = []
for x in names:
    if x not in res:
        res.append(x)
print(res)