import tkinter as tk
import numpy as np
from tkinter import messagebox
from typing import List, Dict, Tuple


def nv_ashes_test(
    empty: float | int, sample: float | int, final: float | int
) -> float | None:

    if not isinstance(empty, (float, int)):
        raise TypeError("Empty weight must be a decimal or integer number.")

    if not isinstance(sample, (float, int)):
        raise TypeError("Final weight must be a decimal or integer number.")

    if not isinstance(sample, (float, int)):
        raise TypeError("Sample weight must be a decimal or integer number.")

    if final < empty:
        raise ValueError("\n\nFinal weight must be greater or equal to empty weight.")

    if sample <= 0:
        raise ValueError("\n\nSample weight must be greater than zero.")

    return (final - empty) / sample


def generate_replicates_elements(
    interface_window,
    _replicates_number: int = 5,
    _initial_row: int = 0,
    _initial_column: int = 0,
    _head_titles: Tuple[str, str, str, str] = ("Empty", "Sample", "Final", "Result"),
):

    _replicates_list = list()

    # head labels
    replicate_label = tk.Label(interface_window, text="Replicate ID")
    replicate_label.grid(row=_initial_row, column=0, padx=25)

    empty_weight_label = tk.Label(interface_window, text=_head_titles[0])
    empty_weight_label.grid(row=_initial_row, column=1, padx=25)

    sample_weight_label = tk.Label(interface_window, text=_head_titles[1])
    sample_weight_label.grid(row=_initial_row, column=2, padx=25)

    final_weight_label = tk.Label(interface_window, text=_head_titles[2])
    final_weight_label.grid(row=_initial_row, column=3, padx=25)

    result_label = tk.Label(interface_window, text=_head_titles[3])
    result_label.grid(row=_initial_row, column=4, padx=25)

    for replicate in range(_replicates_number):
        replicate_dict = {
            "id": tk.Label(interface_window, text=str(replicate + 1)),
            "zero_entry": tk.Entry(interface_window, justify="center"),
            "sample_entry": tk.Entry(interface_window, justify="center"),
            "final_entry": tk.Entry(interface_window, justify="center"),
            "result": tk.Entry(interface_window, state="readonly", justify="center"),
        }

        _replicates_list.append(replicate_dict)

    padx_value = 25

    for replicate_number in range(len(_replicates_list)):
        _replicates_list[replicate_number]["id"].grid(
            column=_initial_column,
            row=_initial_row + replicate_number + 1,
            padx=padx_value,
        )

        _replicates_list[replicate_number]["zero_entry"].grid(
            column=_initial_column + 1,
            row=_initial_row + replicate_number + 1,
            padx=padx_value,
        )

        _replicates_list[replicate_number]["sample_entry"].grid(
            column=_initial_column + 2,
            row=_initial_row + replicate_number + 1,
            padx=padx_value,
        )

        _replicates_list[replicate_number]["final_entry"].grid(
            column=_initial_column + 3,
            row=_initial_row + replicate_number + 1,
            padx=padx_value,
        )

        _replicates_list[replicate_number]["result"].grid(
            column=_initial_column + 4,
            row=_initial_row + replicate_number + 1,
            padx=padx_value,
        )

    _mean_entry = tk.Entry(interface_window, state="readonly", justify="center")

    _mean_entry.grid(
        row=_initial_row + len(_replicates_list) + 1,
        column=_initial_column + 4,
        padx=padx_value,
    )

    return _replicates_list, _mean_entry


def get_values_replicates_elements(
    replicates_elements_list: List[Dict[str, tk.Entry | tk.Label]],
    result_entry: tk.Entry,
    result_function,
) -> None:

    results_list = list()

    for replicate in replicates_elements_list:

        def element_input_checker(_replicate: dict[str, tk.Entry | tk.Label]) -> bool:
            for element in _replicate.values():
                if isinstance(element, tk.Entry) and element["state"] == "normal":
                    if element.get() == "":
                        return False
                    else:
                        try:
                            if float(element.get()) <= 0:
                                messagebox.showerror(
                                    "Error Message",
                                    "All values must be greater than zero.",
                                )
                                return False
                        except ValueError:
                            messagebox.showerror(
                                "Error Message",
                                "All filled entries must be numeric and greater than zero.",
                            )
                            return False
            return True

        if not element_input_checker(replicate):
            continue

        empty_value = float(replicate["zero_entry"].get())
        sample_value = float(replicate["sample_entry"].get())
        final_value = float(replicate["final_entry"].get())

        replicate_result = result_function(empty_value, sample_value, final_value)
        results_list.append(replicate_result)
        replicate["result"].config(state="normal")
        replicate["result"].delete(0, "end")
        replicate["result"].insert(0, f"{(replicate_result*100):.2f}")
        replicate["result"].config(state="readonly")

    if results_list:
        results_mean = np.mean(results_list)
        results_std = np.std(results_list)
    else:
        return

    result_entry.config(state="normal")
    result_entry.delete(0, "end")
    result_entry.insert(0, f"{(results_mean * 100):.2f} ± {(results_std * 100):.2f}")
    result_entry.config(state="readonly")


if __name__ == "__main__":
    pass
