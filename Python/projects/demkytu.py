#tienvu

S = input("")
dem_so = 0
for i in S:
    if S.count(i) == 1:
        dem_so += 1
print(dem_so)
