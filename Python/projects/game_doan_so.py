from random import randint

so_ngau_nhien = randint(1, 100)
luot_thu = 0

print("-- Game đoán số từ 1-100 --")

while True:
    chon_so = int(input("nhap so ban chon: "))
    luot_thu += 1
    
    if chon_so < so_ngau_nhien:
        print("lon hon")
    elif chon_so > so_ngau_nhien:
        print("be hon")
    else:
        print(f"Dung!,ban da doan dung sau {luot_thu} lan")
        break
    if luot_thu >= 10:
        print(f"het luot doan!so dung la:{so_ngau_nhien}")
        break
    

