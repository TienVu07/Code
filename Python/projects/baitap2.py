
options = [
            "1. Xem kho",
            "2. Mua hang",
            "3. Them hang",
            "4. Xoa san pham",
            "5. Kiem tra san pham",
            "6. Thoat"
            ]

kho = {
    "apple": 15,
    "banana": 8,
    "orange": 12
}
def menu():
    while True:

        print("\n-- MENU --")

        for option in options:
            print(option)
    
        choice = input("\n>  ")

# KHO HANG

        if choice == "1":
            print("-- KHO HANG --\n")
            print("apple: ",kho.get('apple'))
            print("banana: ",kho.get('banana'))
            print("orange: ",kho.get('orange'))
    
# MUA HANG
    
        elif choice == "2":
            print("-- MUA HANG --\n")
            ten_sp = input("nhap ten san pham ban can mua: ").lower().strip()
            so_luong = int(input("nhap so luong ban can mua: "))
            if ten_sp in kho and so_luong <= kho.get(ten_sp):
                kho.update({ten_sp : kho.get(ten_sp) - so_luong})
                print("DA MUA!")

            elif ten_sp in kho and so_luong > kho.get(ten_sp):
                print("\n so luong hien tai khong du!")

            elif ten_sp not in kho:
                print("cua hang hien tai khong co sp ban tim!")
        
# THEM HANG


        elif choice == "3":
            print("-- THEM HANG --\n")
            ten_hang = input("nhap ten hang can them: ").strip().lower()
            so_luong_hang = int(input("nhao so luong hang can them: "))
            kho.update({ten_hang:so_luong_hang + kho.get(ten_hang)})
            print(f"{ten_hang} da them {so_luong_hang}!")

# XOA SAN PHAM


        elif choice == "4":
            print("-- XOA SAN PHAM --\n")
            ten_sp_xoa = input("nhap ten san pham can xoa: ").strip().lower()
        
            if ten_sp_xoa in kho:
                del kho[ten_sp_xoa]
                print(f"da xoa {ten_sp_xoa}!")

            else:
                print("san pham khong ton tai!")
    
# KIEM TRA SAN PHAM


        elif choice == "5":
            print("-- KIEM TRA SAN PHAM --\n")
            ten_sp_kt = input("nhap ten sp can kiem tra: ").strip().lower()
            if ten_sp_kt in kho:
                print(f"{ten_sp_kt} con {kho[ten_sp_kt]} qua")

            else:
                print("san pham nay khong ton tai!")
  
# THOAT  

        elif choice == "6":
            break
if __name__ == "__main__":
    menu()
