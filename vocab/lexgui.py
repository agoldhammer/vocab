from dataclasses import dataclass
from enum import Enum

# import debugpy

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
    NOTHING_DISPLAYED = 0
    DEF_SHOWING = 1
    WORD_DISPLAYED = 2


def window_update(window, upd_vec):
    window["-WRD-"].update(upd_vec.word)
    window["-DEF-"].update(upd_vec.defn)
    window["-SUP-"].update(upd_vec.supp)
    window["-SHOWDEF-"].update(disabled=upd_vec.show_btn)
    window["Right"].update(disabled=upd_vec.right_btn)
    window["Wrong"].update(disabled=upd_vec.wrong_btn)


def run_gui(vitems):
    # All the stuff inside your window.
    state = STATES.NOTHING_DISPLAYED
    vitem = next(vitems)
    layout = [
        [sg.Text(vitem.src, font=FONT, key="-WRD-", size=(60, 1))],
        [sg.Text("", font=FONT, size=(60, 1), key="-DEF-", auto_size_text=True)],
        [sg.Text("", font=FONT, size=(60, 3), key="-SUP-")],
        [sg.Button("ShowDef", key="-SHOWDEF-")],
        [sg.Button("Right", disabled=True), sg.Button("Wrong", disabled=True)],
    ]

    # Create the Window
    window = sg.Window("slexy Language Practice App", layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while(True):
        print("src", vitem.src)
        event, values = window.read()
        print("after read: ", state, event, values)

        if state == STATES.NOTHING_DISPLAYED:
            print("nd")
            upd_vec = UpdateVector(vitem.src, "", "", False, True, True)
            window_update(window, upd_vec)
            state = STATES.WORD_DISPLAYED
        elif state == STATES.WORD_DISPLAYED and event == "-SHOWDEF-":
            print("show")
            upd_vec = UpdateVector(vitem.src, vitem.target, vitem.supp, True, False, False)
            window_update(window, upd_vec)
            state = STATES.DEF_SHOWING
        elif state == STATES.DEF_SHOWING and (event == "Right" or event == "Wrong"):
            print("r/w")
            # upd_vec = UpdateVector("", "", "", False, True, True)
            # window_update(window, upd_vec)
            state = STATES.NOTHING_DISPLAYED
            try:
                vitem = next(vitems)
            except StopIteration:
                print("stop")
                break
        elif event == sg.WIN_CLOSED or event == "Exit":
            # if user closes window or clicks cancel
            break
        else:
            print("shouldn't happen")
    window.close()


def gui_conn(n, conn, forward, unlearned):
    vitems = gather_selected(n, conn, forward, unlearned)
    # debugpy.listen(5678)
    # print("Waiting for debugger attach")
    # debugpy.wait_for_client()
    # debugpy.breakpoint()
    # print('break on this line')
    run_gui(vitems)
