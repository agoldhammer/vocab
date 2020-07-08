from enum import Enum

import PySimpleGUI as sg

from vocab.practice import gather_selected, update_row, update_nseen

# global display parameters
FONT = "Helvetica 22"
SMALL_FONT = "Helvetica 11"
sg.theme("LightBlue3")  # Add a touch of color


# state machine for display
# states
class STATES(Enum):
    INIT = -1
    NEW_WORD = 0
    DEF_SHOWING = 1
    WORD_DISPLAYED = 2


def window_update(window, vitem, forward, state):
    """[summary]

    Args:
        window (sg.Window): the window
        vitem (Vitem): represents database row
        forward (bool): true if fwd dirn
        state (STATES): window state machine state
    """
    word = vitem.src if forward else vitem.target
    defn = vitem.target if forward else vitem.src
    should_color1 = (forward and vitem.lrd_from)
    should_color2 = ((not forward) and vitem.lrd_to)
    supp = dis_def = dis_rw = None
    window["-WRD-"].update(word)
    if should_color1 or should_color2:
        window["-WRD-"].update(text_color="green")
    else:
        window["-WRD-"].update(text_color="black")
    if state == STATES.NEW_WORD:
        supp = ""
        defn = ""
        dis_def = False
        dis_rw = True
    elif state == STATES.WORD_DISPLAYED:
        supp = ""
        dis_def = True
        dis_rw = False
    elif state == STATES.DEF_SHOWING:
        supp = vitem.supp
        dis_def = True
        dis_rw = False

    window["-DEF-"].update(defn)
    window["-SUP-"].update(supp)
    window["-NSEEN-"].update(f"Times seen: {vitem.nseen}")

    window["-SHOWDEF-"].update(disabled=dis_def)
    window["Right"].update(disabled=dis_rw)
    window["Wrong"].update(disabled=dis_rw)


def init_window(vitem, forward):
    """[summary]

    Args:
        vitem (Vitem): first vitem to display
        forward (bool): directional flag

    Returns:
        sg.Window: the initialized window
    """
    # All the stuff inside your window.
    word = vitem.src if forward else vitem.target
    layout = [
        [sg.Text(word, font=FONT, key="-WRD-", size=(60, 1))],
        [sg.Text(f"Times seen: {vitem.nseen}", font=SMALL_FONT, key="-NSEEN-", size=(20, 1))],
        [sg.Text("", font=FONT, size=(60, 1), key="-DEF-", auto_size_text=True)],
        [sg.Text("", font=FONT, size=(60, 3), key="-SUP-")],
        [sg.Button("ShowDef", key="-SHOWDEF-"), sg.Button("DEBUG")],
        [sg.Button("Right", disabled=True), sg.Button("Wrong", disabled=True)],
    ]

    # Create the Window
    window = sg.Window("slexy Language Practice App", layout)
    return window
    # Event Loop to process "events" and get the "values" of the inputs


def run_gui(vitems, conn, forward):
    """display vitems in gui

    Args:
        vitems (generator yielding Vitems): the selected vitems
        conn (sqllite.Conn): connection to db
        forward (bool): direction flag

    Raises:
        Exception: exception thrown if user presses exit btn
    """
    window = None
    state = STATES.INIT
    for vitem in vitems:
        # print("src", vitem.src)
        update_nseen(vitem.rowid, conn)
        if state == STATES.INIT:
            window = init_window(vitem, forward)
            state = STATES.WORD_DISPLAYED
        else:
            if state == STATES.NEW_WORD:
                # print("new word")
                # upd_vec = UpdateVector(vitem.src, "", "", vitem.nseen, False, True, True)
                window_update(window, vitem, forward, state)
                state = STATES.WORD_DISPLAYED
        event, values = window.read(timeout=500)  # use timeout version for debug btn
        # event, values = window.read()
        # print(f"after read: s {state}, e {event}, v {values}")

        while(state != STATES.NEW_WORD):
            if event == "-SHOWDEF-":
                # print("show")
                # upd_vec = UpdateVector(vitem.src, vitem.target, vitem.supp, vitem.nseen, True, False, False)
                window_update(window, vitem, forward, state)
                state = STATES.DEF_SHOWING
            elif event == "Right" or event == "Wrong":
                # print("r/w")
                if event == "Right":
                    update_row(forward, vitem.rowid, conn)
                state = STATES.NEW_WORD
                break
            elif event == "DEBUG":
                sg.show_debugger_window()
            elif event == sg.WIN_CLOSED or event == "Exit":
                # if user closes window or clicks cancel, throws back to cli
                raise Exception("User Exit")
            event, values = window.read()
    window.close()


def gui_conn(n, conn, forward, unlearned):
    """connects cli to gui

    Args:
        n (int): number of items to display
        conn (sqlite.Conn): db connectiion
        forward (bool): direction flag
        unlearned (bool): display unlearned only flag
    """
    vitems = gather_selected(n, conn, forward, unlearned)
    run_gui(vitems, conn, forward)
