import periodictable
import re


elements = {element.symbol: element for element in periodictable.elements if not element.symbol == "n"}
symbols = list(elements.keys())

class Element:
    def __init__(self, symbol):
        self.symbol = symbol
        self.element = elements[symbol]

    def __str__(self):
        return self.symbol


class Path(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rest = ""

    def set_rest(self, rest):
        self.rest = rest

    def __add__(self, other):
        return Path(super().__add__(other))


def parse_word(word, path):
    if len(word) == 0:
        path.set_rest("")
        return [path]

    paths = []
    for symbol in symbols:
        if len(word) >= len(symbol):
            if word[:len(symbol)] == symbol.lower():
                paths.extend(parse_word(word[len(symbol):], path + [Element(symbol)]))
    if len(paths) >= 1:
        return paths
    else:
        path.set_rest(word)
        return [path]


def parse_string(string):
    match = re.split(r'(\W+)', string)
    words = [w.lower() for w in match[::2]]
    separators = match[1::2]

    parsed_words = [parse_word(word, Path()) for word in words]
    last_word = parsed_words[-1]
    continuation = []
    if any(path.rest == "" for path in last_word):
        continuation = [symbol[0].lower() for symbol in symbols]
    for path in last_word:
        if len(path.rest) == 1:
            continuation.extend(symbol[1] for symbol in symbols if len(symbol) == 2 and symbol[0].lower() == path.rest)
    continuation = list(set(continuation))
    return parsed_words, separators, continuation


def print_string(result):
    result_string = ""
    for rest, element_list in result:
        result_string += "".join(element_list) + (f"({rest})" if len(rest) >= 1 else "") + " "
    return result_string


def print_elements(result):
    element_string = ""
    for rest, element_list in result:
        for el in element_list:
            element_string += elements[el].name + "\n"
        element_string += "\n"
    return element_string


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        s = f.read()
    r, sep, _ = parse_string(s.lower())
    sr = ""
    el = []
    for i, w in enumerate(r):
        if len(w) > 0:
            p = sorted(w, key=lambda x: x.rest)[0]
            for sy in p:
                sr += sy.symbol
                el.append(sy.element.name)
        sr += (sep[i] if i < len(sep) else "")

    out = sr + "\n\n" + "\n".join(el)
    print(out)
    with open("output.txt", "w") as f:
        f.write(out)

