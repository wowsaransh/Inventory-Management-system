from tkinter import *
from tkinter import messagebox
import mysql.connector
from tkinter import ttk

# Create a variable to track the authenticated user
authenticated_user = None

def login():
    global authenticated_user
    username = entry_username.get()
    password = entry_password.get()

    if username and password:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            if user:
                authenticated_user = user
                messagebox.showinfo("Success", "Authentication successful.")
                open_inventory_window()
            else:
                messagebox.showerror("Authentication Failed", "Invalid username or password.")
            cursor.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Authentication Failed", "Please enter both username and password.")

def open_inventory_window():
    login_window.destroy()
    global treeview  
    global entry_product_name, entry_product_price, entry_stock, entry_category, entry_tags

    root = Tk()
    root.title("MARVELS STORE")
    root.geometry("1024x768")

    left_frame = Frame(root, bg='white')  # White background
    left_frame.pack(side=LEFT, fill='both', expand=True)

    right_frame = Frame(root, bg='#E8E8E8')  # Light gray background
    right_frame.pack(side=RIGHT, fill='both', expand=True)

    left_frame.grid_rowconfigure(0, weight=1)
    left_frame.grid_rowconfigure(1, weight=1)
    left_frame.grid_rowconfigure(2, weight=1)
    left_frame.grid_rowconfigure(3, weight=1)
    left_frame.grid_rowconfigure(4, weight=1)
    left_frame.grid_rowconfigure(5, weight=1)

    label_product_name = Label(left_frame, text="Product Name", font=('calibri 20 bold'), fg='black', anchor='e', justify='right')
    label_product_name.grid(row=0, column=0, pady=10, sticky='e')

    entry_product_name = Entry(left_frame, font=('Calibri 18'), bg='white')
    entry_product_name.grid(row=0, column=1, pady=10, sticky='w')

    label_product_price = Label(left_frame, text="Price", font=('calibri 20 bold'), fg='black', anchor='e', justify='right')
    label_product_price.grid(row=1, column=0, pady=10, sticky='e')

    entry_product_price = Entry(left_frame, font=('Calibri 18'), bg='white')
    entry_product_price.grid(row=1, column=1, pady=10, sticky='w')

    label_stock = Label(left_frame, text="Stock", font=('calibri 20 bold'), fg='black', anchor='e', justify='right')
    label_stock.grid(row=2, column=0, pady=10, sticky='e')

    entry_stock = Entry(left_frame, font=('Calibri 18'), bg='white')
    entry_stock.grid(row=2, column=1, pady=10, sticky='w')

    label_category = Label(left_frame, text="Category", font=('calibri 20 bold'), fg='black', anchor='e', justify='right')
    label_category.grid(row=3, column=0, pady=10, sticky='e')

    entry_category = Entry(left_frame, font=('Calibri 18'), bg='white')
    entry_category.grid(row=3, column=1, pady=10, sticky='w')

    # Create a frame for buttons
    button_frame = Frame(left_frame)
    button_frame.grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky='n')

    add_item_btn = Button(button_frame, text="Add Item", width=18, height=2, bg='#2E86C1', command=add_item)  # Soft blue
    add_item_btn.grid(row=0, column=0, pady=5)

    delete_item_btn = Button(button_frame, text="Delete Item", width=18, height=2, bg='#2E86C1', command=delete_item)  # Soft blue
    delete_item_btn.grid(row=1, column=0, pady=5)

    show_items_btn = Button(button_frame, text="Show Items", width=18, height=2, bg='#2E86C1', command=show_items)  # Soft blue
    show_items_btn.grid(row=2, column=0, pady=5)

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='inventory_system'
    )

    treeview = ttk.Treeview(right_frame, columns=("Serial No.", "Product Name", "Price", "Stock", "Category"))
    treeview.heading("#1", text="Serial No.", anchor='w')
    treeview.heading("#2", text="Product Name")
    treeview.heading("#3", text="Price")
    treeview.heading("#4", text="Stock")
    treeview.heading("#5", text="Category")
    treeview.column("#1", width=100, anchor='w')
    treeview.column("#2", width=250)
    treeview.column("#3", width=100)
    treeview.column("#4", width=100)
    treeview.column("#5", width=100)
    treeview.pack(fill='both', expand=True)

    root.mainloop()

def add_item():
    product_name = entry_product_name.get()
    product_price = entry_product_price.get()
    stock = entry_stock.get()
    category = entry_category.get()

    if product_name and product_price and stock and category:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM inventory WHERE product_name = %s", (product_name,))
            existing_product = cursor.fetchone()
            if existing_product:
                cursor.execute("UPDATE inventory SET stock = stock + %s WHERE product_name = %s", (stock, product_name))
            else:
                cursor.execute("INSERT INTO inventory (product_name, price, stock, category) VALUES (%s, %s, %s, %s)",
                               (product_name, product_price, stock, category))
            conn.commit()
            cursor.close()
            messagebox.showinfo("Success", "Item added to the database")
            show_items()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "Please fill in all the fields.")

    entry_product_name.delete(0, END)
    entry_product_price.delete(0, END)
    entry_stock.delete(0, END)
    entry_category.delete(0, END)

def delete_item():
    selected_item = treeview.selection()
    if selected_item:
        product_name = treeview.item(selected_item, "values")[1]
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT stock FROM inventory WHERE product_name = %s", (product_name,))
            stock = cursor.fetchone()
            if stock:
                if stock[0] > 1:
                    cursor.execute("UPDATE inventory SET stock = stock - 1 WHERE product_name = %s", (product_name,))
                else:
                    cursor.execute("DELETE FROM inventory WHERE product_name = %s", (product_name,))
                conn.commit()
                cursor.close()
                messagebox.showinfo("Success", "Item stock reduced by 1")
                show_items()
        except Exception as e:
            messagebox.showerror("Error", str(e))

def show_items():
    treeview.delete(*treeview.get_children())
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT product_name, price, stock, category FROM inventory")
        serial_number = 1
        for row in cursor:
            product_name, product_price, stock, category = row
            treeview.insert("", "end", values=(serial_number, product_name, f"Rs. {product_price:.2f}", stock, category))
            serial_number += 1
        cursor.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Connect to the MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',
    database='inventory_system'
)

# Create the login window
login_window = Tk()
login_window.title("Login")
login_window.geometry("400x200")

label_username = Label(login_window, text="Username", font=('calibri 20 bold'), fg='black', anchor='e', justify='right')
label_username.grid(row=0, column=0, pady=10, sticky='e')

entry_username = Entry(login_window, font=('Calibri 18'), bg='white')
entry_username.grid(row=0, column=1, pady=10, sticky='w')

label_password = Label(login_window, text="Password", font=('calibri 20 bold'), fg='black', anchor='e', justify='right')
label_password.grid(row=1, column=0, pady=10, sticky='e')

entry_password = Entry(login_window, font=('Calibri 18'), bg='white', show='*')
entry_password.grid(row=1, column=1, pady=10, sticky='w')

authenticate_btn = Button(login_window, text="Authenticate", width=18, height=2, bg='#2E86C1', command=login)  # Soft blue
authenticate_btn.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky='e')

login_window.mainloop()
