import functions as f
import PySimpleGUI as sg


layout = [[[sg.Text("  Pumba Shoes", font=("Calibri", 24))]], [[sg.Button("Search", size=(12, 3)), sg.Button("Purchase", size=(12, 3))],
    [sg.Button("Add", size=(12, 3)), sg.Button("Exit", size=(12, 3))],
    [sg.Button("Daily Checkout", size=(26, 2), button_color="green")]]
]
# Create the window (Home page)
window = sg.Window("Pumba Shoes", layout, margins=(250, 150))

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or presses the OK button
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    elif event == "Search":
        f.Search_Window()
    elif event == "Add":
        f.Add_Window()
    elif event == "Daily Checkout":
        f.UserCheckingWindow()
    elif event == "Purchase":
        f.purchase_window()
   

window.close()