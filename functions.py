from asyncio.windows_events import NULL
import re
import mysql.connector as cn
from tkinter import *
import PySimpleGUI as sg
from connectToMySQL import mydb, mycursor
import datetime  

Admin = {"Sriya": "password", "Nishanth": "password", "Chaitra":"password"}

## SEARCH
def search_sql(model, size=[], color=[]):
    # if the user did not input the size and color, we return all data for this model
    if size == [] and color == []:
        mycursor.execute("SELECT * FROM shoes where numModel = %s", (model,))

    # if the user did not input size (but did input color)
    elif size == []:
        color_ = color[0]
        mycursor.execute("SELECT * FROM shoes where numModel = %s and color = %s", (model, color_))

    # if the user did not input color (but did input size)
    elif color == []:
        size_ = size[0]
        mycursor.execute("SELECT * FROM shoes where numModel = %s and size = %s", (model, size_))

    else:
        size_ = size[0]
        color_ = color[0]

        mycursor.execute("SELECT * FROM shoes WHERE numModel = %s AND size = %s AND color = %s",
                         (model, size_, color_))

    # showing the table data
    myresult = mycursor.fetchall()
    field_names = [i[0] for i in mycursor.description]
    layout = [
        [sg.Text("Details of pairs in stock", font=("Arial", 20), justification=CENTER)],
        [sg.Table(values=myresult, headings=field_names, max_col_width=20, auto_size_columns=True,
                  justification=CENTER, size=(100, 15))],
        [sg.Button("Confirm", font="Arial, 20", button_color='green', size=(8, 1))]]

    window = sg.Window("Inventory Details", layout, element_justification=CENTER, margins=(200, 100))
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Confirm"):
            break
    window.close()

def Search_Window():
    layout_Search = [
        [sg.Text("Which pair of shoes would you like to find?", size=(25, 2), font=('Arial', 15))],
        [sg.Input(size=(10, 4)), sg.Text('Model number*', font=('Arial', 12))],
        [sg.Listbox([36, 36.5, 37, 37.5, 38, 38.5, 39, 39.5, 40, 40.5, 41, 41.5,
                     42, 42.5, 43, 43.5, 44, 44.5, 45, 45.5, 46, 46.5, 47, 47.5, 48],
                    size=(7, 7)), sg.Text('Size', font=('Arial', 12))],
        [sg.Listbox(["red", "black", "white", "green", "gray", "brown", "blue", "colourful"],
                    size=(10, 4)), sg.Text('Color', font=('Arial', 12))],
        [sg.Button(button_text="Confirm", size=(6, 2), pad=(10, 20), button_color="green"),
         sg.Button(button_text="Cancel", size=(6, 2), pad=(10, 20), button_color="red")]
    ]

    SearchWindow = sg.Window("Search", layout_Search, element_justification='center', margins=(100, 50))

    while True:
        event_Search, values_Search = SearchWindow.read()
        if event_Search in (sg.WIN_CLOSED, 'Cancel'):
            break
        # if the user did not input any model
        elif values_Search[0] == "":
            layout_error = [
                [sg.Text("Error! Model number is required", size=(20, 2), text_color="black", font=('Arial', 14))],
                [sg.Button(button_text="Confirm", size=(5, 1), pad=(10, 20), button_color="grey")]]
            ErrorWindow = sg.Window("Error!", layout_error, element_justification='center', margins=(50, 25))
            while True:
                event_error, values_error = ErrorWindow.read()
                if event_error in (sg.WIN_CLOSED, "Confirm"):
                    break
            ErrorWindow.close()
        elif event_Search == "Confirm":
            search_sql(values_Search[0], values_Search[1], values_Search[2])
    SearchWindow.close()

def Add_Window():
    layout_Add = [
        [sg.Text("Which pair of shoes would you like to add to the inventory?", size=(30, 2), font=('Arial', 15))],
        [sg.Input(size=(10, 4), key="MODEL"), sg.Text('Model number*', font=('Arial', 12))],
        [sg.Listbox(["Red", "Black", "White", "Green", "Gray", "Brown", "Blue", "Colorful"], 
                    size=(10, 4), key="COLOR"), sg.Text('Color*', font=('Arial', 12))],
        [sg.Listbox([1, 2], size=(10, 4), key="FLOOR"), sg.Text('Floor*', font=('Arial', 12))],
        [sg.Listbox(["Winter", "Summer", "Autumn", "Spring"], 
                    size=(10, 4), key="SEASON"), sg.Text('Season', font=('Arial', 12))],
        [sg.Button(button_text="Confirm", size=(6, 2), pad=(10, 20), button_color="green"),
         sg.Button(button_text="Cancel", size=(6, 2), pad=(10, 20), button_color="red")]
    ]


    AddWindow = sg.Window("Add", layout_Add, element_justification='center', margins=(100, 40))

    while True:
        event_Add, values_Add = AddWindow.read()
        if event_Add in (sg.WIN_CLOSED, 'Cancel'):
            break

        # if the user did not input model/size/floor -- ERROR WINDOW
        elif values_Add['MODEL'] == "" or values_Add['COLOR'] == [] or values_Add['FLOOR'] == []:
            layout_Error = [[sg.Text("Error! Missing details", size=(20, 2), text_color="black", font=('Arial', 15))],
                            [sg.Button(button_text="Confirm", size=(5, 1), pad=(10, 20), button_color="grey")]]
            ErrorWindow = sg.Window("Error!", layout_Error, element_justification='center', margins=(50, 25))
            while True:
                event_Error, values_Error = ErrorWindow.read()
                if event_Error in (sg.WIN_CLOSED, "Confirm"):
                    break
            ErrorWindow.close()

            
        elif event_Add == "Confirm":
            if values_Add['SEASON'] == []:
                values_Add['SEASON'].append(NULL)
            Add_sql(values_Add['MODEL'], values_Add['COLOR'][0], values_Add['FLOOR'][0], values_Add['SEASON'][0])
    AddWindow.close()

# add to mysql
def Add_sql(model, color, floor, season):
    sizesint = [
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=36), sg.Text('36')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=37), sg.Text('37')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=38), sg.Text('38')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=39), sg.Text('39')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=40), sg.Text('40')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=41), sg.Text('41')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=42), sg.Text('42')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=43), sg.Text('43')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=44), sg.Text('44')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=45), sg.Text('45')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=46), sg.Text('46')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=47), sg.Text('47')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=48), sg.Text('48')],
    ]

    sizeshalfes = [
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=36.5), sg.Text('36.5')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=37.5), sg.Text('37.5')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=38.5), sg.Text('38.5')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=39.5), sg.Text('39.5')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=40.5), sg.Text('40.5')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=41.5), sg.Text('41.5')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=42.5), sg.Text('42.5')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=43.5), sg.Text('43.5')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=44.5), sg.Text('44.5')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=45.5), sg.Text('45.5')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=46.5), sg.Text('46.5')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=47.5), sg.Text('47.5')],
    ]

    buttons = [
        [sg.Button(button_text="Add", size=(6, 2), button_color="green")],
        [sg.Button(button_text="Return", size=(6, 2), button_color="grey")]
    ]
    layout_add_sizes = [[
        sg.Column(sizesint),
        sg.VSeparator(),
        sg.Column(sizeshalfes),
        sg.Column(buttons)]
    ]

    Add_Sizes_Window = sg.Window('Sizes to Add', layout_add_sizes, margins=(250, 100))
    while True:
        event_add_sizes, values_add_sizes = Add_Sizes_Window.read()

        if event_add_sizes == "Add":  # Inserting values
            all_sizes = len(values_add_sizes)
            up = 0  

            try:
                for i in range(all_sizes):
                    size = up + 36
                    # quantity of shoes 
                    if values_add_sizes[up + 36] != 0:

                        size = up + 36
                        quantityInStockQUERY =  "SELECT quantity FROM shoes WHERE numModel = %s AND color = %s AND size = %s AND season = %s AND floor = %s" 
                        mycursor.execute(quantityInStockQUERY, (model, color,size,season,floor))
                        result = mycursor.fetchone()

                        # if the model and color is not in stock
                        if result is None or result[0] == 0:
                            inserting_to_stock = "INSERT INTO shoes (numModel, color, size, quantity ,floor, season)" \
                                            " VALUES (%s, %s, %s, %s, %s, %s)"
                            val = (model, color , up + 36, values_add_sizes[up + 36], floor, season)
                            mycursor.execute(inserting_to_stock, val)
                            # save the changes to the database permanently
                            mydb.commit()

                        else:
                            updateQuery = "UPDATE shoes SET quantity = %s WHERE numModel = %s AND color = %s AND size = %s season = %s"
                            newQuantity = result[0] + values_add_sizes[up + 36]
                            update_values = (newQuantity, model, color, size,season)
                            mycursor.execute(updateQuery, update_values)
                            mydb.commit()
                            mydb.close()

                    up += 0.5

            except cn.Error as e:
                print(f'Error creating tables: {e}')
                
                
            # Confirmation window after inserting   
            layout_confirmation = [  
                [sg.Text("Items have been added as requested", size=(20, 2), text_color="black", font=('Arial', 15))],
                [sg.Button(button_text="Confirm", size=(5, 1), pad=(10, 20), button_color="blue")]]
            confirmation_window = sg.Window("Items Added", layout_confirmation, element_justification='center',
                                            margins=(50, 25))
            while True:
                confirm_event, confirm_values = confirmation_window.read()
                if confirm_event in (sg.WIN_CLOSED, "Confirm"):
                    break
            confirmation_window.close()

            break

        elif event_add_sizes in (sg.WIN_CLOSED, layout_add_sizes[0][3] == "Return"):
            break

        Add_Sizes_Window.close()
    Add_Sizes_Window.close()


def purchase_window():
    layout = [
        [sg.Input(size=(10, 4), key="PRICE"), sg.Text('Price*', font=('Arial', 12))],
        [sg.Input(size=(10, 4), key="MODEL"), sg.Text('Model Number*', font=('Arial', 12))],
        [sg.Listbox(["Red", "Black", "White", "Green", "Gray", "Brown", "Blue", "Colorful"],
                    size=(6, 4), key="COLOR"), sg.Text('Color*', font=('Arial', 12))],
        [sg.Listbox(["1", "2"],
                    size=(3, 2), key="FLOOR"), sg.Text('Floor*', font=('Arial', 12))],
        [sg.Listbox(["Winter", "Summer", "Autumn", "Spring"],
                    size=(10, 4), key="SEASON"), sg.Text('Season', font=('Arial', 12))],
        [sg.Input(size=(10, 4), key="SIZE"), sg.Text('Size*', font=('Arial', 12))],
        [sg.Input(size=(10, 4), key="PHONE"), sg.Text('Phone*', font=('Arial', 12))],
        [sg.Input(size=(10, 4), key="NAME"), sg.Text('Customer Name*', font=('Arial', 12))],

        [sg.Button(button_text="Confirm", size=(6, 2), pad=(20, 20), button_color="green"),
         sg.Button(button_text="Cancel", size=(6, 2), pad=(20, 20), button_color="red")]
    ]

    purchaseW = sg.Window("Purchase", layout, element_justification='center', margins=(60, 60))

    while True:
        event, values = purchaseW.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            purchaseW.close()
            break

        # Extract values
        price = values['PRICE']
        model = values['MODEL']
        name = values['NAME']
        size = values['SIZE']
        color = values['COLOR'][0] if values['COLOR'] else None
        phone = values['PHONE']
        floor = values['FLOOR'][0] if values['FLOOR'] else None
        season = values['SEASON'][0] if values['SEASON'] else None

        # Check if model exists
        if not checkIfmodelExist(model, size, color):
            sg.popup("The model is not in stock.", title="Model Not in Stock")
            continue

        # Check if size is correct
        if not size.isdigit() or not 36 <= int(size) <= 47:
            sg.popup("Please enter a valid size (36-47).", keep_on_top=True)
            continue

        # Ensure all fields are filled
        if event == "Confirm":
            if not all(values.values()):
                sg.popup("Please fill in all fields.", title="Missing Fields")
                continue

            # Validate price and model format
            if not re.match(r'^\d+(\.\d{1,2})?$', price) or not re.match(r'^\d+(\.\d{1,2})?$', model):
                sg.popup("Invalid details provided.", title="Error")
                continue

            # Validate phone number format
            if not re.match(r'^\d{10}$', phone):
                sg.popup("Enter a valid 10-digit phone number.", keep_on_top=True)
                continue

            # Process purchase
            addPurchaseSQL(model, price, size, floor, name, phone, color, season)
            sg.popup("Purchase completed successfully!", title="Success")
            purchaseW.close()
            break


def checkIfmodelExist(model, size, color):
    query = "SELECT * FROM SHOES WHERE numModel = %s AND size = %s AND color = %s"
    values = (model, size, color)
    mycursor.execute(query, values)
    result = mycursor.fetchone()
    if result is not None:
        return True
    else:
        return False
    
# trigger in this function
def addPurchaseSQL(model, price, size, floor, name, phone, color, season):
    
    currentDate = datetime.datetime.now().strftime('%Y-%m-%d')
    try:
        query = "INSERT INTO Orders (numModel, price, size, floor, name, phone, color,order_date) VALUES (%s, %s, %s, %s, %s,%s, %s, %s)"
        values = (model, price ,size, floor, name, phone, color, currentDate)
        mycursor.execute(query, values)

        
        order_id = mycursor.lastrowid # Retrieve the last inserted order_id
        query = "INSERT INTO Customers (phone, name, order_id) VALUES (%s, %s, %s)"
        values = (phone, name, order_id)
        mycursor.execute(query, values)
        
        
        mydb.commit() # Commit the transaction
        # Trigger executed after a purchase
        updateShoesTableAfterPurchase(model, color, size, floor, season)

    except cn.Error as e:
        print(f'Error update order table: {e}')


def updateShoesTableAfterPurchase(model, color , size, floor, season):
    
    try:
        quantityInStockQUERY = "SELECT quantity FROM shoes WHERE numModel = %s AND color = %s AND size = %s AND season = %s AND floor = %s" 
        mycursor.execute(quantityInStockQUERY, (model, color,size, season, floor))
        currentQuantity = mycursor.fetchone()
        newQuantity = currentQuantity[0] - 1

        query = "UPDATE shoes SET quantity = %s Where numModel = %s AND size = %s AND color = %s AND season = %s AND floor = %s"
        values = (newQuantity, model, size, color, season, floor)
        mycursor.execute(query, values)     
        mydb.commit()
        print("commited to table shoes")

    except cn.Error as e:
        print(f'Error update order table: {e}')

def UserCheckingWindow():
    layout = [[sg.Input(size=(10, 4), key="USERNAME"), sg.Text('Username', font=('Arial', 12))],
        [sg.Input(size=(10, 4), key="PASSWORD"), sg.Text('Password', font=('Arial', 12))],
        [sg.Button(button_text="Login", size=(6, 2), pad=(20, 20), button_color="green")]        
    ]

    loginWindow = sg.Window("Admin Login", layout, element_justification='center', margins=(100, 50))

    while True:
        event, values = loginWindow.read()

        if event == sg.WINDOW_CLOSED:
            loginWindow.close()
            break
        
        if event == 'Login':
            uname = values['USERNAME']
            pwd = values['PASSWORD']
            query = "SELECT * FROM Admin WHERE username = %s AND password = %s"
            values = (uname, pwd)
            mycursor.execute(query, values)
            result = mycursor.fetchone()
            if result is not None:
                loginWindow.close()
                DailyCheckOutWindow()
                break
            else:
                loginWindow.close()
                sg.Popup(f"Access denied.", font=('Arial', 16), keep_on_top=True)

def summary_page():
    orderSummaryQuery = "SELECT Orders.order_id, Orders.numModel, Orders.price, Orders.size, Orders.color, Orders.order_date, Customers.name AS customer_name, Customers.phone FROM Orders JOIN Customers ON Orders.phone = Customers.phone;"
    mycursor.execute(orderSummaryQuery)
    myresult = mycursor.fetchall()
    field_names = [i[0] for i in mycursor.description]
    layout = [
        [sg.Text("Details of Orders", font=("Arial", 20), justification=CENTER)],
        [sg.Table(values=myresult, headings=field_names, max_col_width=20, auto_size_columns=True,
                justification=CENTER, size=(100, 15))]]

    window = sg.Window("Order Details", layout, element_justification=CENTER, margins=(200, 100))
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
    window.close()

def DailyCheckOutWindow():
    layout = [
        [sg.Button(button_text="Daily Profit", size=(6, 2), pad=(20, 20), button_color="blue"),
        sg.Button(button_text="Monthly Profit", size=(6, 2), pad=(20, 20), button_color="blue"),
        sg.Button(button_text="Order Summary", size=(8, 2), pad=(20, 20), button_color="blue")],
        [sg.Button(button_text="Exit", size=(6, 2), pad=(10, 20), button_color="red")]
    ]

    window = sg.Window("Checkout", layout, element_justification='center', margins=(100, 50))
    
    currentDate = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # SQL query to calculate the sum of orders for the current day
    dailyProfitQuery = "SELECT SUM(price) FROM Orders WHERE order_date = %s"
    
    # nested query
    # SQL query to calculate the sum of orders for the current month
    monthlyProfitQuery = "SELECT SUM(profit) AS monthly_profit \
                            FROM ( \
                                SELECT price AS profit \
                                FROM Orders \
                                WHERE MONTH(order_date) = MONTH(CURRENT_DATE()) \
                                AND YEAR(order_date) = YEAR(CURRENT_DATE()) \
                            ) AS MonthlyProfits;"
    
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Exit':
            # window.close()
            break
        
        if event == 'Daily Profit':
            # Execute the daily profit query
            mycursor.execute(dailyProfitQuery, (currentDate,))
            result = mycursor.fetchone()
            dailyProfit1 = result[0]
            sg.Popup(f"The amount accumulated today is {dailyProfit1}", font=('Arial', 16), keep_on_top=True)
            print("Daily profit:", dailyProfit1)

        if event == 'Monthly Profit':
            # Execute the monthly profit query
            mycursor.execute(monthlyProfitQuery)
            result = mycursor.fetchone()
            monthlyProfit1 = result[0]
            sg.Popup(f"The amount accumulated this month is {monthlyProfit1}", font=('Arial', 16), keep_on_top=True)
            print("Monthly profit:", monthlyProfit1)
        
        if event == "Order Summary":
            summary_page()
    
    window.close()