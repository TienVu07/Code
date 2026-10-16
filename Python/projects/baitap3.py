# Du lieu dau vao(dict)
kho = {
    "ao": {"ton": 10, "ban": 5},
    "quan": {"ton": 8, "ban": 4},
    "giay": {"ton": 6, "ban": 6}
}
#menu chuc nang(list)
options = [
        "1. Xem kho",
        "2. Them hang moi",
        "3. Nhap them hang",
        "4. Ban hang",
        "5. Xoa hang",
        "6. Phan tich kho",
        "7. Thoat"
        ]

# NHAP SO

def nhap_so(text):
    while True:
        so = input(text)
        if so.isdigit() and int(so) > 0:
            return int(so)
        
        print("vui long nhap lai!")

# 1. XEM KHO

def xem_kho():
    print("-- KHO HANG --\n")

    if not kho:
        print("khong co mat hang nao trong kho!")
        return
    for hang, du_lieu in kho.items():
        ton = du_lieu["ton"]
        ban = du_lieu["ban"]
        print(f"{hang}:ton {ton}|ban {ban} ")

# 2. THEM HANG

def them_hang():
    print("-- THEM HANG --")

    ten_hang_moi = input("Ten hang moi: ").strip().lower()
        
    if ten_hang_moi in kho:
        print("MAT HANG DA TON TAI!")
    else:
        so_luong_hang_moi = nhap_so("So luong hang moi: ")
        kho[ten_hang_moi] = {
                "ton": so_luong_hang_moi,
                "ban": 0
                    }
        print("DONE!")

# 3.NHAP HANG

def nhap_hang():
    print("-- NHAP HANG --")
    ten_nhap_hang = input("nhap ten hang can nhap: ").strip().lower()
    if ten_nhap_hang not in kho:
        print("Chua co mat hang nay!")
    else:
            so_luong_hang_nhap = nhap_so("so luong hang: ")
            kho[ten_nhap_hang]["ton"] += so_luong_hang_nhap
                #memories: bug xD
                #kho[ten_nhap_hang]["ban"] += 0
                
            print("DONE!")

# 4. BAN HANG

def ban_hang():
    print("-- BAN HANG --")
        
    ten_hang_ban = input("nhap ten hang can ban: ").strip().lower()
    if ten_hang_ban not in kho:
        print("Hien chua co mat hang nay!")
    else:
        so_luong_ban_hang = nhap_so("nhap so luong hang can ban: ")
        if so_luong_ban_hang > kho[ten_hang_ban]["ton"]:
            print("Mat hang khong du!")
        else:
            kho[ten_hang_ban]["ton"] -= so_luong_ban_hang
            kho[ten_hang_ban]["ban"] += so_luong_ban_hang
            print("DONE!")

# 5. XOA HANG

def xoa_hang():
    print("-- XOA HANG --")
    ten_hang_xoa = input("nhap ten hang can xoa: ").strip().lower()
    if ten_hang_xoa not in kho:
        print("Hang nay khong ton tai!")
    else:
        del kho[ten_hang_xoa]
        print("DONE!")

# 6. PHAN TICH KHO

def phan_tich_kho():
    print("-- PHAN TICH KHO --")
    max_hieu_suat = -1
    best_sp = ""
    for hang, du_lieu in kho.items():
        ton = du_lieu["ton"]
        ban = du_lieu["ban"]
        tong = ton + ban
        if tong == 0:
            print("du lieu khong hop le!")
        else:
            hieu_suat = ban / tong
            if hieu_suat > max_hieu_suat:
                max_hieu_suat = hieu_suat
                best_sp = hang
    print(f"\n Mat hang ban chay nhat la:{best_sp}")
    print(f"Hieu suat cao nhat:{max_hieu_suat}")

def menu():
    while True:
        print("\n=== MENU ===")
    
        for option in options:
            print(option)

        choice = input("\n> ")


        if choice == "1":
            xem_kho()
        elif choice == "2":
            them_hang()
        elif choice == "3":
            nhap_hang()
        elif choice == "4":
            ban_hang()
        elif choice == "5":
            xoa_hang()
        elif choice == "6":
            phan_tich_kho()
        elif choice == "7":
            break
        else:
            print("???")
if __name__ == "__main__":
    menu()        
