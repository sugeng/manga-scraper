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


