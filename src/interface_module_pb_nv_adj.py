import tkinter as tk
from typing import Tuple
from tkinter import messagebox
from copy import copy
from typing import Dict
from src.procedure_textbox import *


def pb_nv_adj_interface_window(master_window=None):
    if master_window is None:
        interface_pb_nv_adj_window = tk.Tk()
    else:
        interface_pb_nv_adj_window = tk.Toplevel(master=master_window)

    interface_pb_nv_adj_window.title("P/B and NV Adjustment")

    initial_row = 0
    initial_col = 0

    frames = {
        "target": BathFrame(
            interface_pb_nv_adj_window,
            "Target Bath",
            initial_row,
            initial_col,
            ("Weight", "NV%", "P/B%"),
            resin_pigment_frame=False,
        ),
        "initial": BathFrame(
            interface_pb_nv_adj_window,
            "Initial Bath",
            initial_row,
            initial_col + 2,
            ("Weight", "NV%", "P/B%"),
            elements_states=("readonly", "normal", "normal"),
            resin_pigment_frame=False,
        ),
        "paste": BathFrame(
            interface_pb_nv_adj_window,
            "Paste",
            initial_row,
            initial_col + 4,
            ("Weight", "Binder%", "Pigment%"),
            elements_states=("readonly", "normal", "normal"),
        ),
        "resin": BathFrame(
            interface_pb_nv_adj_window,
            "Resin",
            initial_row,
            initial_col + 6,
            ("Weight", "Binder%", "Pigment%"),
            elements_states=("readonly", "normal", "disabled"),
        ),
        "water": BathFrame(
            interface_pb_nv_adj_window,
            "Water",
            initial_row,
            initial_col + 8,
            ("Weight", "Binder%", "Pigment%"),
            elements_states=("readonly", "disabled", "disabled"),
        ),
    }

    # symbols labels and grid
    symbol_label = tk.Label(interface_pb_nv_adj_window, text="=", font=("", 30, "bold"))
    symbol_label.grid(row=initial_row, column=initial_col + 1)
    symbol_label = tk.Label(interface_pb_nv_adj_window, text="+", font=("", 30, "bold"))
    symbol_label.grid(row=initial_row, column=initial_col + 3)
    symbol_label = tk.Label(interface_pb_nv_adj_window, text="+", font=("", 30, "bold"))
    symbol_label.grid(row=initial_row, column=initial_col + 5)
    symbol_label = tk.Label(interface_pb_nv_adj_window, text="+", font=("", 30, "bold"))
    symbol_label.grid(row=initial_row, column=initial_col + 7)

    # Botões
    run_button = tk.Button(
        interface_pb_nv_adj_window, text="Run", command=lambda: run(frames), width=15
    )
    run_button.grid(
        row=initial_row + 1, column=initial_col, columnspan=1, pady=25, padx=10
    )

    # procedure widget
    procedure_path = "procedures/material_balance.txt"
    procedure_textbox(
        interface_pb_nv_adj_window,
        _row=initial_row + 2,
        _column=0,
        _procedure_path=procedure_path,
    )

    if master_window is None:
        interface_pb_nv_adj_window.mainloop()


class Bath:

    def __init__(
        self,
        bath_weight: int | float | None = None,
        bath_nv: int | float = 0,
        bath_pb: int | float = 0,
    ):

        if not isinstance(bath_weight, (int, float, type(None))):
            raise TypeError("Bath weight must be an integer or float.")

        if not isinstance(bath_nv, (int, float)):
            raise TypeError("Bath NV must be an integer or float.")
        elif not 0 <= bath_nv <= 1:
            raise ValueError("Bath NV must be between 0 and 1.")

        if not isinstance(bath_pb, (int, float)):
            raise TypeError("Bath PB must be an integer or float.")
        elif bath_pb < 0:
            raise ValueError("Bath PB must be non-negative.")

        if bath_weight is None:
            bath_weight = 0

        self.weight = float(bath_weight)
        self.pigment = float((bath_nv * bath_pb) / (1 + bath_pb))
        self.binder = bath_nv - self.pigment

    def __str__(self):
        return (
            f"W: {self.weight:.4f} | NV: {self.nv():.4f} | PB: {self.pb():.4f} | "
            f"P: {self.pigment:.4f} | B: {self.binder:.4f}"
        )

    # def pigment(self):
    #     return self.__pigment * self.weight

    # def binder(self):
    #     return self.__binder * self.weight

    def pb(self):
        """
        Calculates the Pigmento to Binder (P/B) ratio.

        :return: float
        """

        if self.binder == 0:
            return 0.0

        return self.pigment / self.binder

    def nv(self):
        """
        Calculates the Non-Volatile ratio.
        :return: float
        """
        if self.weight == 0:
            return 0

        return self.pigment + self.binder

    def volatiles(self):
        return 1 - self.pigment - self.binder

    def remove_bath(self, new_bath_weight: int | float = 0):
        """
        Removes an aliquot of the bath.
        :param new_bath_weight:
        :return:
        """

        if new_bath_weight < 0:
            raise ValueError("Bath PB must be non-negative.")
        elif new_bath_weight > self.weight:
            raise ValueError("Aliquot weight cannot be greater than the bath weight.")

        aliquot = Bath(new_bath_weight, bath_nv=self.nv(), bath_pb=self.pb())

        self.weight -= aliquot.weight

        return aliquot

    def add_bath(self, *other_bath):

        weight_accumulator = self.weight
        pigment_accumulator = self.weight * self.pigment
        binder_accumulator = self.weight * self.binder

        for bath in other_bath:
            weight_accumulator += bath.weight
            pigment_accumulator += bath.pigment * bath.weight
            binder_accumulator += bath.binder * bath.weight

        self.weight = weight_accumulator
        self.pigment = pigment_accumulator / weight_accumulator
        self.binder = binder_accumulator / weight_accumulator

        return None

    def add_pigment(self, amount_of_pigment: int | float):
        total_weight = self.weight + amount_of_pigment
        self.pigment = (amount_of_pigment + self.pigment * self.weight) / total_weight
        self.binder = (self.binder * self.weight) / total_weight
        self.weight = total_weight

        return self

    def add_binder(self, amount_of_binder: int | float):
        total_weight = self.weight + amount_of_binder
        self.binder = (amount_of_binder + self.binder * self.weight) / total_weight
        self.pigment = (self.pigment * self.weight) / total_weight
        self.weight = total_weight

        return self


class BathFrame:
    def __init__(
        self,
        _root_window: tk.Tk,
        frame_title: str,
        frame_row: int,
        frame_col: int,
        elements_labels: Tuple[str, str, str],
        elements_states=("normal", "normal", "normal"),  # defines entries state
        resin_pigment_frame: bool = True,  # defines if it is a nv/pb (false) or resin/pigment (true) frame
    ):

        self.resin_pigment_frame = resin_pigment_frame

        self.frame = tk.Frame(
            _root_window, padx=10, pady=10, borderwidth=2, relief="solid"
        )
        self.frame.grid(row=frame_row, column=frame_col, padx=10, pady=10)

        frame_label = tk.Label(
            self.frame, text=frame_title, font=("Helvetica", 12, "bold")
        )
        frame_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.elements = (
            {
                "row": 1,
                "id": "weight",
                "label": tk.Label(self.frame, text=elements_labels[0]),
                "entry": tk.Entry(self.frame, state=elements_states[0]),
            },
            {
                "row": 2,
                "id": "resin or nv",
                "label": tk.Label(self.frame, text=elements_labels[1]),
                "entry": tk.Entry(self.frame, state=elements_states[1]),
            },
            {
                "row": 3,
                "id": "pigment or pb",
                "label": tk.Label(self.frame, text=elements_labels[2]),
                "entry": tk.Entry(self.frame, state=elements_states[2]),
            },
        )

        # elements grid and setting of entries default value
        for element in self.elements:
            element["label"].grid(row=element["row"], column=0, sticky="e")
            element["entry"].grid(row=element["row"], column=1, padx=5, pady=5)

            entry_initial_state = element["entry"]["state"]
            element["entry"]["state"] = "normal"
            element["entry"].insert(0, "0")
            element["entry"]["state"] = entry_initial_state

    def get_bath(self) -> Bath | None:

        for element in self.elements:
            if float(element["entry"].get()) < 0:
                raise ValueError

        if self.resin_pigment_frame:
            bath = Bath(float(self.elements[0]["entry"].get()))
            bath.binder = (
                float(self.elements[1]["entry"].get()) / 100
            )  # convert binder% to binder (decimal)
            bath.pigment = (
                float(self.elements[2]["entry"].get()) / 100
            )  # convert pigment% to pigment (decimal)
        else:
            bath = Bath(
                float(self.elements[0]["entry"].get()),
                bath_nv=float(self.elements[1]["entry"].get())
                / 100,  # convert NV% to NV (decimal)
                bath_pb=float(self.elements[2]["entry"].get()) / 100,
            )  # convert P/B% to P/B (decimal)

        return bath

    def change_weight_entry(self, new_weight):

        initial_state = self.elements[0]["entry"]["state"]

        self.elements[0]["entry"]["state"] = "normal"
        self.elements[0]["entry"].delete(0, tk.END)
        self.elements[0]["entry"].insert(0, f"{new_weight:.2f}")
        self.elements[0]["entry"]["state"] = initial_state

    def entry_reset(self):

        initial_state = self.elements[0]["entry"]["state"]

        self.elements[0]["entry"]["state"] = "normal"
        self.elements[0]["entry"].delete(0, tk.END)
        self.elements[0]["entry"].insert(0, "0")
        self.elements[0]["entry"]["state"] = initial_state


def run(frames: Dict[str, BathFrame]):
    try:
        _results = adjust_bath(
            frames["target"].get_bath(),
            frames["initial"].get_bath(),
            frames["paste"].get_bath(),
            frames["resin"].get_bath(),
            frames["water"].get_bath(),
        )
    except ValueError:
        # ValueError raises when there is any non-numeric entry value or numeric values less than zero

        # entries reset
        for bath in frames.keys():
            frames[bath].entry_reset()

        messagebox.showerror(
            "Error Message",
            "All entries must be numeric and equal to or greater than zero values.",
        )
        return

    except ZeroDivisionError:
        # ZeroDivisionError raises when Run is pressed with all entries equal to zero
        return

    # weight entries update
    for bath in frames.keys():
        frames[bath].change_weight_entry(_results[bath].weight)


def adjust_bath(
    target_bath: Bath,
    initial_bath: Bath,
    paste: Bath,
    resin: Bath,
    water: Bath,
    target_weight: bool = True,
    paste_min: int | float = 0,
) -> Dict[str, Bath]:

    bf = target_bath.weight
    p_bf = target_bath.pigment
    b_bf = target_bath.binder

    p_bi = initial_bath.pigment
    b_bi = initial_bath.binder

    b_r = resin.binder

    p_p = paste.pigment
    b_p = paste.binder

    w = 0
    while True:
        initial_bath_weight = (
            b_bf * bf * p_p
            - b_p * bf * p_bf
            + b_r * bf * p_bf
            - b_r * bf * p_p
            + b_r * p_p * w
        ) / (b_bi * p_p - b_p * p_bi + b_r * p_bi - b_r * p_p)
        paste_weight = (
            -b_bf * bf * p_bi
            + b_bi * bf * p_bf
            - b_r * bf * p_bf
            + b_r * bf * p_bi
            - b_r * p_bi * w
        ) / (b_bi * p_p - b_p * p_bi + b_r * p_bi - b_r * p_p)
        resin_weight = (
            b_bf * bf * p_bi
            - b_bf * bf * p_p
            - b_bi * bf * p_bf
            + b_bi * bf * p_p
            - b_bi * p_p * w
            + b_p * bf * p_bf
            - b_p * bf * p_bi
            + b_p * p_bi * w
        ) / (b_bi * p_p - b_p * p_bi + b_r * p_bi - b_r * p_p)

        if (
            paste_weight >= paste_min
            and initial_bath_weight >= 0
            and paste_weight >= 0
            and resin_weight >= 0
        ):
            break

        if w > bf:
            break

        w += target_bath.weight / 1000

    initial_bath.weight = initial_bath_weight
    paste.weight = paste_weight
    resin.weight = resin_weight
    water.weight = w

    test_bath = copy(initial_bath)
    test_bath.add_bath(paste, resin, water)

    return {
        "target": target_bath,
        "initial": initial_bath,
        "paste": paste,
        "resin": resin,
        "water": water,
        "test_bath": test_bath,
    }


if __name__ == "__main__":
    pb_nv_adj_interface_window()
