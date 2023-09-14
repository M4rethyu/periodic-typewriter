import periodictable
from parser import parse_string


if __name__ == "__main__":
    sr = ""
    for el in periodictable.elements:
        s = el.name
        r, sep, _ = parse_string(s.lower())
        for i, w in enumerate(r):
            if len(w) > 0:
                p = sorted(w, key=lambda x: x.rest)[0]
                if len(p.rest) > 0:
                    continue
                for sy in p:
                    sr += sy.symbol
                sr += "\n"
    print(sr)