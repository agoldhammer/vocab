import PySimpleGUI as sg

FONT = "Helvetica 20"

sg.theme("LightBlue")  # Add a touch of color
# All the stuff inside your window.
layout = [
    [sg.Text("Nachbarschaft", font=FONT, key="-WRD-")],
    [sg.Text("", font=FONT, size=(40, 1), key="-DEF-",
     auto_size_text=True)],
    [sg.Text("Supp", font=FONT, key="-SUP-")],
    [sg.Button("ShowDef"), sg.Button("Exit")],
    [sg.Button('Right'), sg.Button('Wrong')]
]


def words():
    mywords = ["Nachbar", "Schwester", "Bruder"]
    for word in mywords:
        yield word


# Create the Window
window = sg.Window("Window Title", layout)

# Event Loop to process "events" and get the "values" of the inputs
wlist = words()
while True:
    event, values = window.read()
    if (
        event == sg.WIN_CLOSED or event == "Exit"
    ):  # if user closes window or clicks cancel
        break
    elif event == "ShowDef":
        wrd = next(wlist)
        # sg.eprint(wrd)
        window["-DEF-"].update(wrd)
    # print("You entered ", values[0])

window.close()
