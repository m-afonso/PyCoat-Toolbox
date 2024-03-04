import tkinter as tk


def procedure_textbox(
    nv_interface_window: tk.Tk, _row: int, _column: int, _procedure_path: str
) -> None:

    try:
        with open(_procedure_path, "r", encoding="utf-8") as file:
            _procedure_text = file.read()
        procedure_label = tk.Label(
            nv_interface_window, justify="left", text=_procedure_text
        )

        procedure_label.grid(
            row=_row, column=_column, pady=10, padx=10, columnspan=5, sticky="W"
        )
    except FileNotFoundError:
        pass
