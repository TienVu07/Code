import baitap
import baitap2
import baitap3

options = [
        "1. Bai tap 1",
        "2. Bai tap 2",
        "3. Bai tap 3",
        "4. Thoat"
        ]
   

def main():
    while True:
        print("-- MENU --")
        for option in options:
            print(option)
        choice = input("\n>  ")

        if choice == "1":
            baitap.menu()
            input("Press Enter to continue...")
        elif choice == "2":
            baitap2.menu()
            input("Press Enter to continue...")
        elif choice == "3":
            baitap3.menu()
            input("Press Enter to continue...")
        elif choice == "4":
            break
        else:
            print("?")

if __name__ == "__main__":
    main()
