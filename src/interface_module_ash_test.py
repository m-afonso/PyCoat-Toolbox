import tkinter as tk
import numpy as np
from tkinter import messagebox
from typing import List, Dict, Tuple
from src.generate_replicates_elements import *
from src.procedure_textbox import *


def ash_test_interface(master_window: tk.Tk | None = None) -> None:

    if master_window is None:
        ash_test_interface_window = tk.Tk()
    else:
        ash_test_interface_window = tk.Toplevel(master_window)

    ash_test_interface_window.title('Ash Test')

    initial_row = 1
    initial_column = 0
    replicates_number = 5
    replicates_list, mean_entry = generate_replicates_elements(
        ash_test_interface_window,
        _replicates_number=replicates_number,
        _initial_row=initial_row,
        _initial_column=initial_column,
        _head_titles=('Empty Crucible (M0)', 'Sample (M1)', 'Residue + Crucible (M2)', 'Ashes%')
    )

    run_button = tk.Button(
        ash_test_interface_window,
        text="Run",
        command=lambda: get_values_replicates_elements(replicates_list,
                                                       mean_entry,
                                                       nv_ashes_test),
        width=15
    )
    run_button.grid(row=initial_row + replicates_number + 6, column=0, pady=25, padx=10)

    # procedure widget
    procedure_path = "procedures/ashes_test.txt"
    procedure_textbox(ash_test_interface_window,
                      _row=(initial_row + replicates_number + 7),
                      _column=0,
                      _procedure_path=procedure_path)

    if master_window is None:
        ash_test_interface_window.mainloop()


if __name__ == '__main__':
    ash_test_interface()
