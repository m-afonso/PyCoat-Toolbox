import tkinter as tk
import numpy as np
from tkinter import messagebox
from typing import List, Dict, Tuple
from src.generate_replicates_elements import *


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

    # procedure widget
    procedure_label = tk.Label(ash_test_interface_window, justify='left',
                               text='''
                               Procedure:
                                 
                               1. Begin by weighing the crucible when it is empty. (M0)
                               2. Measure out 3-5g of the sample and place it into the crucible. (M1)
                               3. Place the crucible with the sample in an oven, either for 1h@120°C or for 3h@105°C.
                               4. Transfer the crucible and its contents to an ashing furnace and heat for 2h@600°C.
                               5. Once the process is complete, remove the crucible from the furnace and allow it to cool in a desiccator.
                               6. Finally, weigh the crucible with the remaining residues to complete the procedure. (M2)
                               
                               Ashes% = ((M2 - M0) / M1) * 100
                               
                               Reference: Brüggemann, Michael, and Anja Rach. Electrocoat. Vincentz Network, 2020.
                               '''.replace('                               ', '    '))

    procedure_label.grid(row=initial_row + replicates_number + 6, column=0, pady=10, columnspan=5, sticky="W")

    run_button = tk.Button(
        ash_test_interface_window,
        text="Run",
        command=lambda: get_values_replicates_elements(replicates_list,
                                                       mean_entry,
                                                       nv_ashes_test),
        width=15
    )

    run_button.grid(row=initial_row + replicates_number + 8, column=0, pady=25, padx=10)

    if master_window is None:
        ash_test_interface_window.mainloop()


if __name__ == '__main__':
    ash_test_interface()
