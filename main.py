from copy import copy
import numpy as np
from typing import *
from bath import Bath
import tkinter as tk
from scipy.optimize import minimize
from adjustment import adjust_bath


def interface_window():
    program_title = 'AutoPB'
    version = 'v0.0.1'
    release_date = '20240128'

    target_bath = Bath()
    initial_bath = Bath()
    paste = Bath()
    resin = Bath()
    water = Bath()

    def on_submit():
        nonlocal target_bath, initial_bath, paste, resin, water
        for entry in entries:
            print(entry.get())

        try:
            target_bath = Bath(float(target_bath_frame_w_entry.get()),
                               float(target_bath_frame_nv_entry.get()),
                               float(target_bath_frame_pb_entry.get()))
            initial_bath = Bath(0,
                                float(initial_bath_frame_nv_entry.get()),
                                float(initial_bath_frame_pb_entry.get()))
            paste = Bath(0, 0, 0)
            paste.binder = float(paste_frame_binder_entry.get())
            paste.pigment = float(paste_frame_pigment_entry.get())
            resin = Bath(0, 0, 0)
            resin.binder = float(resin_frame_binder_entry.get())
            water = Bath(0, 0, 0)

            results = adjust_bath(target_bath, initial_bath, resin, paste, water)

            initial_bath_frame_w_entry.config(state="normal")
            initial_bath_frame_w_entry.delete(0, tk.END)
            initial_bath_frame_w_entry.insert(0, '{:.2f}'.format(results['initial_bath'].weight))
            initial_bath_frame_w_entry.config(state="readonly")

            paste_frame_w_entry.config(state="normal")
            paste_frame_w_entry.delete(0, tk.END)
            paste_frame_w_entry.insert(0, '{:.2f}'.format(results['paste'].weight))
            paste_frame_w_entry.config(state="readonly")

            resin_frame_w_entry.config(state="normal")
            resin_frame_w_entry.delete(0, tk.END)
            resin_frame_w_entry.insert(0, '{:.2f}'.format(results['resin'].weight))
            resin_frame_w_entry.config(state="readonly")

            water_frame_w_entry.config(state="normal")
            water_frame_w_entry.delete(0, tk.END)
            water_frame_w_entry.insert(0, '{:.2f}'.format(results['water'].weight))
            water_frame_w_entry.config(state="readonly")
        except:
            pass

    root = tk.Tk()
    root.title(program_title)

    entries = []
    labels = []

    # Criação da caixa "Target Bath"
    target_bath_frame = tk.Frame(root, padx=10, pady=10, borderwidth=2, relief="solid")
    target_bath_label = tk.Label(target_bath_frame, text="Target Bath", font=("Helvetica", 12, "bold"))
    target_bath_label.grid(row=0, column=0, columnspan=2, pady=5)

    target_bath_frame_w_label = tk.Label(target_bath_frame, text="Weight")
    target_bath_frame_w_label.grid(row=1, column=0, sticky="e")
    target_bath_frame_w_entry = tk.Entry(target_bath_frame)
    target_bath_frame_w_entry.insert(0, "0")
    target_bath_frame_w_entry.grid(row=1, column=1, padx=5, pady=5)

    target_bath_frame_nv_label = tk.Label(target_bath_frame, text="NV")
    target_bath_frame_nv_label.grid(row=2, column=0, sticky="e")
    target_bath_frame_nv_entry = tk.Entry(target_bath_frame)
    target_bath_frame_nv_entry.insert(0, "0")
    target_bath_frame_nv_entry.grid(row=2, column=1, padx=5, pady=5)

    target_bath_frame_pb_label = tk.Label(target_bath_frame, text="P/B")
    target_bath_frame_pb_label.grid(row=3, column=0, sticky="e")
    target_bath_frame_pb_entry = tk.Entry(target_bath_frame)
    target_bath_frame_pb_entry.insert(0, "0")
    target_bath_frame_pb_entry.grid(row=3, column=1, padx=5, pady=5)

    target_bath_frame.grid(row=0, column=0, padx=10, pady=10)

    symbol_label = tk.Label(root, text="=")
    symbol_label.grid(row=0, column=1)

    # Criação da caixa "Initial Bath"
    initial_bath_frame = tk.Frame(root, padx=10, pady=10, borderwidth=2, relief="solid")
    initial_bath_label = tk.Label(initial_bath_frame, text="Initial Bath", font=("Helvetica", 12, "bold"))
    initial_bath_label.grid(row=0, column=0, columnspan=2, pady=5)

    initial_bath_frame_w_label = tk.Label(initial_bath_frame, text="Weight")
    initial_bath_frame_w_label.grid(row=1, column=0, sticky="e")
    initial_bath_frame_w_entry = tk.Entry(initial_bath_frame)
    initial_bath_frame_w_entry.insert(0, "0")
    initial_bath_frame_w_entry.grid(row=1, column=1, padx=5, pady=5)
    initial_bath_frame_w_entry.config(state="readonly")

    initial_bath_frame_nv_label = tk.Label(initial_bath_frame, text="NV")
    initial_bath_frame_nv_label.grid(row=2, column=0, sticky="e")
    initial_bath_frame_nv_entry = tk.Entry(initial_bath_frame)
    initial_bath_frame_nv_entry.insert(0, "0")
    initial_bath_frame_nv_entry.grid(row=2, column=1, padx=5, pady=5)

    initial_bath_frame_pb_label = tk.Label(initial_bath_frame, text="P/B")
    initial_bath_frame_pb_label.grid(row=3, column=0, sticky="e")
    initial_bath_frame_pb_entry = tk.Entry(initial_bath_frame)
    initial_bath_frame_pb_entry.insert(0, "0")
    initial_bath_frame_pb_entry.grid(row=3, column=1, padx=5, pady=5)

    initial_bath_frame.grid(row=0, column=2, padx=10, pady=10)

    symbol_label = tk.Label(root, text="+")
    symbol_label.grid(row=0, column=3)

    # Criação da caixa "Paste"
    paste_frame = tk.Frame(root, padx=10, pady=10, borderwidth=2, relief="solid")
    paste_label = tk.Label(paste_frame, text="Paste", font=("Helvetica", 12, "bold"))
    paste_label.grid(row=0, column=0, columnspan=2, pady=5)

    paste_frame_w_label = tk.Label(paste_frame, text="Weight")
    paste_frame_w_label.grid(row=1, column=0, sticky="e")
    paste_frame_w_entry = tk.Entry(paste_frame)
    paste_frame_w_entry.insert(0, "0")
    paste_frame_w_entry.grid(row=1, column=1, padx=5, pady=5)
    paste_frame_w_entry.config(state="readonly")

    paste_frame_binder_label = tk.Label(paste_frame, text="Binder")
    paste_frame_binder_label.grid(row=2, column=0, sticky="e")
    paste_frame_binder_entry = tk.Entry(paste_frame)
    paste_frame_binder_entry.insert(0, "0")
    paste_frame_binder_entry.grid(row=2, column=1, padx=5, pady=5)

    paste_frame_pigment_label = tk.Label(paste_frame, text="Pigment")
    paste_frame_pigment_label.grid(row=3, column=0, sticky="e")
    paste_frame_pigment_entry = tk.Entry(paste_frame)
    paste_frame_pigment_entry.insert(0, "0")
    paste_frame_pigment_entry.grid(row=3, column=1, padx=5, pady=5)

    paste_frame.grid(row=0, column=4, padx=10, pady=10)

    symbol_label = tk.Label(root, text="+")
    symbol_label.grid(row=0, column=5)

    # Criação da caixa "Resin"
    resin_frame = tk.Frame(root, padx=10, pady=10, borderwidth=2, relief="solid")
    resin_label = tk.Label(resin_frame, text="Resin", font=("Helvetica", 12, "bold"))
    resin_label.grid(row=0, column=0, columnspan=2, pady=5)

    resin_frame_w_label = tk.Label(resin_frame, text="Weight")
    resin_frame_w_label.grid(row=1, column=0, sticky="e")
    resin_frame_w_entry = tk.Entry(resin_frame)
    resin_frame_w_entry.insert(0, "0")
    resin_frame_w_entry.grid(row=1, column=1, padx=5, pady=5)
    resin_frame_w_entry.config(state="readonly")

    resin_frame_binder_label = tk.Label(resin_frame, text="Binder")
    resin_frame_binder_label.grid(row=2, column=0, sticky="e")
    resin_frame_binder_entry = tk.Entry(resin_frame)
    resin_frame_binder_entry.insert(0, "0")
    resin_frame_binder_entry.grid(row=2, column=1, padx=5, pady=5)

    resin_frame.grid(row=0, column=6, padx=10, pady=10)

    symbol_label = tk.Label(root, text="+")
    symbol_label.grid(row=0, column=7)

    # Criação da caixa "Water"
    water_frame = tk.Frame(root, padx=10, pady=10, borderwidth=2, relief="solid")
    water_label = tk.Label(water_frame, text="Water", font=("Helvetica", 12, "bold"))
    water_label.grid(row=0, column=0, columnspan=2, pady=5)

    water_frame_w_label = tk.Label(water_frame, text="Weight")
    water_frame_w_label.grid(row=1, column=0, sticky="e")
    water_frame_w_entry = tk.Entry(water_frame)
    water_frame_w_entry.insert(0, "0")
    water_frame_w_entry.grid(row=1, column=1, padx=5, pady=5)
    water_frame_w_entry.config(state="readonly")

    water_frame.grid(row=0, column=8, padx=10, pady=10)

    # Botões
    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.grid(row=1, column=0, columnspan=2, pady=10)

    exit_button = tk.Button(root, text="Exit", command=root.destroy)
    exit_button.grid(row=1, column=2, columnspan=2, pady=10)

    # version label
    info_label = tk.Label(root, text=f'{program_title} {version} {release_date}')
    info_label.grid(row=5, column=0)

    root.mainloop()

if __name__ == "__main__":
    interface_window()
