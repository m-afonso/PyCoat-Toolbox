from copy import copy
import numpy as np
from typing import *
from bath import Bath
import tkinter as tk
from scipy.optimize import minimize
from adjustment import adjust_bath
<<<<<<< HEAD

=======
>>>>>>> 48f74ee70e67f4e17cb7778cec88d3303b068234

def interface_window():
    program_title = 'AutoPB'
    version = 'v0.0.1'
    release_date = '20240128'

    def on_submit():
        for entry in entries:
            print(entry.get())

    root = tk.Tk()
    root.title(program_title)

    # Função para criar uma caixa com título, três labels e entries
    def create_box(parent, title, labels):
        box_frame = tk.Frame(parent, padx=10, pady=10, borderwidth=2, relief="solid")

        # Adiciona o título à caixa
        title_label = tk.Label(box_frame, text=title, font=("Helvetica", 12, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=5)

        for i, label_text in enumerate(labels, start=1):
            label = tk.Label(box_frame, text=label_text)
            label.grid(row=i, column=0, sticky="e")

            entry = tk.Entry(box_frame)
            entry.grid(row=i, column=1, padx=5, pady=5)

            entries.append(entry)

        return box_frame

    # Lista de rótulos e títulos para cada caixa
    box_titles = ["Final Bath", "Initial Bath", "Paste", "Resin"]
    box_labels = [
        ["Weight", "NV", "P/B"],
        ["Weight", "NV", "P/B"],
        ["Weight", "Binder", "Pigment"],
        ["Weight", "Binder", "Pigment"]
    ]

    # Lista para armazenar as entries para facilitar o acesso posterior
    entries = []

    # Criação das quatro caixas
    for i, (title, labels) in enumerate(zip(box_titles, box_labels), start=1):
        box = create_box(root, title, labels)
        box.grid(row=0, column=(2 * i - 2), padx=10, pady=10)

        # Adicionar símbolo "+" entre as caixas, exceto após a última
        if i < len(box_titles):
            plus_label = tk.Label(root, text="+")
            plus_label.grid(row=0, column=(2 * i - 1))

    # Botões
    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.grid(row=1, column=0, columnspan=2, pady=10)

    exit_button = tk.Button(root, text="Exit", command=root.destroy)
    exit_button.grid(row=1, column=2, columnspan=2, pady=10)

    # version label
    info_label = tk.Label(root, text=f'{program_title} {version} {release_date}')
    info_label.grid(row=5, column=0, columnspan=7, pady=10)

    root.mainloop()


if __name__ == "__main__":
    interface_window()
