import periodictable
from main import convert_string


if __name__ == "__main__":
    for el in periodictable.elements:
        rest, element_list = convert_string(el.name)[0]
        if rest == "":
            print("".join(element_list))
