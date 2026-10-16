name = input("nhap ten: ").strip()

while not name:
    name = input("nhap ten: ").strip()

print("ten cua ban duoc danh van la:", end=" ")

for letter in name:
    print(letter, end=" ")
