import json

def main():
    file = "closed"
    directory = "cat_closed"
    labels = []

    with open(file, "r") as fhandle:
        # parse x:
        y = json.load(fhandle)
        # the result is a Python dictionary:
        print(y)


if __name__ == "__main__":
    main()