#bai tap ve vong lap while,if elif else


def menu():
    while True:
        print("-- MENU --")
        print("1. Nhap thong tin user")
        print("2. Tim trai cay")
        print("3. Thoat")
        
        choice = input("nhap: ")

# NHAP THONG TIN USER:))
       
        if choice == "1":
            print("-- NHAP THONG TIN --")

# NHAP TEN

            while True:
                name = input("nhap ten cua ban: ").strip()

                if name.replace(" ", "").isalpha():
                    break
                else:
                    print("vui long nhap lai!")

# NHAP TUOI

            while True:
                age = input("nhap tuoi cua ban: ").strip()
                
                if age.isdigit():
                    age = int(age)
                    break
                else:
                    print("vui long nhap lai!")

# NHAP VE

            ticket = input("ban da co ve chua?(true/false): ").strip().lower() == "true"

# KET QUA

            print(f"Name: {name}")
            print(f"Age: {age}")
            print(f"Has ticket: {int(ticket)}")

            if age < 18 and not ticket:
                print("Access denied")
        


# TIM TRAI CAY

        elif choice == "2":
            print("-- TIM TRAI CAY --")
            fruits = {"apple", "banana", "mango", "orange", "coconut"}
            fruit = input("nhap ten trai ban can tim(en): ").strip()
            if fruit in fruits:
                print(f"{fruit} was found!")
            else:
                print(f"{fruit} not found!")

# THOAT

        elif choice == "3":
            break

if __name__ == "__main__":
    menu()
