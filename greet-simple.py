with open("names.txt") as file:
    for line in file:
        if name := line.strip():
            print(f"Hello, {name}!")
