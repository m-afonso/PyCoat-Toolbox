import tkinter as tk
import numpy as np
from tkinter import messagebox
from typing import List, Dict, Tuple
from src.generate_replicates_elements import *
from src.procedure_text import *


def nv_interface(master_window: tk.Tk | None = None) -> None:

    if master_window is None:
        nv_interface_window = tk.Tk()
    else:
        nv_interface_window = tk.Toplevel(master_window)

    nv_interface_window.title('Solids Content')

    initial_row = 1
    initial_column = 0
    replicates_number = 5
    replicates_list, mean_entry = generate_replicates_elements(
        nv_interface_window,
        _replicates_number=replicates_number,
        _initial_row=initial_row,
        _initial_column=initial_column,
        _head_titles=('Empty Cup (M0)', 'Sample (M1)', 'Residue + Cup (M2)', '%NV')
    )

    run_button = tk.Button(
        nv_interface_window,
        text="Run",
        command=lambda: get_values_replicates_elements(replicates_list,
                                                       mean_entry,
                                                       nv_ashes_test),
        width=15
    )
    run_button.grid(row=initial_row + replicates_number + 6, column=0, pady=25, padx=10)

    # procedure widget
    procedure_path = "../procedures/nv_test.txt"
    procedure_textbox(nv_interface_window,
                      _row=(initial_row + replicates_number + 7),
                      _column=0,
                      _procedure_path=procedure_path)

    if master_window is None:
        nv_interface_window.mainloop()


if __name__ == '__main__':
    nv_interface()
