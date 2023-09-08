import periodictable


symbols = [el.symbol for el in periodictable.elements if el.symbol[0].isupper()]
elements = {element.symbol: element for element in periodictable.elements}


def convert_word(string, element_list):
    paths = [convert_word(string[len(symbol):], element_list + [symbol]) for symbol in symbols if (len(symbol) <= len(string)) and string[:len(symbol)].lower() == symbol.lower()]
    paths.sort(key=lambda tuple_: len(tuple_[0]))
    if len(paths) >= 1:
        return paths[0]
    else:
        return string, element_list


def convert_string(string):
    words = string.split()
    converted_words = [convert_word(word, []) for word in words]
    return converted_words


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


if __name__ == "__main__":
    input_string = "python is neat"

    result = convert_string(input_string)

    print(print_string(result))
    print("")
    print(print_elements(result))

