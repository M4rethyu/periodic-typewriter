import periodictable

symbols = [el.symbol for el in periodictable.elements if el.symbol[0].isupper()]

input_string = "python"


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


result = convert_string(input_string)
print(result)

result_string = ""
for rest, element_list in result:
    result_string += "".join(element_list) + (f"({rest})" if len(rest) >= 1 else "") + " "
print(result_string)

elements = {element.symbol: element for element in periodictable.elements}
for rest, element_list in result:
    for el in element_list:
        print(elements[el].name)


"""for el in periodictable.elements:
    rest, element_list = convert_string(el.name)[0]
    if rest == "":
        print("".join(element_list))"""
