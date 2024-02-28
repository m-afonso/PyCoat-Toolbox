import tkinter as tk
from tkinter import ttk
import numpy as np


def nv_interface(master_window=None):

    if master_window is None:
        nv_interface_window = tk.Tk()
    else:
        nv_interface_window = tk.Toplevel(master_window)

    nv_interface_window.title('Non-volatile Calculator')

    initial_row = 1
    initial_column = 0

    def generate_replicates(replicates_number):
        nonlocal initial_row, initial_column

        # top labels
        replicate_label = tk.Label(nv_interface_window, text='Replicate ID')
        replicate_label.grid(row=initial_row, column=0, padx=25)
        zero_weight_label = tk.Label(nv_interface_window, text='Zero')
        zero_weight_label.grid(row=initial_row, column=1, padx=25)
        sample_weight_label = tk.Label(nv_interface_window, text='Sample')
        sample_weight_label.grid(row=initial_row, column=2, padx=25)
        final_weight_label = tk.Label(nv_interface_window, text='Final Weight')
        final_weight_label.grid(row=initial_row, column=3, padx=25)
        nv_label = tk.Label(nv_interface_window, text='NV%')
        nv_label.grid(row=initial_row, column=4, padx=25)

        replicates_list = list()

        for replicate in range(replicates_number):

            replicate_dict = {
                'id': tk.Label(nv_interface_window, text=str(replicate + 1)),
                'zero_entry': tk.Entry(nv_interface_window, justify='center'),
                'sample_entry': tk.Entry(nv_interface_window, justify='center'),
                'final_entry': tk.Entry(nv_interface_window, justify='center'),
                'result': tk.Entry(nv_interface_window, state='readonly', justify='center')
            }

            replicates_list.append(replicate_dict)

        padx_value = 25
        for replicate_number in range(len(replicates_list)):
            replicates_list[replicate_number]['id'].grid(row=initial_row + replicate_number + 1, column=initial_column,
                                                         padx=padx_value)
            replicates_list[replicate_number]['zero_entry'].grid(row=initial_row + replicate_number + 1,
                                                                 column=initial_column + 1, padx=padx_value)
            replicates_list[replicate_number]['sample_entry'].grid(row=initial_row + replicate_number + 1,
                                                                   column=initial_column + 2, padx=padx_value)
            replicates_list[replicate_number]['final_entry'].grid(row=initial_row + replicate_number + 1,
                                                                  column=initial_column + 3, padx=padx_value)
            replicates_list[replicate_number]['result'].grid(row=initial_row + replicate_number + 1,
                                                             column=initial_column + 4, padx=padx_value)

        # mean_label = tk.Label(nv_interface_window, text='Average')
        # mean_label.grid(row=initial_row + len(replicates_list), column=initial_column)
        mean_entry = tk.Entry(nv_interface_window, state='readonly', justify='center')
        mean_entry.grid(row=initial_row + len(replicates_list) + 1, column=initial_column + 4, padx=padx_value)

        return replicates_list, mean_entry

    replicates_number = 5
    replicates_list, mean_entry = generate_replicates(replicates_number)

    # procedure widget
    procedure_label = tk.Label(nv_interface_window, justify='left',
                               text='''
                               Procedure:

                               1. Begin by weighing the cup when it is empty. (M0)
                               2. Measure out 0.8-1.0g of the sample and place it into the cup. (M1)
                               3. Place the crucible with the sample in an oven, at test conditions.
                               5. Once the process is complete, remove the cup from the oven and allow it to cool in a desiccator.
                               6. Finally, weigh the cup with the remaining residues to complete the procedure. (M2)

                               NV% = ((M2 - M0) / M1) * 100

                               Reference: Brüggemann, Michael, and Anja Rach. Electrocoat. Vincentz Network, 2020.
                               '''.replace('                               ', '    '))

    procedure_label.grid(row=initial_row + replicates_number + 6, column=0, pady=10, columnspan=5, sticky="W")

    run_button = tk.Button(nv_interface_window, text="Run", command=lambda: get_values(), width=15)
    run_button.grid(row=initial_row + replicates_number + 8, column=0, pady=25, padx=10)

    def get_values():
        nv_results = list()
        nonlocal replicates_list
        nonlocal initial_column, initial_row, mean_entry

        for replicate in replicates_list:

            zero_value = float(replicate['zero_entry'].get()) if str.isnumeric(replicate['zero_entry'].get().replace(".", "")) else 0.0
            sample_value = float(replicate['sample_entry'].get()) if str.isnumeric(replicate['sample_entry'].get().replace(".", "")) else 0.0
            final_value = float(replicate['final_entry'].get()) if str.isnumeric(replicate['final_entry'].get().replace(".", "")) else 0.0

            if sample_value == 0 or zero_value == 0 or final_value == 0:
                continue

            replicate_result = (final_value - zero_value) / sample_value
            nv_results.append(replicate_result)
            replicate['result'].config(state='normal')
            replicate['result'].delete(0, 'end')
            replicate['result'].insert(0, f'{(replicate_result*100):.2f}')
            replicate['result'].config(state='readonly')

        if nv_results:
            nv_results_mean = np.mean(nv_results)
            nv_results_std = np.std(nv_results)
        else:
            return

        mean_entry.config(state='normal')
        mean_entry.delete(0, 'end')
        mean_entry.insert(0, f'{(nv_results_mean * 100):.2f} ± {(nv_results_std * 100):.2f}')
        mean_entry.config(state='readonly')

    if master_window is None:
        nv_interface_window.mainloop()


if __name__ == '__main__':
    nv_interface()
