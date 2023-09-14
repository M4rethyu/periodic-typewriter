import sys, os

import tkinter as tk
from PIL import Image, ImageTk

import parser


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class PeriodicUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Periodic Typewriter - M4rethyu")
        self.iconbitmap(resource_path("assets/PeriodicTypewriterIcon.ico"))
        self.bind("<Configure>", self.on_resize)
        self.geometry("")

        self.input_field = tk.Text(self, fg="black", bg="lightblue", width=50, height=6)
        self.input_field.tag_configure("grey", foreground="grey")
        self.input_field.bind('<KeyRelease>', self.input_callback)
        self.input_field.grid(row=0, column=0)
        self.input_field.focus()

        def keyboard_callback(letter):
            self.input_field.insert("end -2 chars", letter)
            self.input_callback(None)

        self.keyboard = ScreenKeyboard(self, command=keyboard_callback)
        self.keyboard.grid(row=0, column=1, padx=10)

        self.element_list_string = tk.StringVar()
        self.element_list_field = tk.Text(self, wrap="word", width=50, height=6)
        self.element_list_field.configure(state="disabled")
        self.element_list_field.grid(row=0, column=2, columnspan=2)

        self.symbol_area = tk.Text(self, bg="#231F20", yscrollcommand=lambda *args: self.symbol_area_scroll_bar.set(*args))
        self.symbol_rows = []
        self.symbol_area.grid(row=2, column=0, columnspan=3, sticky='news')
        self.symbol_area_scroll_bar = tk.Scrollbar(self, command=self.symbol_area.yview)
        self.symbol_area_scroll_bar.grid(row=2, column=3, rowspan=2, sticky="nes")

        self.group_area = tk.Text(self, bg="#231F20", height=6)
        self.groups = []
        self.group_area.grid(row=3, column=0, columnspan=3, sticky='news')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)

    def on_resize(self, event):
        print("resized!")

    def input_callback(self, event):
        input_string = self.input_field.get("1.0", tk.END).rstrip("\n")
        self.update_output(input_string)

    def update_output(self, input_string):
        # parse input
        result, separators, continuation = parser.parse_string(input_string)

        #select path from each word in result (path that leaves the least rest, or if 2 are the same, then the one that uses fewer symbols)
        final_paths = []
        for word in result:
            final_path = word[0]
            for path in word:
                if len(path.rest) < len(final_path.rest):
                    final_path = path
                elif len(path.rest) == len(final_path.rest) and len(path) < len(final_path):
                    final_path = path
            final_paths.append(final_path)

        # save cursor and selection
        cursor_position = self.input_field.index("insert")
        selection_range = self.input_field.tag_ranges("sel")

        self.input_field.delete("1.0", tk.END)
        for i, path in enumerate(final_paths):
            self.input_field.insert(tk.END, "".join(element.symbol for element in path))
            self.input_field.insert(tk.END, path.rest, "grey")
            if i < len(separators):
                self.input_field.insert(tk.END, separators[i], "grey")
        self.input_field.insert(tk.END, "\n")
        num_newlines = sum(separator.count("\n") for separator in separators) + 1
        self.input_field.configure(height=max(6, num_newlines+1))

        # restore cursor and selection
        self.input_field.mark_set("insert", cursor_position)
        if len(selection_range) > 0:
            self.input_field.tag_add("sel", *selection_range)

        # write list of elements
        self.element_list_field.configure(state='normal')
        self.element_list_field.delete("1.0", tk.END)
        element_list = []
        for path in final_paths:
            for element in path:
                element_list.append(element.element.name)
        self.element_list_field.insert("1.0", ", ".join(element_list))
        self.element_list_field.configure(state='disabled')

        # resize element list to fit all elements
        height = self.element_list_field.tk.call((self.element_list_field._w, "count", "-update", "-displaylines", "1.0", "end"))
        self.element_list_field.configure(height=max(6, height))

        # set state of keyboard
        self.keyboard.set_keys_status(continuation)

        # delete previous symbol_rows
        for symbol_row in self.symbol_rows:
            symbol_row.destroy()
        self.symbol_rows = []

        # create a new symbol_row for each word
        displayed_groups = set()
        self.symbol_area.configure(state="normal")
        for element_list in final_paths:
            symbol_row = SymbolRow(self.symbol_area, element_list, 200)
            self.symbol_area.window_create("insert", window=symbol_row, padx=10, pady=10)
            self.symbol_rows.append(symbol_row)
            displayed_groups.update(symbol.get_group() for symbol in symbol_row.symbols)  # track groups of all displayed symbols
        self.symbol_area.configure(state="disabled")

        # delete previous groups
        for group in self.groups:
            group.destroy()
        self.groups = []

        # show all groups which contain displayed symbols
        self.group_area.configure(state="normal")
        i = 0
        for group_name in displayed_groups:
            group = Group(self.group_area, group_name, 100)
            self.group_area.window_create("insert", window=group, padx=1, pady=1)
            self.groups.append(group)
            i += 1
        self.group_area.configure(state="disabled")

        height = self.group_area.tk.call((self.group_area._w, "count", "-update", "-displaylines", "1.0", "end"))
        print(height)
        self.group_area.configure(height=max(1, 6*height))


class Symbol(tk.Label):
    def __init__(self, parent, symbol, size=200):
        self.symbol = symbol
        path = resource_path(f"assets/element_icons/{symbol}.png")
        self.img = ImageTk.PhotoImage(Image.open(path).resize((size, size)))
        super().__init__(
            parent,
            image=self.img, bg="#231F20"
        )

    def get_group(self):
        n = self.symbol.element.number
        if n in (3, 11, 19, 37, 55, 87):
            group = "alkali_metal"
        elif n in (4, 12, 20, 38, 56, 88):
            group = "alkaline_earth"
        elif n in (13, 31, 49, 50, 81, 82, 83, 113, 114, 115, 116):
            group = "basic_metal"
        elif n in (5, 14, 32, 33, 51, 52, 84):
            group = "semimetal"
        elif n in (1, 6, 7, 8, 15, 16, 34):
            group = "nonmetal"
        elif n in (9, 17, 35, 53, 85, 117):
            group = "halogen"
        elif n in (2, 10, 18, 36, 54, 86, 118):
            group = "noble_gas"
        elif 57 <= n <= 71:
            group = "lanthanide"
        elif 89 <= n <= 103:
            group = "actinide"
        else:
            group = "transition_metal"
        return group

class SymbolRow(tk.Frame):
    def __init__(self, parent, symbols, size=200):
        super().__init__(parent)
        self.symbols = []
        for i, sy in enumerate(symbols):
            symbol = Symbol(self, sy, size)
            symbol.grid(row=0, column=i)
            self.symbols.append(symbol)


class Group(tk.Label):
    def __init__(self, parent, group, size=100):
        path = resource_path(f"assets/element_groups/{group}.png")
        self.img = ImageTk.PhotoImage(Image.open(path).resize((size*2, size)))
        super().__init__(
            parent,
            image=self.img, bg="#231F20"
        )


class ScreenKeyboard(tk.Canvas):
    def __init__(self, *args, **kwargs):
        if "command" in kwargs:
            self.command = kwargs["command"]
            kwargs.pop("command")

        super().__init__(*args, **kwargs)
        self.rows = []
        self.keys = {}
        for i, letters in enumerate(("qwertzuiop", "asdfghjkl", "yxcvbnm")):
            row = tk.Frame(self)
            spacer = tk.Frame(row)
            spacer.grid(row=0, column=0, padx=({0: 0, 1: 4, 2: 10}[i]))
            for j, letter in enumerate(letters):
                key = tk.Button(row, text=letter.upper(), command=self.get_function(letter), width=2, height=1)
                key.grid(row=0, column=j+1)
                self.keys[letter] = key
            row.pack(anchor="w")
            self.rows.append(row)

    def get_function(self, letter):
        return lambda : self.key_callback(letter)

    def key_callback(self, letter):
        if self.command:
            self.command(letter)

    def set_keys_status(self, key_list):
        # set keys in key_list active, all others inactive
        for letter, key in self.keys.items():
            if letter in key_list:
                key.configure(state=tk.NORMAL)
            else:
                key.configure(state=tk.DISABLED)

if __name__ == "__main__":
    root = PeriodicUI()
    #root.input_string.set("python is neat")
    root.mainloop()
