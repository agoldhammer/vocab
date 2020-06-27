import PySimpleGUI as sg


def pairs():
    mywords = [("Nachbar", "Neighbor"), ("Schwester", "Sister"), ("Bruder", "Brother")]
    for word in mywords:
        yield word


def run_gui():
    FONT = "Helvetica 20"

    sg.theme("LightBlue")  # Add a touch of color
    # All the stuff inside your window.
    wpairs = pairs()
    wrd, defn = next(wpairs)
    layout = [
        [sg.Text(wrd, font=FONT, key="-WRD-", size=(60, 1))],
        [sg.Text("", font=FONT, size=(60, 1), key="-DEF-", auto_size_text=True)],
        [sg.Text("Supp", font=FONT, key="-SUP-")],
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
            window["-DEF-"].update(defn)
            window["-SHOWDEF-"].update(disabled=True)
            window["Right"].update(disabled=False)
            window["Wrong"].update(disabled=False)
        elif event == "Right":
            try:
                wrd, defn = next(wpairs)
            except StopIteration:
                break
            window["-WRD-"].update(wrd)
            window["-DEF-"].update("")
            window["-SHOWDEF-"].update(disabled=False)
            window["Right"].update(disabled=True)
            window["Wrong"].update(disabled=True)
        elif event == "Wrong":
            try:
                wrd, defn = next(wpairs)
            except StopIteration:
                break
            window["-WRD-"].update(wrd)
            window["-DEF-"].update("")
            window["-SHOWDEF-"].update(disabled=False)
            window["Right"].update(disabled=True)
            window["Wrong"].update(disabled=True)

    window.close()


run_gui()
