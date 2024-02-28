import tkinter as tk
from src.interface_module_pb_nv_adj import *
from src.interface_module_nv import *
from src.interface_module_ash_test import *
from src.interface_module_pb import *
def main_interface():
    program_title = 'PyCoat Wizard'
    version = 'v0.1.0'
    release_date = '2024-02-28'

    main_interface_window = tk.Tk()
    main_interface_window.title(program_title)

    # general section
    general_section_label = tk.Label(main_interface_window, text=f'General Modules')

    nv_button = tk.Button(main_interface_window, text="Solids Content", command=lambda: nv_interface(main_interface_window), height=2, width=25)

    # electrocoat section
    ed_section_label = tk.Label(main_interface_window, text='Electrocoat Modules')
    ash_button = tk.Button(main_interface_window, text='Ash Test', command=lambda: ash_test_interface(main_interface_window), height=2, width=25)
    pb_button = tk.Button(main_interface_window, text="Pigment-to-binder ratio", command=lambda: pb_interface(main_interface_window), height=2, width=25)

    pb_nv_adj_button = tk.Button(
        main_interface_window,
        text="P/B and NV Adjustment",
        command=lambda: pb_nv_adj_interface_window(main_interface_window),
        height=2, width=25
    )

    # window control section
    exit_button = tk.Button(main_interface_window, text="Exit", command=main_interface_window.destroy)

    # infos section
    info_label = tk.Label(main_interface_window, text=f'{program_title} {version} {release_date}')

    # grid settings
    general_section_label.grid(row=0, column=0, pady=10, padx=50)
    nv_button.grid(row=1, column=0, pady=10, padx=50)

    ed_section_label.grid(row=0, column=1, pady=10, padx=50)
    ash_button.grid(row=1, column=1, pady=10, padx=50)
    pb_button.grid(row=2, column=1, pady=10, padx=50)
    pb_nv_adj_button.grid(row=3, column=1, pady=10, padx=50)


    # exit_button.grid(row=30, column=0, pady=10, padx=50)
    info_label.grid(row=31, column=0, pady=20, padx=50, columnspan=2)

    main_interface_window.mainloop()


if __name__ == '__main__':
    main_interface()