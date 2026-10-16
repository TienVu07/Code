fruits = {"apple", "pineappple", "coconut", "orange", "banana", "mango"}

fruit = input("enter a fruit to search for: ")

if fruit in fruits:
    print(f"{fruit} was found!")
else:
    print(f"{fruit} not found!")
