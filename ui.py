import tkinter as tk
from PIL import Image, ImageTk

import parser


class PeriodicUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Periodic Typewriter")
        self.iconbitmap("./assets/PeriodicTypewriterIcon.ico")

        self.input_string = tk.StringVar()
        self.input_string.trace("w", self.input_callback)
        self.input_field = tk.Entry(self, textvariable=self.input_string, fg="black", bg="lightblue", width=50)
        self.input_field.grid(row=0, column=0)
        self.input_field.focus()

        self.arrow = tk.Label(self, text="->", width=2)
        self.arrow.grid(row=0, column=1)

        self.output_field = tk.Label(self, text="")
        self.output_field.grid(row=0, column=2)

        self.symbol_area = tk.Frame(self, bg="#231F20")
        self.symbol_area.grid(row=1, column=0, columnspan=3, sticky='news')
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.symbol_rows = []

    def input_callback(self, var, index, mode):
        input_string = self.input_string.get()
        parse_result = parser.convert_string(input_string)
        self.update_output(parse_result)

    def update_output(self, result):
        self.output_field.config(text=parser.print_string(result))
        for symbol_row in self.symbol_rows:
            symbol_row.destroy()
        self.symbol_rows = []

        for rest, element_list in result:
            symbol_row = SymbolRow(self.symbol_area, element_list, 200)
            symbol_row.pack()
            self.symbol_rows.append(symbol_row)

        self.geometry("")


class Symbol(tk.Label):
    def __init__(self, parent, symbol, size=200):
        path = f"assets/element_icons/{symbol}.png"
        self.img = ImageTk.PhotoImage(Image.open(path).resize((size, size)))
        super().__init__(
            parent,
            image=self.img, bg="#231F20"
        )


class SymbolRow(tk.Frame):
    def __init__(self, parent, symbols, size=200):
        super().__init__(parent)
        self.symbols = []
        for i, sy in enumerate(symbols):
            symbol = Symbol(self, sy, size)
            symbol.grid(row=0, column=i)
            self.symbols.append(symbol)


if __name__ == "__main__":
    root = PeriodicUI()
    root.input_string.set("python is neat")
    root.mainloop()