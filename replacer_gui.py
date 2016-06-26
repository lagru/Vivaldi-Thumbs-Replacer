#!/usr/bin/env python

"""
GUI implementation of the Replacer
"""

import tkinter as tk


class Application(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(padx=10, pady=10, sticky=tk.N+tk.S+tk.E+tk.W)

        # create widgets
        self.bookmark_label = tk.Label(self, text="Bookmarks")
        self.thumbnail_label = tk.Label(self, text="Thumbnails")
        self.bookmark_list = tk.Listbox(self)
        self.thumbnail_list = tk.Listbox(self)
        self.path_button = tk.Button(
            self, text="Edit Paths", padx=10, command=edit_paths
        )
        self.replace_button = tk.Button(
            self, text="Replace", padx=10, command=replace
        )

        self.init_layout()

    def init_layout(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        # configure grid
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # place widgets
        self.bookmark_label.grid(row=0, column=0, sticky=tk.NW)
        self.thumbnail_label.grid(row=0, column=1, sticky=tk.NW)
        self.bookmark_list.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.thumbnail_list.grid(row=1, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
        self.path_button.grid(row=2, column=0, sticky=tk.S)
        self.replace_button.grid(row=2, column=1, sticky=tk.S)


def edit_paths():
    print("edit_paths()")


def replace():
    print("replace()")


def main():
    app = Application()
    app.master.title("Vivaldi Thumbnail Replacer")
    app.mainloop()


if __name__ == "__main__":
    main()