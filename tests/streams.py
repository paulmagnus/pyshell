with open("target01.py", "r") as f:
    print(type(f))
    for line in f:
        print(line, end="")