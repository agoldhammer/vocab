from dataclasses import dataclass
from enum import Enum

import PySimpleGUI as sg

from vocab.practice import gather_selected

# global display parameters
FONT = "Helvetica 22"
sg.theme("LightBlue3")  # Add a touch of color


@dataclass
class UpdateVector:
    word: str
    defn: str
    supp: str
    show_btn: bool
    right_btn: bool
    wrong_btn: bool


# state machine for display
# states
# -- NOTHING_DISPLAYED
# -- DEF_SHOWING
# -- INPUTS: SHOW, DIRN, RIGHT/WRONG + vitem


class STATES(Enum):
    INIT = -1
    NEW_WORD = 0
    DEF_SHOWING = 1
    WORD_DISPLAYED = 2


def window_update(window, upd_vec):
    window["-WRD-"].update(upd_vec.word)
    window["-DEF-"].update(upd_vec.defn)
    window["-SUP-"].update(upd_vec.supp)
    window["-SHOWDEF-"].update(disabled=upd_vec.show_btn)
    window["Right"].update(disabled=upd_vec.right_btn)
    window["Wrong"].update(disabled=upd_vec.wrong_btn)


def init_window(vitem):
    # All the stuff inside your window.

    layout = [
        [sg.Text(vitem.src, font=FONT, key="-WRD-", size=(60, 1))],
        [sg.Text("", font=FONT, size=(60, 1), key="-DEF-", auto_size_text=True)],
        [sg.Text("", font=FONT, size=(60, 3), key="-SUP-")],
        [sg.Button("ShowDef", key="-SHOWDEF-"), sg.Button("DEBUG")],
        [sg.Button("Right", disabled=True), sg.Button("Wrong", disabled=True)],
    ]

    # Create the Window
    window = sg.Window("slexy Language Practice App", layout)
    return window
    # Event Loop to process "events" and get the "values" of the inputs


def run_gui(vitems):
    window = None
    state = STATES.INIT
    for vitem in vitems:
        print("src", vitem.src)
        if state == STATES.INIT:
            window = init_window(vitem)
            state = STATES.WORD_DISPLAYED
        else:
            if state == STATES.NEW_WORD:
                print("new word")
                upd_vec = UpdateVector(vitem.src, "", "", False, True, True)
                window_update(window, upd_vec)
                state = STATES.WORD_DISPLAYED
        event, values = window.read(timeout=500)  # use timeout version for debug btn
        # event, values = window.read()
        print(f"after read: s {state}, e {event}, v {values}")

        while(state != STATES.NEW_WORD):
            if event == "-SHOWDEF-":
                print("show")
                upd_vec = UpdateVector(vitem.src, vitem.target, vitem.supp, True, False, False)
                window_update(window, upd_vec)
                state = STATES.DEF_SHOWING
            elif event == "Right" or event == "Wrong":
                # print("r/w")
                state = STATES.NEW_WORD
                break
            elif event == "DEBUG":
                sg.show_debugger_window()
            elif event == sg.WIN_CLOSED or event == "Exit":
                # if user closes window or clicks cancel
                break
            event, values = window.read()
    window.close()


def gui_conn(n, conn, forward, unlearned):
    vitems = gather_selected(n, conn, forward, unlearned)
    run_gui(vitems)
