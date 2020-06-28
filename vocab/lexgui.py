import PySimpleGUI as sg

from vocab.practice import gather_selected


# def pairs():
#     mywords = [("Nachbar", "Neighbor"), ("Schwester", "Sister"), ("Bruder", "Brother")]
#     for word in mywords:
#         yield word


def run_gui(vitems):
    FONT = "Helvetica 22"

    sg.theme("LightBlue3")  # Add a touch of color
    # All the stuff inside your window.
    # wpairs = pairs()
    # wrd, defn = next(wpairs)
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
    while True:
        event, values = window.read()
        if (
            event == sg.WIN_CLOSED or event == "Exit"
        ):  # if user closes window or clicks cancel
            break
        elif event == "-SHOWDEF-":
            window["-DEF-"].update(vitem.target)
            window["-SHOWDEF-"].update(disabled=True)
            window["-SUP-"].update(vitem.supp)
            window["Right"].update(disabled=False)
            window["Wrong"].update(disabled=False)
        elif event == "Right":
            try:
                # wrd, defn = next(wpairs)
                vitem = next(vitems)
            except StopIteration:
                break
            window["-WRD-"].update(vitem.src)
            window["-DEF-"].update("")
            window["-SUP-"].update("")
            window["-SHOWDEF-"].update(disabled=False)
            window["Right"].update(disabled=True)
            window["Wrong"].update(disabled=True)
        elif event == "Wrong":
            try:
                # wrd, defn = next(wpairs)
                vitem = next(vitems)
            except StopIteration:
                break
            window["-WRD-"].update(vitem.src)
            window["-DEF-"].update("")
            window["-SUP-"].update("")
            window["-SHOWDEF-"].update(disabled=False)
            window["Right"].update(disabled=True)
            window["Wrong"].update(disabled=True)

    window.close()


# run_gui()


def gui_conn(n, conn, forward, unlearned):
    vitems = gather_selected(n, conn, forward, unlearned)
    run_gui(vitems)
