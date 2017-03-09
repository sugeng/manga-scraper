import re


def parse_dash(choices):
    if re.search('-', choices):
        data = []
        for choice in choices.split('-'):
            choice = choice.strip()
            data.append(int(choice))

        return data

    pass


def parse_comma(choices):
    if re.search(',', choices):
        data = []
        for choice in choices.split(','):
            choice = choice.strip()
            data.append(int(choice))

        return data

    pass


methods = {
    'dash': parse_dash,
    'comma': parse_comma
}


def parse_input(choices):
    for parse in methods:
        chapters = methods[parse](choices)
        if chapters is not None:
            print(chapters)


chap = parse_input("1, 3, 20, 200")

# print(chap)
